# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 18:25:39 2020

Github: https://github.com/tjczec01

@author: Travis J Czechorski

E-mail: tjczec01@gmail.com

"""

from setuptools import setup, find_packages


description_chemsys = str("""Interactive GUI based program that generates the overall species balance,
                  system of ODEs needed for the solve_ivp and odeint method,
                  and calculates the Jacobian both symbolically and numerically.
                  The resulting code can easily be copied and pasted as is to be integrated with the aforementioned SciPy functions.""")

setup(
    name="ChemSys", # Replace with your own username
    version="1.0.29",
    author="Travis Czechorski",
    author_email="tjczec01@gmail.com",
    description="{}".format(description_chemsys),
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url=r"https://github.com/tjczec01/chemsys/tree/master",
    packages=find_packages(),
    keywords = ['chemical engineering', 'chemistry', 'engineering'],
    install_requires=["sympy", "IPython", "matplotlib", "pytest-runner"],
    setup_requires=["sympy", "IPython", "matplotlib", "pytest-runner"],
    tests_require=["pytest"],
    license='LICENSE.txt',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"],
    python_requires='>=3.6')
