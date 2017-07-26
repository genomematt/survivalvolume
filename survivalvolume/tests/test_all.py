#!/usr/bin/env python3
# encoding: utf-8
"""
survivalvolume/test_all.py

Functions and classes for plotting tumour volume vs time and survival endpoints based on volume thresholds

Created by Matthew Wakefield.
Copyright (c) 2016  Matthew Wakefield, The Walter and Eliza Hall Institute and The University of Melbourne. All rights reserved.

   
   This program is distributed in the hope that it will be useful  but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.


"""

import unittest
from survivalvolume.tests.test_parse import *
from survivalvolume.tests.test_plot import *

__author__ = "Matthew Wakefield"
__copyright__ = "Copyright 2011-2016 Matthew Wakefield, The Walter and Eliza Hall Institute and The University of Melbourne"
__credits__ = ["Matthew Wakefield",]
__license__ = "GPLv3"
__version__ = "1.1.0"
__maintainer__ = "Matthew Wakefield"
__email__ = "wakefield@wehi.edu.au"
__status__ = "Production"

if __name__ == "__main__":
    unittest.main(buffer=True)