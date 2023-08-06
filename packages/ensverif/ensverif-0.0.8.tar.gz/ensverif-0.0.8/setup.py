#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 14:03:18 2020

@author: marie-amelie
"""

from setuptools import setup, find_packages

Classifier = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Education',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Programming Language :: Python :: 3'
]

setup(
      name = 'ensverif',
      version = '0.0.8',
      description = 'This library contains functions to assess the quality of ensemble forecasts or simulations',
      long_description = open('README.txt', encoding='utf-8').read(),
      url = '',
      author = 'Marie-Amelie Boucher and collab.',
      author_email = 'marie-amelie.boucher@usherbrooke.ca',
      licence = 'GNU AFFERO GENERAL PUBLIC LICENSE',
      classifiers = Classifier,
      keywords='ensemble forecasts verification,',
      packages=find_packages(),
      install_requires=['numpy', 'scipy']
)
