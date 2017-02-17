# 
# stats.py
# 
# This file contains code to help compute
# various basic stats for a given piece of text
# 

# imports #

from data import *


# constants #

VOWELS = "aeiou"


# functions #

def __remove_extra(s):
    '''
    Removes trailing non-alphabetic characters (,!?;:) from s
    '''

    i = len(s)

    while i > 0 and not s[i - 1].isalpha():
        
        i = i - 1

    return s[:i]

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

    NOTE: This function is case-insensitive

    NOTE 2: If a vowel does not exist in the 
            input string, it is absent from
            the keys of the output dict
    '''
    
    return __build_counts(s, lambda ch : ch.isalpha() and ch in VOWELS)

def num_consonants(s):
    '''
    Given a string, returns a dict mapping each consonant
    to a count of number of occurrences

    NOTE: This function is case-insensitive

    NOTE 2: If a consonant does not exist in
            the input string, it will be absent
            from the keys of the output dict
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

        w = __remove_extra(w.lower())

        counts[w] = counts.get(w, 0) + 1
    
    return counts

def get_mood(s):
    '''
    Given a string, returns a "mood" (positive/neutral/negative)
    associated with the content of this text
    '''
    
    # build a mapping between each word and its mood
    raw_data = read_dataset()
    
    sentiment_map = {d['word'] : d['polarity'] for d in raw_data}

    scores = {'positive' : 0, 'negative' : 0, 'neutral' : 0}

    # determine mood for each word in the input text
    for word in s.split():

        word = __remove_extra(word.lower())

        if word in sentiment_map:
            
            polarity = sentiment_map[word]
            scores[polarity] = scores.get(polarity, 0) + 1
    
    # return one of positive, negative, or neutral category
    category, count = max(scores.items(), key = lambda kv : kv[1])

    if count == 0 or scores['positive'] == scores['negative']:
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


def report_json_summary(s):
    '''
    returns a python dictionary containing 
    various summary stats after analyzing 
    the given input string

    The keys of this dictionary are defined as follows:

    - vowel_count : a dictionary mapping vowels to number of occurrences
    - consonant_count : a dictionary mapping consonants to number of occurrences
    - word_count : a dictionary mapping words to number of occurences
    - mood : a string representing the "mood" of the entire text {positive, neutral, negative}
    - content : the content of the input string itself
    '''
    
    info_dict = {}

    info_dict['vowel_count'] = num_vowels(s)

    info_dict['consonant_count'] = num_consonants(s)

    info_dict['word_count'] = num_words(s)

    info_dict['mood'] = get_mood(s)

    info_dict['content'] = s

    return info_dict
