# 
# main logic for text analyzer program
# 
# NOTE: This project requires Python 3 to work properly
# 


# FEATURE LIST #

# add option to control output verbosity
# add ability to export analysis results to JSON
# add support for "terminal graphing" mode
# add docstrings to function definitions


# imports #

from __future__ import print_function

import matplotlib.pyplot as plt

import argparse
import os
import glob

from stats import *
from data  import *
from summary import *
from plot import *


# main logic #

def main():

    # parse arguments from command line (list of strings, list of filenames, list of urls)

    parser = argparse.ArgumentParser(description='Analyze & compute basic stats for given corpus of text')
    
    # create attributes to hold list of strings, files, and urls
    parser.add_argument('-f', nargs='*', default=[])
    parser.add_argument('-s', nargs='*',  default=[])
    parser.add_argument('-u', nargs='*',  default=[])

    ns = parser.parse_args()

    #print('ns:', ns) # dummy code

    # process each string in turn
    for str in ns.s:
        
        print('Summary for string : "{}"'.format(str), end='\n\n')
    
        print_summary_from_string(str)
    
    # expand any unix wildcards specified in list of path names
    path_list = []
    
    for path in ns.f:
        
        path_list.extend(glob.glob(path))
        
    # process each file as given by list of filenames
    for filename in path_list:
        
        print_summary_from_file(filename)

    # retrieve data from each url and analyze text
    for url in ns.u:
        
        print_summary_from_url(url)
    
    
# boilerplate code #

if __name__ == '__main__':
    main()
