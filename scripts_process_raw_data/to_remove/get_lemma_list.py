import sys
import os
import glob

from collections import defaultdict

sys.path.append('../utils/')
from data_utils import load_data
from data_utils import data_to_file


def main():

    lemmas = set()

    word_list_dir = 'wordlists'
    if not os.path.isdir(word_list_dir):
        os.mkdir(word_list_dir)


    collections = ['perceptual', 'activities', 'complex', 'parts']
    source = 'concepts_additional_info'

    for collection in collections:
        data_dict = load_data(collection, source)

        for property, concept_dict_list in data_dict.items():
            for concept_dict in concept_dict_list:
                lemma = concept_dict['lemma']
                lemmas.add(lemma)

    with open(f'{word_list_dir}/all_lemmas.txt', 'w') as outfile:
        outfile.write('\n'.join(lemmas))

if __name__ == '__main__':
    main()
