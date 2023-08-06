#!/usr/bin/env python

import os
from setuptools import setup, find_packages

with open('hail/hail_pip_version') as f:
    hail_pip_version = f.read().strip()

with open("README.md", "r") as fh:
    long_description = fh.read()

dependencies = [
    "aiohttp>=3.6,<3.7",
    "aiohttp_session>=2.7,<2.8",
    "asyncinit>=0.2.4,<0.3",
    "bokeh>1.1,<1.3",
    "decorator<5",
    "Deprecated>=1.2.10,<1.3",
    "dill>=0.3.1.1,<0.4",
    "gcsfs==0.2.2",
    "humanize==1.0.0",
    "hurry.filesize==0.9",
    "nest_asyncio",
    "numpy<2",
    "pandas>0.24,<0.26",
    "parsimonious<0.9",
    "PyJWT",
    "pyspark==3.0.0",
    "python-json-logger==0.1.11",
    "requests==2.22.0",
    "scipy>1.2,<1.4",
    "tabulate==0.8.3",
    "tqdm==4.42.1",
    "google-cloud-storage==1.25.*"
]

setup(
    name="j11hail",
    version=hail_pip_version,
    author="Hail Team",
    author_email="hail@broadinstitute.org",
    description="Scalable library for exploring and analyzing genomic data.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://hail.is",
    project_urls={
        'Documentation': 'https://hail.is/docs/0.2/',
        'Repository': 'https://github.com/hail-is/hail',
    },
    packages=find_packages('.'),
    package_dir={
        'hail': 'hail',
        'hailtop': 'hailtop'},
    package_data={
        'hail': ['hail_pip_version',
                 'hail_version',
                 'experimental/datasets.json'],
        'hail.backend': ['hail-all-spark.jar'],
        'hailtop.hailctl': ['hail_version', 'deploy.yaml']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.6",
    install_requires=dependencies,
    entry_points={
        'console_scripts': ['hailctl = hailtop.hailctl.__main__:main']
    },
    setup_requires=["pytest-runner", "wheel"],
    tests_require=["pytest"]
)
