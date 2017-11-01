[![Build Status](https://travis-ci.org/genomematt/survivalvolume.svg?branch=master)](https://travis-ci.org/genomematt/survivalvolume)
[![DOI](https://zenodo.org/badge/72341202.svg)](https://zenodo.org/badge/latestdoi/72341202)
[![JOSS](http://joss.theoj.org/papers/2876777be3db1050198a70bb6a8306a9/status.svg)](http://dx.doi.org/10.21105/joss.00111)
[![PyPI](https://img.shields.io/pypi/v/survivalvolume.svg)](https://pypi.python.org/pypi/survivalvolume/)

# SurvivalVolume
v1.2.0
Matthew Wakefield

Treatment studies of cancer frequently use tumour volume to measure response to therapy.  Therapeutic response will be apparent at different time points during the experiment.  Progressive disease (increasing volume), stable disease and regression (reduction in volume) under therapy are important measures of response in addition to the overall time to reach a defined maximum volume.  Traditional methods of presenting this data involve 3 unconnected graphs: line graphs of each individual, average volume of each group with standard error of the mean, and a Kaplan-Meier graph of time to maximum volume.

Survival volume is a python package to produce an integrated plot of these three representations of the same data, and to provide interaction with the plots of volume to enhance exploration of outliers and subgroups that are of interest clinically.

Survival volume can also be applied to any other survival application where a measurement is taken over time, and a threshold used to determine failure, eg tyre tread wear.

# Installation

Survival volume is written for use with Python3

It has dependencies on matplotlib v1.3-1.5, mpld3, lifelines, scipy, pandas, numpy and xlrd.

It is recommended that you use a pyvenv virtual environment.

For a simple install using the release version of mpld3 you can either install from the Python Package Index (PyPI)

```pip3 install survivalvolume```

or from the github repository

```pip3 install git+https://github.com/genomematt/survivalvolume.git```

To run the tests use

```python3 -m survivalvolume.tests.test_all```

It is also recommended to run the user_guide.ipynb file and visually compare it to the html version (see below)

# Usage

Worked examples of how to use survivalvolume are provided in the user guide

Github will not render all the graphics in the User Guide jupyter notebook in the github repository, you can see the text just not the output.
To look at the graphics you can either download the html version and open in your browser, or view the html on github.io

[User Guide on github.io](https://genomematt.github.io/survivalvolume/docs/user_guide.html)

[API documentation for parsing files](https://genomematt.github.io/survivalvolume/docs/parse.m.html)

[API documentation for plotting files](https://genomematt.github.io/survivalvolume/docs/plot.m.html)

# Contributing to survivalvolume
Survivalvolume is licensed under the GPLv3.  You are free to fork this repository under the terms of that license.  If you have suggested changes please start by raising an issue in the issue tracker.  Pull requests are welcome and will be included at the discretion of the author.
Bug reports should be made to the issue tracker.  Difficulty in understanding how to use the software is a documentation bug, and should also be raised on the issue tracker with the tag `question` so your question and my response are easily found by others.


# Citing survivalvolume

Survivalvolume is published in the Journal of Open Source Software. Please cite the paper in academic publications [DOI:10.21105/joss.00111](http://dx.doi.org/10.21105/joss.00111). Each release also has a Zenodo DOI identifier for each release.  In an ideal world this is what you would cite to indicate the code you use, and make everything more reproducible but academic credit is better served at the moment by the paper. Try and include the Zenodo DOI or a version number in your methods.  The DOI for the current release is [![Zenodo DOI](https://zenodo.org/badge/72341202.svg)](https://zenodo.org/badge/latestdoi/72341202)

```
@article{JWakefield2016,
  doi = {10.21105/joss.00111},
  url = {http://dx.doi.org/10.21105/joss.00111},
  year  = {2016},
  month = {dec},
  publisher = {The Open Journal},
  volume = {1},
  number = {8},
  author = {Matthew J. Wakefield},
  title = {{SurvivalVolume}: interactive volume threshold survival graphs},
  journal = {The Journal of Open Source Software}
}
```

# References
Davidson-Pilon, C., Lifelines, (2016), Github repository, https://github.com/CamDavidsonPilon/lifelines
