import sys
#from collections import defaultdict
import os
from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk import stem

from get_mipvu_vocab import load_mipvu_metaphors

#sys.path.append('../utils/')


def get_met_pos(met_vocab, pos):

    met_pos_vocab = []
    for w in met_vocab:
        syns = wn.synsets(w)

        pos_tags = [syn.pos() for syn in syns]

        if pos in pos_tags:
            met_pos_vocab.append(w)

    return met_pos_vocab

def met_pos_vocab_to_file(word_domain_dict, pos):

    if not os.path.isdir('mip_met_vocab'):
        os.mkdir('mip_met_vocab')

    with open(f'mip_met_vocab/{pos}-concepts-definitions.csv', 'w') as outfile:
        outfile.write('word\tdefinition\tconcepts\n')

        for word, def_domain_nouns in word_domain_dict.items():
            for definition, domain_nouns in def_domain_nouns:

                outfile.write(f'{word}\t{definition}\t{" ".join(domain_nouns)}\n')




def get_domains_from_examples(word, pos):

    pos_dict = {
                'a': wn.ADJ,
                'v': wn.VERB,
                'n': wn.NOUN
    }

    syns = wn.synsets(word, pos = pos_dict[pos])

    lmtzr = stem.wordnet.WordNetLemmatizer()

    def_domain_nouns = []

    if len(syns) > 1:
        for syn in syns:
            examples = syn.examples()
            definition = syn.definition()
            #print(definition)
            domain_nouns = set()
            for example in examples:
                tokens = word_tokenize(example)
                pos_tagged_tokens = pos_tag(tokens)
                for w, pos in pos_tagged_tokens:
                    if pos in ['NN', 'NNS', 'NNP', 'NNPS']:
                        lemma = lmtzr.lemmatize(w, 'n')
                        domain_nouns.add(lemma)
            def_domain_nouns.append((definition, domain_nouns))

    return def_domain_nouns










def main():
    pos = sys.argv[1]
    path = '../../../Data/mipvu/corpus/VUAMC.xml'
    mip_vocab, met_counts  = load_mipvu_metaphors(path)

    met_vocab = [w for w, labels in mip_vocab.items() if 'met' in labels]
    met_pos_vocab = get_met_pos(met_vocab, pos)

    word_domain_dict = dict()

    for w in met_pos_vocab:
        domain_def_nouns = get_domains_from_examples(w, pos)
        word_domain_dict[w] = domain_def_nouns

    met_pos_vocab_to_file(word_domain_dict, pos)




if __name__ == '__main__':
    main()
