import argparse, json, typing

import objects.lexical, settings, util

def _args():
    parser = argparse.ArgumentParser(
        prog="Lingua Python",
        description="wut",
        epilog="do"
    )
    parser.add_argument('file')
    return parser.parse_args()

def _process(file) -> None:
    w, s = _ingest(file)
    w, s = _contextualize(w, s)
    _persist(w, s, file)

def _ingest(file) -> typing.Tuple[settings.corpus, settings.text]:    
    infile = open(file, 'r')
    char = not None
    buff_w, buff_q, buff_s = '', [], []

    corpus, text = [], []
    w_count, s_count = 0, 0

    while char:
        char = infile.read(1).lower()

        # loop flags
        w_end = util.word_ended(char, buff_w)
        s_end = util.sentence_ended(char)
        punctuate = util.punctuated(char)
        quote = util.quoted(char)
        quoting = util.quoting(buff_s)

        # if about to unquote
        if quoting and quote:
            if settings.tokens['quotation'] not in corpus:
                corpus.append(settings.tokens['quotation'])

            buff_s.append(settings.tokens['quotation'])
            
        # if about to quote or unquote
        if quote:
            if settings.tokens['quote'] not in corpus:
                corpus.append(settings.tokens['quote'])

            buff_s.append(settings.tokens['quote'])
                
            print(f'Found quote mark: {settings.tokens["quote"]}')

            # if about to unquote and the quoted sentence has terminated.
            if quoting and len(buff_q) == 0:
                sentence = objects.lexical.Sentence(buff_s)
                buff_s = []
                print(f'Found quotation sentence: {sentence}')

        # if word or sentence about to end
        if w_end or s_end:
            
            word = objects.lexical.Word(buff_w)

            if word not in corpus:
                corpus.append(word)

            if quoting:
                buff_q.append(word)

            else:
                buff_s.append(word)

            buff_w = ''
            w_count += 1

            print(f'Found word: {word}')

        # if about to punctuate
        if punctuate:
            punc = objects.lexical.Word(char)

            if punc not in corpus:
                corpus.append(punc)

            if quoting:
                buff_q.append(punc)
                
            else:
                buff_s.append(punc)

            print(f'Found punctuation: {punc}')

        # if sentence about to end
        if s_end:
            
            if quoting:
                sentence = objects.lexical.Sentence(buff_q)
                buff_q = []
                print(f'Found quoted sentence: {sentence}')


            else: 
                sentence = objects.lexical.Sentence(buff_s)
                buff_s = []
                print(f'Found sentence: {sentence}')

            text.append(sentence)
            s_count += 1
 
        if char not in settings.word_ignores:
            buff_w = buff_w + char

    print("Total Word Count: ", w_count)
    print("Total Sentence Count: ", s_count)
    # observation: the cardinality of sentences must be greater than the cardinality of words
    #      reason: Every word is the answer to the question "Which word is next?".
    #     counter: The question "Which word is next?" is a meta-question.
    # observation: However, an observed corpus will always (with prob approx 1) exceed the 
    #               the cardinality of the text. I think. We shall see.
    infile.close()
    
    return corpus, text

def _contextualize(corpus: settings.corpus, text: settings.text):

    for s in text:
        s_length = len(s.words)

        for s_index in range(s_length):
            start, end = None, None

            if s_index != 0:
                start = s.words[s_index - 1]

            if s_index != s_length - 1:
                end = s.words[s_index + 1]

            try:
                w_index = corpus.index(s.words[s_index])
                corpus[w_index].add_context(start, end)
            except:
                print(s.words[s_index])

    return corpus, text

def _persist(corpus: settings.corpus, text: settings.text, file):
    
    filename = file.split('.')[0]

    corpus.sort()

    save_file = {}
    save_file['corpus'] = {}
    save_file['text'] = {}

    for w in corpus:
        save_file['corpus'][w.content] = dict(w)

    for i, s in enumerate(text):
        save_file['text'][i] = str(s)

    
    with open(f'{filename}_analysis.json', 'w') as outfile:
        json.dump(save_file, outfile)


if __name__ == "__main__":
    ar = _args()

    _process(ar.file)
