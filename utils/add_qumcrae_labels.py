

import sys
from collections import defaultdict
from collections import Counter

def load_quantified_mcrea():

    prop_concept_dict = defaultdict(dict)
    # load txt file of features for which there is a majority
    path = '../data/source_data/McRae-quantified/mcrae-quantified-majority.txt'
    with open(path) as infile:
        lines = infile.read().split('#')[-1].strip().split('\n')

    for line in lines:
        line_list = line.split('\t')
        concept = line_list[1]
        feature = line_list[2]
        annotations = line_list[3:]
        annotation_count = Counter(annotations)
        majority_voting, cnt = list(annotation_count.most_common(1))[0]

        #concept_dict = dict()
        #concept_dict[concept] = majority_voting
        prop_concept_dict[feature][concept] = majority_voting

    return prop_concept_dict


def add_qumcrae_labels(concept_dict_list, qumcrae_property_dict):

    new_concept_dict_list = []
    for concept_dict in concept_dict_list:
        concept = concept_dict['concept']
        sources  = concept_dict['sources_str'].split(' ')
        concept_dict['qumcrae_label'] = '-'
        if 'mcrae' in sources:
            #print('mcrae')
            label = concept_dict['label']
            search_terms = concept_dict['categories_str'].split(' ')

            qumcrae_dicts_search_terms = [(qumcrae_property_dict[search_term], search_term) for \
                            search_term in search_terms\
                            if search_term in qumcrae_property_dict]
            #print(len(qumcrae_dicts_search_terms))
            for qumcrae_dict, st in qumcrae_dicts_search_terms:
                #print(qumcrae_dict.keys())
                if concept in qumcrae_dict:
                    #print('found entry for ', concept)
                    concept_dict['qumcrae_label'] = label+'-'+st+'-'+qumcrae_dict[concept]
                    if concept_dict not in new_concept_dict_list:
                        new_concept_dict_list.append(concept_dict)
        else:
            if concept_dict not in new_concept_dict_list:
                new_concept_dict_list.append(concept_dict)
    return new_concept_dict_list
