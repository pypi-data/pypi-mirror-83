# -*- coding: utf-8 -*-


"""setup.py: setuptools control."""


import re
from setuptools import setup


version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('test_pypi_anbltest/entry.py').read(),
    re.M
    ).group(1)

setup(
    name = "cmdline-test_pypi_anbltest",
    packages = ["test_pypi_anbltest"],
    entry_points = {
        "console_scripts": ['test_pypi_anbltest = test_pypi_anbltest.entry:main']
        },
    version = version,
    description = "Python command line application bare bones template.",
    long_description = long_descr,
    author = "Jan-Philip Gehrckeqqw",
    author_email = "jgehrckqwwqe@googlemail.com",
    url = "http://gehrcke.de/2014/02/distributing-a-python-command-line-applicationqwqw",
    )
