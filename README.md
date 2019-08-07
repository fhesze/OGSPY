# OGSPY

This is a Python package providing Python bindings for the OpenGeoSys (OGS) scientific open source project.

Created May 2015, Copyright 2015 

Contact Falk He"sse - falk.hesse (at) ufz.de or Miao Jing - miao.jing (at) ufz.de

The package has to be in your Python path. For example in bash:
    export PYTHONPATH=/path/to/the/ogspy/package
It can also be installed with the usual setup.py commands using distutils:
    python setup.py install
If one wants to use the development capabilities of setuptools, you can use something like
    python -c "import setuptools; execfile('setup.py')" develop
This basically creates an .egg-link file and updates an easy-install.pth file so that the project
is on sys.path by default.
Distutils also allows to make Windows installers with
    python setup.py bdist_wininst


The documentation of the package is in the docstring of __init__.py so that one can get help on the
Python prompt:
>>> import ogspy
>>> help(ogspy)

The individual functions also provide their help as doctrings.
Getting, for example, help on run() for running the ogs project:
>>> import ogspy
>>> help(ogspy.run)

The Python package is compatible with 3 (> 3.2).

Essential third-party packages are numpy and scipy.
Some functions provide visual checks using matplotlib for plotting.
