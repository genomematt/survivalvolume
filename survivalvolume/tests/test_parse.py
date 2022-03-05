#!/usr/bin/env python3
# encoding: utf-8
"""
survivalvolume/test_parse.py

Functions and classes for plotting tumour volume vs time and survival endpoints based on volume thresholds

Created by Matthew Wakefield.
Copyright (c) 2016  Matthew Wakefield, The Walter and Eliza Hall Institute and The University of Melbourne. All rights reserved.

   
   This program is distributed in the hope that it will be useful  but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.


"""

import sys, io, unittest
import pandas
from numpy import nan
from survivalvolume.tests.test_data import test_data
from survivalvolume.parse import *

__author__ = "Matthew Wakefield"
__copyright__ = "Copyright 2016 Matthew Wakefield, The Walter and Eliza Hall Institute and The University of Melbourne"
__credits__ = ["Matthew Wakefield",]
__license__ = "GPLv3"
__version__ = "1.2.4"
__version__ = "1.2.4"
__maintainer__ = "Matthew Wakefield"
__email__ = "wakefield@wehi.edu.au"
__status__ = "production"


class test_parse(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_split_on_nans(self):
        data = pandas.read_csv(io.StringIO('''
,,,,,,\n
,,,,,,\n
,,,A,B,\n
,,1,181.22,261.01,\n
,,4,277.63,552.57,\n
,,,,,,\n
,,,,,,\n
,,,,,,\n
,,,C,D,\n
,,1,180.22,260.01,\n
,,4,278.63,550.57,\n
,,,,,,\n
'''))
        
        result = split_on_nans(data)
        self.assertEqual(result[4].to_csv(),""",Unnamed: 0,Unnamed: 1,Unnamed: 2,Unnamed: 3,Unnamed: 4,Unnamed: 5,Unnamed: 6
7,,,,C,D,,
8,,,1.0,180.22,260.01,,
9,,,4.0,278.63,550.57,,
10,,,,,,,
""")

    def test_clean_tv_table(self):
        data = pandas.DataFrame({0: {16: nan, 7: nan, 8: nan, 9: nan, 10: nan, 11: nan, 12: nan, 13: nan, 14: nan, 15: nan},
        1: {16: nan, 7: 'Vehicle', 8: 'Day', 9: 1, 10: 4, 11: 8, 12: 11, 13: 15, 14: 18, 15: 22},
        2: {16: nan, 7: nan, 8: 'A', 9: 100.24, 10: 150.14, 11: 200.69, 12: 300.83, 13: 400.35, 14: 500.62, 15: 750.18},
        3: {16: nan, 7: nan, 8: 'B', 9: 150.14, 10: 200.69, 11: 300.83, 12: 400.35, 13: 500.62, 14: 750.18, 15: nan},
        4: {16: nan, 7: nan, 8: 'C', 9: 200.69, 10: 300.83, 11: 400.35, 12: 500.62, 13: 750.18, 14: nan, 15: nan},
        5: {16: nan, 7: nan, 8: 'Mean', 9: 150.35666666666665, 10: 217.22, 11: 300.62333333333333, 12: 400.6000000000001, 13: 550.3833333333333, 14: 625.4, 15: 750.18}})
        result = clean_tv_table(data)
        self.assertEqual(result[0],'Vehicle')
        self.assertEqual(result[1].to_csv(),"""Day,A,B,C
1,100.24,150.14,200.69
4,150.14,200.69,300.83
8,200.69,300.83,400.35
11,300.83,400.35,500.62
15,400.35,500.62,750.18
18,500.62,750.18,
22,750.18,,
""")

    def test_studylog_prism_df_to_tv_tables(self):
        data = pandas.read_csv(io.StringIO(""",0,1,2,3,4,5
,,,,,
Test Data Sheet with vital features of a studylog Prism export file,,,,,
,,,,,
Tumor Volume (All Animals),,,,,
,,,,,
,,,,,
Tumor Volume (All Animals),,,,,
,Vehicle,,,,
,Day,A,B,C,Mean
,1,100.24,150.14,200.69,150.35666666666665
,4,150.14,200.69,300.83,217.22
,8,200.69,300.83,400.35,300.62333333333333
,11,300.83,400.35,500.62,400.6000000000001
,15,400.35,500.62,750.18,550.3833333333333
,18,500.62,750.18,,625.4
,22,750.18,,,750.18
,,,,,
,Treat,,,,
,Day,T,Mean,,
,1,230.79,230.79,,
,4,194.62,194.62,,
,8,161.48,161.48,,
,,,,,
,,,,,
,,,,,
,,,,,
Scatterplot information for Prism,,,,,"""), header=None)
        result = studylog_prism_df_to_tv_tables(data)
        self.assertEqual(repr(result['Vehicle']),
"""9         A       B       C
Day                        
1    100.24  150.14  200.69
4    150.14  200.69  300.83
8    200.69  300.83  400.35
11   300.83  400.35  500.62
15   400.35  500.62  750.18
18   500.62  750.18     NaN
22   750.18     NaN     NaN""")

    def test_studylog_absolute_df_to_tv_tables(self):
        data = pandas.read_csv(io.StringIO("""FakeTestData,,,,,,,,,,,,
Task: Tumor Volume (mm_),,,,,,,,,,,,
Absolute Values,,,,,,,,,,,,
,,,,,,,,,,,,
,,,,,,,,,,,,
Group,Animal ID,"Study Days
Data Type","1","5","26","30","33","36","40","44","44","47"
DPBS,9981,Abs,221.72,321.42,543.99,579.91,646.02,642.85,790.69,,,
DPBS,9982,Abs,278.24,188.04,635.60,540.36,702.74,,,,,
DPBS,ABCD,Abs,215.42,213.96,524.10,508.32,466.58,595.97,429.50,626.53,554.09,850.12
Mock,9986 (T3),Abs,225.25,243.62,520.71,672.37,656.77,,,,,
Mock,9991,Abs,197.33,342.86,373.02,248.24,302.37,342.32,531.49,426.04,501.13,555.22
Mock,9992,Abs,237.19,238.24,436.23,503.68,646.62,595.41,673.14,620.50,764.15,"""), header=5)
        result = studylog_absolute_df_to_tv_tables(data)
        self.assertEqual(repr(result['DPBS']),
"""Animal ID    9981    9982    ABCD
1          221.72  278.24  215.42
5          321.42  188.04  213.96
26         543.99   635.6   524.1
30         579.91  540.36  508.32
33         646.02  702.74  466.58
36         642.85     NaN  595.97
40         790.69     NaN   429.5
44            NaN     NaN  626.53
44.1          NaN     NaN  554.09
47            NaN     NaN  850.12""")
        
    def test_fixed_length_alternate_steps(self):
        self.assertEqual(fixed_length_alternate_steps(1,12,3,4),[1, 4, 8, 11, 15, 18, 22, 25, 29, 32, 36, 39])
        self.assertEqual(fixed_length_alternate_steps(7,2,3,4),[7,10])
        self.assertEqual(fixed_length_alternate_steps(1,10,2,-1),[1, 3, 2, 4, 3, 5, 4, 6, 5, 7])
        self.assertEqual(fixed_length_alternate_steps(-7,12,1,7),[-7, -6, 1, 2, 9, 10, 17, 18, 25, 26, 33, 34])
    
    def test_standardise_days(self):
        df = pandas.DataFrame([[1,2,3],[4,5,6],[7,8,9]])
        self.assertEqual(repr(standardise_days(df,first_interval=5,second_interval=2)),'   0  1  2\n1  1  2  3\n6  4  5  6\n8  7  8  9')

    
if __name__ == '__main__':
    unittest.main()