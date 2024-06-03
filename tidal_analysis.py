#!/usr/bin/env python3
"""
Tidal Analysis

This module is capable of reading in text file tidal data and formatting it appropriately,
as well as returning a variety of information, including means of single year data, 
means of specified time slices and characterists of tides. This includes sea level 
rise and tidal constituents. 
"""
# import the modules you need here
import argparse
import datetime
import numpy as np
import pandas as pd
import pytz
import uptide
import matplotlib.dates as mdates

def read_tidal_data(filename):
    """
    Reads in a sea level data text file 
    Returns cleaned and sorted table of data with datetime index
    
    Keyword arguments:
    filename- the path to the data file

    """
    headings = ['Cycle', 'Date', 'Time', 'Sea Level', 'Residual']
    data = pd.read_table(filename, skiprows= 11, names = headings, sep=r"\s+")
    data.index = pd.to_datetime(data['Date'] + ' ' + data['Time'])
    #replace all values ending in N, M or T with NaN values
    data.replace(to_replace=".*(N|M|T)$",value={'Sea Level':np.nan},regex=True,inplace=True)
    data['Sea Level'] = data['Sea Level'].astype(float)
    return data

def extract_single_year_remove_mean(year, data):
    """
    Reads in multiple sea level data text files
    Returns mean sea level for data of a given 'year'
    
    Keyword arguments:
    year- the target year of the data
    data- the joined sea level data text files to be analysed

    """
    #read in data where the datetime index year is equal to the given one
    data = data[data.index.year == int(year)]
    mean_sea_level = data['Sea Level'].mean()
    #subtract the sea level data from the mean sea level
    data.loc[:,'Sea Level'] = mean_sea_level - data.loc[:,'Sea Level']
    return data

def extract_section_remove_mean(start, end, data):
    """
    Reads in multiple sea level data text files
    Returns means sea level for data of a given time period
    
    Keyword arguments:
    start- the date the data slice begins at
    end- the date the data slice ends at

    """
    data = data.loc[start : end, ['Sea Level']]
    mean_sea_level = data['Sea Level'].mean()
    data_segment = mean_sea_level - data
    return data_segment

def join_data(data1, data2):
    """
    Reads in two sea level data text files 
    Returns a joined table of both datasets
    
    Keyword arguments:
    data1- the first of the two joining sea level data files
    data2- the second of the two joining sea level data files
    """
    headings = ['Cycle', 'Date', 'Time', 'Sea Level', 'Residual']
    left = data2
    right = data1
    #merge the datasets together
    #information on how to do this found at:
    #https://pandas.pydata.org/docs/reference/api/pandas.merge.html
    data = pd.merge(left, right, on=headings, how = 'outer')
    data.index = pd.to_datetime(data['Date'] + ' ' + data['Time'])
    return data

def sea_level_rise(data):
    """
    Reads in multiple sea level text files
    Returns values for gradient and p value of line of best fit for sea level data against days 

    """
    data = data.dropna(subset=['Sea Level'])
    #convert datetimes to numbers counting from 0
    #information on how to do this found at:
    #https://matplotlib.org/stable/api/dates_api.html#matplotlib.dates.date2num
    x_axis = ((mdates.date2num(data['Sea Level'].index)) - mdates.date2num(data.index[0]))*24
    y_axis = data["Sea Level"]
    #add regression line
    #information on how to do this found at:
    #https://stackoverflow.com/questions/9538525/calculating-slopes-in-numpy-or-scipy
    slope = np.polyfit(x_axis,y_axis,1)[0]
    return slope

def tidal_analysis(data, constituents, start_datetime):
    """
    Reads in data for multiple sea level data text files
    Returns values for the requested tidal constituents' amplitude and phase
    
    Keyword arguments:
    data- the joined sea level data files to be analysed
    constituents- the harmonic constituents for amplitude and phase to be found
    start_datetime- the datetime that the data will be counted from

    """
    tide = uptide.Tides(constituents)
    tide.set_initial_time(start_datetime)
    data = data.dropna(subset=['Sea Level'])
    seconds_since = (data.index.astype('int64').to_numpy()/1e9) - (start_datetime).timestamp()
    amp, pha = uptide.harmonic_analysis(tide, data['Sea Level'].to_numpy(), seconds_since)
    return amp, pha

def get_longest_contiguous_data(data):
    return data

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
                     prog="UK Tidal analysis",
                     description="Calculate tidal constiuents and RSL from tide gauge data",
                     epilog="Copyright 2024, Jon Hill"
                     )

    parser.add_argument("directory",
                    help="the directory containing txt files with data")
    parser.add_argument('-v', '--verbose',
                    action='store_true',
                    default=False,
                    help="Print progress")

    args = parser.parse_args()
    dirname = args.directory
    verbose = args.verbose
    