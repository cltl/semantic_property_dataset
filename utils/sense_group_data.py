import sys
import os
import glob
from collections import defaultdict
from nltk.corpus import wordnet as wn
import xml.etree.ElementTree as ET
import csv


def load_frequencies(path):

    token_count_dict = dict()
    with open(path) as infile:
        for line in infile:
            token = line.split(',')[0].strip('"')
            count = int(line.split(',')[1])
            token_count_dict[token] = count
    return token_count_dict


def get_navigly_clusters(path):

    word_sense_dict = defaultdict(list)

    with open(path) as infile:
        lines = infile.read().split('\n')

    for line in lines:
        line_list = line.split(' ')
        words = [sense_key.split('%')[0] for sense_key in line_list]
        for word in set(words):
            word_sense_dict[word].append(line_list)
            if word == 'kingfisher':
                print('kingfisher', line_list)
    return word_sense_dict


def parse_onto_xml(xmlfile):

    # https://docs.python.org/3/library/xml.etree.elementtree.html

    word_pos = os.path.basename(xmlfile).split('.')[0]
    #print(word_pos)
    word_tree = ET.parse(xmlfile)


    root = word_tree.getroot()
    elements = root.getchildren()
    senses = [el for el in root.getchildren() if el.tag == 'sense']

    data = defaultdict(list)

    for s in senses:
        data['name'].append(s.attrib['name'])
        mappings = s.find('mappings')
        wn_mappings = []
        for mapping in mappings:
            if mapping.tag == 'wn':
                version = mapping.attrib['version']
                senses = mapping.text
                wn_mappings.append(version+'_'+str(senses))

        data['senses'].append(wn_mappings)

    return word_pos, data


def load_mipvu_metaphors():

    mipvu_dict = dict()

    with open('../scripts_lexical_information/wordlists/mipvu_metaphor_words.csv') as infile:
        dict_list = list(csv.DictReader(infile))

    for d in dict_list:
        mipvu_dict[d['word']] = d['annotations']
    return mipvu_dict


def load_metonymy_entities(path):
    with open(path) as infile:
        vocab = set(infile.read().strip().split('\n'))
    return vocab


def get_ontonotes_sense_dict(dir_path):

    word_sense_dict = dict()
    onto_mapping_files = glob.glob(dir_path+'*.xml')
    for xmlfile in onto_mapping_files:
        word_pos, data = parse_onto_xml(xmlfile)
        word_sense_dict[word_pos] = data

    return word_sense_dict

def get_onto_senses(lemma, onto_sense_dict):
    onto_senses = []
    for lemma_pos in [lemma+'-v', lemma+'-n']:
        if lemma_pos in onto_sense_dict.keys():
            senses = onto_sense_dict[lemma_pos]['senses']
            onto_senses.extend(senses)
    return onto_senses
