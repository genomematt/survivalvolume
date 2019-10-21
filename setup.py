#!/usr/bin/env python
from setuptools import setup

setup(
    name='survivalvolume',
    version='1.2.2',
    author='Matthew Wakefield',
    author_email='matthew.wakefield@unimelb.edu.au',
    install_requires = [
      'setuptools',
      'lifelines>=0.22.8',
      'matplotlib',
      'mpld3',
      'numpy',
      'pandas>=0.25.1',
      'scipy',
      'xlrd',
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
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Topic :: Scientific/Engineering :: Bio-Informatics',
    ],

)
