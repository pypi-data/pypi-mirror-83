#!/usr/bin/env python

import os
from setuptools import setup, find_packages

setup(name='iotbotocredentialprovider',
      version='1.0.10',
      description='AWS IoT Credential Provider: create boto sessions which obtain and renew credentials from an AWS IoT device certificate',
      author='Craig I. Hagan',
      author_email='hagan@cih.com',
      url='https://github.com/craighagan/iotbotocredentialprovider',
      license='MIT',
      packages = find_packages(exclude=["test"]),
      install_requires=["boto3","requests"],
      setup_requires=["pytest-runner", "setuptools"],
      tests_require=["pytest", "pytest-runner", "pytest-cov", "pytest-mock", "pylint>=2.5.0", "pytest-pylint>=0.16.0"],
      scripts=["bin/fakemetadata-server.py"],
)
