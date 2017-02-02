# 
# main logic for text analyzer program
# 
# NOTE: This project requires Python 3 to work properly
# 


# FEATURE LIST #

# improve code for argument parsing to use "argparse" module
# remove extraneous formatting from input text (i.e. ! . ; ? etc.)
# implement stemmer/lemmatizer to improve semantic analysis algorithm
# add support for Unix file globs (i.e. *.txt)
# add option to control output verbosity
# separate code into different modules
# fix bug causing issues between 'Happy => neutral' and 'happy => positive'
# fix 'a nexus of pure evil' bug
# add ability to read from multiple files and compile results into one summary
# add ability to export analysis results to JSON
# add '--graph-words' or '--graph-chars' or '--graph' flag option


# imports #

from __future__ import print_function

import requests
import matplotlib.pyplot as plt

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

def __build_counts(s, p=lambda x : True):
    '''
    Given a string s and a predicate p
    builds up a dict mapping each char
    in s to its count (if p(char) evaluates to True)

    NOTE - p must be a function which takes a char
           as input and produces a bool as output
    '''

    counts = {}

    for ch in s:
        
        ch = ch.lower()

        if p(ch):
            counts[ch] = counts.get(ch, 0) + 1
    
    return counts

def num_vowels(s):
    '''
    Given a string, returns a dict mapping each vowel
    to a count of number of occurrences

    NOTE: This function is NOT case-sensitive
    '''
    
    return __build_counts(s, lambda ch : ch.isalpha() and ch in VOWELS)

def num_consonants(s):
    '''
    Given a string, returns a dict mapping each consonant
    to a count of number of occurrences

    NOTE: This function is NOT case-sensitive
    '''

    return __build_counts(s, lambda ch : ch.isalpha() and ch not in VOWELS)

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

    # values for clean output display
    max_count = max(v_counts.values())

    fmt_str = '{} : {:' + str(len(str(max_count)) + 1) + 'd}'

    for ch, count in sorted(v_counts.items()):
        print(fmt_str.format(ch, count))

    # values for clean display of output
    max_count = max(w_counts.values())
    longest_word = max(w_counts.keys(), key=lambda x : len(x))

    fmt_str = '{:' + str(len(longest_word) + 1) + 's} : {:' + str(len(str(max_count)) + 1) + '}'

    print()

    # each word with its count (sorted in descending order by frequency)
    for word, count in sorted(w_counts.items(), key = lambda wc : wc[1], reverse=True):
        print(fmt_str.format(word, count))

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

def __print_summary_from_url(url):
    '''
    Prints the summary statistics
    obtained after analyzing the text
    pointed to via the provided url
    '''

    try:
        
        r = requests.get(url)

    except requests.exceptions.ConnectionError:

        print('Invalid url: {}'.format(url))

    else:
        
        __print_summary_from_string(r.content)

def __graph_chars(info):
    '''
    Given a tuple of summary stats
    such as that returned by report_summary
    this function plots character frequency 
    data via matplotlib
    '''

    # retrieve info from summary tuple
    v_counts = info[0]
    c_counts = info[1]

    v_counts.update(c_counts)

    # set up data for x- and y-axes of data plot
    x_labels = [x for x, _ in sorted(v_counts.items())]

    x = list(range(len(v_counts)))
    y = [y for _, y in sorted(v_counts.items())]

    # plot bar graph of letter vs frequency

    bar_width = 1/1.5

    plt.bar(x, y, width=bar_width, tick_label=x_labels)
    
    plt.show()

def __graph_words(info):
    '''
    This function is similar to the __graph_chars
    function, except that it plots word frequencies
    instead of character frequencies
    '''

    # retrieve appropriate summary stats
    w_counts = info[2]

    # set up data for x- and y-axes
    x = list(range(len(w_counts)))
    y = [c for _, c in sorted(w_counts.items())]

    x_labels = [w for w, _ in sorted(w_counts.items())]

    # plot frequencies on a bar graph
    plt.xticks(x, x_labels, rotation='vertical')

    bar_width = 1/1.5

    plt.bar(x, y, width=bar_width)

    plt.subplots_adjust(bottom=0.15)

    plt.show()

# main logic #

def main():

    if len(sys.argv) == 2:

        arg = sys.argv[1]

        # read in a (single) string directly from command line
        if not os.path.exists(arg):

            # check if string is actually a url
            if arg.startswith('http://') or arg.startswith('https://'):

                __print_summary_from_url(arg)

            elif arg.startswith('www.'):
                
                __print_summary_from_url('http://' + arg)
                
            # argument is a literal string entered via command line 
            else:

                __print_summary_from_string(arg)

        # read in text from a (single) file specified on command line
        # WARNING - currently only handles .txt files
        elif os.path.exists(arg):

            __print_summary_from_file(arg)


# boilerplate code #

if __name__ == '__main__':
    main()
