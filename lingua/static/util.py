import static.settings as settings

def log(msg, level = "INFO"):
    if settings.log_levels.index(level) <= settings.log_level: 
        print(level + " : " + msg)

def word_ended(char, word):
    return char in settings.syntax['endings']['word'] and word != ''

def sentence_ended(char):
    return char in settings.syntax['endings']['sentence']

def punctuated(char):
    return char in settings.syntax['punctuation']

def quoted(char):
    return char in settings.syntax['quotation']
