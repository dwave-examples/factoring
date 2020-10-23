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

import time
import logging
import functools
from collections import OrderedDict

import dwavebinarycsp as dbc
from dwave.system import DWaveSampler, EmbeddingComposite

log = logging.getLogger(__name__)

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

    num_reads = 50
    sampleset = sampler.sample(bqm, num_reads=50)

    log.debug('embedding and sampling time: %s', time.time() - sample_time)

    # Output results
    # ==============

    output = {
        "results": [],
        #    {
        #        "a": Number,
        #        "b": Number,
        #        "valid": Boolean,
        #        "numOfOccurrences": Number,
        #        "percentageOfOccurrences": Number
        #    }
        "timing": {
            "actual": {
                "qpuProcessTime": None  # microseconds
            }
        },
        "numberOfReads": None
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
            results_dict[(a, b, P)]["numOfOccurrences"] += num_occurrences
            results_dict[(a, b, P)]["percentageOfOccurrences"] = 100 * \
                results_dict[(a, b, P)]["numOfOccurrences"] / num_reads
        else:
            results_dict[(a, b, P)] = {"a": a,
                                       "b": b,
                                       "valid": a * b == P,
                                       "numOfOccurrences": num_occurrences,
                                       "percentageOfOccurrences": 100 * num_occurrences / num_reads}

    output['results'] = list(results_dict.values())
    output['numberOfReads'] = num_reads

    output['timing']['actual']['qpuProcessTime'] = sampleset.info['timing']['qpu_access_time']

    return output
