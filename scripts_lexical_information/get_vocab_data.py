# get lists of polysemous, homonemous and both words from the ldoce dict (text file)


import os
import sys
import csv
from nltk.corpus import wordnet as wn
from collections import defaultdict
from collections import Counter

from synset_distances import get_average_distance_to_word
from synset_distances import get_monosemous_words

sys.path.append('../utils/')

from wordnet_data import get_wordnet_data
from wordnet_data import get_abstract_concrete
from wordnet_data import get_synsets
from wordnet_data import check_wordnet_noun
from wordnet_data import get_all_wup_sims


from sense_group_data import get_ontonotes_sense_dict
from sense_group_data import get_onto_senses
from sense_group_data import get_navigly_clusters
from sense_group_data import load_mipvu_metaphors
from sense_group_data import load_metonymy_entities

from data_utils import load_frequencies

from load_models import load_model




def load_dict(path):

    # structure:
    # {word (unique) : [ {word_pos (unique among polysemous senses: [sense1, sense2, sense3] }]
    word_dict = defaultdict(list)
    #word_dict = dict()
    all_words = []
    with open(path) as infile:
        all_entries =  infile.read().strip().split('------')
    for entry in all_entries:
        entry_lines = entry.strip().split('\n')
        if len(entry_lines) > 1:
            #print(entry_lines)
            entry_dict = dict()
            word = entry_lines[0].split(',')
            word = word[0].strip()
            if word.startswith('('):
                word = all_words[-1]
            all_words.append(word)
            pos = entry_lines[1]
            senses = entry_lines[2:]
            entry_dict[word+'_'+pos] = senses
            word_dict[word].append(entry_dict)

    return word_dict

def words_to_file(word_list, path):

    if not os.path.isdir('wordlists'):
        os.mkdir('wordlists')

    header = list(word_list[0].keys())

    with open(path, 'w') as outfile:
        writer = csv.DictWriter(outfile, fieldnames = header)
        writer.writeheader()
        for wd in word_list:
            writer.writerow(wd)



def main():
    path = '../../../Data/Homonymy-polysemy-dict/ldoce-headwords.txt'
    ldoce_dict = load_dict(path)

    new_path = '../data/vocab/all_lodce.csv'


    word_list = []

    navigli_path = '../../../Data/senses/coarse_grained_sense_inventory_semeval2007/training/sense_clusters-21.senses'
    navigli_sense_dict = get_navigly_clusters(navigli_path)
    onto_dir_path = '../../../Data/Ontonotes/sense-inventories/'
    onto_sense_dict = get_ontonotes_sense_dict(onto_dir_path)

    metonymy_path = '../../../Data/metonymy/voc_from_minimalist.txt'
    metonymy_words = load_metonymy_entities(metonymy_path)
    mipvu_dict = load_mipvu_metaphors()


    wiki_freq_path = '../wikipedia_corpus_data/token_counts_from_full_wiki_corpus.csv'
    token_count_dict = load_frequencies(wiki_freq_path)

    path_wiki_sgns = '../../../Data/dsm/wikipedia_full/sgns_pinit1/sgns_pinit1/sgns_rand_pinit1'
    model = load_model(path_wiki_sgns, 'sgns')
    # use all interesting words even if they are not in the lodce dict

    all_words = set()
    all_words.update(ldoce_dict.keys())
    all_words.update(mipvu_dict.keys())
    all_words.update(metonymy_words)



    #for word, entries in list(word_dict.items()):
    for word in sorted(list(all_words)):
        entries = ldoce_dict[word]
        # check if a word has more than a single entry, which means it is
        # homoneouns:
        word_dict = dict()
            #pos_set = set()
        pos_counter = Counter()
        n_senses = 0
        for entry in entries:
            for word, senses in entry.items():
                word, pos = word.split('_')
                pos_counter[pos] += 1
                n_senses += len(senses)
        if pos_counter.keys():
            highest_pos_value = max([c for pos, c in pos_counter.items()])
        else:
            highest_pos_value = None
            senses = []
        word_dict['word'] = word
        word_dict['n_entries'] = len(entries)
        word_dict['n_senses_total'] = n_senses
        word_dict['wn_synsets'] = len(wn.synsets(word))


        if (len(entries) > 1) and (highest_pos_value == 1):
            word_dict['polysemy_type'] = 'homonyms_only_different_pos'
            #homonyms_only_different_pos.append(word_dict)
        elif len(entries) >  1:
            #homonyms_also_same_pos.append(word_dict)
            word_dict['polysemy_type'] = 'homonyms_also_same_pos'
        elif len(entries) == 1 and len(senses) > 1:
            #poly_words.append(word_dict)
            word_dict['polysemy_type'] = 'poly'
        elif len(senses) == 1:
            #mon_words.append(word_dict)
            word_dict['polysemy_type'] = 'mon'
        else:
            word_dict['polysemy_type'] = None

        # add other info
        exists, noun, n_senses, min_wn_sense_sim = get_wordnet_data(word)
        word_dict['n_synsets'] = n_senses
        word_dict['min_wup_sim'] = min_wn_sense_sim

        word_dict['n_navigli_clusters'] = len(navigli_sense_dict[word])
        onto_senses = get_onto_senses(word, onto_sense_dict)
        word_dict['n_onto_senses_n_v'] = len(onto_senses)
        word_dict['wn-abs-conc'] = get_abstract_concrete(word)

        if word_dict['n_synsets'] != 0:
            word = word_dict['word']
            monosemous_words_dict = get_monosemous_words(word)
            all_mon_words = []
            [all_mon_words.extend(mon_words) for mon_words in monosemous_words_dict.values()]
            if all_mon_words:
                av_distance_word = get_average_distance_to_word(model, word, all_mon_words)
                word_dict['av_cos_mon_synonyms_to_word'] = av_distance_word
            else:
                word_dict['av_cos_mon_synonyms_to_word'] = None
        else:
            word_dict['av_cos_mon_synonyms_to_word'] = None

        if word in mipvu_dict:
            annotation =  mipvu_dict[word]
            if annotation == 'met non-met' or annotation == 'met':
                word_dict['mipvu'] = True
            else:
                word_dict['mipvu'] = False
        else:
            word_dict['mipvu'] = False

        if word in metonymy_words:
            word_dict['metonymy_entities'] = True
        else:
            word_dict['metonymy_entities'] = False

        synsets = get_synsets(word)

        all_wup_sims = get_all_wup_sims(synsets)
        if all_wup_sims:
            word_dict['av_wup_sim'] = sum(all_wup_sims)/len(all_wup_sims)
        else:
            word_dict['av_wup_sim'] = None

        noun = check_wordnet_noun(synsets)
        if word in token_count_dict.keys():
            word_dict['wiki_frequency'] = token_count_dict[word]
        else:
            word_dict['wiki_frequency'] = None
        word_dict['wn_noun'] = noun

        word_list.append(word_dict)


    words_to_file(word_list, new_path)
    #words_to_file(homonyms_only_different_pos, 'homonyms_only_different_pos')
    #words_to_file(homonyms_also_same_pos, 'homonyms_also_same_pos')
    #words_to_file(mon_words, 'monosemous')



if __name__ == '__main__':
    main()
