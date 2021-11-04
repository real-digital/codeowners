#!/usr/bin/env python

from distutils.core import setup

setup(
    name='codeowners',
    version='1.0',
    description='Pre-commit hook to generate gitlab CODEOWNERS file from `owners.yaml` file',
    scripts=['generate_codeowners.py'],
    install_requires=['PyYAML', 'yamale'],
)
