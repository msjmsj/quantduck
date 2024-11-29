# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name="quantduck",
    version="0.1.26",
    packages=find_packages(),
    python_requires=">=3.8,<3.12",
    install_requires=[
        "psycopg2-binary>=2.9.0",
        "pytz",
    ],
) 