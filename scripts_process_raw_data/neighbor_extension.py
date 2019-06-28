import os
import glob
import sys
import csv
from collections import defaultdict

sys.path.append('../utils/')

from load_models import load_model
from load_models import create_centroid
from load_models import get_nearest_neighbors
from load_models import represent
from load_models import get_cosine

from data_utils import load_data
from data_utils import data_to_file
from data_utils import overview_to_file


def remove_oov(dsm_vocab, concept_dict_list):
    clean_concept_list = [cd for cd in concept_dict_list if cd['concept'] in dsm_vocab]
    return clean_concept_list


def get_get_candidate_neighbors(model, concept_list_pos, n = 200):

    matrix = []
    for concept in concept_list_pos:
        vec = represent(model, concept)
        matrix.append(vec)
    if matrix:
        centroid = create_centroid(matrix)
        neighbors = get_nearest_neighbors(model, centroid, n)
        # get distance to other concepts
    else:
        neighbors = []
        centroid = []


    return neighbors, centroid


def get_cosines_to_centroid(model, concepts, centroid):

    concept_cosine_dict = dict()
    for concept in concepts:
        if centroid != []:
            vec_concept = represent(model, concept)
            cos = get_cosine(vec_concept, centroid)
            concept_cosine_dict[concept] = cos
        else:
            concept_cosine_dict[concept] = '-'

    return concept_cosine_dict


def main():
    collection = sys.argv[1]
    #target_property = sys.argv[2]
    source = 'data_extracted_sorted'
    target = 'data_for_concept_selection_cosine_centroid'

    dsm_path = '../../../Data/dsm/wikipedia_full/sgns_pinit1/sgns_pinit1/sgns_rand_pinit1'
    model = load_model(dsm_path, 'sgns')
    model_creation_type, matrix, wi_dict, dsm_vocab = model

    data_dict = load_data(collection, source)
    extended_data_dict = dict()

    overview_dict_list = []

    for property, concept_dict_list in data_dict.items():
        #if property == target_property:
        print(property)
        clean_concept_dict_list = remove_oov(dsm_vocab, concept_dict_list)
        new_concept_dict_list = []

        n = 200
        # get neighbors of positive concept centroid:
        concepts_pos = [cd['concept'] for cd in clean_concept_dict_list if cd['label'] == 'pos']
        concepts = [cd['concept'] for cd in clean_concept_dict_list]
        neighbors, centroid = get_get_candidate_neighbors(model, concepts_pos, n = n)
        concept_cosine_dict = get_cosines_to_centroid(model, concepts, centroid)
        #print(len(concept_cosine_dict.keys()))
        # get cosines to centroid of all concepts

        # use nltk pos tagging to select nouns only:
        if neighbors:
            neighbors_clean = [(c, n) for c, n in neighbors if n not in concepts]
            #neighbors_nouns = select_nouns_pos(neighbors_clean)
            for cosine, neighbor in neighbors_clean:
                neighbor_dict = dict()
                neighbor_dict['concept'] = neighbor
                neighbor_dict['label'] = 'neg/pos'
                neighbor_dict['certainty'] = 'not_certain'
                neighbor_dict['sources_str'] = 'wikipedia_sgns_model'
                neighbor_dict['categories_str'] = 'neighbors'+'-'+str(n)
                neighbor_dict['cosine_centroid'] = str(cosine)
                new_concept_dict_list.append(neighbor_dict)

        for cd in  clean_concept_dict_list:
            cos = concept_cosine_dict[cd['concept']]
            cd['cosine_centroid'] = str(cos)
            print(cd['concept'], cd['cosine_centroid'])
            new_concept_dict_list.append(cd)


        sorted_concept_dict_list = sorted([(cd['cosine_centroid'], cd) for cd \
                                    in new_concept_dict_list if cd['cosine_centroid'] != '-'])
        if sorted_concept_dict_list:
            extended_data_dict[property] = [cd for cosine, cd in sorted_concept_dict_list]
            print(property, len(extended_data_dict[property]))
        else:
            print('no concepts in the model vocab: ', property)

        data_to_file(collection, extended_data_dict, target)






if __name__ == '__main__':
    main()
