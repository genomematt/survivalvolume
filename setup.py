#!/usr/bin/env python
from setuptools import setup

setup(
    name='survivalvolume',
    version='1.0.0b1',
    author='Matthew Wakefield',
    author_email='matthew.wakefield@unimelb.edu.au',
    install_requires = [
      'setuptools >= 1.1.6',
      'lifelines >= 0.9.0.0',
      'matplotlib >= 1.4.3',
      'mpld3 >= 0.2',
      'numpy >= 1.10.1',
      'pandas >= 0.17.0',
      'scipy >= 0.16.1',
      'seaborn >= 0.6.0',
      'xlrd >= 0.9.4',
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
          'Development Status :: 6 - beta',
          'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
          'Operating System :: POSIX',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Topic :: Scientific/Engineering :: Bio-Informatics',
    ],

)
