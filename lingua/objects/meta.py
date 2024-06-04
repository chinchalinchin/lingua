import typing

import objects.lexical

Corpus : typing.TypeAlias = list[typing.Type[objects.lexical.Sentence]]
Vocab : typing.TypeAlias = list[typing.Type[objects.lexical.Word]]

# TOKENS
tokens = {
    'quotation': objects.lexical.Word('φ'),
    'end': objects.lexical.Word('#'),
    'null': objects.lexical.Word('∅'),
    'quote': objects.lexical.Word('"'),
    'comma': objects.lexical.Word(","),
    'exclamative': objects.lexical.Word("!"),
    'interrogative': objects.lexical.Word("?"),
    'declarative': objects.lexical.Word(".")
}

def quoting(sentence):
    q = [
        w 
        for w in sentence
        if w == tokens['quote']
    ]

    return len(q) % 2 != 0