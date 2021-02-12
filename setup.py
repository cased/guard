import os
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


setup(
    name="cased",
    version="0.5.7",
    description="Cased Guard adds security and visibility features to the command line tools you and your team love.",
    long_description="Cased Guard adds security and visibility features to the command line tools you and your team love. https://cased.com/guard",
    author="Cased",
    author_email="support@cased.com",
    url="https://github.com/cased/guard-client",
    license="BSL 1.1",
    keywords="cased api",
    packages=find_packages(exclude=["tests", "tests.*"]),
    zip_safe=False,
    scripts=["cased-init", "cguard/cased"],
    python_requires=">3.5",
    install_requires=[
        "requests",
        "responses",
        "mock",
        "pytest >= 4.0c0",
        "pytest-mock",
        "pytest-xdist",
        "yaspin",
    ],
    project_urls={
        "Bug Tracker": "https://github.com/cased/guard/issues",
        "Documentation": "https://docs.cased.com/guard",
        "Source Code": "https://github.com/cased/guard",
    },
)
