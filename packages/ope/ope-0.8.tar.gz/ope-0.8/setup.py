#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

from version import get_version

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

with open('ope/VERSION') as version_file:
    __version__ = version_file.read().strip()

requirements = ['Click>=7.0', 'numpy', 'pandas', 'screed']
test_requirements = ['pytest>=3', 'pytest-runner']

setup(
    author="Camille Scott",
    author_email='cswel@ucdavis.edu',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Abstracts away running gnu-parallel on tools with FASTA input and provides parsers for some common formats produced by said tools.",
    entry_points={
        'console_scripts': [
            'ope=ope.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='ope',
    name='ope',
    packages=find_packages(include=['ope', 'ope.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/camillescott/ope',
    version=__version__,
    zip_safe=False,
)
