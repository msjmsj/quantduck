# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name="quantduck",
    version="0.1.5",
    packages=find_packages(),
    install_requires=[
        "psycopg2-binary",
        "pytz",
        "pandas",
    ],
    description="A quantitative analysis library",
    author="Your Name",
    author_email="your.email@example.com",
) 