"""Setup."""
from setuptools import find_packages, setup

with open("README.rst", encoding="UTF-8") as readme_file:
    README = readme_file.read()

INSTALL_REQUIRES = ["ruamel.yaml>0.16"]

SETUP_REQUIREMENTS = ["pytest-runner"]

TEST_REQUIREMENTS = ["pytest"]

setup(
    name="yamkix",
    version="0.9.1rc2",
    author="Christophe Furmaniak",
    author_email="christophe.furmaniak@gmail.com",
    description="An opinionated yaml formatter based on ruamel.yaml",
    long_description=README,
    long_description_content_type="text/x-rst",
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
