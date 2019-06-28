#from nltk.stem import PorterStemmer
#from nltk.corpus import wordnet as wn
import sys
import glob
import os
import csv

from nltk import pos_tag
import spacy

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


# Spacy functions

def lemmatize(nlp, concept):

    doc = nlp(concept)
    concept_token = doc[0]
    lemma = concept_token.lemma_
    pos = concept_token.pos_
    if pos == 'NOUN':
        noun =  True
    else:
        noun = False
    return lemma, noun





def load_ldoce_polysemy_data():

    f = '../scripts_lexical_information/wordlists/all_lodce.csv'
    ldoce_dict = dict()

    #for f in files:
    #    name = os.path.basename(f).split('.')[0]
    with open(f) as infile:
        reader = csv.DictReader(infile)
        for d in reader:
            ldoce_dict[d['word']] = d['polysemy_type']
    return ldoce_dict


def filter_concept(concept_dict, criteria = ['space_selection', 'word_in_wn?',\
                                'word_noun_in_wn?', 'word_noun_spacy?']):

    values = [concept_dict[c] for c in criteria]
    print(values)

    if all([v == True for v in values]):
        print('include')
        return True
    else:
        print('exclude')
        return False

def word_data_to_dict(concept_dict, token_count_dict, navigli_sense_dict, \
                    onto_sense_dict, poly_dict, mipvu_dict):

    concept = concept_dict.pop('concept')
    concept_dict['word'] = concept

    lemma, noun_spacy = lemmatize(nlp, concept)
    concept_dict['lemma'] = lemma

    # Frequency:
    concept_dict['wiki_frequency'] = token_count_dict[concept_dict['word']]

    #Get word/pos info:
    exists, noun, n_senses, min_wn_sense_sim = get_wordnet_data(lemma)
    if exists:
        synsets = get_synsets(lemma)
        all_wup_sims = get_all_wup_sims(synsets)
        if all_wup_sims:
            av_wup_sim = sum(all_wup_sims)/len(all_wup_sims)
        else:
            av_wup_sim = None
    else:
        av_wup_sim = None
    concept_dict['word_in_wn?'] = exists
    concept_dict['word_noun_in_wn?'] = noun
    concept_dict['word_noun_spacy?'] = noun_spacy

    # Get sense and group data:
    concept_dict['n_navigli_clusters'] = len(navigli_sense_dict[lemma])
    onto_senses = get_onto_senses(lemma, onto_sense_dict)
    concept_dict['n_onto_senses_n_v'] = len(onto_senses)
    concept_dict['n_wn_senses'] = n_senses
    concept_dict['min_wn_sim_wup'] = min_wn_sense_sim
    concept_dict['av_sim_wup'] = av_wup_sim

    if lemma in poly_dict:
        concept_dict['polysemy_type'] = poly_dict[lemma]
    else:
        concept_dict['polysemy_type'] = None

    if lemma in mipvu_dict:
        concept_dict['mipvu'] = mipvu_dict[lemma]
    else:
        concept_dict['mipvu'] = None

    concept_dict['wn_abs_conc'] = get_abstract_concrete(lemma)

    filter_decision = filter_concept(concept_dict)
    if filter_decision == True:
        concept_dict['filter'] = True
    else:
        concept_dict['filter'] = False

    concept_dict['conc'] = get_mrc_score(concept, word_conc_dict)
    concept_dict['fam'] = get_mrc_score(concept, word_fam_dict)
    concept_dict['aoa'] = get_mrc_score(concept, word_aoa_dict)






def main():
    collection = sys.argv[1]
    source = 'data_for_concept_selection_cosine_centroid'
    extension = 'selected'
    target = 'concepts_additional_info'

    data_dict = load_data(collection, source, extension = extension)
    filtered_data_dict = dict()

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
        selected_concept_dict_list = apply_selection(concept_dict_list)
        # add qu_mcrae_norms
        qu_mcrae_selected_concept_dict_list = add_qumcrae_labels(\
                                                selected_concept_dict_list,\
                                                 qumcrae_property_dict)


        new_concept_dict_list = []
        for concept_dict in qu_mcrae_selected_concept_dict_list:

            word_data_to_dict(concept_dict, token_count_dict, navigli_sense_dict, \
                                onto_sense_dict, poly_dict, mipvu_dict)
            
            new_concept_dict_list.append(concept_dict)

        filtered_data_dict[property[:-9]] = new_concept_dict_list

    data_to_file(collection, filtered_data_dict, target)




if __name__ == '__main__':
    main()
