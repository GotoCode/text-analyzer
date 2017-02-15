#
# data.py
#
# This file contains code to read 
# in sentiment data (from sentiment analysis)
# from the data source specified by the 
# DATA_SOURCE constant 
#

# imports #

import os
import re


# constants #

DATA_SOURCE = 'subjectivity_clues/subjclueslen1-HLTEMNLP05.tff'


# functions #

def __get_match(pat, str, n=0):
    '''
    Given a regex pattern and an input string
    returns the nth match found
    
    By default, n is 0
    '''
    
    matches = re.findall(pat, str)
    
    if 0 <= n < len(matches):
        
        return matches[n]
    
    else:
        
        return None

def read_dataset():
    '''
    Reads in sentiment data from the Sentiment Lexicon
    as a list of dictionaries

    Raises RuntimeError if sentiment file does not exist
    '''

    if os.path.exists(DATA_SOURCE):

        entries = []

        with open(DATA_SOURCE) as f:
            
            for line in f:
                
                # define patterns for each field in source file
                type_pat = r'type=(\w+)'
                len_pat  = r'len=(\d+)'
                word_pat = r'word\d+=(\w+)'
                pos_pat  = r'pos\d+=(\w+)'
                stemmed_pat = r'stemmed\d+=(\w)'
                polarity_pat = r'priorpolarity=(\w+)'

                # extract (key, value) pairs for each field in current line
                type = ('type', __get_match(type_pat, line))
                len  = ('len', __get_match(len_pat, line))
                word = ('word', __get_match(word_pat, line))
                pos  = ('pos', __get_match(pos_pat, line))
                stemmed  = ('stemmed', __get_match(stemmed_pat, line))
                polarity = ('polarity', __get_match(polarity_pat, line))

                # add current row to list of data entries
                entries.append(dict([type, len, word, pos, stemmed, polarity]))

        return entries

    else:

        raise RuntimeError('Cannot find data source at "{}"'.format(DATA_SOURCE))
