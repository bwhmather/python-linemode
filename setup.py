# -*- coding: utf-8 -*-
import sys
from setuptools import setup, find_packages


setup(
    name='nm-printing',
    url='github.com/NewmanOnline/nm-printing',
    version='0.0.1',
    author='Newman Team',
    author_email='newman@newmanonline.org.uk',
    maintainer='',
    license='Commercial, All rights reserved.',
    description='Drivers and templates for thermal printers',
    long_description=__doc__,
    install_requires=[
    ],
    extras_require={
        'XMLRenderer': [
            'lxml >= 2.3, < 4',
        ],
        'Serial': [
            'pyserial',
        ],
    },
    packages=find_packages(),
    package_data={
        '': ['*.*'],
    },
    zip_safe=False,
    test_suite='nm_printing.tests.suite',
)
