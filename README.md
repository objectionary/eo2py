# eo-python

![build](https://github.com/nikololiahim/eo-python/actions/workflows/maven.yml/badge.svg) [![codecov](https://codecov.io/gh/nikololiahim/eo-python/branch/main/graph/badge.svg?token=CuHSiScipH)](https://codecov.io/gh/nikololiahim/eo-python)

A Python implementation of [EO](https://github.com/cqfn/eo).

## Repository contains:
* Parser: XSL sheets for "transcompilation" (let's be fancy about it)
* Python runtime environment: [pip package](https://pypi.org/project/eo2py/) 
* Tests
* Examples of translated programs in `eo-python-runtime/tests/example_programs` as `pytest` unit tests.
* Sandbox to compile and execute your own EO programs! Checkout `README.md` in `sandbox` directory.

### Supported features:
* Abstraction
* One-time full application
* Decoration (nested decoration, free decoratees)
* Inner objects, both closed and abstract
* Varargs

### Unsupported features:
* Arrays
* Partial Application
* Metas
* Maybe some more (whenever you experience a bug, feel free to submit an issue)

## How to use
Checkout `README.md` in `sandbox` directory.

## Code mappings
//TODO

## Justification of design decisions
//TODO

## Further considerations
//TODO
