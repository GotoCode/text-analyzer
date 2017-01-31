# 
# main logic for text analyzer program
# 
# NOTE: This project requires Python 3 to work properly
# 


# FEATURE LIST #

# read in text from url
# improve code for argument parsing to use "argparse" module
# refactor code for vowel and consonant counting
# report longest and shortest word
# support for graphing frequencies via matplotlib
# add support for adaptive (non hard-coded) display of output number 'widths'
# remove extraneous formatting from input text (i.e. ! . ; ? etc.)
# implement stemmer/lemmatizer to improve semantic analysis algorithm
# add support for Unix file globs (i.e. *.txt)
# add option to control output verbosity
# separate code into different modules
# fix bug causing issues between 'Happy => neutral' and 'happy => positive'
# fix 'a nexus of pure evil' bug
# add ability to read from multiple files and compile results into one summary
# add ability to export analysis results to JSON


# imports #

from __future__ import print_function

import sys
import os
import re


# constants #

VOWELS = "aeiou"

DATA_SOURCE = 'subjectivity_clues/subjclueslen1-HLTEMNLP05.tff'


# helper functions #

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

def __read_dataset():
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

def num_vowels(s):
    '''
    Given a string, returns a dict mapping each vowel
    to a count of number of occurrences

    NOTE: This function is NOT case-sensitive
    '''
    
    counts = {}

    for ch in s:

        ch = ch.lower()
        
        if ch.isalpha() and ch in VOWELS:
            counts[ch] = counts.get(ch, 0) + 1
    
    return counts

def num_consonants(s):
    '''
    Given a string, returns a dict mapping each consonant
    to a count of number of occurrences

    NOTE: This function is NOT case-sensitive
    '''
    
    counts = {}
    
    for ch in s:

        ch = ch.lower()

        if ch.isalpha() and ch not in VOWELS:
            counts[ch] = counts.get(ch, 0) + 1
        
    return counts

def num_words(s):
    '''
    Given a string, returns a dict mapping each word
    to a count of number of occurrences
    
    NOTE: This function is NOT case-sensitive
    '''

    counts = {}
    
    for w in s.split():

        w = w.lower()

        counts[w] = counts.get(w, 0) + 1
    
    return counts

def get_mood(s):
    '''
    Given a string, returns a "mood" (positive/neutral/negative)
    associated with the content of this text
    '''
    
    # build a mapping between each word and its mood
    raw_data = __read_dataset()
    
    sentiment_map = {d['word'] : d['polarity'] for d in raw_data}

    scores = {'positive' : 0, 'negative' : 0, 'neutral' : 0}

    # determine mood for each word in the input text
    for word in s.split():
        
        if word in sentiment_map:
            
            polarity = sentiment_map[word]
            scores[polarity] = scores.get(polarity, 0) + 1
    
    # return one of positive, negative, or neutral category
    category, count = max(scores.items(), key = lambda kv : kv[1])

    if count == 0:
        category = 'neutral'

    return category if category != 'both' else 'neutral'

def report_summary(s):
    '''
    Returns a tuple of various stats after
    analyzing the given input string
    '''

    vowel_counts = num_vowels(s)

    consonant_counts = num_consonants(s)

    word_counts = num_words(s)

    mood = get_mood(s)

    return (vowel_counts, consonant_counts, word_counts, mood)

def __print_summary(v_counts, c_counts, w_counts, mood):
    '''
    Prints the summary stats obtained as params
    via a call to the report_summary function
    '''

    print()
    
    # render output of analysis to the terminal
    print('This text contains {} vowels'.format(len(v_counts)))
    print('This text contains {} consonants'.format(len(c_counts)), end='\n\n')

    # each character with its count (sorted in alphabetical order)
    v_counts.update(c_counts)

    for ch, count in sorted(v_counts.items()):
        print('{} : {:3d}'.format(ch, count))

    print()

    # each word with its count (sorted in descending order by frequency)
    for word, count in sorted(w_counts.items(), key = lambda wc : wc[1], reverse=True):
        print('{:10s} : {:3d}'.format(word, count))

    print()

    # output the predicted "mood" for the text
    print('This text has a "{}" mood'.format(mood), end='\n\n')

def __print_summary_from_string(s):
    '''
    Prints the summary statistics when
    a user directly inputs text via the
    command line
    '''

    info = report_summary(s)

    __print_summary(*info)

def __print_summary_from_file(filename):
    '''
    Prints the summary statistics
    associated with the file located
    at filename

    NOTE - this function is very memory-intensive
           as it loads the entire file into memory 
           at once
    '''
    
    with open(filename) as f:
        
        s = f.read()
    
    __print_summary_from_string(s)

# main logic #

def main():

    if len(sys.argv) == 2:

        arg = sys.argv[1]

        # read in a (single) string directly from command line
        if not os.path.exists(arg):

            __print_summary_from_string(arg)

        # read in text from a (single) file specified on command line
        # WARNING - currently only handles .txt files
        elif os.path.exists(arg):

            __print_summary_from_file(arg)


# boilerplate code #

if __name__ == '__main__':
    main()
