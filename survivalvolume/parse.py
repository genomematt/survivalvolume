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

__author__ = "Matthew Wakefield"
__copyright__ = "Copyright 2016 Matthew Wakefield, The Walter and Eliza Hall Institute and The University of Melbourne"
__credits__ = ["Matthew Wakefield",]
__license__ = "GPL"
__version__ = "1.2.3"
__maintainer__ = "Matthew Wakefield"
__email__ = "wakefield@wehi.edu.au"
__status__ = "production"

def split_on_nans(data):
    """Split a pandas data frame at rows that contain all null values

    Argument:

        data - a pandas data frame

    Returns:

        a list of pandas data frames

    """
    result = []
    null_lines = data[data.isnull().all(axis=1) == True].index
    start = 0
    for line_index in sorted(null_lines):
        data_subset = data.loc[start:line_index]
        result.append(data_subset)
        start = line_index+1
    return result

def clean_tv_table(dirty_tv_table):
    """The Tumour Volume tables generated by splitting on NaN lines
    have flanking NaN columns and rows
    Returns the table name/title and a pandas dataframe with samples
    as column ids and days as row ids

    Argument:

        dirty_tv_table - a pandas data frame with a title row
                         followed by a header row and rows of
                         data lines, surrounded by arbitrary 
                         NaN null cell entries

    Returns:

        name     - the value of the title row
        tv_table - a pandas data frame with named row columns
                   and row item identifiers
    """
    tv_table = dirty_tv_table.copy()
    tv_table = tv_table.dropna(axis=1,how='all')
    tv_table = tv_table.dropna(axis=0,how='all')
    name = tv_table[1].iloc[0]
    tv_table.columns = tv_table.iloc[1]
    tv_table.index = tv_table['Day']
    tv_table = tv_table.iloc[2:,1:]
    tv_table = tv_table.drop('Mean',axis=1)
    return name,tv_table

def studylog_prism_df_to_tv_tables(df):
    """abstracted from studylog_prism_to_tv_tables to allow sane testing
    Use studylog_prism_to_tv_tables"""
    start_of_tv = df.loc[df[0] == 'Tumor Volume (All Animals)'].index[1]
    end_of_tv = df.loc[df[0] == 'Scatterplot information for Prism'].index[0]
    tv_tables = []
    for x in split_on_nans(df[start_of_tv+1:end_of_tv]):
        if len(x.index) > 3:
            cleaned = clean_tv_table(x)
            if not (cleaned[1].empty):
                tv_tables.append(cleaned)
    return dict(tv_tables)

def studylog_prism_to_tv_tables(xlsx_filename, sheetname='PrismRaw'): #pragma no cover
    """A function for converting study log Absolute TV format Excel files
    to dataframes.
    
    Arguments:

        xlsx_filename - a Studylog Excel Prism output file
        sheetname     - the name of the sheet to extract from
                        Default: 'PrismRaw'

    Returns:

        a python dictionary of {name:dataframe} where name is the
        title of the experimental group and dataframe is a pandas
        data frame with columns for each individual and rows for
        volume measurements at a given time point
    """
    df = pandas.read_excel(xlsx_filename, sheetname=sheetname, header=None)
    return studylog_prism_df_to_tv_tables(df)

def clean_studylog_absolute_tv(absolute_tv_df):
    """Cleans and reformat a dataframe of volume measurements
    that has been extracted from a Studylog Absolute TV excel
    spreadsheet.
    Returns the table name/title and a pandas dataframe with samples
    as column ids and days as row ids

    Argument:

        dirty_tv_table - a pandas data frame where the first
                         three columns are Group, Animal ID	and
                         Study Days Data Type followed by left
                         aligned measurement columns named by day
                         padded by NaN null cell entries.
                         All entries must be from the same group

    Returns:

        tv_table - a pandas data frame with named row columns
                   and row item identifiers
    """
    absolute_tv_df.dropna(axis=1, how='all', inplace=True)
    absolute_tv_df.dropna(axis=0, how='all', inplace=True)
    absolute_tv_df.index = absolute_tv_df['Animal ID']
    return absolute_tv_df.T[3:]

def studylog_absolute_to_tv_tables(xlsx_filename,
                                   sheetname='Absolute_TV',
                                   header_length=5): #pragma no cover
    """A function for converting study log Prism format Excel files
    to dataframes.
    
    Arguments:

        xlsx_filename - a Studylog Excel Absolute TV output file
        sheetname     - the name of the sheet to extract from
                        Default: 'Absolute_TV'

    Returns:

        a python dictionary of {name:dataframe} where name is the
        title of the experimental group and dataframe is a pandas
        data frame with columns for each individual and rows for
        volume measurements at a given time point
        Note: Raw days are returned - use standardise_days to fix
    """
    absolute_df = pandas.read_excel(xlsx_filename,
                                    sheet_name=sheetname,
                                    header=header_length)
    return studylog_absolute_df_to_tv_tables(absolute_df)

def studylog_absolute_df_to_tv_tables(absolute_df):
    """abstracted from studylog_absolute_to_tv_tables to allow sane testing
    Use studylog_absolute_to_tv_tables"""
    absolute_df.sort_values(by=['Group'], inplace=True)
    absolute_df.set_index(keys=['Group'], drop=False, inplace=True)
    groups = absolute_df['Group'].unique().tolist()
    tv_tables = {elem : pandas.DataFrame for elem in groups}
    for key in tv_tables.keys():
        tv_tables[key] = clean_studylog_absolute_tv(absolute_df[:][absolute_df.Group == key])
    return tv_tables

def fixed_length_alternate_steps(start,length,step1,step2):
    """Generate list of numbers that increments buy
    steps of alternating magnitude eg [1,4,8,11,15]
    
    Arguments:

        start    -  value of first entry in list
        length   -  length of list to be generated
        step1    -  the magnitude of odd numbered steps
        step2    -  the magnitude of even numbered steps

    Returns:

        a list of numeric values
    """
    result = []
    x=start
    result.append(x)
    second_step = False
    while len(result) < length:
        if second_step:
            x += step2
        else:
            x += step1
        result.append(x)
        second_step = not second_step
    return result

def standardise_days(dataframe,first_interval=3,second_interval=4):
    """Renumber days in study log files by changing
    day numbers to series incrementing by alternating periods.
    (eg 3 day and 4 day periods) to adjust for individuals going
    on study on different days of the week.
    
    Arguments:

        dataframe          -  a pandas data frame with a
                              day based row index
        first_interval     -  the magnitude of odd numbered steps
        second_interval    -  the magnitude of even numbered steps
    
    Returns:

        a pandas dataframe with standardised days as index.
    """
    dataframe.index = fixed_length_alternate_steps(1,len(dataframe.index),first_interval,second_interval)
    return dataframe


