  
from skbuild import setup
from setuptools import find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name = "epanetmsx",
    version = "2",
    author = "Kyle Arrowood",
    author_email = "kyle.a.arrowood@gmail.com",
    description = "a thin wrapper for epanet-msx toolkit",
    long_description = long_description,
    long_description_content_type="text/markdown",
    url = "https://github.com/karrowood/epanet-msx-python",
    #cmake_args=["-DCMAKE_OSX_DEPLOYMENT_TARGET:STRING=10.9"],
    #cmake_with_sdist = True,
    package_dir = {"":"packages"},
    packages = ["epanetmsx"],
    package_data = {"epanetmsx":["*.dylib", "*.dll", "*.so"]},
    zip_safe=False
)