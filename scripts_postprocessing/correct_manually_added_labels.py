import sys
import os
import csv
sys.path.append('../utils/')



def load_manually_added():

    with open('../data/manually_included/properties_overview_selected.csv') as infile:
        manually_included_dicts = list(csv.DictReader(infile, delimiter = '\t'))
    return manually_included_dicts

def load_crowd_input(collection):

    with open(f'../data/crowd_input/{collection}.csv') as infile:
        input_dicts = list(csv.DictReader(infile, delimiter = ','))
    return input_dicts

def corrected_crowd_input_to_file(collection, corrected_dicts):

    fieldnames = list(corrected_dicts[0].keys())
    with open(f'../data/crowd_input/{collection}.csv', 'w') as infile:
        writer = csv.DictWriter(infile, fieldnames = fieldnames)
        writer.writeheader()
        for d in corrected_dicts:
            writer.writerow(d)


def create_lookup_manually_included(manually_included_dicts):

    pair_loopup = dict()
    label_keys = ['pos', 'pos_met', 'neg', 'neg_met']
    for d in manually_included_dicts:
        property = d['property']
        for l in label_keys:
            concepts = d[l].split(' ')
            label = l.split('_')[0]
            for concept in concepts:
                pair_loopup[(property, concept)] = label
    return pair_loopup


if __name__ == '__main__':


    manually_included_dicts = load_manually_added()
    pair_loopup_manually_included = create_lookup_manually_included(manually_included_dicts)

    collections = ['perceptual', 'activities', 'parts', 'complex']

    for collection in collections:
        input_dicts = load_crowd_input(collection)

        for d in input_dicts:
            pair = (d['property'], d['lemma'])
            if pair in pair_loopup_manually_included.keys():
                correct_label = pair_loopup_manually_included[pair]
                if pair_loopup_manually_included[pair] != d['label']:
                    d['label'] = correct_label
                    d['certainty'] = 'certain'

        corrected_crowd_input_to_file(collection, input_dicts)
