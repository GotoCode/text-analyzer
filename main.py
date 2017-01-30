# 
# main logic for text analyzer program
# 
# NOTE: This project requires Python 3 to work properly
# 


# FEATURE LIST #

# "calculate" mood from text (naive method)
# read in text from command line
# read in text from file
# read in text from url
# refactor code for vowel and consonant counting
# support for graphing frequencies via matplotlib


# imports #

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
                
                type_pat = r'type=(\w+)'
                len_pat  = r'len=(\d+)'
                word_pat = r'word\d+=(\w+)'
                pos_pat  = r'pos\d+=(\w+)'
                stemmed_pat = r'stemmed\d+=(\w)'
                polarity_pat = r'priorpolarity=(\w+)'

                type = ('type', __get_match(type_pat, line))
                len  = ('len', __get_match(len_pat, line))
                word = ('word', __get_match(word_pat, line))
                pos  = ('pos', __get_match(pos_pat, line))
                stemmed  = ('stemmed', __get_match(stemmed_pat, line))
                polarity = ('polarity', __get_match(polarity_pat, line))

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
    category, count = max(scores.items(), key = lambda (k, v) : v)

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


# main logic #

def main():
    
    pass


# boilerplate code #

if __name__ == '__main__':
    main()
