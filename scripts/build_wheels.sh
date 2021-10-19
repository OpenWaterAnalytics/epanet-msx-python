#!/bin/bash

#
#  Taken from swmm-python

set -e -x


# Install a system package required by our library
sudo yum install -y swig


# Setup
mkdir -p ./combined-dist

# Build wheels
for PYBIN in /opt/python/cp{36,37,38,39}*/bin; do
    # Setup python virtual environment for build
    ${PYBIN}/python -m venv --clear ./build-env
    source ./build-env/bin/activate

    # Install build requirements
    python -m pip install -r build-requirements.txt

    # Build wheel
    python setup.py bdist_wheel
    mv ./dist/*.whl ./combined-dist/

    # cleanup
    python setup.py clean
    deactivate
done

# Cleanup
rm -rf ./build-env

# Bundle external shared libraries into the wheels
for WHL in ./combined-dist/*-linux_x86_64.whl; do
    auditwheel repair -L '' -w ./combined-dist $WHL
done
