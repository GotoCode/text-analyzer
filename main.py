# 
# main logic for text analyzer program
# 
# NOTE: This project requires Python 3 to work properly
# 


# FEATURE LIST #

# "calculate" mood from text (naive method)
# report summary of analysis
# read in text from command line
# read in text from file
# read in text from url
# refactor code for vowel and consonant counting
# support for graphing frequencies via matplotlib


# imports #


# constants #

VOWELS = "aeiou"


# helper functions #

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
    Given an input string, this function returns a
    mood (happy, sad, etc.) for the given text
    '''

    pass

def get_mood(s):
    '''
    Given a string, returns a "mood" (positive/neutral/negative)
    associated with the content of this text
    '''
    
    pass

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
