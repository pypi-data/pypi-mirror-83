#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [ ]

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="Kai Friedrich",
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="LoggingHandler to move logs into gziped archives in a smart way",
    install_requires=requirements,
    license="MIT license",
    long_description_content_type="text/x-rst",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='compressedlogger',
    name='compressedlogger',
    packages=find_packages(include=['compressedlogger', 'compressedlogger.*']),
    setup_requires=setup_requirements,
    test_suite='',
    tests_require=test_requirements,
    version='0.3.3'
)
