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