---
title: 'SurvivalVolume: interactive volume threshold survival graphs'
tags:
  - bioinformatics
  - biostatisics
  - visualisation
  - treatment studies
authors:
 - name: Matthew J. Wakefield
   orcid: 0000-0001-6624-4698
   affiliation: The Walter and Eliza Hall Institute
   affiliation: The University of Melbourne
date: 31 Oct 2016
bibliography: paper.bib
---

# Summary

Treatment studies of cancer frequently use tumour volume to measure response to therapy.  Therapeutic response will be apparent at different time points during the experiment.  Progressive disease (increasing volume), stable disease and regression (reduction in volume) under therapy are important measures of response in addition to the overall time to reach a defined maximum volume.  Traditional methods of presenting this data involve 3 unconnected graphs: line graphs of each individual, average volume of each group with standard error of the mean, and a Kaplan-Meier graph of time to maximum volume.
Survival volume is a python package to produce an integrated plot of these three representations of the same data, and to provide interaction with the plots of volume to enhance exploration of outliers and subgroups that are of interest clinically.

Survival volume is written for python3 and uses matplotlib [@MATPLOTLIB] and lifelines [@LIFELINES] Kaplan-Meier [@KAPLANMEIER] implementation for generating plots, mpld3 [@MPLD3] for interactivity. Utility functions are provided for importing data from spreadsheets using xlrd [@Machin], preprocessing to provide consistent time scales for comparison of treatments, and conversion from volume measurements to survival format.  Statistics are calculated using lifelines and scipy.stats [@SCIPY].  Pandas [@PANDAS] data frames are used to provide flexible manipulation of data and use within Jupyter [@IPYTHON] notebooks is supported and encouraged.

Plot elements are presented in a visual hierarchy giving greatest weight to the information rich mean, and transparency is used to legibly overplot the confidence interval of the mean and the complete dataset.  Interactivity through mouseover and plot zooming provides rich access to the full data set.  By co-plotting the Kaplan-Meier representation with a shared x-axis endpoint and censoring events can be related between the plots enriching the information accessible about each event.

Survival volume is released under the GPLv3 and is available from GitHub and PyPI.


# References

