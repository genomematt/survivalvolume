#!/usr/bin/env python3
# encoding: utf-8
"""
survivalvolume/test_data.py

Functions and classes for plotting tumour volume vs time and survival endpoints based on volume thresholds

Created by Matthew Wakefield.
Copyright (c) 2016  Matthew Wakefield, The Walter and Eliza Hall Institute and The University of Melbourne. All rights reserved.

   
   This program is distributed in the hope that it will be useful  but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.


"""

import pandas

__author__ = "Matthew Wakefield"
__copyright__ = "Copyright 2016 Matthew Wakefield, The Walter and Eliza Hall Institute and The University of Melbourne"
__credits__ = ["Matthew Wakefield",]
__license__ = "GPLv3"
__version__ = "1.2.1"
__maintainer__ = "Matthew Wakefield"
__email__ = "wakefield@wehi.edu.au"
__status__ = "production"


good_treatment = {'1231': {1: 196.6511265488, 4: 153.77168576, 8: 256.2981557136, 11: 233.54513028, 15: 206.6672908608, 18: 150.1259375, 22: 172.9756540512, 25: 205.4925104848, 29: 126.5664078448, 32: 145.55837835, 36: 184.172373, 39: 157.5682973172, 43: 110.0958860232, 46: 139.7430835416, 50: 129.8203368, 53: 123.3139826688, 57: 42.0091489972, 60: 65.1947298156, 64: 28.644472626, 67: 59.83617024, 71: 46.8841576896, 74: 19.5307208712, 78: 6.346032},
            '1232': {1: 229.1180661, 4: 194.61646512, 8: 361.9426867056,},
            '1233': {1: 183.5260924728, 4: 258.1537805, 8: 206.0693312832, 11: 201.5585256608, 15: 221.6776331308, 18: 177.5269444256, 22: 231.3327050804, 25: 136.5463379896, 29: 121.9458179632, 32: 106.513885016, 36: 45.938737152, 39: 54.3971558592, 43: 37.49786271, 46: 31.7043318592, 50: 23.6841605924, 53: 12.292366086, 57: 21.7628103924, 60: 34.2981478224, 64: 27.2308343076, 67: 52.36984368, 71: 47.5547274972, 74: 60.9342940052, 78: 62.2214070016, 81: 112.7826608832, 314: 131.7468853008, 315: 167.2883066624, 316: 137.5284157632},
            '1234': {1: 234.0284905728, 4: 207.2189851424, 8: 237.84955425, 11: 219.7504652112, 15: 233.4085848248, 18: 233.3102914912, 22: 288.3961483788, 25: 245.9228164624, 29: 146.3589465184, 32: 314.2432927172, 36: 259.1684953088, 39: 217.8321916848, 43: 165.3796610928},
            '1235': {1: 258.0944953664, 4: 262.3705271264, 8: 310.1161408576},
                }
             
vehicle = {'6666': {1: 189.2, 4: 278.13, 8: 274.69, 11: 347.82, 15: 507.35, 18: 322.61, 22: 729.18,},
         '6661': {1: 181.22, 4: 277.63, 8: 300.63, 11: 570.15, 15: 584.07, 18: 841.32,},
         '6663': {1: 261.01, 4: 552.57, 8: 414.30, 11: 557.21, 15: 725.49},
         '6665': {1: 219.89, 4: 243.41, 8: 592.57, 11: 416.23, 15: 725.89},
         '6664': {1: 204.29, 4: 344.84, 8: 346.97, 11: 351.16, 15: 575.32, 18: 647.39, 22: 618.77, 25: 856.63},
         '6669': {1: 207.047, 4: 270.52, 8: 265.35, 11: 276.19, 15: 300.78, 18: 530.20, 22: 342.98, 25: 488.18, 29: 364.79, 32: 919.84,},
         '6668': {1: 209.51, 4: 317.32, 8: 276.04, 11: 244.11, 15: 225.95, 18: 338.84, 22: 492.96, 25: 337.02, 29: 579.10, 32: 836.56,},
         '6667': {1: 211.23, 4: 199.20, 8: 154.58, 11: 317.42, 15: 326.65, 18: 594.09, 22: 411.46}}

other_treatment = {'7777': {1: 205.87, 4: 226.10, 8: 234.33, 11: 182.44, 15: 309.25, 18: 289.30, 22: 304.97, 25: 435.59, 29: 519.82, 32: 416.33, 36: 378.47, 39: 304.65, 43: 404.30, 46: 520.44, 50: 469.02, 53: 659.01, 57: 621.55, 60: 936.90},
         '7778': {1: 216.34, 4: 322.32, 8: 271.37, 11: 343.72, 15: 291.81, 18: 358.62, 22: 285.22, 25: 315.05, 29: 434.54, 32: 404.01, 36: 438.36, 39: 491.29, 43: 388.94, 46: 349.65, 50: 401.75, 53: 427.08, 57: 679.41, 60: 331.22, 64: 585.14, 67: 397.11, 71: 463.75, 74: 699.54, 78: 591.15, 81: 935.46},
         '7787': {1: 231.16, 4: 374.92, 8: 343.65, 11: 345.35, 15: 448.42, 18: 419.56, 22: 470.97, 25: 540.67},
         '7770': {1: 190.97, 4: 166.82, 8: 124.78},
         '7774': {1: 181.21, 4: 405.24, 8: 387.50, 11: 372.32, 15: 575.06, 18: 494.77, 22: 495.59, 25: 597.82, 29: 404.61, 32: 452.67, 36: 542.27, 39: 601.97, 43: 581.08, 46: 631.09, 50: 550.44, 53: 591.91, 57: 581.89, 60: 690.35, 64: 644.36, 67: 465.57, 71: 672.72, 74: 823.05},
         '7977': {1: 184.06, 4: 209.46, 8: 308.73, 11: 297.70, 15: 390.09, 18: 390.18, 22: 289.90, 25: 328.92, 29: 316.34, 32: 506.06, 36: 427.04, 39: 231.35, 43: 444.26, 46: 466.25, 50: 220.78, 53: 420.070, 57: 145.70, 60: 531.80, 64: 581.16, 67: 597.15, 71: 611.8, 74: 975.76},
         '7780': {1: 195.79, 4: 189.58, 8: 233.46, 11: 309.60, 15: 176.75, 18: 215.26, 22: 300.10, 25: 264.31, 29: 215.50, 32: 170.03, 36: 330.75, 39: 433.92, 43: 273.39, 46: 411.27, 50: 224.40, 53: 413.50, 57: 321.95, 60: 579.78, 64: 381.73, 67: 443.9, 71: 458.04, 74: 644.89, 78: 612.72},
         '7776': {1: 205.26, 4: 273.28, 8: 102.86, 11: 164.89, 15: 197.55, 18: 238.56, 22: 138.23},
         '7771': {1: 268.25, 4: 500.81, 8: 275.55, 11: 190.23, 15: 356.46, 18: 168.84, 22: 294.92}}
test_data = {'other_treatment': pandas.DataFrame(other_treatment),
            'vehicle': pandas.DataFrame(vehicle),
            'good_treatment': pandas.DataFrame(good_treatment),}

test_data['vehicle']