#    Copyright 2018 D-Wave Systems Inc.

#    Licensed under the Apache License, Version 2.0 (the "License")
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at

#        http: // www.apache.org/licenses/LICENSE-2.0

#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import sys
import time
import logging
import functools
from collections import OrderedDict

import dwavebinarycsp as dbc
from dwave.system import DWaveSampler, EmbeddingComposite

log = logging.getLogger(__name__)

def sanitised_input(description, variable, range_):
    start = range_[0]
    stop = range_[-1]

    while True:
        ui = input("Input {:15}({:2} <= {:1} <= {:2}): ".format(description, start, variable, stop))

        try:
            ui = int(ui)
        except ValueError:
            print("Input type must be int")
            continue

        if ui not in range_:
            print("Input must be between {} and {}".format(start, stop))
            continue

        return ui

def validate_input(ui, range_):
    start = range_[0]
    stop = range_[-1]

    if not isinstance(ui, int):
        raise ValueError("Input type must be int")

    if ui not in range_:
        raise ValueError("Input must be between {} and {}".format(start, stop))

def factor(P):

    # Construct circuit
    # =================
    construction_start_time = time.time()

    validate_input(P, range(2 ** 6))

    # Constraint satisfaction problem
    csp = dbc.factories.multiplication_circuit(3)

    # Binary quadratic model
    bqm = dbc.stitch(csp, min_classical_gap=.1)

    # multiplication_circuit() creates these variables
    p_vars = ['p0', 'p1', 'p2', 'p3', 'p4', 'p5']

    # Convert P from decimal to binary
    fixed_variables = dict(zip(reversed(p_vars), "{:06b}".format(P)))
    fixed_variables = {var: int(x) for(var, x) in fixed_variables.items()}

    # Fix product qubits
    for var, value in fixed_variables.items():
        bqm.fix_variable(var, value)

    log.debug('bqm construction time: %s', time.time() - construction_start_time)

    # Run problem
    # ===========

    sample_time = time.time()

    # Set a QPU sampler
    sampler = EmbeddingComposite(DWaveSampler())

    num_reads = 100
    sampleset = sampler.sample(bqm,
                               num_reads=num_reads,
                               label='Example - Factoring')

    log.debug('embedding and sampling time: %s', time.time() - sample_time)

    # Output results
    # ==============

    output = {
        "Results": [],
        #    {
        #        "a": Number,
        #        "b": Number,
        #        "Valid": Boolean,
        #        "Occurrences": Number,
        #        "Percentage of results": Number
        #    }
        "Timing": {
            "Actual": {
                "QPU processing time": None  # microseconds
            }
        },
        "Number of reads": None
    }

    # multiplication_circuit() creates these variables
    a_vars = ['a0', 'a1', 'a2']
    b_vars = ['b0', 'b1', 'b2']

    results_dict = OrderedDict()
    for sample, num_occurrences in sampleset.data(['sample', 'num_occurrences']):
        # Convert A and B from binary to decimal
        a = b = 0
        for lbl in reversed(a_vars):
            a = (a << 1) | sample[lbl]
        for lbl in reversed(b_vars):
            b = (b << 1) | sample[lbl]
        # Cast from numpy.int to int
        a, b = int(a), int(b)
        # Aggregate results by unique A and B values (ignoring internal circuit variables)
        if (a, b, P) in results_dict:
            results_dict[(a, b, P)]["Occurrences"] += num_occurrences
            results_dict[(a, b, P)]["Percentage of results"] = 100 * \
                results_dict[(a, b, P)]["Occurrences"] / num_reads
        else:
            results_dict[(a, b, P)] = {"a": a,
                                       "b": b,
                                       "Valid": a * b == P,
                                       "Occurrences": num_occurrences,
                                       "Percentage of results": 100 * num_occurrences / num_reads}

    output['Results'] = list(results_dict.values())
    output['Number of reads'] = num_reads

    output['Timing']['Actual']['QPU processing time'] = sampleset.info['timing']['qpu_access_time']

    return output

def display_output(output):
    header1_str = 'Factors    Valid?  Percentage of Occurrences'
    header2_str = ' ' * header1_str.index('P') + 'Numeric & Graphic Representation'
    total_width = 80  # Assumed total console width
    # Width available to draw bars:
    available_width = total_width - header1_str.index('P') - 4

    header_len = max(len(header1_str), len(header2_str))
    print('-'*header_len)
    print(header1_str)
    print(header2_str)
    print('-'*header_len)

    for result in output['Results']:
        percentage = result['Percentage of results']
        print('({:3},{:3})  {:3}     {:3.0f} '.format(result['a'], result['b'], 'Yes' if result['Valid'] else '', percentage), end='')
        nbars = int(percentage/100 * available_width)
        print('*' * nbars)


if __name__ == '__main__':
    # get input from user
    print("Enter a number to be factored:")
    P = sanitised_input("product", "P", range(2 ** 6))

    # send problem to QPU
    print("Running on QPU")
    output = factor(P)

    # output results
    display_output(output)
