import typing
import math

import static.settings as settings
import static.util as util
import objects.lexical
import objects.meta

def quoting(sentence):
    q = [
        w 
        for w in sentence
        if w == objects.meta.tokens['quote']
    ]

    return len(q) % 2 != 0

def ingest(file) -> typing.Tuple[objects.meta.Vocab, objects.meta.Corpus]:    
    infile = open(file, 'r')
    char = not None
    buff_w, buff_q, buff_s = '', [], []

    vocab, corpus = [], []
    w_count, s_count = 0, 0

    while char:
        char = infile.read(1).lower()

        # loop flags
        w_end = util.word_ended(char, buff_w)
        s_end = util.sentence_ended(char)
        punctuate = util.punctuated(char)
        quote = util.quoted(char)
        quoting = objects.meta.quoting(buff_s)

        # if about to unquote
        if quoting and quote:
            buff_s.append(objects.meta.tokens['quotation'])

        if quote:
            buff_s.append(objects.meta.tokens['quote'])
                
            util.log(
                f'Found quote mark: {objects.meta.tokens["quote"]}',
                'DEBUG'
            )

            # if about to unquote and the quoted sentence has terminated.
            if quoting and len(buff_q) == 0:
                sentence = objects.lexical.Sentence(buff_s)
                corpus.append(sentence)
                buff_s = []
                
                util.log(f'Found quotation sentence: {sentence}')

        if w_end or s_end:
            
            word = objects.lexical.Word(buff_w)

            if word not in vocab:
                vocab.append(word)
            
            if quoting:
                buff_q.append(word)
            else:
                buff_s.append(word)

            buff_w = ''
            w_count += 1

            util.log(f'Found word: {word}', 'DEBUG')

        if punctuate:
            punc = objects.lexical.Word(char)

            if quoting:
                buff_q.append(punc)
            else: 
                buff_s.append(punc)


            util.log(f'Found punctuation: {punc}', 'DEBUG')

        if s_end:
            
            if quoting:
                sentence = objects.lexical.Sentence(buff_q)
                buff_q = []
                
                util.log(f'Found quoted sentence: {sentence}')


            else: 
                sentence = objects.lexical.Sentence(buff_s)
                buff_s = []
                
                util.log(f'Found sentence: {sentence}')

            corpus.append(sentence)
            s_count += 1
 
        if char not in settings.word_ignores:
            buff_w = buff_w + char

    util.log(f"Total Word Count: {w_count}")
    util.log(f"Total Sentence Count: {s_count}")
    
    infile.close()
    
    return vocab, corpus

def process(vocab: objects.meta.Vocab, corpus: objects.meta.Corpus):
    v_len = len(vocab)

    for s in corpus:
        s_len = len(s.words)

        for s_i in range(s_len):
            
            if s.words[s_i] not in objects.meta.tokens.values():
          
                buff_s_i = s_i
                while buff_s_i >= 0:
                    try:
                        buff_s_i -= 1

                        if s.words[buff_s_i - 1] not in objects.meta.tokens.values():
                            prior = s.words[buff_s_i - 1]
                            break
                            
                    except IndexError:
                        prior = objects.meta.tokens['null']

                buff_s_i = s_i
                while buff_s_i <= s_len - 1:
                    try:
                        buff_s_i += 1

                        if s.words[buff_s_i + 1] not in objects.meta.tokens.values():
                            post = s.words[buff_s_i + 1]
                            break

                    except IndexError: 
                        post = objects.meta.tokens['null']

                w_of_s_i = vocab.index(s.words[s_i])
                vocab[w_of_s_i].add_context(prior, post)
    
    for o_i in range(v_len):
        o_word = vocab[o_i]
        o_freq = o_word.frequency()
        o_starts = o_word.prior_contexts()
        o_ends = o_word.post_contexts()

        for i_i in range(o_i + 1,v_len):
            i_word = vocab[i_i]
            i_freq = i_word.frequency()
            i_starts = i_word.prior_contexts()
            i_ends = i_word.post_contexts()

            prior_i_freq = len([ i_s for i_s in i_starts if i_s in o_starts ])
            post_i_freq = len([ i_e for i_e in i_ends if i_e in o_ends ])

            prior_o_freq = len([ o_s for o_s in o_starts if o_s in i_starts ])
            post_o_freq = len([ o_e for o_e in o_ends if o_e in i_ends ])

            total_i_dist = math.sqrt(prior_i_freq ** 2 + post_i_freq ** 2)
            total_o_dist = math.sqrt(prior_o_freq ** 2 + post_o_freq ** 2)

            if total_i_dist > 0:
                total_i_dist = total_i_dist / i_freq

                vocab[i_i].set_distance(o_word, total_i_dist)

            if total_o_dist > 0:
                total_o_dist = total_o_dist / o_freq

                vocab[o_i].set_distance(i_word, total_o_dist)

        vocab[o_i].sort_distances()

    vocab.sort(reverse = True)
     
    return vocab, corpus

def format(vocab: objects.meta.Vocab, corpus: objects.meta.Corpus):
    
    return {
        w.content: dict(w)
        for w in vocab
        if w not in objects.meta.tokens.values()
    }
