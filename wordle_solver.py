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

    # add green
    def add_green(self, green): 
        self.greens=np.append(self.greens, str(green))
        self.green_added()
    
    # add yellow
    def add_yellow(self, yellow): 
        self.yellows=np.append(self.yellows, str(yellow))
        self.yellow_added()

    # add used
    def add_used(self, u): 
        for i in range(len(str(u))): self.used=np.append(self.used, str(u)[i])
        self.used_added(len(u))

    # get index/letter map
    def ind_map(self, s):
        inds = dict()
        for i in range(5): 
            if s[i].isalpha(): inds[i] = s[i]
        return inds

    # adjust possible after green added
    def green_added(self):
        inds = self.ind_map(self.greens[len(self.greens)-1])

        res = []
        for i in range(len(self.possible)):
            for (ind, let) in inds.items():
                if self.possible[i][ind] != let: res += [i]; break

        res = np.sort(res)[::-1]
        for i in res: self.possible.remove(self.possible[i])

    # adjust possible after yellow added
    def yellow_added(self):
        inds = self.ind_map(self.yellows[len(self.yellows)-1])

        res = []
        for i in range(len(self.possible)):
            for (ind, let) in inds.items():
                if self.possible[i][ind] == let: res += [i]; break
                b=False
                for j in range(5):
                    if j!=ind and self.possible[i][j] == let: break
                    elif (j==4 and ind!=4) or (j==3 and ind==4): res += [i]; b=True
                if b: break

        res = np.sort(res)[::-1]
        for i in res: self.possible.remove(self.possible[i])

    # adjust possible after letters used
    def used_added(self,  n):
        u = self.used[-n:]
        needed = []
        for i in range(len(self.yellows)):
            for let in self.ind_map(self.yellows[i]).values():
                needed += [let]
        for i in range(len(self.greens)):
            for let in self.ind_map(self.greens[i]).values():
                needed += [let]
        for x in needed:
            for y in u:
                if x==y: u = np.delete(u, np.where(u == y))

        res = []
        for i in range(len(self.possible)):
            for j in range(len(u)):
                if u[j] in self.possible[i]: res += [i]; break

        res = np.sort(res)[::-1]
        for i in res: self.possible.remove(self.possible[i])

    # sort and print possible words
    def print_possible(self):
        stacked = dict()
        for word in self.possible:
            try: stacked[word] = int(self.freqs[word])
            except KeyError as ke: stacked[word] = 0   

        stacked = {k: v for k, v in np.array(sorted(stacked.items(), key=lambda item: item[1]))[::-1]}
        print(f'\n{len(ws.possible)} possible word(s):')
        for num, word in enumerate(stacked.keys(), 1): 
            if num < 11: print(f'{num}. {word}')
            else: break

    # reset
    def reset(self):
        self.possible = self.words
        self.greens = np.array([])
        self.yellows = np.array([])
        self.used = np.array([])


if __name__=='__main__':
    go = True
    while go:
        ws = wordle_solver()
        cont = True
        while cont:
            g = input('\nenter greens: ')
            ws.add_green(g)
            y_done = False
            while not y_done:
                y = input('enter yellows (type "end" to continue): ')
                if y=='end': y_done = True
                else: ws.add_yellow(y)
            u = input('enter used letters: ')
            ws.add_used(u)
            ws.print_possible()
            c = input('\ncontinue? (y/n) ')
            if c != 'y': cont=False
        aw = input('another word? (y/n)')
        if aw != 'y': go = False        
