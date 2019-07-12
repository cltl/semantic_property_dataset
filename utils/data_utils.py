import os
from collections import defaultdict
import csv
import glob
import json


def load_data(collection, source, extension = None):
    property_concepts_dict = defaultdict(list)
    if extension:
        data_set_files = glob.glob(f'../data/{source}/{collection}/*_{extension}.csv')
    else:
        data_set_files = glob.glob(f'../data/{source}/{collection}/*.csv')

    for f in data_set_files:
        property = os.path.basename(f).split('.')[0]
        with open(f) as infile:
            lines = infile.read().strip().split('\n')
        if ',' in lines[0]:
            deli = ','
        elif '\t' in lines[0]:
            deli = '\t'

        if '"' in lines[0]:
            quotechar='"'
        else:
            quotechar = ''

        header = lines[0].split(deli)
        for line in lines[1:]:
            concept_dict = dict()
            line_list = line.split(deli)
            for h, item in zip(header, line_list):
                concept_dict[h.strip(quotechar)] = item.strip(quotechar)
            property_concepts_dict[property].append(concept_dict)
    return property_concepts_dict



def load_log(collection_name):

    #with open(f'../scripts_raw_data_extraction/{collection_name}.csv') as infile:
        #lines = infile.read().strip().split('\n')[1:]

    # change to log
    with open('../scripts_raw_data_extraction/log.json') as infile:
        search_command_list = json.load(infile)

    property_dict = defaultdict(list)
    for search_dict in search_command_list:
        if search_dict['collection'] == collection_name:
            property = search_dict['property_name']
            property_dict[property].append(search_dict)

    return property_dict

def data_to_file(collection, data_dict, target):

    if not os.path.isdir(f'../data/{target}'):
        os.mkdir(f'../data/{target}')

    if not os.path.isdir(f'../data/{target}/{collection}'):
        os.mkdir(f'../data/{target}/{collection}')

    for prop, concept_dict_list in data_dict.items():
        header = list(concept_dict_list[0].keys())
        #print(header)
        filepath = f'../data/{target}/{collection}/{prop}.csv'
        with open(filepath, 'w') as outfile:
            writer = csv.DictWriter(outfile, fieldnames = header)
            writer.writeheader()
            for concept_dict in concept_dict_list:
                writer.writerow(concept_dict)

def overview_to_file(collection, overview_dict_list, target):

    if not os.path.isdir(f'../data/{target}/overviews/'):
        os.mkdir(f'../data/{target}/overviews/')
    print(overview_dict_list)
    header = list(overview_dict_list[0].keys())
    with open(f'../data/{target}/overviews/{collection}.csv', 'w') as outfile:
        writer = csv.DictWriter(outfile, fieldnames = header)
        writer.writeheader()
        for od in overview_dict_list:
            writer.writerow(od)


def filter_concepts(concept_dict_list, filter = ['space_selection', 'word_in_wn?',\
                                                'word_noun_in_wn?', 'word_noun_spacy?']):

    clean_concept_dict_list = []

    for concept_dict in concept_dict_list:
        values = []
        for f in filter:
            values.append(concept_dict[f])
        if all([v == str(True) for v in values]):
            clean_concept_dict_list.append(concept_dict)

    return clean_concept_dict_list


def load_frequencies(path):

    token_count_dict = dict()
    with open(path) as infile:
        for line in infile:
            token = line.split(',')[0].strip('"')
            count = int(line.split(',')[1])
            token_count_dict[token] = count
    return token_count_dict




def load_full_lodce_data():

    f = '../data/vocab/all_lodce.csv'

    #for f in files:
    #    name = os.path.basename(f).split('.')[0]
    with open(f) as infile:
        dict_list = list(csv.DictReader(infile))

    return dict_list

def load_mrc_data(dtype):
    word_dict = dict()
    with open(f'../data/mrc_data/{dtype}.txt') as infile:
        #dict_list = list(csv.DictReader(infile))
        lines = infile.read().strip().split('\n')

    for line in lines:
        line_list = line.split(',')
        if len(line_list) == 3:
            word = ', '.join(line_list[:2])
            score = line_list[-1]
        else:
            word, score = line_list
        if score == 'no entry':
            score = None
        word_dict[word] = score


    return word_dict

def get_mrc_score(word, score_dict):

    if word in score_dict.keys():
        score = score_dict[word]
    else:
        score = None
    return score


def load_frequencies(frequency_path):

    token_count_dict = dict()
    with open(frequency_path) as infile:
        for line in infile:
            token = line.split(',')[0].strip('"')
            count = int(line.split(',')[1])
            token_count_dict[token] = count
    return token_count_dict
