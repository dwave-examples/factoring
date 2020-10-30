[![Linux/Mac/Windows build status](https://circleci.com/gh/dwave-examples/factoring.svg?style=svg)](https://circleci.com/gh/dwave-examples/factoring)

# Factoring

This code demonstrates the use of the D-Wave system to solve a factoring
problem. This is done by turning the problem into a three-bit multiplier
circuit.

## Usage

A minimal working example using the main interface function can be seen by
running:

```bash
python demo.py
```

The user is prompted to enter a six-bit integer: P, which represents a product
to be factored.

```bash
Input product        ( 0 <= P <= 63):
```

The algorithm returns possible A and B values, which are the inputs the circuit
multiplies to calculate the product, P.

## Code Overview

Integer factoring is the decomposition of an integer into factors that, when
multiplied together, give the original number. For example, the factors of 15
are 3 and 5.

D-Wave quantum computers allow us to factor numbers in an entirely new way, by
turning a multiplication circuit into a constraint satisfaction problem that
allows the quantum computer to compute inputs from a predefined output.
Essentially, this means running the multiplication circuit in reverse!

A Boolean logic circuit is usually viewed as computing outputs from inputs
based on the logic of the gates. However, the problem can also be thought of as
seeking an assignment of values to the inputs and outputs consistent with the
logic of all the gates in the circuit.  This perspective of constraint
satisfaction has no directionality. That is, input values do not need to flow
through a series of gates to yield a result, as they do in a multiplication
circuit.

## License

Released under the Apache License 2.0. See [LICENSE](LICENSE) file.
