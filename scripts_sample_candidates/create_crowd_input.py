import glob
from collections import defaultdict
from collections import Counter
import sys
import csv
import os

sys.path.append('../utils/')
from data_utils import load_data


#### new code ####

def get_lemma_concept_dict(concept_dict_list):
    lemma_concepts_dict = defaultdict(list)
    [lemma_concepts_dict[d['lemma']].append(d) for d in concept_dict_list]
    return lemma_concepts_dict


def find_label_certainty(concept_dict_list):
    lemma_concepts_dict = get_lemma_concept_dict(concept_dict_list)
    final_lemma_dict_list = []
    for lemma, concepts_list in lemma_concepts_dict.items():
        lemma_dict = dict()
        lemma_dict['lemma'] = lemma
        labels = []
        sources = []
        for d in concepts_list:
            sources.append(d['sources_str'])
            if d['certainty'] == 'certain':
                labels.append(d['label'])
                certainty = 'certain'
                break
            elif d['qumcrae_label'] != '-':
                #print(d['qumcrae_label'])
                #print(d['label'])
                labels.append(d['label'])
                certainty = 'certain'
                break
        if labels == []:
            for d in concepts_list:
                labels.append(d['label'])
                certainty = 'not_certain'

        if len(set(labels)) == 1:
            lemma_dict['label'] = list(set(labels))[0]
            lemma_dict['certainty'] = certainty
        else:
            lemma_dict['label'] = '/'.join(sorted(list(set(labels))))
            lemma_dict['certainty'] = 'uncertain'
        lemma_dict['sources_str'] = ' '.join(sources)
        final_lemma_dict_list.append(lemma_dict)

    return final_lemma_dict_list



def candidates_to_file(property_lemma_dict, collection):
    path = f'../data/crowd_input/{collection}.csv'
    fieldnames = ['property']

    fieldnames.extend(list(property_lemma_dict.values())[0][0].keys())

    with open(path, 'w') as outfile:
        outfile.write(','.join(fieldnames)+'\n')
        for property, lemma_dict_list in property_lemma_dict.items():
            for d in lemma_dict_list:
                line = [property]
                line.extend([d[header] for header in fieldnames[1:]])
                outfile.write(','.join(line)+'\n')

def overview_to_file(overview_dict_list, collection):

    path = f'../data/crowd_input/overview_{collection}.csv'
    fieldnames = overview_dict_list[0].keys()

    with open(path, 'w') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        for d in overview_dict_list:
            writer.writerow(d)



def main():
    collection = sys.argv[1]
    source = 'sampled_candidates'
    #target = 'annotation_task_input'
    data_dict = load_data(collection, source)
    property_lemma_dict = dict()
    overview_dict_list = []

    for property, concept_dict_list in data_dict.items():
        #print(property)
        final_lemma_dict_list = find_label_certainty(concept_dict_list)
        property_lemma_dict[property] = final_lemma_dict_list
        #prop_counter[property] = len(final_lemma_dict_list)
        overview_dict = dict()

        overview_dict['property'] = property
        overview_dict['pos'] = len([d for d in final_lemma_dict_list if d['label'] == 'pos'])
        overview_dict['neg'] = len([d for d in final_lemma_dict_list if d['label'] == 'neg'])
        overview_dict['pos/neg'] = len([d for d in final_lemma_dict_list if '/' in d['label']])
        overview_dict['total'] = len(final_lemma_dict_list)
        overview_dict_list.append(overview_dict)


    candidates_to_file(property_lemma_dict, collection)
    overview_to_file(overview_dict_list, collection)


if __name__ == '__main__':
    main()
