# 
# main logic for text analyzer program
# 
# NOTE: This project requires Python 3 to work properly
# 


# FEATURE LIST #

# count words
# "calculate" mood from text
# report summary of analysis
# read in text from command line
# read in text from file
# read in text from url
# refactor code for vowel and consonant counting


# imports #


# constants #

VOWELS = "aeiou"

# helper functions #

def num_vowels(s):
    '''
    Given a string, returns a dict mapping each vowel
    to a count of number of occurrences
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
    '''
    
    pass


# main logic #

def main():
    
    pass


# boilerplate code #

if __name__ == '__main__':
    main()
