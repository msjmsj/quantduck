from setuptools import setup, find_packages

setup(
    name="quantduck",
    version="0.1.3",
    packages=find_packages(),
    install_requires=[
        "psycopg2-binary",
        "pytz",
        "pandas",
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A quantitative analysis library",
    long_description="Quantduck - A quantitative analysis library",
    long_description_content_type="text/markdown",
    url="https://github.com/msjmsj/quantduck",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
) 