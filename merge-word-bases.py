import numpy as np
import pandas as pd

# load 5 letter words from file
def load_words(filepath):
    word_file = open(filepath, 'r')
    words = word_file.readlines()
    for i in range(len(words)): words[i]=words[i][:5]
    word_file.close()
    return words

# load map of words and their frequency
def load_word_freqs():
    filepath = 'data/5letter_unigram_freq.csv'
    return dict(pd.read_csv(filepath).to_numpy())


if __name__=='__main__':
    words_txt1 = load_words('data/5letterwords.txt')
    words_txt2 = load_words('data/5letterwords2.txt')
    words_csv = np.array(list(load_word_freqs().keys()))
    words_merged = np.array(list(set(list(np.append(np.append(words_txt1, words_txt2), words_csv)))))

    print(f'words in original text file 1: {len(words_txt1)}')
    print(f'words in original text file 2: {len(words_txt2)}')
    print(f'words in original csv file   : {len(words_csv)}')
    print(f'word count total             : {len(words_merged)}')

    filepath = 'data/5letterwords-updated.txt'
    file = open(filepath, 'w')
    for word in words_merged:
        file.write(word+'\n')
    file.close()