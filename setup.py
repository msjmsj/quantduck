from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="quantduck",
    version="0.1.0",
    packages=find_packages(exclude=["tests", "tests.*"]),
    install_requires=[
        "numpy>=1.19.0",
        "pandas>=1.2.0",
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A quantitative analysis library for financial markets",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/quantduck",
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/quantduck/issues",
        "Documentation": "https://github.com/yourusername/quantduck/wiki",
        "Source Code": "https://github.com/yourusername/quantduck",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Office/Business :: Financial",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.6",
    test_suite="tests",
) 