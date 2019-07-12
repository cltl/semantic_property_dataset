import sys
import random
from collections import defaultdict
from collections import Counter
import math
import json
import os
import csv
from get_bins import get_polysemy_info
from get_bins import get_bins_from_distribution

sys.path.append('../utils/')
from data_utils import load_data



def load_bin_dict():

    with open('bins.json') as infile:
        bin_dict = json.load(infile)
    return bin_dict

def get_cosine_distribution(concept_dict_list):

    name = 'cosine_centroid'
    n_bins = 3
    bin_dict = get_bins_from_distribution(concept_dict_list, name, n_bins, \
                                mapping = False, restriction = None)

    return bin_dict

def get_lemmas(concept_dict_list):
    lemmas = set([d['lemma'] for d in concept_dict_list])
    return list(lemmas)


def assign_to_bin(concept_dict, bin_dict, name):

    #get_polysemy_info(concept_dict)

    if name == 'polysemy':
        concept_value = get_polysemy_info(concept_dict)
        bin = concept_value
    else:
        if concept_dict[name] != '':
            concept_value = float(concept_dict[name])
            if bin_dict[name]['mapping'] == 'log':
                concept_value = math.log(concept_value)
            for n, interval in enumerate(bin_dict[name]['bins']):
                start, end = interval
                if start <= concept_value < end:
                    bin = n
                    break
                else:
                    bin = None
        else:
            bin = None
    return bin

def collect_words_bin(concept_dict_list, bin_dict, name):

    bin_concepts_dict = defaultdict(list)
    for concept_dict in concept_dict_list:
        bin = assign_to_bin(concept_dict, bin_dict, name)
        #print('assigning word to bin: ', concept_dict['word'], bin, name)
        bin_concepts_dict[bin].append(concept_dict['lemma'])
    return bin_concepts_dict

def draw_random_sample_from_list(concept_dict_list):

    # chose a random integer (lenth is out of list index)
    selected_int = random.randint(0, len(concept_dict_list)-1)
    # get data item from list and remove selected item from list
    selected_item = concept_dict_list.pop(selected_int)

    return selected_item, selected_int

def get_bin_list(names, bin_dict, concept_dict_list):
    bin_name_dict = defaultdict(list)
    for name in names:
        #print(name)
        bin_dict_list = collect_words_bin(concept_dict_list, bin_dict, name)
        #for name, words in bin_dict_list.items():
            #print(name, words)
        #print('\n----\n')
        bin_name_dict[name].extend(list(bin_dict_list.values()))
    return bin_name_dict


def sort_concept_dicts_labels(concept_dict_list):

    label_concept_dict_lists = defaultdict(list)
    for concept_dict in concept_dict_list:
        if concept_dict['filter'] == 'True':
            #print(concept_dict['label'], concept_dict['word'])
            label_concept_dict_lists[concept_dict['label']].append(concept_dict)
    new_label_concept_dict_lists = defaultdict(list)
    for label, concept_dict_list in label_concept_dict_lists.items():
        if '/' in label:
            new_label_concept_dict_lists['pos/neg'].extend(concept_dict_list)
        else:
            new_label_concept_dict_lists[label].extend(concept_dict_list)
    return new_label_concept_dict_lists

def sample(bin_name_dict, preselected_lemmas, target_n):

    selected_lemmas = list(preselected_lemmas)
    print('number of manually preselected lemmas: ', len(selected_lemmas), selected_lemmas)
    bin_indices_dict = defaultdict(list)
    bin_word_lists_dict = defaultdict(list)

    bins_flat = []
    names = []

    for name, bins in bin_name_dict.items():
        for bin in bins:
            bins_flat.append(bin)
            names.append(name)


    while (len(selected_lemmas) < target_n) and (len(bins_flat) != 0):

        bin_name_counter = Counter()
        for n, bin_name in enumerate(zip(names, bins_flat)):
            name, bin = bin_name
            bin_name_counter[name] += 1
            if bin:
                selected_lemma, selected_int = draw_random_sample_from_list(bin)
                bin_indices_dict[name+'_'+str(bin_name_counter[name])].append(str(selected_int))


                if selected_lemma not in selected_lemmas:
                    selected_lemmas.append(selected_lemma)

            else:
                removed_list = bins_flat.pop(n)
            #print('the total number of selected lemmas is', len(selected_lemmas))
            #print('the current bin still has candidates: ', len(bin))
            #print('there are still bins: ', len(bins))
            if len(selected_lemmas) > target_n:
            #    print('reached max')
                break
            if len(bins_flat) == 0:
            #    print('no more candidates')
                break
    return selected_lemmas, bin_indices_dict


def candidates_to_file(collection, property, selected_lemmas_dict, lemma_concepts_dict):

    data_dirs = f'../data/sampled_candidates/{collection}'
    if not os.path.isdir(data_dirs):
        os.makedirs(data_dirs)

    fieldnames = list(lemma_concepts_dict.values())[0][0].keys()

    with open(f'{data_dirs}/{property}.csv', 'w') as outfile:
        writer = csv.DictWriter(outfile, fieldnames = fieldnames)
        writer.writeheader()
        for label, lemmas in selected_lemmas_dict.items():
            for lemma in lemmas:
                for concept_dict in lemma_concepts_dict[lemma]:
                    writer.writerow(concept_dict)
                #outfile.write(f'{lemma},{label}\n')

def map_lemmas_to_concepts(concept_dict_list):

    lemma_concepts_dict = defaultdict(list)

    for d in concept_dict_list:
        lemma = d['lemma']
        lemma_concepts_dict[lemma].append(d)

    return lemma_concepts_dict

def get_manually_selected_lemmas(concept_dict_list):

    selected_concept_dict_list = [d for d in concept_dict_list if \
                                'manually_included' in d['sources_str'].split(' ')]

    preselected_lemmas = set([d['lemma'] for d in selected_concept_dict_list])
    return preselected_lemmas


def sample_candidates_by_label(property, label, label_concept_dict_lists, bin_dict, names, target_n):

    selected_lemmas_dict = dict()


    concept_dict_list = label_concept_dict_lists[label]
    preselected_lemmas = get_manually_selected_lemmas(concept_dict_list)
    bin_name_dict = get_bin_list(names, bin_dict, concept_dict_list)
    #print('bin list: ', len(bins))
    selected_lemmas_dict[label], bin_indices_dict = sample(bin_name_dict, preselected_lemmas, target_n)

    if '/' in label:
        label = label.replace('/', '-')
    with open(f'replication_random_indices/{property}_{label}.csv', 'w') as outfile:
        outfile.write('name,indices\n')
        for name, indices in bin_indices_dict.items():
            outfile.write(f'{name},{" ".join(indices)}\n')

    return selected_lemmas_dict


def sample_property_candidates(property, concept_dict_list, bin_dict, names, target_n_total):

    selected_lemmas_dict = dict()
    target_n = target_n_total / 3

    label_concept_dict_lists = sort_concept_dicts_labels(concept_dict_list)
    lemma_concepts_dict = map_lemmas_to_concepts(concept_dict_list)
    bin_dict_cosine = get_cosine_distribution(concept_dict_list)
    bin_dict.update(bin_dict_cosine)

    label = 'neg'
    neg_selected_lemmas_dict = sample_candidates_by_label(property, label, label_concept_dict_lists, bin_dict, names, target_n)
    selected_lemmas_dict.update(neg_selected_lemmas_dict)

    label = 'pos'
    pos_selected_lemmas_dict = sample_candidates_by_label(property, label, label_concept_dict_lists, bin_dict, names, target_n)
    selected_lemmas_dict.update(pos_selected_lemmas_dict)


    # if we do not have enough concepts with a likely label, select get difference from unlabeled
    status = len(selected_lemmas_dict['neg']) + len(selected_lemmas_dict['pos'])
    print('status', status)
    target_n_posneg = target_n_total - status
    print('target pos/neg ', target_n_posneg)
    label = 'pos/neg'

    posneg_selected_lemmas_dict = sample_candidates_by_label(property, label, label_concept_dict_lists, bin_dict, names, target_n_posneg)
    selected_lemmas_dict.update(posneg_selected_lemmas_dict)

    print(len(set(selected_lemmas_dict['neg'])), selected_lemmas_dict['neg'][:3])
    print(len(set(selected_lemmas_dict['pos'])), selected_lemmas_dict['pos'][:3])
    print(len(set(selected_lemmas_dict['pos/neg'])), selected_lemmas_dict['pos/neg'][:3])

    return selected_lemmas_dict




def main():

    collection = sys.argv[1]
    target_property = sys.argv[2]
    target_n_total = int(sys.argv[3])

    source = 'concepts_additional_info'
    names = ['wiki_frequency', 'cosine_centroid', 'polysemy', 'conc', 'fam', 'aoa']
    bin_dict = load_bin_dict()

    property_concept_dict_list = load_data(collection, source)


    for property, concept_dict_list in property_concept_dict_list.items():
        if target_property != 'None':
            if property == target_property:
                label_concept_dict_lists = sort_concept_dicts_labels(concept_dict_list)
                lemma_concepts_dict = map_lemmas_to_concepts(concept_dict_list)
                bin_dict_cosine = get_cosine_distribution(concept_dict_list)
                bin_dict.update(bin_dict_cosine)

                selected_lemmas_dict = sample_property_candidates(property, concept_dict_list, bin_dict, names, target_n_total)

                candidates_to_file(collection, property, selected_lemmas_dict, lemma_concepts_dict)
        else:
            label_concept_dict_lists = sort_concept_dicts_labels(concept_dict_list)
            lemma_concepts_dict = map_lemmas_to_concepts(concept_dict_list)
            selected_lemmas_dict = dict()
            bin_dict_cosine = get_cosine_distribution(concept_dict_list)
            bin_dict.update(bin_dict_cosine)

            selected_lemmas_dict = sample_property_candidates(property, concept_dict_list, bin_dict, names, target_n_total)

            candidates_to_file(collection, property, selected_lemmas_dict, lemma_concepts_dict)



if __name__ == '__main__':
    main()


# Factors:

# distance to centroid: even distribution
# frequency: even distribution
# pos, neg, pos/neg
# metaphor_mipvu
# homonyms
# polysemous words
# shift between abstract and concrete
# manually selected words have to be in the dataset
