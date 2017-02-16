#
# summary.py
#
# This file contains code designed to print
# out (display to the user) various summary
# statistics computed using the functions
# defined by the stats.py file
#

# imports #

from __future__ import print_function

import json

import requests

from stats import *


# functions #

def print_summary(v_counts, c_counts, w_counts, mood, verbosity=0):
    '''
    Prints the summary stats obtained as params
    via a call to the report_summary function

    verbosity level == 0 : display word counts...
    verbosity level == 1 : ...and display mood for text...
    verbosity level >= 2 : ...and display character counts
    '''
        
    if verbosity >= 2:
        # render output of analysis to the terminal
        print('This text contains {} vowels'.format(len(v_counts)))
        print('This text contains {} consonants'.format(len(c_counts)), end='\n\n')

    v_counts.update(c_counts)

    # values for clean output display
    max_count = max(v_counts.values())

    fmt_str = '{} : {:' + str(len(str(max_count)) + 1) + 'd}'

    if verbosity >= 2:
        # each character with its count (sorted in alphabetical order)
        for ch, count in sorted(v_counts.items()):
            print(fmt_str.format(ch, count))
        
        print()

    # values for clean display of output
    max_count = max(w_counts.values())
    longest_word = max(w_counts.keys(), key=lambda x : len(x))

    fmt_str = '{:' + str(len(longest_word) + 1) + 's} : {:' + str(len(str(max_count)) + 1) + '}'

    if verbosity >= 0:

        # each word with its count (sorted in descending order by frequency)
        for word, count in sorted(w_counts.items(), key = lambda wc : wc[1], reverse=True):
            print(fmt_str.format(word, count))

        print()

    if verbosity >= 1:
    
        # output the predicted "mood" for the text
        print('This text has a "{}" mood'.format(mood), end='\n\n')

def print_summary_from_string(s, verbosity=0, json_mode=False):
    '''
    Prints the summary statistics when
    a user directly inputs text via the
    command line
    '''

    # JSON output display mode
    if json_mode:

        info_dict = report_json_summary(s)

        info_dict['name'] = s

        print(json.dumps(info_dict), end='\n\n')

    else:

        v, c, w, m = report_summary(s)

        print('Summary for string : "{}"'.format(s), end='\n\n')

        print_summary(v, c, w, m, verbosity)

def print_summary_from_file(filename, verbosity=0, json_mode=False):
    '''
    Prints the summary statistics
    associated with the file located
    at filename

    NOTE - this function is very memory-intensive
           as it loads the entire file into memory 
           at once
    '''

    # JSON output display mode
    if json_mode:

        with open(filename) as f:

            info_dict = report_json_summary(f.read())

            info_dict['name'] = filename

            print(json.dumps(info_dict), end='\n\n')

    else:

        print('Summary for file : "{}"'.format(filename), end='\n\n')

        if not os.path.exists(filename):

            print('Cannot find file : {}'.format(filename))

        else:

            with open(filename) as f:
        
                s = f.read()
    
                print_summary_from_string(s, verbosity)

def print_summary_from_url(url, verbosity, json_mode=False):
    '''
    Prints the summary statistics
    obtained after analyzing the text
    pointed to via the provided url
    '''

    # JSON output display mode
    if json_mode:
        
        r = requests.get(url)
        
        info_dict = report_json_summary(r.content)
        
        info_dict['name'] = url

        print(json.dumps(info_dict), end='\n\n')
        
    else:

        print('Summary for text at : "{}"'.format(url), end='\n\n')

        try:
        
            r = requests.get(url)

        except requests.exceptions.ConnectionError:

            print('Invalid url: {}'.format(url))

        else:
        
            print_summary_from_string(r.content, verbosity)
