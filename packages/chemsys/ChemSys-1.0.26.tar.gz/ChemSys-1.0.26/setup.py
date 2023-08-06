# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 18:25:39 2020

Github: https://github.com/tjczec01

@author: Travis J Czechorski

E-mail: tjczec01@gmail.com

"""

from setuptools import setup, find_packages
from sphinx.setup_command import BuildDoc
cmdclass = {'build_sphinx': BuildDoc}


description_chemsys = str("""Interactive GUI based program that generates the overall species balance,
                  system of ODEs needed for the solve_ivp and odeint method,
                  and calculates the Jacobian both symbolically and numerically.
                  The resulting code can easily be copied and pasted as is to be integrated with the aforementioned SciPy functions.""")

with open(r"C:\Users\tjcze\Desktop\ChemSys\README.md", "r") as fh:
    long_description = fh.read()

with open(r'C:\Users\tjcze\Desktop\ChemSys\LICENSE.txt') as f:
    license = f.read()

name = "ChemSys" # Replace with your own username
version = "1.0.26"
release = '1.0.26'

setup(
    name="ChemSys", # Replace with your own username
    version="1.0.26",
    author="Travis Czechorski",
    author_email="tjczec01@gmail.com",
    description="{}".format(description_chemsys),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=r"https://github.com/tjczec01/chemsys/tree/master",
    packages=find_packages(),
    install_requires=["sphinx", "sympy", "IPython", "matplotlib"],
    setup_requires=["sphinx", "sympy", "IPython", "matplotlib", "pytest-runner"],
    tests_require=["pytest"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"],
    python_requires='>=3.6',
    cmdclass=cmdclass,
    # these are optional and override conf.py settings
    command_options={
        'build_sphinx': {
            'project': ('setup.py', name),
            'version': ('setup.py', version),
            'release': ('setup.py', release),
            'source_dir': ('setup.py', r'C:\Users\tjcze\Desktop\ChemSys\source')}})
