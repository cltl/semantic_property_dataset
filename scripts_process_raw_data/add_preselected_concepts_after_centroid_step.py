import sys
import glob
import os
import csv

from nltk import pos_tag
import spacy

from get_wordnet_data import word_data_to_dict

sys.path.append('../utils/')

from wordnet_data import get_wordnet_data
from wordnet_data import get_abstract_concrete
from wordnet_data import get_all_wup_sims
from wordnet_data import get_synsets

from sense_group_data import get_ontonotes_sense_dict
from sense_group_data import get_onto_senses
from sense_group_data import get_navigly_clusters
from sense_group_data import load_mipvu_metaphors

from annotation_selection import apply_selection

from add_qumcrae_labels import load_quantified_mcrea
from add_qumcrae_labels import add_qumcrae_labels

from data_utils import load_data
from data_utils import data_to_file
from data_utils import load_frequencies

from data_utils import load_mrc_data
from data_utils import get_mrc_score



def load_manually_selected():

    path = '../data/manually_included_after_centroid/properties_overview_selected.csv'
    property_concept_dict = defaultdict(list)

    with open(path) as infile:
        dict_list = list(csv.DictReader(infile, delimiter = '\t'))

    for d in dict_list:
        property = d['property']
        for label in ['pos', 'pos_met', 'neg', 'neg_met']:
            for concept in d[label].split(' '):
                concept_dict = dict()
                concept_dict['word'] = concept
                if label.startswith('pos'):
                    concept_dict['label'] = 'pos'
                elif label.startswith('neg'):
                    concept_dict['label'] = 'neg'
                concept_dict['categories_str'] = label
                concept_dict['sources_str'] = 'manually_included'
                concept_dict['certainty'] = 'certain'
                property_concept_dict[property].append(concept_dict)

    return property_concept_dict

def dict_list_to_dict(dict_list):

    word_dict_dict = dict()
    for d in dict_list:
        word_dict_dict[d['word']] = d
    return word_dict_dict


def merge_with_collected_concepts(dict_list, dict_list_manually_selected):

    word_dict_dict = dict_list_to_dict(dict_list)
    word_dict_dict_selected = dict_list_to_dict(dict_list_manually_selected)

    merged_dict_list = []

    for word, word_dict in word_dict_dict.items():
        if word in word_dict_dict_selected.keys():
            print('aready in the list: ', word)
            word_dict_selected = word_dict_dict[word]
            label = word_dict['label']

            word_dict['label'] = label
            word_dict['sources_str'] = word_dict['sources_str']+' '+'manually_included_after_centroid'
            word_dict['categories_str'] = word_dict['categories_str']+' '+word_dict_selected['categories_str']
            word_dict['certainty'] = 'certain'

            merged_dict_list.append(word_dict)
        else:
            merged_dict_list.append(word_dict)

    for word, word_dict in word_dict_dict_selected.items():
        if word not in word_dict_dict.keys():
            merged_dict_list.append(word_dict)
            print('adding ', word)

    return merged_dict_list







def main():
    collection = sys.argv[1]
    source = 'concepts_additional_info'
    target = 'concepts_additional_info'


    data_dict = load_data(collection, source)
    data_dict_manually_selected = load_manually_selected()
    extended_data_dict = dict()


    nlp = spacy.load('en_core_web_lg')

    qumcrae_property_dict = load_quantified_mcrea()
    poly_dict = load_ldoce_polysemy_data()
    wiki_freq_path = '../wikipedia_corpus_data/token_counts_from_full_wiki_corpus.csv'
    token_count_dict = load_frequencies(wiki_freq_path)
    navigli_path = '../../../Data/senses/coarse_grained_sense_inventory_semeval2007/training/sense_clusters-21.senses'
    navigli_sense_dict = get_navigly_clusters(navigli_path)
    onto_dir_path = '../../../Data/Ontonotes/sense-inventories/'
    onto_sense_dict = get_ontonotes_sense_dict(onto_dir_path)

    mipvu_dict = load_mipvu_metaphors()

    word_conc_dict = load_mrc_data('conc')
    word_fam_dict = load_mrc_data('fam')
    word_aoa_dict = load_mrc_data('aoa')

    for property, concept_dict_list in data_dict.items():
        concept_dict_list_manually_selected = data_dict_manually_selected[property]
        merged_dict_list = merge_with_collected_concepts(concept_dict_list,concept_dict_list_manually_selected)
        new_dict_list = []
        for concept_dict in merged_dict_list:
            # check which of the dicts is new:
            if 'wiki_frequency' not in concept_dict.keys():
                word_data_to_dict(concept_dict, token_count_dict, navigli_sense_dict, \
                                    onto_sense_dict, poly_dict, mipvu_dict)
                new_dict_list.append(concept_dict)
            else:
                new_dict_list.append(concept_dict)
        extended_data_dict[property] = new_dict_list

        #extended_data_dict[property] = merged_dict_list

    data_to_file(collection, extended_data_dict, target)


if __name__ == '__main__':
    main()
