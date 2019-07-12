import sys
from collections import defaultdict


def load_mcrae():

    with open('../data/source_data/McRae-norms/concepts_features.csv') as infile:
        lines = infile.read().strip().split('\n')

    prop_concept_dict = defaultdict(list)

    for line in lines[1:]:
        line_list = line.strip().split('\t')
        if len(line_list) >1:
            concept = line_list[0]
            property = line_list[1]

            prop_concept_dict[property].append(concept)

    return prop_concept_dict


def collect_concepts_mcrae(target_property):

    prop_concept_dict = load_mcrae()
    selection_list = []

    if target_property in prop_concept_dict.keys():
        concepts = prop_concept_dict[target_property]
    else:
        concepts = []

    return concepts, selection_list




def main():

    prop_concept_dict = load_mcrae()
    prop_counter = 0

    number_concepts_properties = [(len(concepts), prop) for prop, concepts in prop_concept_dict.items()]

    for n_concepts, prop in sorted(number_concepts_properties, reverse = True):
        print(prop, n_concepts)
        if n_concepts < 10:
            break

if __name__ == '__main__':
    main()
