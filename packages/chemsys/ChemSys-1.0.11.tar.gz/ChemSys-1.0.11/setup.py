# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 18:25:39 2020

Github: https://github.com/tjczec01

@author: Travis J Czechorski

E-mail: tjczec01@gmail.com

"""

from setuptools import setup, find_packages
import json
import urllib.request


def versions(package_name):
    url = "https://pypi.org/pypi/{}/json".format(package_name)
    data = json.load(urllib.request.urlopen(urllib.request.Request(url)))
    versions = list(data["releases"].keys())
    return versions[-1]


# def update(v1, v2, v3):
#     if v3 <= 99:
#         v3 += 1
#     elif v3 >= 100 and v2 <= 99:
#         v2 += 1
#         v3 = 0
#     elif v2 >= 100 and v3 >= 99:
#         v1 += 1
#         v2 = 0
#         v3 = 0
#     return [v1, v2, v3]


# vv = str(versions("ChemSys"))
# v1b = int(vv[0])
# v2b = int(vv[2])
# v3b = int(vv[4])
# v1, v2, v3 = update(v1b, v2b, v3b)

description_chemsys = str("""Interactive GUI based program that generates the overall species balance,
                  system of ODEs needed for the solve_ivp and odeint method,
                  and calculates the Jacobian both symbolically and numerically.
                  The resulting code can easily be copied and pasted as is to be integrated with the aforementioned SciPy functions.""")

with open(r"C:\Users\tjcze\Desktop\ChemSys\README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="ChemSys", # Replace with your own username
    version="1.0.11",
    author="Travis Czechorski",
    author_email="tjczec01@gmail.com",
    description="{}".format(description_chemsys),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=r"https://github.com/tjczec01/chemsys/tree/master",
    packages=find_packages(),
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"],
    python_requires='>=3.6')
