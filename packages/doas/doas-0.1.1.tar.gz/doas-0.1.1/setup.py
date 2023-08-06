#!/usr/bin/env python

import os

from setuptools import setup, find_packages

__version__ = '0.1.1'


def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()


setup(
    name='doas',
    version=__version__,
    description='DOAS processing utility library',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    license='MIT',
    install_requires=[
        'sqlalchemy',
    ],
    author='Indra Rudianto',
    author_email='indrarudianto.official@gmail.com',
    url='https://gitlab.com/bpptkg/doas',
    zip_safe=False,
    packages=find_packages(
        exclude=['tests', 'docs', 'resources', 'samples', 'work']),
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Operating System :: POSIX :: Linux',
        'Intended Audience :: Science/Research',
        'Natural Language :: Indonesian',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ]
)
