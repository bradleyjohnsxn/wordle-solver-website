import numpy as np
import pandas as pd

class  wordle_solver():

    def __init__(self):
        self.load_words()
        self.load_word_freqs()
        self.possible = self.words
        self.greens = np.array([])
        self.yellows = np.array([])
        self.used = np.array([])

    # load 5 letter words from file
    def load_words(self):
        filepath = 'data/5letterwords.txt'
        word_file = open(filepath, 'r')
        self.words = word_file.readlines()
        for i in range(len(self.words)): self.words[i]=self.words[i][:5]
        word_file.close()

    # load map of words and their frequency
    def load_word_freqs(self):
        filepath = 'data/5letter_unigram_freq.csv'
        self.freqs =  dict(pd.read_csv(filepath).to_numpy())



if __name__=='__main__':
    ws = wordle_solver()
