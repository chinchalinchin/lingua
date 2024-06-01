import typing

import objects.lexical 

text : typing.TypeAlias = list[typing.Type[objects.lexical.Sentence]]
corpus : typing.TypeAlias = list[typing.Type[objects.lexical.Word]]

syntax = {
    'endings': {
        'word': [
            ' ',
            ',',
            '\n',
            '\t'
        ],
        'sentence': [
            '.',
            '?',
            '!',
            '"',
            '”'
        ]
    },
    'punctuation': [
        ',',
        '!',
        '.',
        '?'
    ],
    'quotation': [
        '"',
        '”',
        '“'
    ],
    'ignore': [
        '*',
        '_'
    ]
}

def word_ended(char, word):
    return char in syntax['endings']['word'] and word != ''