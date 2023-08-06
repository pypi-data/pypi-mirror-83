#!/usr/bin/env python3
# Setup python package - python setup.py sdist

from setuptools import setup

setup(
    name='filewrap',
    version='1.1.1',
    py_modules=['filewrap'],
    license='MIT',
    description='A Python package for file/archive manipulation & management.',
    long_description=open('README.txt').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/CodeConfidant/filewrap-os',
    author='Drew Hainer',
    author_email='codeconfidant@gmail.com',
    platforms=['Windows', 'Linux']
)