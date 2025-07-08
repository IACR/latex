# Tests for iacrj.cls and metacapture.sty

This directory contains code and data for testing iacrj.cls and
metacapture.sty. There is a main driver `compile_tests.py` that
contains all of the tests (though they could be broken up
differently). These tests use whatever TeX environment you have
installed, so that they may not reflect what happens in the submission
server itself.

In order to run tests, you need to have `pytest` and a latex environment
installed. In order to run all tests, use
```
pytest compile_tests.py -vv
```
The `-vv` argument produces more verbose output, which is useful
if a test fails. You can also try just `-v`.

These tests are quite slow, so you may want to run only one.
In order to run a single test, use:
```
pytest compile_tests.py::test1_test -vv
```
This will run only `test1_test()` in `compile_tests.py`.
