from setuptools import setup

long_description = open('README.rst').read()

setup(
    name='yamkix',
    description='An opinionated yaml formatter based on ruamel.yaml',
    long_description=long_description,
    url='https://github.com/looztra/yamkix',
    author='Christophe Furmaniak',
    author_email='christophe.furmaniak@gmail.com',
    version='0.2.2',
    scripts=['yamkix'],
    license='[Apache License 2.0](http: // www.apache.org / licenses /)',
    install_requires=['ruamel.yaml>0.15'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2',
        'Topic :: Utilities',
    ],
    keywords='yaml format'
)
