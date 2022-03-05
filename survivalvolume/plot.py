#!/usr/bin/env python3
# encoding: utf-8
"""
survivalvolume/plot.py

Functions and classes for plotting tumour volume vs time and survival endpoints based on volume thresholds

Created by Matthew Wakefield.
Copyright (c) 2016  Matthew Wakefield, The Walter and Eliza Hall Institute and The University of Melbourne. All rights reserved.

   
   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.


"""

import pandas
import matplotlib
import mpld3
import lifelines
from lifelines.statistics import logrank_test
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats
from mpld3 import plugins, utils

__author__ = "Matthew Wakefield"
__copyright__ = "Copyright 2016 Matthew Wakefield, The Walter and Eliza Hall Institute and The University of Melbourne"
__credits__ = ["Matthew Wakefield",]
__license__ = "GPLv3"
__version__ = "1.2.4"
__maintainer__ = "Matthew Wakefield"
__email__ = "wakefield@wehi.edu.au"
__status__ = "production"

def version():
    """Return the symatic versioning format version number"""
    return __version__
    
def get_survival_status(tv_series, endpoint=700):
    """Convert a pandas series of tumour volume measurements
    organised with one individual per column and indexed by time
    to a pandas data frame with columns for time and endpoint observed
    (the inverse of censored) and indexed by individual.
    
    Arguments:
    
        tv_series - a pandas series of tumour volume measurements
                    indexed by time
    
        endpoint  - the volume threshold at which and endpoint
                    event is deemed to have occurred
    
    Returns:
    
        time      - the last time index observed
    
        observed  - a boolean for whether the endpoint has
                    been reached (inverse of censored status)
    """
    tv_series = tv_series.dropna()
    observed = True
    try:
        if tv_series.iloc[-1] < endpoint:
            observed = False
        return tv_series.index[-1], observed
    except:
        print(tv_series)
        raise

def volume_to_survival(tv_data, endpoint=700):
    """Convert a pandas data frame of tumour volume measurements
    organised with one individual per column and indexed by time
    to a pandas data frame with columns for time and endpoint observed
    (the inverse of censored) and indexed by individual.
    
    Arguments:
    
        tv_data   - a pandas data frame of volume measurements
                    arranged with individuals in columns and
                    indexed by time
    
        endpoint  - the volume threshold at which and endpoint
                    event is deemed to have occurred
    
    Returns:
    
        A pandas data frame with columns 'Time' and 'Observed'
        indexed by individuals (column names in tv_data)
        Time      - the last time index observed
        Observed  - a boolean for whether the endpoint has
                    been reached (inverse of censored status)
    """
    survival = pandas.DataFrame(
                        {x:get_survival_status(tv_data[x],endpoint=endpoint) \
                        for x in tv_data if tv_data[x].any()}
                        ).T
    survival.columns=['Time','Observed']
    return survival

def make_km(tv_data, label='Untitled',endpoint=700):
    """Construct a Kaplan-Meier function for a dataframe
    of tumour volume measurements
    
    Arguments:
    
        tv_data  - a pandas data frame of volume measurements
                   with individuals in columns and timepoints
                   as rows.  Individuals are removed from study
                   at the first NaN timepoint
    
        label    - a title for this grouping
    
        endpoint - the volume at which the endpoint is reached
                   Default: 700
    
    Returns:
    
        a lifelines KaplanMeierFitter object
    """
    survival = volume_to_survival(tv_data, endpoint=endpoint)
    kmf = lifelines.KaplanMeierFitter()
    kmf.fit(survival['Time'],event_observed=survival['Observed'],label=label)
    return kmf

class HighlightLines(plugins.PluginBase): #pragma non cover
    """A plugin to highlight lines on hover
    Adapted from mpld3 example code"""

    JAVASCRIPT = """
    mpld3.register_plugin("linehighlight", LineHighlightPlugin);
    LineHighlightPlugin.prototype = Object.create(mpld3.Plugin.prototype);
    LineHighlightPlugin.prototype.constructor = LineHighlightPlugin;
    LineHighlightPlugin.prototype.requiredProps = ["line_ids"];
    LineHighlightPlugin.prototype.defaultProps = {alpha_bg:0.3, alpha_fg:1.0}
    function LineHighlightPlugin(fig, props){
        mpld3.Plugin.call(this, fig, props);
    };

    LineHighlightPlugin.prototype.draw = function(){
      for(var i=0; i<this.props.line_ids.length; i++){
         var obj = mpld3.get_element(this.props.line_ids[i], this.fig),
             alpha_fg = this.props.alpha_fg;
             alpha_bg = this.props.alpha_bg;
         obj.elements()
             .on("mouseover.highlight", function(d, i){
                            d3.select(this).transition().duration(50)
                              .style("stroke-opacity", alpha_fg); })
             .on("mouseout.highlight", function(d, i){
                            d3.select(this).transition().duration(200)
                              .style("stroke-opacity", alpha_bg); });
      }
    };
    """

    def __init__(self, lines):
        self.lines = lines
        self.dict_ = {"type": "linehighlight",
                      "line_ids": [utils.get_id(line) for line in lines],
                      "alpha_bg": lines[0].get_alpha(),
                      "alpha_fg": 1.0}

class TumourVolumePlot():
    """Construct a plot of volume vs time
    This plot is designed to consist of measurements for individuals,
    a mean volume for the group and a standard error of the mean.
    When used to produce html the resulting graph is interactive with
    mouse over highlighting of individuals and labeling with the column
    name.  Static pdfs can also be generated.
    """
    def __init__(self, **kw):
        """Initiate a new tumour TumourVolumePlot object
        
        Arguments:
        
            **kw - keyword arguments are passed to
                   matplotlib.pyplot.subplots
        """
        self.fig, self.ax = plt.subplots(**kw)
        self.lines = {}
        self.means = {}
        self.intervals = {}
        self.title = 'Untitled'
        self.ylabel = 'Tumour Volume mm$^{3}$'
        self.xlabel = 'Days'
        self.xlim = None
        self.ylim = None
        self.fontsize = None
        self.n_in_legend = False
        pass
    
    def remove_legend(self):
        """Remove any existing matplotlib axis legend"""
        if self.ax.legend_:
            self.ax.legend_.remove()
        pass
    
    def set_spines_and_ticks(self, axes = None,
                            remove_spines=['right','top'],
                            y_set_ticks = ['left'],
                            x_set_ticks = ['bottom'],
                            ):
        """Set spines (the lines along the axis) and
        tick locations for the plot
        
        Arguments:
            
            axes - the matplotlib.axis object to act on
                   Default: None (interpreted as self.ax)
            
            remove_spines - a list of spines to remove.
                   Default: ['right','top']
            
            y_set_ticks - a list of locations of y axis ticks
                   Default: ['left']
            
            x_set_ticks - a list of locations of x axis ticks
                   Default: ['bottom']
        """
        if not axes:
            axes = [self.ax,]
        for ax in axes:
            for spine in remove_spines:
                ax.spines[spine].set_visible(False)
            for pos in y_set_ticks:  
                ax.yaxis.set_ticks_position(pos)
            for pos in x_set_ticks:  
                ax.xaxis.set_ticks_position(pos)
            if self.fontsize:
                for item in (ax.get_xticklabels() + ax.get_yticklabels()):
                    item.set_fontsize(self.fontsize)
        pass
    
    def set_limits(self):
        """Apply the axis limits set by self.xlim and self.ylim
        to the graph axis"""
        if self.xlim or self.ylim:
            self.ax.set_xlim(self.xlim)
            ylim = self.ylim if self.ylim else [-2,1000] #set below zero so zero is visible
            self.ax.set_ylim(ylim)
            self.ax.set_autoscaley_on(False)
        else:
            self.ax.set_autoscaley_on(True)
        pass
    
    def display(self, legend=True, update=True, use_mpld3=True, hide_volume_labels = False, **kw):
        """Generate the figure and return an object for display
        This function is for viewing figures in a Jupyter notebook
        
        Arguments:
        
            legend   -  boolean for displaying a legend
                        Default: True
        
            update   -  boolean for reapplying spine, tick, title and 
                        axis limits to the graph
                        Default: True
        
            use_mpld3 - boolean for using mpld3 to produce interactive html
                        Default: True
        
            hide_volume_labels - boolean for hiding x axis volume labels
                        Default: False
        
            **kw      - additional keyword arguments are passed to mpld3.display
        """
        if legend == True:
            self.add_legend()
        elif legend == 'custom':
            pass
        else:
            self.remove_legend()
        if update:
            self.set_spines_and_ticks()
            self.set_title_and_labels(hide_volume_labels = hide_volume_labels)
            self.set_limits()
        if use_mpld3:
            return mpld3.display(self.fig, **kw)
        else:
            return self.fig
    
    def save_html(self, fileobj=None, legend=True, update=True, template_type = "general", **kw):
        """Generate the figure as a html file
        
        Arguments:
        
            fileobj  -  a python file object
                        Default: None (saved to a new file with the same
                                       name as the parent object with .html)
        
            legend   -  boolean for displaying a legend
                        Default: True
        
            update   -  boolean for reapplying spine, tick, title and 
                        axis limits to the graph
                        Default: True
        
            template_type - string specifying the type of HTML template to use.
                        Options from mpld3 are:
                        "simple" suitable for simple html page with one figure.
                        Will fail if require.js is available on the page.
                        "notebook" assumes require.js and jquery are available.
                        "general" works both in and out of the notebook,
                        whether or not require.js and jquery are available
                        Default: general
        
            **kw      - additional keyword arguments are passed to mpld3.save_html
        """
        if legend == True:
            self.add_legend()
        elif legend == 'custom':
            pass
        else:
            self.remove_legend()
        if not fileobj:
            fileobj='{0}.html'.format(self.name)
        if update:
            self.set_spines_and_ticks()
            self.set_title_and_labels()
            self.set_limits()
        mpld3.save_html(fig=self.fig,
                        fileobj=fileobj,
                        template_type=template_type,
                        **kw)
        pass
    
    def save_pdf(self, fileobj=None, legend=True, update=True, **kw):
        """Generate the figure as a pdf file
        
        Arguments:
        
            fileobj  -  a python file object
                        Default: None (saved to a new file with the same
                                       name as the parent object with .html)
        
            legend   -  boolean for displaying a legend
                        Default: True
        
            update   -  boolean for reapplying spine, tick, title and 
                        axis limits to the graph
                        Default: True
        
            **kw      - additional keyword arguments are passed to 
                        matplotlib.PdfPages.savefig
        """
        if legend == True:
            self.add_legend()
        elif legend == 'custom':
            pass
        else:
            self.remove_legend()
        if update:
            self.set_spines_and_ticks()
            self.set_title_and_labels()
            self.set_limits()
        if not fileobj:
            fileobj='{0}.html'.format(self.name)
        from matplotlib.backends.backend_pdf import PdfPages
        with PdfPages(fileobj) as pdf:
            pdf.savefig(self.fig, **kw)
        pass
    
    def add_individuals(self, name, tv_table,
                        color = 'black', alpha=0.1,
                        lw=3, dashes = [2,2],
                        **kw):
        """Add line plots of individual volume vs time for all individuals in
        a tumour volume table. These should be a logical group (eg treatment)
        When used to produce html plots mouse over events will make the line
        opaque (alpha=1.0) and label the line with the column name
        
        Arguments:
        
            name     -  The legend label for this group
        
            tv_table -  a pandas data frame of volume measurements
                        with individuals in columns and timepoints
                        as rows.  Individuals are removed from study
                        at the first NaN timepoint
        
            color    -  the color to plot this data group
                        Valid colors include matplotlib named colors
                        html colors (eg '#029386') or RGB tuples
                        (eg (0.0078, 0.58, 0.53))
        
            alpha    -  Percent transparency as a value between
                        0.0 (transparent) and 1.0 (opaque)
        
            lw       -  line width in points
        
            dashes   -  A line dash pattern as an even length list
                        of on off lengths in points
        
            **kw     -  additional key word arguments are passed to
                        matplotlib.axes.plot and can be any
                        matplotlib.Line2D attributes
        """
        self.lines[name] = self.ax.plot(tv_table.index, tv_table.to_numpy(),
                                        color=color, alpha=alpha,
                                        lw=lw, dashes=dashes,
                                        **kw)
        plugins.connect(self.fig, HighlightLines(self.lines[name]))
        for i, l in enumerate(self.lines[name]):
            plugins.connect(self.fig,
                            plugins.LineLabelTooltip(l, str(tv_table.columns[i])))
        pass
        
    def add_mean(self, name, tv_table, threshold=2,
                        color = 'black', alpha=0.8,
                        lw=4, dashes = [],
                        **kw):
        """Calculate and add to the plot a line for the mean volume vs time 
        for all individuals in a tumour volume table. These individuals 
        should be a logical group (eg treatment)
        
        Arguments:
        
            name     -  The legend label for this group
        
            tv_table -  a pandas data frame of volume measurements
                        with individuals in columns and timepoints
                        as rows.  Individuals are removed from study
                        at the first NaN timepoint
        
            threshold - the minimum group size to plot at a given
                        time point.
                        Default: 2
        
            color    -  the color to plot this data group
                        Valid colors include matplotlib named colors
                        html colors (eg '#029386') or RGB tuples
                        (eg (0.0078, 0.58, 0.53))
        
            alpha    -  Percent transparency as a value between
                        0.0 (transparent) and 1.0 (opaque)
        
            lw       -  line width in points
        
            dashes   -  A line dash pattern as an even length list
                        of on off lengths in points
        
            **kw     -  additional key word arguments are passed to
                        matplotlib.axes.plot and can be any
                        matplotlib.Line2D attributes
        """
        self.means[name] = self.ax.plot(tv_table[tv_table.count(axis=1) > threshold].index,
                                        tv_table[tv_table.count(axis=1) > threshold].mean(axis=1),
                                        color=color, alpha=alpha,
                                        lw=lw, dashes=dashes,
                                        **kw)
        pass

    def _calc_t_ci(self, tv_table, ci=0.95):
        uppers = []
        lowers = []
        means = []
        for entry in tv_table.T:
            data = tv_table.T[entry].dropna()
            mean = np.mean(data)
            (lower,upper) = scipy.stats.t.interval(0.95,
                                df=len(data)-1,
                                loc=mean,
                                scale=np.std(data,ddof=1) / np.sqrt(len(data)),
                                )
            uppers.append(upper)
            lowers.append(lower)
            means.append(mean)
        cis = pandas.DataFrame({'mean':means,
                              'lower bound':[max(0,x) for x in lowers], #limit to +ve
                              'upper bound':uppers,
            }).dropna()
        cis.index = tv_table.index[:len(cis.index)]
        return cis
    
    
    def _calc_norm_ci(self, tv_table, ci=0.95):
        interval = scipy.stats.norm.interval(ci, loc=tv_table.mean(axis=1),
                                               scale=tv_table.sem(axis=1))
        cis = pandas.DataFrame({'mean':tv_table.mean(axis=1),
                              'lower bound':[max(0,x) for x in interval[0]], #limit to +ve
                              'upper bound':interval[1],
            }).dropna()
        return cis
    
    def add_interval(self, name, tv_table, threshold=2, ci=0.95,
                        color = 'black', alpha=0.2,
                        lw=0, dashes = [],
                        **kw):
        """Calculate the confidence interval of the mean and add to the 
        plot as a shaded band around the mean. These individuals should be a
        logical group (eg treatment).
        Note that the value is the confidence interval for the standard
        error of the mean and indicates the range the mean is expected
        to lie within ci % of the time.
        This should not be confused with the standard deviation of the data 
        (the range within individual data is expected to lie) or the standard
        error of the mean.
        As most data is expected to have a small number of observations, the
        95% confidence interval is calculated using a t distribution.
        Results match R's t-test and Graphpad Prism's 95% CI
        
        Arguments:
        
            name     -  The legend label for this group
        
            tv_table -  a pandas data frame of volume measurements
                        with individuals in columns and timepoints
                        as rows.  Individuals are removed from study
                        at the first NaN timepoint
            
            threshold - the minimum group size to plot a confidence
                        interval for
                        Default: 2
        
            ci -        the confidence interval range to plot
                        Default: 0.95
        
            color    -  the color to plot this data group
                        Valid colors include matplotlib named colors
                        html colors (eg '#029386') or RGB tuples
                        (eg (0.0078, 0.58, 0.53))
        
            alpha    -  Percent transparency as a value between
                        0.0 (transparent) and 1.0 (opaque)
        
            lw       -  line width in points
        
            dashes   -  A line dash pattern as an even length list
                        of on off lengths in points
        
            **kw     -  additional key word arguments are passed to
                        matplotlib.axes.fill_between
        """
        cis = self._calc_t_ci(tv_table[tv_table.count(axis=1) > threshold], ci=ci)
        self.intervals[name] = self.ax.fill_between([int(x) for x in cis.index],
                                                   cis['lower bound'],
                                                   cis['upper bound'],
                                                   color=color, alpha=alpha,
                                                   lw=lw, dashes=dashes,
                                                   **kw)
        pass
    
    def set_title_and_labels(self, title=None, ylabel=None, xlabel=None, hide_volume_labels=False, **kw):
        """Set plot titles and axis labels
        
        Arguments:
        
            title   -   main plot title
                        Default: None (uses self.title)
        
            ylabel  -   y axis label
                        Default: None (uses self.ylabel)
        
            xlabel  -   x axis label
                        Default: None (uses self.xlabel)
        
            hide_volume_labels - for compatibility with dual plot
                        Default: False
        """
        if title == None:
            title = self.title
        if ylabel  == None:
            ylabel = self.ylabel
        if xlabel  == None:
            xlabel = self.xlabel
        self.ax.set_title(title, **kw)
        self.ax.set_ylabel(ylabel, **kw)
        self.ax.set_xlabel(xlabel, **kw)
        pass
    
    def add_legend(self, loc='best', **kw):
        """Create a legend from axis data after removing any existing
        legends
        
        Arguments:
        
            loc   -   location of legend from: 'best','upper right',
                      'upper left','lower left','lower right','right',
                      'center left','center right','lower center',
                      'upper center','center'
                      Default: 'best'
        
            **kw  -   keyword arguments passed to matplotlib.axes.legend
        """
        self.remove_legend()
        patches = []
        for key in self.means:
            color=self.means[key][0].get_color()
            if self.n_in_legend:
                if self.lines[key]:
                    label_text = '{0} (n={1})'.format(key,len(self.lines[key]))
                else:
                    label_text = '{0} (n=?)'.format(key)
            else:
                label_text = key
            patches.append(matplotlib.lines.Line2D([],[],color=color, label=label_text, lw=3))
        self.ax.legend(handles=patches,
                      loc=loc,
                      **kw)
        pass
    
    def show_treatment_days(self, days, facecolor="lightgrey",lw=0, **kw):
        """Add rectangular patches on the x axis to indicate days
        on which treatment occurred.
        
        Arguments:
        
            days   -   an integer list of days eg [1,3,5]
        
            facecolor - the fill color for the rectangular patches
                        Valid colors include matplotlib named colors
                        html colors (eg '#029386') or RGB tuples
                        (eg (0.0078, 0.58, 0.53))
        
            lw     -   the width of the line bordering the patch in points
                       Default: 0 (no line)
        
            **kw  -   keyword arguments passed to matplotlib.patches.Rectangle
        """
        for day in days:
            self.ax.add_patch(matplotlib.patches.Rectangle((day, 0), 1, 20, facecolor=facecolor, lw=lw, **kw))
        pass
    
    def shade_interval(self, start, end, facecolor="lightgrey", alpha=0.2, lw=0, **kw):
        """Add rectangular fill the full height of the axis to indicate
        a date range (eg for treatment).
        
        Arguments:
        
            start   -   the start point of the rectangle
        
            end   -     the end point of the rectangle
        
            facecolor - the fill color for the rectangular patches
                        Valid colors include matplotlib named colors
                        html colors (eg '#029386') or RGB tuples
                        (eg (0.0078, 0.58, 0.53))
        
            alpha    -  Percent transparency as a value between
                        0.0 (transparent) and 1.0 (opaque)
                        Default: 0.2
        
            lw     -   the width of the line bordering the patch in points
                       Default: 0 (no line)
        
            **kw  -   keyword arguments passed to matplotlib.patches.Rectangle
        """
        miny,maxy = self.ax.get_yaxis().get_data_interval()
        self.ax.add_patch(matplotlib.patches.Rectangle((start, min(miny,self.ylim[0])), end, max(maxy,self.ylim[1]),
                                                        facecolor="lightgrey",alpha=alpha, lw=0, **kw))
        pass
    

class VolumeSurvivalPlot(TumourVolumePlot):
    """Initiate a new dual panel Tumour Volume and Survival plot object
    
    Arguments:
    
        km_size  -  The relative size of the survival plot
                    Default: 0.5 (ie half or 1/3 total plot area)
    
        vertical -  Stack the Tumour Volume plot over the survival plot
                    with a shared x axis (days) so events co occur.
                    Default: True
    
        **kw - keyword arguments are passed to
               matplotlib.pyplot.subplots
    """
    def __init__(self, km_size=0.5, vertical=True, **kw):
        if vertical:
            self.fig, (self.ax, self.km_ax) = plt.subplots(nrows=2, ncols=1, sharex=True, gridspec_kw={'height_ratios':[1,km_size]},**kw)
        else:
            self.fig, (self.ax, self.km_ax) = plt.subplots(nrows=1, ncols=2, gridspec_kw={'width_ratios':[1,km_size]},**kw)
        self.lines = {}
        self.means = {}
        self.kmfs = {}
        self.intervals = {}
        self.title = 'Untitled'
        self.ylabel = 'Tumour Volume mm$^{3}$'
        self.xlabel = 'Days'
        self.km_title = ''
        self.km_ylabel = 'Survival'
        self.km_xlabel = 'Days'
        self.km_yticks = [0,0.25,0.5,0.75,1.0]
        self.km_ci_show = True
        self.km_show_censors = True
        self.vertical = vertical
        self.volume_data = {}
        self.endpoint = None
        self.xlim = None
        self.ylim = None
        self.fontsize = None
        self.n_in_legend = False
        pass
    
    def remove_legend(self):
        """Remove any existing matplotlib axis legend"""
        if self.ax.legend_:
            self.ax.legend_.remove()
        if self.km_ax.legend_:
            self.km_ax.legend_.remove()
        pass
    
    def add_mean(self, name, tv_table,
                        endpoint = 700,
                        threshold=2,
                        color = 'black', alpha=0.8,
                        lw=4, dashes = [],
                        **kw):
        """Calculate and add to the plot a line for the mean volume vs time 
        for all individuals in a tumour volume table. These individuals 
        should be a logical group (eg treatment)
        
        Arguments:
        
            name     -  The legend label for this group
        
            tv_table -  a pandas data frame of volume measurements
                        with individuals in columns and timepoints
                        as rows.  Individuals are removed from study
                        at the first NaN timepoint
        
            endpoint -  the volume at which the endpoint is reached
                        Default: 700
        
            threshold - the minimum group size to plot at a given
                        time point.
                        Default: 2
        
            color    -  the color to plot this data group
                        Valid colors include matplotlib named colors
                        html colors (eg '#029386') or RGB tuples
                        (eg (0.0078, 0.58, 0.53))
        
            alpha    -  Percent transparency as a value between
                        0.0 (transparent) and 1.0 (opaque)
        
            lw       -  line width in points
                        Default: 4
        
            dashes   -  A line dash pattern as an even length list
                        of on off lengths in points
        
            **kw     -  additional key word arguments are passed to
                        matplotlib.axes.plot and 
                        lifelines.kmf.plot and can be any
                        matplotlib.Line2D attributes
        """
        super(VolumeSurvivalPlot, self).add_mean(name=name, tv_table=tv_table,
                        threshold=threshold,
                        color=color, alpha=alpha,
                        lw=lw, dashes = dashes,
                        **kw)
        self.volume_data[name] = tv_table
        self.add_kmf(name, tv_table,
                     endpoint = endpoint,
                     color = color, alpha=alpha,
                     lw=lw, dashes = dashes,
                     **kw)
        pass

    def add_kmf(self, name, tv_table,
                        endpoint = 700,
                        color = 'black', alpha=0.8,
                        lw=4, dashes = [],
                        **kw):
        """Calculate and add a Kaplan Meier curve to the second panel
        of the plot for all individuals in a tumour volume table.
        These individuals should be a logical group (eg treatment)
        
        Arguments:
        
            name     -  The legend label for this group
        
            tv_table -  a pandas data frame of volume measurements
                        with individuals in columns and timepoints
                        as rows.  Individuals are removed from study
                        at the first NaN timepoint

            endpoint -  the volume at which the endpoint is reached
                        Default: 700
        
            color    -  the color to plot this data group
                        Valid colors include matplotlib named colors
                        html colors (eg '#029386') or RGB tuples
                        (eg (0.0078, 0.58, 0.53))
        
            alpha    -  Percent transparency as a value between
                        0.0 (transparent) and 1.0 (opaque)
        
            lw       -  line width in points
                        Default: 4
        
            dashes   -  A line dash pattern as an even length list
                        of on off lengths in points
        
            **kw     -  additional key word arguments are passed to
                        lifelines.kmf.plot and can be any
                        matplotlib.Line2D attributes
        """
        self.kmfs[name] = make_km(tv_table, label=name, endpoint=endpoint)
        self.endpoint = endpoint
        self.kmfs[name].plot_survival_function(color = color, alpha=alpha,
                     lw=lw, dashes = dashes,
                     show_censors = self.km_show_censors,
                     ci_show = self.km_ci_show,
                     ax=self.km_ax,
                     **kw)
        pass
    
    def set_title_and_labels(self, title=None, ylabel=None, xlabel=None,
                             km_title=None, km_ylabel=None, km_xlabel=None,
                             hide_volume_labels = True,**kw):
        """Set plot titles and axis labels
        
        Arguments:
        
            title   -   main plot title
                        Default: None (uses self.title)
        
            ylabel  -   y axis label
                        Default: None (uses self.ylabel)
        
            xlabel  -   x axis label
                        Default: None (uses self.xlabel)
        
            kmtitle   - Kaplan Meier plot label
                        Default: None (uses self.km_title)
        
            ylabel  -   y axis label
                        Default: None (uses self.km_ylabel)
        
            xlabel  -   x axis label
                        Default: None (uses self.km_xlabel)
        
            hide_volume_labels - do not display x axis label
                        between volume plot and Kaplan-Meier
                        Default: True
        """
        if title == None:
            title = self.title
        if ylabel  == None:
            ylabel = self.ylabel
        if xlabel  == None:
            xlabel = self.xlabel
        if km_title == None:
            km_title = self.km_title
        if km_ylabel  == None:
            km_ylabel = self.km_ylabel
        if km_xlabel  == None:
            km_xlabel = self.km_xlabel
        if self.fontsize and not 'fontsize' in kw:
            kw['fontsize'] = self.fontsize
        self.ax.set_title(title, **kw)
        self.ax.set_ylabel(ylabel, **kw)
        if hide_volume_labels:
            self.ax.set_xlabel('', **kw)
        else:
            self.ax.set_xlabel(xlabel, **kw)
        self.km_ax.set_title(km_title, **kw)
        self.km_ax.set_ylabel(km_ylabel, **kw)
        self.km_ax.set_xlabel(km_xlabel, **kw)
        
        pass
    
    def set_spines_and_ticks(self, axes = None,
                            remove_spines=['right','top'],
                            y_set_ticks = ['left'],
                            x_set_ticks = ['bottom'],
                            ):
        """Set spines (the lines along the axis) and
        tick locations for the plot
        
        Arguments:
            
            axes - the matplotlib.axis object to act on
                   Default: None
                   (interpreted as self.ax and self.km_ax)
            
            remove_spines - a list of spines to remove.
                   Default: ['right','top']
            
            y_set_ticks - a list of locations of y axis ticks
                   Default: ['left']
            
            x_set_ticks - a list of locations of x axis ticks
                   Default: ['bottom']
        """
        if axes == None:
            axes = [self.km_ax, self.ax]
        super(VolumeSurvivalPlot, self).set_spines_and_ticks(axes = axes,
                                                            remove_spines = remove_spines,
                                                            y_set_ticks = y_set_ticks,
                                                            x_set_ticks = x_set_ticks,)
        self.km_ax.yaxis.set_ticks(self.km_yticks)
        
        pass
    
    def set_limits(self):
        """Apply the axis limits set by self.xlim and self.ylim
        to the graph axes.  The Kaplan-Meier y axis will remain
        [0,1.02]"""
        if self.xlim or self.ylim:
            self.ax.set_xlim(self.xlim)
            ylim = self.ylim if self.ylim else [-2,1000] #set so zero is visible
            self.ax.set_ylim(ylim)
            self.ax.set_autoscaley_on(False)
            self.km_ax.set_xlim(self.xlim)
            self.km_ax.set_ylim([0,1.02]) #set >1 so lines retain full width
            self.km_ax.set_autoscaley_on(False)
        else:
            self.ax.set_autoscaley_on(True)
            self.km_ax.set_ylim([0,1.02])
            self.km_ax.set_autoscaley_on(True)
        pass
    
    def logrank_test(self, treatment_a, treatment_b, t1error=0.05):
        """Calculate a log rank test (Mantel-Cox) statistic between two treatments
        Calls lifelines.statistics.logrank_test for calculation.

        Arguments:

            treatment_a     -  The legend label for this group as used
                               with add_mean.

            treatment_b     -  The legend label for this group as used
                               with add_mean.

            t1error         -  probability of a type 1 error (alpha)
                               Default: 0.05
        """
        if not self.endpoint or not self.volume_data:
            print('you need to add data with .add_mean() before using logrank_test')
            raise ValueError
        survival_a = volume_to_survival(self.volume_data[treatment_a], endpoint=self.endpoint)
        survival_b = volume_to_survival(self.volume_data[treatment_b], endpoint=self.endpoint)
        result = logrank_test(list(survival_a['Time']),
                                                   list(survival_b['Time']),
                                                   list(survival_a['Observed']),
                                                   list(survival_b['Observed']),
                                                   alpha=1-t1error)
        result.print_summary()
        return result
    
    def display(self, legend=True, use_mpld3=True, update=True, hide_volume_labels=True, **kw):
        """Display the dual tumour volume and Kaplan Meier plot
        KNOWN BUG - mpld3 does not correctly display the step plot in version < 0.3
        """
        result = super(VolumeSurvivalPlot, self).display(legend=legend,
                                                use_mpld3=use_mpld3,
                                                update=update,
                                                hide_volume_labels = hide_volume_labels,
                                                **kw)
        if use_mpld3:
            return result







