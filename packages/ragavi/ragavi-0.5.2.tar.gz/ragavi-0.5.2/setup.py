#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

import os
from setuptools import setup
from ragavi import __version__

pkg = 'ragavi'

build_root = os.path.dirname(__file__)


def readme():
    """Get readme content for package long description"""
    with open(os.path.join(build_root, 'README.rst')) as f:
        return f.read()


def requirements():
    """Get package requirements"""
    with open(os.path.join(build_root, 'requirements.txt')) as f:
        return [pname.strip() for pname in f.readlines()]


setup(name='ragavi',
      version=__version__,
      description='Radio Astronomy Gain and Visibility Inspector',
      long_description=readme(),
      url='https://github.com/ratt-ru/ragavi',
      classifiers=[
          "Intended Audience :: Developers",
          "Operating System :: OS Independent",
          "Programming Language :: Python :: 3.6",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "Topic :: Scientific/Engineering :: Astronomy"],
      author='Lexy Andati',
      author_email='andatilexy@gmail.com',
      license='MIT',
      packages=[pkg],
      install_requires=requirements(),
      scripts=["ragavi/bin/" + i for i in os.listdir("ragavi/bin/")],
      include_package_data=True,
      python_requires=">=3.6")
