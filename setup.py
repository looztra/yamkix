"""Setup."""

from setuptools import setup

LONG_DESCRIPTION = open("README.rst").read()

INSTALL_REQUIRES = ["ruamel.yaml>0.16"]

setup(
    name="yamkix",
    description="An opinionated yaml formatter based on ruamel.yaml",
    long_description=LONG_DESCRIPTION,
    url="https://github.com/looztra/yamkix",
    author="Christophe Furmaniak",
    author_email="christophe.furmaniak@gmail.com",
    version="0.6.1",
    scripts=["yamkix"],
    license="[Apache License 2.0](http: // www.apache.org / licenses /)",
    install_requires=INSTALL_REQUIRES,
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Topic :: Utilities",
    ],
    keywords="yaml format",
)
