# epanet-msx-python
The python wrapper for [epanet-msx](https://github.com/OpenWaterAnalytics/epanet-msx).

# Build
Ensure the epanet-msx subproject is initialized by running git submodule update --init.
Then run and running the following commands (only run clean if you can run bash scripts).
The following method uses scikit-build to invoke cmake for compiling and linking the shared libaries, and builds a python wheel.
```
./scripts/clean.sh
python setup.py sdist bdist_wheel
pip install dist/*.whl
```
There is also a script called build that will run the three commands from above. (build.sh should be called from the root)
```
./scripts/build.sh
```

# Usage
Most of the functions are used in the same fashion as they would be in the C API, however it is not necessary to
check the return values for an error code anymore. If an error occurs, an exception will be thrown stating the error code.
The only major difference in calling functions using the python wrapper for epanet-msx is the way that values are returned.
If a function in the C API took in a pointer as a parameter that was intended to be used as an output, it now will be returned
by the function.
For example:
```
// In C
int MSXgetindex(int type, char *id, int *index);
# In Python
index = msx.getindex(type, id)
```
If there are multiple pointers given that will be used for output. Python handles it like this:
```
// In C
int MSXgetspecies(int index, int *type, char *units, double *aTol, double *rTol);
# In Python
type, units, aTol, rTol = msx.getspecies(index)
```
Currently there is only one function that uses a pointer variable for both input and output and it is the "t" variable in MSXstep.
Example usage:
```
t, tleft = msx.step(t)
```

# Tests
There is a tests directory with a file that can be run using pytest for unit tests. All of the tests that are currently available
are very basic, and mainly only test functions that are not utilized in either of the examples. Both of the examples are working,
and therefore all of the critical functions that those use are working. It is more important that the example functions are running
properly than the tests passing since the examples use more critical functions.
To run the tests:
```
pytest tests/test_msx.py
```