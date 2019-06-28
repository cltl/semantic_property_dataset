# summarize all candidate data + information
import sys
import csv
from collections import defaultdict

sys.path.append('../utils/')
from data_utils import load_data


def all_tokens_to_file(all_tokens_dict_list, path):

    header = all_tokens_dict_list[0].keys()

    with open(path, 'w') as outfile:
        writer = csv.DictWriter(outfile, fieldnames = header)
        writer.writeheader()
        for token_dict in all_tokens_dict_list:
            writer.writerow(token_dict)

def concept_props_to_file(concept_properties_dict, path):

    with open(path, 'w') as outfile:
        outfile.write('concept-lemma, candidate for properties\n')
        for lemma, properties in concept_properties_dict.items():
            outfile.write(f'{lemma}, {" ".join(properties)}\n')

def main():
    #collection = sys.argv[1]
    source = 'data_for_concept_selection_cosine_centroid'
    #extension = 'selected'
    target = 'concepts_additional_info'

    collections = ['perceptual', 'activities', 'complex', 'parts']
    source = 'concepts_additional_info'

    target_info = ['manual_coarse_grained' ,'lemma', 'wiki_frequency',
                    'n_wn_senses', 'min_wn_sim_wup', 'poly_type', 'mipvu_met',
                    'wn_abs_conc']

    path_concepts = '../data/concepts_additional_info/all_concepts.csv'
    path_concepts_properties = '../data/concepts_additional_info/concepts_properties.csv'

    all_tokens_dict_list = []
    concept_properties_dict = defaultdict(list)

    for collection in collections:
        data_dict = load_data(collection, source)
        for prop, tokens in data_dict.items():
            for token_dict in tokens:
                new_token_dict = dict()
                lemma  = token_dict['lemma']
                concept_properties_dict[lemma].append(prop)
                new_token_dict['concept'] = token_dict['concept']
                for key in token_dict.keys():
                    if key in target_info:
                        new_token_dict[key] = token_dict[key]

                    if new_token_dict not in all_tokens_dict_list:
                        all_tokens_dict_list.append(new_token_dict)


    all_tokens_to_file(all_tokens_dict_list, path_concepts)
    concept_props_to_file(concept_properties_dict, path_concepts_properties)

if __name__ == '__main__':
    main()
