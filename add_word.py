FILEPATH = 'data/5letterwords.txt'

def isduplicate(word):
    file = open(FILEPATH, 'r')
    words = file.readlines()
    if (word+'\n') in words: return True
    return False

def isvalid(word):
    if len(word) != 5: return False
    for let in word:
        if not let.isalpha(): return False
    return True

def add_word(word):
    if isvalid(word) and  not isduplicate(word):
        file = open(FILEPATH, 'a')
        file.write(word+'\n')
        file.close()
