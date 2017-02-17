#
# main.py
#  
# main logic for the text analyzer program
# 


# FEATURE LIST #

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

    # output verbosity level
    v_level = 0

    # parse arguments from command line (list of strings, list of filenames, list of urls)
    parser = argparse.ArgumentParser(description='analyze & compute basic stats for given corpus of text')
    
    # create attributes to hold list of strings, files, and urls
    parser.add_argument('-f', nargs='*', default=[], help='specify a list of local files to analyze')
    parser.add_argument('-s', nargs='*', default=[], help='specify a list of strings to analyze directly')
    parser.add_argument('-u', nargs='*', default=[], help='specify a list of urls to analyze text from webpages')

    # add argument for output verbosity levels
    parser.add_argument('-v', action='count', default=0, help='specify verbosity level -v -vv -vvv etc.')

    # add argument for JSON output option
    parser.add_argument('--json', action='store_true', help='enable JSON output mode')
    
    ns = parser.parse_args()
    
    # update variable for output verbosity level
    v_level = ns.v

    # process each string in turn
    for str in ns.s:

        print_summary_from_string(str, v_level, ns.json)

    # expand any unix wildcards specified in list of path names
    path_list = []
    
    for path in ns.f:
        
        path_list.extend(glob.glob(path))
        
    # process each file as given by list of filenames
    for filename in path_list:

        print_summary_from_file(filename, v_level, ns.json)

    # retrieve data from each url and analyze text
    for url in ns.u:

        print_summary_from_url(url, v_level, ns.json)


# boilerplate code #

if __name__ == '__main__':
    main()
