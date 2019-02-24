from setuptools import setup

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except ImportError:
    long_description = open('README.md').read()

setup(
    name='yamkix',
    description='''
        An opinionated yaml formatter based on ruamel.yaml,
        that works fine for k8s descriptors
        ''',
    long_description=long_description,
    url='https://github.com/looztra/yamkix',
    author='Christophe Furmaniak',
    author_email='christophe.furmaniak@gmail.com',
    version='0.1.1',
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