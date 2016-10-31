[![Build Status](https://travis-ci.org/genomematt/survivalvolume.svg?branch=master)](https://travis-ci.org/genomematt/survivalvolume)
[![DOI](https://zenodo.org/badge/72341202.svg)](https://zenodo.org/badge/latestdoi/72341202)
# SurvivalVolume
v1.0.0
Matthew Wakefield

A set of tools for parsing measurement with threshold over time data (eg tyre wear, tumour treatment studies) and generating interactive and static plots.

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

### Optionally install the development version of mpld3

Survival Volume is most fully featured with mpld3 version 0.3dev post commit 559dfc6.  Currently the easiest way to install a compatible version is to install from the current development master branch on github.
Some features will still not work reliably until the required changes make their way into the javascript that gets downloaded by the html.  As of the last revision of this document in October 2016 the dual plots only display correctly in mpld3 if you use mpld3.show() or modify the url in the output.  Cached files can also create issues.

The mpld3 development version is only needed for interactive html dual volume and survival plots.  PDF plots and volume plots are not affected by the inability to draw stepped lines in in mpld3 v0.2.

To install the development version of mpld3 you will need to

```git clone https://github.com/mpld3/mpld3
cd mpld3/
python3 setup.py submodule
python3 setup.py install```

In your jupyter notebooks you will also need to redirect mpld3 to the local javascript files.

```import mpld3
mpld3.enable_notebook(d3_url='file://d3.v3.min.js',
                     mpld3_url='file://mpld3.v0.3git.js')```

A mpld3 release v0.3 is in preparation and will remove the need to install the development version.

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


#Citing survivalvolume

Survivalvolume is currently unpublished and has a Zenodo id for each release. Please include the Zenodo DOI or a version number in your methods, and cite the github URL if supported by your journal.

Wakefield, M.J, survivalvolume, (2016), Github repository, https://github.com/genomematt/survivalvolume

#References
Davidson-Pilon, C., Lifelines, (2016), Github repository, https://github.com/CamDavidsonPilon/lifelines