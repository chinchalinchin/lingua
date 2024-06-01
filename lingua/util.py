import settings

def word_ended(char, word):
    return char in settings.syntax['endings']['word'] and word != ''

def sentence_ended(char):
    return char in settings.syntax['endings']['sentence']

def punctuated(char):
    return char in settings.syntax['punctuation']

def quoted(char):
    return char in settings.syntax['quotation']

def quoting(sentence):
    q = [
        w 
        for w in sentence
        if w == settings.tokens['quote']
    ]

    return len(q) % 2 != 0