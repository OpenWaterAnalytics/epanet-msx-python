#!/bin/bash

./scripts/clean.sh

python setup.py sdist bdist_wheel

pip install --force-reinstall dist/*.whl