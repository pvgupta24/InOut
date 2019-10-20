
import sys
import os
from filler_words import filler_words

def read_file(filename):
    ''' Takes in a file name and reads it in as a list of words
    '''
    with open(filename, 'r') as f:
        return f.read().lower().split()

def filler_percentage(segments, filler=[]):
    ''' Takes in a list of segments and an optional list of filler
        words to search for and returns the % of the filler word's
        occurrence.
    '''
    num_filler = 0
    for word in filler:
        num_filler += segments.count(word.lower())
    total_words = len(segments)

    print('Total_words:', total_words)
    print('Number of filler words: ', num_filler)
    percent = num_filler/total_words
    print('Percent of filler words', percent)
    print('as compared to TED standard frequency of filler words (0.005589%)')
    compare_to_standard(percent, 0.005589)
    return percent

def compare_to_standard(percent, standard):
    ''' This function takes in the percentage of the user's usage of filler
        words and compares it with the gold standard and compares against it
    '''
    if percent < standard:
        print('Good speech. Less fillers')
    else:
        print('Too many filler words')

if __name__=='__main__':
    TRANSCRIPT_DIR = 'transcripts/'
    filename = os.path.join(TRANSCRIPT_DIR, 'test.txt')
    read = read_file(filename) 
    percentage_filler_words = filler_percentage(read, filler_words)
    print(("Percentage of filler words is: " + str(percentage_filler_words)))