import os

log_levels = [ 'NONE', 'INFO', 'DEBUG', 'VERBOSE']

log_level = log_levels.index(
    os.environ.setdefault('LOG_LEVEL', 'INFO')
)

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