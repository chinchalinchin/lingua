import argparse, json, typing

import objects.lexical, settings, util

word_ignores = [
    *settings.syntax['endings']['word'],
    *settings.syntax['endings']['sentence'],
    *settings.syntax['punctuation'],
    *settings.syntax['quotation'],
    *settings.syntax['ignore']
]

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
    buff_word, buff_sentence = '', []

    corpus, text = [], []
    w_count, s_count = 0, 0

    while char:
        char = infile.read(1).lower()

        word_ended = util.word_ended(char, buff_word)
        sentence_ended = util.sentence_ended(char)
        punctuated = util.punctuated(char)
        quoted = util.quoted(char)

        if word_ended or sentence_ended:
            
            word = objects.lexical.Word(buff_word)

            if word not in corpus:
                corpus.append(word)

            buff_sentence.append(word)
            buff_word = ''
            w_count += 1

            print(f'Found word: {word}')

        if punctuated or quoted:
            punc = objects.lexical.Word(char)

            if punc not in corpus:
                corpus.append(punc)

            buff_sentence.append(punc)

            print(f'Found punctuation: {punc}')


        if sentence_ended:

            quotes = [ w for w in buff_sentence if w in settings.syntax['quotation'] ]
            
            if len(quotes) % 2 == 0:
                sentence = objects.lexical.Sentence(buff_sentence)
                text.append(sentence)
                
                buff_sentence = []
                s_count += 1

                print(f'Found sentence: {sentence}')

        # missing the case where a sentence is entirely a quote:
        #       "Yes."
        #       "I do not remember it."

        # in this case, the sentence_end occurs before the end quote.

        # in other words, a 'quote', by its nature, needs to look at:
            # the last character of the quoted sentence 
            # the next character after the quotation

        # in order to determine if the sentence continues. 
        if char not in word_ignores:
            buff_word = buff_word + char

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

            w_index = corpus.index(s.words[s_index])
            corpus[w_index].add_context(start, end)

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
