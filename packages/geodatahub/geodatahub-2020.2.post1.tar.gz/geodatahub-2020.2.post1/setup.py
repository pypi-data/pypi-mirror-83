#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from codecs import open
with open('README.md', encoding='utf-8') as f:
    README = f.read()


def get_version():
    with open('geodatahub/__init__.py') as f:
        for line in f:
            if line.startswith('__version__'):
                return eval(line.split('=')[-1])


setup(name='geodatahub',
      version=get_version(),
      description='Official GeoDataHub API client',
      long_description=README,
      long_description_content_type='text/markdown',
      author='GeoDataHub',
      author_email='info@geodatahub.dk',
      url='https://geodatahub.dk',
      packages=find_packages(exclude=['test']),
      install_requires=['requests >= 2.16.2', 'geojson'],
      tests_require=['coverage'],   # must equal test/requirements.txt
      license='Apache License v2',

      # For a list of valid classifiers, see
      # https://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=['Development Status :: 2 - Pre-Alpha',
                   'Intended Audience :: End Users/Desktop',
                   'Intended Audience :: Science/Research',
                   'License :: OSI Approved :: Apache Software License',
                   'Programming Language :: Python :: 2',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.6',
                   ],

      project_urls={
          'Documentation': 'https://geodatahub.dk/docs/',
          'Bug Reports': 'https://gitlab.com/GeoDataHub/geodatahublib/issues',
          'Source': 'https://gitlab.com/GeoDataHub/geodatahublib/',
      },
      )
