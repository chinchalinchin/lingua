import argparse
import json

import context

def _args():
    parser = argparse.ArgumentParser(
        prog="Lingua Python",
        description="A command line utility for lexical analysis.",
    )
    parser.add_argument('function', choices = ["context"])
    parser.add_argument('-infile','--infile', '-i', '--i')
    parser.add_argument('-outfile', '--outfile', '-o', '--o')
    return parser.parse_args()

def _context(file) -> None:
    filename = file.split('.')[0]
    v, c = context.ingest(file)
    v, c = context.process(v, c)
    save = context.format(v, c)

    filename = file.split('.')[0]

    with open(f'{filename}_context.json', 'w') as outfile:
        json.dump(save, outfile)

if __name__ == "__main__":
    ar = _args()

    if ar.function == 'context':
        _context(ar.infile)
