#!/usr/bin/env python3
# encoding: utf-8
"""
survivalvolume/test_plot.py

Functions and classes for plotting tumour volume vs time and survival endpoints based on volume thresholds

Created by Matthew Wakefield.
Copyright (c) 2016  Matthew Wakefield, The Walter and Eliza Hall Institute and The University of Melbourne. All rights reserved.

   
   This program is distributed in the hope that it will be useful  but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.


"""

import sys, io, os, unittest
import pandas
from numpy import nan
from survivalvolume.tests.test_data import test_data
from survivalvolume.plot import *
from hashlib import md5

__author__ = "Matthew Wakefield"
__copyright__ = "Copyright 2016 Matthew Wakefield, The Walter and Eliza Hall Institute and The University of Melbourne"
__credits__ = ["Matthew Wakefield",]
__license__ = "GPLv3"
__version__ = "1.2.4"
__maintainer__ = "Matthew Wakefield"
__email__ = "wakefield@wehi.edu.au"
__status__ = "production"



class test_parse(unittest.TestCase):
    def setUp(self):
        pass

    def test_version(self):
        self.assertEqual(version(), __version__)

    def test_get_survival_status(self):
        self.assertEqual(get_survival_status(pandas.Series([100,200,750,nan])),(2,True))
        self.assertEqual(get_survival_status(pandas.Series([100,200,750]),endpoint=1000),(2,False))
        self.assertEqual(get_survival_status(pandas.Series([100,200,nan])),(1,False))
        self.assertRaises(AttributeError, get_survival_status, 1)

    def test_volume_to_survival(self):
        df = pandas.DataFrame([[100,300,100],
                               [200,750,200],
                               [750,nan,300],
                               ])
        self.assertEqual(repr(volume_to_survival(df)).replace(' ',''),
                        "TimeObserved\n02True\n11True\n22False")
        self.assertEqual(repr(volume_to_survival(df, endpoint=1000)).replace(' ',''),
                        "TimeObserved\n02False\n11False\n22False")

    def test_make_km(self):
        df = pandas.DataFrame([[100,300,100],
                               [200,750,200],
                               [750,nan,300],
                               ])
        try:
            self.assertEqual(repr(make_km(df)),'<lifelines.KaplanMeierFitter:"Untitled", fitted with 3 total observations, 1 right-censored observations>')
            self.assertEqual(repr(make_km(df, endpoint=1000)),'<lifelines.KaplanMeierFitter:"Untitled", fitted with 3 total observations, 3 right-censored observations>')
        except:
            self.assertEqual(repr(make_km(df)),'<lifelines.KaplanMeierFitter:"Untitled", fitted with 3 total observations, 1 right-censored observations>')
            self.assertEqual(repr(make_km(df, endpoint=1000)),"<lifelines.KaplanMeierFitter: fitted with 3 observations, 3 censored>")

    def test_TumourVolumePlot_add_individuals(self):
        tvp = TumourVolumePlot()
        df = pandas.DataFrame([[100,300,100],
                               [200,750,200],
                               [750,nan,300],
                               ])
        tvp.add_individuals('TestData',df)
        self.assertEqual(list(tvp.lines),['TestData'])
        self.assertEqual(len(tvp.lines['TestData']),3)
        self.assertEqual(repr(tvp.lines['TestData'][0].get_data()).replace(' ',''),"(array([0,1,2]),array([100.,200.,750.]))")
        self.assertEqual(repr(tvp.lines['TestData'][1].get_data()).replace(' ',''),"(array([0,1,2]),array([300.,750.,nan]))")
        self.assertEqual(repr(type(tvp.lines['TestData'][0])),"<class 'matplotlib.lines.Line2D'>")

    def test_TumourVolumePlot_add_mean(self):
        tvp = TumourVolumePlot()
        df = pandas.DataFrame([[100,300,100],
                               [200,750,200],
                               [750,nan,300],
                               ])
        tvp.add_mean('TestData',df,threshold=1)
        self.assertEqual(list(tvp.means),['TestData'])
        self.assertEqual(len(tvp.means['TestData']),1)
        self.assertEqual(repr(tvp.means['TestData'][0].get_data()).replace(' ',''),'(array([0,1,2]),array([166.66666667,383.33333333,525.]))')
        self.assertEqual(repr(type(tvp.means['TestData'][0])),"<class 'matplotlib.lines.Line2D'>")

    def test_TumourVolumePlot__calc_norm_ci(self):
        tvp = TumourVolumePlot()
        df = pandas.DataFrame([[100,300,100],
                               [200,750,200],
                               [750,nan,300],
                               ])
        self.assertEqual(tvp._calc_norm_ci(df).to_dict(),
            {'lower bound': {0: 36.002401030663037,
                             1: 24.00660283432336,
                             2: 84.00810347848784},
             'mean': {0: 166.66666666666666,
                      1: 383.33333333333331,
                      2: 525.0},
             'upper bound': {0: 297.33093230267025,
                             1: 742.66006383234321,
                             2: 965.99189652151222}
             })
    
    def test_TumourVolumePlot__calc_t_ci(self):
        tvp = TumourVolumePlot()
        df = pandas.DataFrame([[100,300,100],
                               [200,750,200],
                               [750,nan,300],
                               ])
        df.index = [7,14,21]
        self.assertEqual(list(tvp._calc_t_ci(df).index),[7,14,21])
        self.assertEqual(tvp._calc_t_ci(df).to_dict(),
            {'lower bound': {7: 0, 14: 0, 21: 0},
             'mean': {7: 166.66666666666666,
                      14: 383.33333333333331,
                      21: 525.0},
             'upper bound': {7: 453.51018199408497,
                             14: 1172.1530004837336,
                             21: 3383.8960656972213}
            })
        df = pandas.DataFrame([[101,99,100,102,98,100],
                               [201,199,200,202,198,200],
                               [501,499,500,502,498,500],
                               ])
        self.assertEqual(tvp._calc_t_ci(df).to_dict(),
            {'lower bound': {0: 98.515873884656514,
                             1: 198.51587388465651,
                             2: 498.51587388465651},
             'mean': {0: 100.0, 1: 200.0, 2: 500.0},
             'upper bound': {0: 101.48412611534349,
                             1: 201.48412611534349,
                             2: 501.48412611534349}
            })

    def test_TumourVolumePlot_add_interval(self):
        tvp = TumourVolumePlot()
        df = pandas.DataFrame([[100,300,100],
                               [200,750,200],
                               [750,nan,300],
                               ])
        tvp.add_interval('TestData',df,threshold=1)
        self.assertEqual(list(tvp.intervals),['TestData'])
        self.assertEqual(repr(type(tvp.intervals['TestData'])),"<class 'matplotlib.collections.PolyCollection'>")
        self.assertEqual(repr(tvp.intervals['TestData'].__dict__['_paths']).replace(' ',''),"""[Path(array([[  0.00000000e+00,   4.53510182e+02],
       [  0.00000000e+00,   0.00000000e+00],
       [  1.00000000e+00,   0.00000000e+00],
       [  2.00000000e+00,   0.00000000e+00],
       [  2.00000000e+00,   3.38389607e+03],
       [  2.00000000e+00,   3.38389607e+03],
       [  1.00000000e+00,   1.17215300e+03],
       [  0.00000000e+00,   4.53510182e+02],
       [  0.00000000e+00,   4.53510182e+02]]), array([ 1,  2,  2,  2,  2,  2,  2,  2, 79], dtype=uint8))]""".replace(' ',''))

    #@unittest.expectedFailure
    def test_TumourVolumePlot_display(self):
        tvp = TumourVolumePlot()
        df = pandas.DataFrame([[100,300,100],
                               [200,750,200],
                               [750,nan,300],
                               ])
        tvp.add_mean('TestData',df)
        d = tvp.display().data
        self.assertEqual(d.count('"data03": [[0.01612903225806453, 0.9067708333333333], [0.27861643145161297, 0.9067708333333333], [0.27861643145161297, 0.9791666666666665], [0.01612903225806453, 0.9791666666666665]]'),0)
        self.assertEqual(d.count('"data02": [[0.038709677419354854, 0.9458333333333332], [0.08387096774193549, 0.9458333333333332]]'),0)
        self.assertEqual(d.count('"data01": [[0.0, 166.66666666666666], [1.0, 383.3333333333333], [2.0, 525.0]]'),0)
        tvp.add_mean('TestData',df)
        self.assertEqual(repr(type(tvp.display(use_mpld3=False))),"<class 'matplotlib.figure.Figure'>")

    def test_TumourVolumePlot_set_spines_and_ticks(self):
        tvp = TumourVolumePlot()
        tvp.set_spines_and_ticks()
        self.assertEqual(tvp.ax.spines['top'].get_visible(),False)
        self.assertEqual(tvp.ax.spines['right'].get_visible(),False)
        self.assertEqual(tvp.ax.spines['left'].get_visible(),True)
        self.assertEqual(tvp.ax.spines['bottom'].get_visible(),True)
        tvp = TumourVolumePlot()
        tvp.set_spines_and_ticks(remove_spines=['left','bottom'],y_set_ticks = ['right'],x_set_ticks = ['top'],)
        self.assertEqual(tvp.ax.spines['top'].get_visible(),True)
        self.assertEqual(tvp.ax.spines['right'].get_visible(),True)
        self.assertEqual(tvp.ax.spines['left'].get_visible(),False)
        self.assertEqual(tvp.ax.spines['bottom'].get_visible(),False)
        self.assertEqual(tvp.ax.xaxis.get_ticks_position(),'top')
        self.assertEqual(tvp.ax.yaxis.get_ticks_position(),'right')
    
    def test_TumourVolumePlot_set_limits(self):
        tvp = TumourVolumePlot()
        tvp.ylim = [0,500]
        tvp.xlim = [1,7]
        tvp.set_limits()
        self.assertEqual(tvp.ax.get_ylim(),(0.0,500.0))
        self.assertEqual(tvp.ax.get_xlim(),(1.0,7.0))

    def test_TumourVolumePlot_set_title_and_labels(self):
        tvp = TumourVolumePlot()
        tvp.title = 'fabulous looking plot'
        tvp.ylabel = 'hugeness'
        tvp.xlabel = 'time'
        tvp.set_title_and_labels()
        self.assertEqual(tvp.ax.get_title(),'fabulous looking plot')
        self.assertEqual(tvp.ax.get_ylabel(),'hugeness')
        self.assertEqual(tvp.ax.get_xlabel(),'time')
        tvp.set_title_and_labels(title='software',xlabel='lines of code',ylabel='bugs')
        self.assertEqual(tvp.ax.get_title(),'software')
        self.assertEqual(tvp.ax.get_xlabel(),'lines of code')
        self.assertEqual(tvp.ax.get_ylabel(),'bugs')

    def test_TumourVolumePlot_add_legend(self):
        tvp = TumourVolumePlot()
        df = pandas.DataFrame([[100,300,100],
                               [200,750,200],
                               [750,nan,300],
                               ])
        tvp.add_mean('TestData',df)
        tvp.add_legend()
        self.assertEqual(tvp.ax.legend_.__dict__['_visible'],True)
        self.assertEqual(str(tvp.ax.legend_.__dict__['texts'][0]).replace(' ',''),"Text(0,0,'TestData')")
        tvp.add_mean('MoreData',df)
        tvp.add_legend()
        self.assertEqual(tvp.ax.legend_.__dict__['_visible'],True)
        # Result order are non deterministic in python 3.0-3.5 so we need to sort
        self.assertEqual(sorted([str(x).replace(' ','') for x in tvp.ax.legend_.__dict__['texts']]),["Text(0,0,'MoreData')","Text(0,0,'TestData')"])

    #Test only in pdf
    #def test_TumourVolumePlot_show_treatment_days(self):
    #def test_TumourVolumePlot_shade_interval(self):

    def test_VolumeSurvivalPlot_add_mean(self):
        dual = VolumeSurvivalPlot()
        df = pandas.DataFrame([[100,300,100],
                               [200,750,200],
                               [750,nan,300],
                               ])
        dual.add_mean('TestData',df,threshold=1)
        self.assertEqual(list(dual.means),['TestData'])
        self.assertEqual(len(dual.means['TestData']),1)
        self.assertEqual(repr(dual.means['TestData'][0].get_data()).replace(' ',''),"(array([0,1,2]),array([166.66666667,383.33333333,525.]))")
        self.assertEqual(repr(type(dual.means['TestData'][0])),"<class 'matplotlib.lines.Line2D'>")
        try:
            self.assertEqual(repr(dual.kmfs['TestData']),"<lifelines.KaplanMeierFitter: fitted with 3 total observations, 1 right-censored observations>")
        except:
            self.assertEqual(repr(dual.kmfs['TestData']),'<lifelines.KaplanMeierFitter:"TestData", fitted with 3 total observations, 1 right-censored observations>')
        print()

    #Tested in test_VolumeSurvivalPlot_add_mean
    #def test_VolumeSurvivalPlot_add_kmf(self):
    
    def test_VolumeSurvivalPlot_set_spines_and_ticks(self):
        dual = VolumeSurvivalPlot()
        dual.set_spines_and_ticks()
        self.assertEqual(dual.ax.spines['top'].get_visible(),False)
        self.assertEqual(dual.ax.spines['right'].get_visible(),False)
        self.assertEqual(dual.ax.spines['left'].get_visible(),True)
        self.assertEqual(dual.ax.spines['bottom'].get_visible(),True)
        self.assertEqual(dual.km_ax.spines['top'].get_visible(),False)
        self.assertEqual(dual.km_ax.spines['right'].get_visible(),False)
        self.assertEqual(dual.km_ax.spines['left'].get_visible(),True)
        self.assertEqual(dual.km_ax.spines['bottom'].get_visible(),True)
        dual = VolumeSurvivalPlot()
        dual.set_spines_and_ticks(remove_spines=['left','bottom'],y_set_ticks = ['right'],x_set_ticks = ['top'],)
        self.assertEqual(dual.ax.spines['top'].get_visible(),True)
        self.assertEqual(dual.ax.spines['right'].get_visible(),True)
        self.assertEqual(dual.ax.spines['left'].get_visible(),False)
        self.assertEqual(dual.ax.spines['bottom'].get_visible(),False)
        self.assertEqual(dual.ax.xaxis.get_ticks_position(),'top')
        self.assertEqual(dual.ax.yaxis.get_ticks_position(),'right')
        self.assertEqual(dual.km_ax.spines['top'].get_visible(),True)
        self.assertEqual(dual.km_ax.spines['right'].get_visible(),True)
        self.assertEqual(dual.km_ax.spines['left'].get_visible(),False)
        self.assertEqual(dual.km_ax.spines['bottom'].get_visible(),False)
        self.assertEqual(dual.km_ax.xaxis.get_ticks_position(),'top')
        self.assertEqual(dual.km_ax.yaxis.get_ticks_position(),'right')
    
    def test_VolumeSurvivalPlot_set_limits(self):
        dual = VolumeSurvivalPlot()
        dual.ylim = [0,500]
        dual.xlim = [1,7]
        dual.set_limits()
        self.assertEqual(dual.ax.get_ylim(),(0.0,500.0))
        self.assertEqual(dual.ax.get_xlim(),(1.0,7.0))
        self.assertEqual(dual.km_ax.get_ylim(),(0.0,1.02))
        self.assertEqual(dual.km_ax.get_xlim(),(1.0,7.0))

    def test_VolumeSurvivalPlot_set_title_and_labels(self):
        dual = VolumeSurvivalPlot()
        dual.title = 'fabulous looking plot'
        dual.ylabel = 'hugeness'
        dual.xlabel = 'time'
        dual.set_title_and_labels()
        self.assertEqual(dual.ax.get_title(),'fabulous looking plot')
        self.assertEqual(dual.ax.get_ylabel(),'hugeness')
        self.assertEqual(dual.ax.get_xlabel(),'')
        self.assertEqual(dual.km_ax.get_title(),'')
        self.assertEqual(dual.km_ax.get_ylabel(),'Survival')
        self.assertEqual(dual.km_ax.get_xlabel(),'Days')
        dual.set_title_and_labels(title='software',xlabel='lines of code',ylabel='bugs',km_xlabel='lines of code',km_ylabel='bugs',hide_volume_labels=False)
        self.assertEqual(dual.ax.get_title(),'software')
        self.assertEqual(dual.ax.get_xlabel(),'lines of code')
        self.assertEqual(dual.ax.get_ylabel(),'bugs')
        self.assertEqual(dual.km_ax.get_title(),'')
        self.assertEqual(dual.km_ax.get_ylabel(),'bugs')
        self.assertEqual(dual.km_ax.get_xlabel(),'lines of code')
    
    
    def test_VolumeSurvivalPlot_logrank_test(self):
        dual = VolumeSurvivalPlot()
        for name in test_data:
            dual.add_mean(name, test_data[name])
        result = dual.logrank_test('vehicle','good_treatment')
        print(dir(result))
        self.assertAlmostEqual(result.p_value,0.013300935934119806) 
        self.assertAlmostEqual(result.test_statistic,6.1286371924585152) 
    
    @unittest.expectedFailure
    def test_VolumeSurvivalPlot_to_PDF(self):
        #make a plot with all the bells and whistles and export to pdf
        dual = VolumeSurvivalPlot(figsize=(15,8))

        dual.xlim = [0,85]
        dual.ylim = [-2,1000]

        dual.km_show_censors = True
        dual.km_ci_show = False

        dual.add_mean('A treatment',test_data['other_treatment'],color='orange')
        dual.add_individuals('A treatment',test_data['other_treatment'],color='orange', dashes = [1,1])
        dual.add_interval('A treatment',test_data['other_treatment'],color='orange')

        dual.add_mean('Vehicle',test_data['vehicle'],color='blue')
        dual.add_individuals('Vehicle',test_data['vehicle'],color='blue', dashes = [3,3])
        dual.add_interval('Vehicle',test_data['vehicle'],color='blue')

        dual.add_mean('Good Treatment',test_data['good_treatment'],color='green')
        dual.add_individuals('Good Treatment',test_data['good_treatment'],color='green', dashes = [1,2,3,2])
        dual.add_interval('Good Treatment',test_data['good_treatment'],color='green')
        
        dual.show_treatment_days([1,3,5,8,10,12,], facecolor="lightgrey")
        dual.show_treatment_days([15,17,19], facecolor="lightblue")

        dual.ax.axhline(200,color='lightgrey',lw=1,alpha=0.3)
        
        dual.shade_interval(0,25)

        dual.title = 'My Great Experiment'
        
        #dual.save_pdf(os.path.join(os.path.dirname(__file__), 'data/combined_test.pdf'))
        dual.save_pdf(os.path.join(os.path.dirname(__file__), 'data/compare_to_combined_test.pdf'))

        #if sys.version_info[0:2] > (3, 5):
        outfile = io.BytesIO()
        dual.save_pdf(fileobj=outfile)
        self.assertEqual(md5(outfile.getvalue()).hexdigest(),'')
        
        
if __name__ == '__main__':
    unittest.main(buffer=True)
