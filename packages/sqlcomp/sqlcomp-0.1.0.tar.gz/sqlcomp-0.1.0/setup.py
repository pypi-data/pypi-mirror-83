"""
Setup.py for sqlcomp.
"""
from setuptools import setup

setup(
    name='sqlcomp',
    version='0.1.0',
    packages=['lib', 'lib.config', 'lib.expand', 'lib.compress', 'test', 'test.config', 'test.expand', 'test.compress'],
    url='https://github.com/Romulus10/sqlcomp',
    license='GPL v3',
    author='Romulus10',
    author_email='romulus108@protonmail.com',
    description='A library for edge cases where shortening SQL is helpful.'
)
