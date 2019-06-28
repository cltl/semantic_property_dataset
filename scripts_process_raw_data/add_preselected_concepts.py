import os
import glob
import sys
import csv
from collections import defaultdict

sys.path.append('../utils/')


from data_utils import load_data
from data_utils import data_to_file



def load_manually_selected():

    path = '../data/manually_included/properties_overview_selected.csv'
    property_concept_dict = defaultdict(list)

    with open(path) as infile:
        dict_list = list(csv.DictReader(infile, delimiter = '\t'))

    for d in dict_list:
        property = d['property']
        for label in ['pos', 'pos_met', 'neg', 'neg_met']:
            for concept in d[label].split(' '):
                concept_dict = dict()
                concept_dict['concept'] = concept
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
        word_dict_dict[d['concept']] = d
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
            word_dict['sources_str'] = word_dict['sources_str']+' '+'manually_included'
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
    source = 'data_extracted_sorted'
    target = 'data_extracted_sorted'


    data_dict = load_data(collection, source)
    data_dict_manually_selected = load_manually_selected()
    extended_data_dict = dict()

    for property, concept_dict_list in data_dict.items():
        concept_dict_list_manually_selected = data_dict_manually_selected[property]
        merged_dict_list = merge_with_collected_concepts(concept_dict_list,concept_dict_list_manually_selected)
        extended_data_dict[property] = merged_dict_list

    data_to_file(collection, extended_data_dict, target)


if __name__ == '__main__':
    main()
