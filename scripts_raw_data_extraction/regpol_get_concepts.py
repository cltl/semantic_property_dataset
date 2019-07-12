import glob
import os
from collections import defaultdict

def load_dataset(shift):

    if shift == 'artifact-information':
        name = 'artinfo'
    elif shift == 'animal-meat':
        name = 'animeat'
    elif shift == 'container-content':
        name = 'cont'
    elif shift == 'location-organization':
        name = 'locorg'
        print(name)
    elif shift == 'process-result':
        name = 'procres'

    path = '../data/source_data/regpol/en_'+name+'.csv'

    with open(path) as infile:
        lines = infile.read().strip().split('\n')

    lemma_annotations_dict = defaultdict(set)


    coders = []

    if '\t' in lines[0]:
        for item in lines[0].split('\t'):
            if item.startswith('C'):
                coders.append(item)

    elif ',' in lines[0]:

        for item in lines[0].split(','):
            if item.startswith('C'):
                coders.append(item)
    number_annotations = len(coders)

    for line in lines[1:]:
        if '\t' in line:
            line_list = [item for item in line.strip().split('\t') if item != '']
        elif ',' in line:
            line_list = [item for item in line.strip().split(',') if item != '']

        if len(line_list) > 1:
            lemma = line_list[2]
            annotations = set(line_list[-number_annotations:])

            lemma_annotations_dict[lemma].update(annotations)

    return lemma_annotations_dict


def get_concepts_per_sense(lemma_annotation_dict):

    sense_dict = defaultdict(list)

    all_senses = sorted(set([sense for senses in lemma_annotation_dict.values()\
                            for sense in senses]))


    if 'DOT' in all_senses:
        all_senses.remove('DOT')




    for sense in all_senses:
        sense_dict[sense]

    sense_shift = '-'.join(all_senses)
    #print(sense_shift)

    for lemma, annotations in lemma_annotation_dict.items():

        # DOT annotation should always be counted as ambiguous
        if 'DOT' in annotations:
            sense = sense_shift
        else:
            sense = '-'.join(sorted(annotations))


        sense_dict[sense].append(lemma)

    return sense_dict





def collect_concepts_regpol(sense):

    shifts_dict = {
    'artifact-information': ['ART', 'INFO'],
    'animal-meat': ['ANIMAL', 'MEAT'],
    'container-content': ['CONTAINER','CONTENT'],
    'location-organization':['LOC', 'ORG'],
    'process-result': ['PROC', 'RES']
    }

    if sense in shifts_dict.keys():
        target_shift = sense
        sense_key = '-'.join(sorted(shifts_dict[target_shift]))

    else:
        for shift in shifts_dict.keys():
            if sense in shift.split('-'):
                target_shift = shift
                index_sense = shift.split('-').index(sense)
                sense_key = shifts_dict[target_shift][index_sense]
                break


    lemma_annotation_dict = load_dataset(target_shift)
    sense_dict = get_concepts_per_sense(lemma_annotation_dict)


    concepts = sense_dict[sense_key]

    return concepts, []


def main():

    sense = 'process-result'

    concepts, selection_list = collect_concepts_regpol(sense)

    print(concepts)


if __name__ == '__main__':
    main()
