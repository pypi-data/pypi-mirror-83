#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import io
from setuptools import setup, find_packages


setup(name='zenfilter',
      version='0.6.3',
      description='Filter stdin to avoid excessive output',
      keywords='zenfilter',
      author='Shlomi Fish',
      author_email='shlomif@cpan.org',
      url='https://github.com/shlomif/zenfilter',
      license='3-clause BSD',
      long_description=io.open(
          './docs/README.rst', 'r', encoding='utf-8').read(),
      platforms='any',
      zip_safe=False,
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=['Development Status :: 1 - Planning',
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.5',
                   'Programming Language :: Python :: 3.6',
                   'Programming Language :: Python :: 3.7',
                   'Programming Language :: Python :: 3.8',
                   ],
      packages=find_packages(exclude=('tests', 'tests.*')),
      include_package_data=True,
    
    entry_points={'console_scripts':['zenfilter=zenfilter:zenfilter',],},
      install_requires=[],
      )
