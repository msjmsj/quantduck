from setuptools import setup, find_packages

setup(
    name="quantduck",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "psycopg2-binary",  # PostgreSQL数据库驱动
        "pytz",             # 时区支持
    ],
    python_requires=">=3.7",
    author="Your Name",
    author_email="your.email@example.com",
    description="A quantitative trading library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/quantduck",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
) 