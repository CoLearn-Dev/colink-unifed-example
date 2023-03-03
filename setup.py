#!/usr/bin/env python

from setuptools import setup, find_namespace_packages

FRAMEWORK_NAME = 'example'

setup(name=f'colink-unifed-{FRAMEWORK_NAME}',
      version='0.0',
      packages=find_namespace_packages(
          'src', exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
      package_dir={'': 'src'},
      install_requires=[
          'colink >= 0.2.6',
      ],
      entry_points={
          'console_scripts': [
              f'unifed-{FRAMEWORK_NAME} = unifed.frameworks.{FRAMEWORK_NAME}:run_protocol',
          ] + ([] if FRAMEWORK_NAME != 'example' else ["unifed-example-workload = unifed.frameworks.example:simulate_workload"]),
      }
      )
