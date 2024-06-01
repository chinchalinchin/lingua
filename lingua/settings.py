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
            '!'
        ]
    },
    'tokens': {
        'end': '(END)',
        'null': '(NULL)',
        'quote': '(QUOTE)'
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
    'ignores': [
        '*',
        "—",
        '_'
    ]
}

word_ignores = [
    *syntax['endings']['word'],
    *syntax['endings']['sentence'],
    *syntax['punctuation'],
    *syntax['quotation'],
    *syntax['ignores']
]

# TOKENS
tokens = {
    'quotation': objects.lexical.Word('(QUOTATION)'),
    'end': objects.lexical.Word('(END)'),
    'null': objects.lexical.Word('(NULL)'),
    'quote': objects.lexical.Word('(QUOTE)'),
    'comma': objects.lexical.Word('(COMMA)')
}