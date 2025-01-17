import math
import nltk
import time
from collections import Counter
import string

# Constants to be used by you when you fill the functions
START_SYMBOL = '*'
STOP_SYMBOL = 'STOP'
MINUS_INFINITY_SENTENCE_LOG_PROB = -1000

# TODO: IMPLEMENT THIS FUNCTION
# Calculates unigram, bigram, and trigram probabilities given a training corpus
# training_corpus: is a list of the sentences. Each sentence is a string with tokens separated by spaces, ending in a newline character.
# This function outputs three python dictionaries, where the keys are tuples expressing the ngram and the value is the log probability of that ngram
def calc_probabilities(training_corpus):
    unigram_p = {}
    bigram_p = {}
    trigram_p = {}

    # training_corpus = ["he is good"+ " \n " + "he is bad" ]
    unigram_words_set = []
    bigram_words_set = []
    trigram_words_set = []

    for line in training_corpus:
        # Strip new line and other space characters at the end.
        line = line.strip()

        # Remove punctuation symbols from the string.
        line = line.translate(string.maketrans("",""), string.punctuation)

        line = START_SYMBOL + ' ' + line + ' ' + STOP_SYMBOL

        words_list = line.split(' ')
        i = 0
        len_words = len(words_list)
        for word in words_list:
            if(not(word is START_SYMBOL) and not(word is STOP_SYMBOL)):
                unigram_words_set.append(word)
            if i<len_words-1:
                bigram_words_set.append(words_list[i+1] + " " + words_list[i])
                if i<len_words-2:
                    trigram_words_set.append(words_list[i+2] + " " + words_list[i+1] + " " + words_list[i])
            i+=1

    unigram_words_counter = Counter(unigram_words_set)
    bigram_words_counter = Counter(bigram_words_set)
    trigram_words_counter = Counter(trigram_words_set)

    total_words = sum(unigram_words_counter.values()) #len(unigram_words_counter.keys())
    for word in unigram_words_counter:
        unigram_p[word] = math.log(float(unigram_words_counter[word])/total_words)

    for word in bigram_words_counter:
        bigram_i_1_word = word.split(' ')[0]
        bigram_p[word] = math.log(float(bigram_words_counter[word])/float(unigram_words_counter[bigram_i_1_word]))

    for word in trigram_words_counter:
        trigram_i_2_1_word = word.split(' ')[0] + " " + word.split(' ')[1]
        trigram_p[word] = math.log(float(trigram_words_counter[word])/float(bigram_words_counter[trigram_i_2_1_word]))


    return unigram_p, bigram_p, trigram_p

# Prints the output for q1
# Each input is a python dictionary where keys are a tuple expressing the ngram, and the value is the log probability of that ngram
def q1_output(unigrams, bigrams, trigrams, filename):
    # output probabilities
    outfile = open(filename, 'w')

    unigrams_keys = unigrams.keys()
    unigrams_keys.sort()
    for unigram in unigrams_keys:
        outfile.write('UNIGRAM ' + unigram[0] + ' ' + str(unigrams[unigram]) + '\n')

    bigrams_keys = bigrams.keys()
    bigrams_keys.sort()
    for bigram in bigrams_keys:
        outfile.write('BIGRAM ' + bigram[0] + ' ' + bigram[1]  + ' ' + str(bigrams[bigram]) + '\n')

    trigrams_keys = trigrams.keys()
    trigrams_keys.sort()    
    for trigram in trigrams_keys:
        outfile.write('TRIGRAM ' + trigram[0] + ' ' + trigram[1] + ' ' + trigram[2] + ' ' + str(trigrams[trigram]) + '\n')

    outfile.close()


# TODO: IMPLEMENT THIS FUNCTION
# Calculates scores (log probabilities) for every sentence
# ngram_p: python dictionary of probabilities of uni-, bi- and trigrams.
# n: size of the ngram you want to use to compute probabilities
# corpus: list of sentences to score. Each sentence is a string with tokens separated by spaces, ending in a newline character.
# This function must return a python list of scores, where the first element is the score of the first sentence, etc. 
def score(ngram_p, n, corpus):
    scores = []
    return scores

# Outputs a score to a file
# scores: list of scores
# filename: is the output file name
def score_output(scores, filename):
    outfile = open(filename, 'w')
    for score in scores:
        outfile.write(str(score) + '\n')
    outfile.close()

# TODO: IMPLEMENT THIS FUNCTION
# Calculates scores (log probabilities) for every sentence with a linearly interpolated model
# Each ngram argument is a python dictionary where the keys are tuples that express an ngram and the value is the log probability of that ngram
# Like score(), this function returns a python list of scores
def linearscore(unigrams, bigrams, trigrams, corpus):
    scores = []
    return scores

DATA_PATH = 'data/'
OUTPUT_PATH = 'output/'

# DO NOT MODIFY THE MAIN FUNCTION
def main():
    # start timer
    time.clock()

    # get data
    infile = open(DATA_PATH + 'Brown_train.txt', 'r')
    corpus = infile.readlines()
    infile.close()

    # calculate ngram probabilities (question 1)
    unigrams, bigrams, trigrams = calc_probabilities(corpus)

    # question 1 output
    q1_output(unigrams, bigrams, trigrams, OUTPUT_PATH + 'A1.txt')

    # score sentences (question 2)
    uniscores = score(unigrams, 1, corpus)
    biscores = score(bigrams, 2, corpus)
    triscores = score(trigrams, 3, corpus)

    # question 2 output
    score_output(uniscores, OUTPUT_PATH + 'A2.uni.txt')
    score_output(biscores, OUTPUT_PATH + 'A2.bi.txt')
    score_output(triscores, OUTPUT_PATH + 'A2.tri.txt')

    # linear interpolation (question 3)
    linearscores = linearscore(unigrams, bigrams, trigrams, corpus)

    # question 3 output
    score_output(linearscores, OUTPUT_PATH + 'A3.txt')

    # open Sample1 and Sample2 (question 5)
    infile = open(DATA_PATH + 'Sample1.txt', 'r')
    sample1 = infile.readlines()
    infile.close()
    infile = open(DATA_PATH + 'Sample2.txt', 'r')
    sample2 = infile.readlines()
    infile.close() 

    # score the samples
    sample1scores = linearscore(unigrams, bigrams, trigrams, sample1)
    sample2scores = linearscore(unigrams, bigrams, trigrams, sample2)

    # question 5 output
    score_output(sample1scores, OUTPUT_PATH + 'Sample1_scored.txt')
    score_output(sample2scores, OUTPUT_PATH + 'Sample2_scored.txt')

    # print total time to run Part A
    print "Part A time: " + str(time.clock()) + ' sec'

if __name__ == "__main__": main()
