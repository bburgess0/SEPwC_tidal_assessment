#!/usr/bin/env python3

# import the modules you need here
import argparse
import numpy as np
import pandas as pd
import datetime

def read_tidal_data(filename):
        
    data = pd.read_table(filename, skiprows= 11, names = [ 'Cycle', 'Date', 'Time', 'Sea Level', 'Residual' ], sep=r"\s+")
    data.index = pd.to_datetime(data['Date'] + ' ' + data['Time'])
    
    data.replace(to_replace=".*(N|M|T)$",value={'Sea Level':np.nan},regex=True,inplace=True)
    data['Sea Level'] = data['Sea Level'].astype(float)
    
    return data
    

def extract_single_year_remove_mean(year, data):
   

    return 


def extract_section_remove_mean(start, end, data):


    return 


def join_data(data1, data2):
    
    

    return 



def sea_level_rise(data):

                                                     
    return 

def tidal_analysis(data, constituents, start_datetime):


    return 

def get_longest_contiguous_data(data):


    return 

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
    


