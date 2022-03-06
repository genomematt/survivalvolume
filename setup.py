#!/usr/bin/env python
from setuptools import setup

setup(
    name='survivalvolume',
    version='1.2.4',
    author='Matthew Wakefield',
    author_email='matthew.wakefield@unimelb.edu.au',
    python_requires=">=3.8",
    install_requires = [
      'setuptools',
      'lifelines>=0.26',
      'matplotlib>=3.3',
      'mpld3',
      'numpy>=1.16.5',
      'pandas>=1.2',
      'scipy>=1.6',
      'xlrd',
      'openpyxl',
      'jinja2'
    ],
    packages=['survivalvolume',
              ],
    zip_safe = True,
    include_package_data = True,
    url='https://git@bitbucket.org/genomematt/SurvivalVolume.git',
    license='GPLv3',
    description='Plotting tools for survival data',
    long_description='',
    classifiers=[
          'Development Status :: 5 - Production/Stable',
          'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
          'Operating System :: POSIX',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.10',
          'Topic :: Scientific/Engineering :: Bio-Informatics',
    ],

)
