"""Setup."""
import os
import codecs
import re
from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    README = readme_file.read()

INSTALL_REQUIRES = ["ruamel.yaml>0.16"]

SETUP_REQUIREMENTS = ["pytest-runner"]

TEST_REQUIREMENTS = ["pytest"]

HERE = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    """Read a file and returns its content."""
    with codecs.open(os.path.join(HERE, *parts), "r") as file_pointer:
        return file_pointer.read()


def find_version(*file_paths):
    """Get the version value from the input path."""
    version_file = read(*file_paths)
    version_match = re.search(
        r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M
    )
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name="yamkix",
    version=find_version("yamkix", "__init__.py"),
    author="Christophe Furmaniak",
    author_email="christophe.furmaniak@gmail.com",
    description="An opinionated yaml formatter based on ruamel.yaml",
    long_description=README,
    url="https://github.com/looztra/yamkix",
    license="[Apache License 2.0](http: // www.apache.org / licenses /)",
    install_requires=INSTALL_REQUIRES,
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Topic :: Utilities",
    ],
    keywords="yaml format",
    packages=find_packages(include=["yamkix"]),
    include_package_data=True,
    python_requires=">=3.6",
    entry_points={"console_scripts": ["yamkix = yamkix.__main__:main"]},
    setup_requires=SETUP_REQUIREMENTS,
    test_suite="tests",
    tests_require=TEST_REQUIREMENTS,
)
