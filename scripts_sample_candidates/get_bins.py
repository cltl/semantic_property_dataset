import sys
import os
import csv
import numpy as np
import matplotlib.pyplot as plt
import math
import json
from collections import Counter

def load_vocab(path):

    with open(path) as infile:
        reader = csv.DictReader(infile)
        dict_list = list(reader)
    return dict_list



def get_bins_from_distribution(concept_dict_list, name, n_bins, \
                            mapping = False, restriction = None):

    if mapping == False:
        if restriction == None:
            values = [float(d[name]) for d in concept_dict_list if d[name] != '']
        else:
            print('restricting data')
            values = [float(d[name]) for d in concept_dict_list if \
                    (d[name] != '') and (float(d[name]) != restriction)]
    elif mapping == 'log':
        print('taking the log')
        if restriction == None:
            values = [math.log(float(d[name])) for d in concept_dict_list if d[name] != '']
        else:
            print('taking log and restricting data')
            values = [math.log(float(d[name])) for d in concept_dict_list if \
                    (d[feature] != '') and (float(d[name]) != restriction)]

    frequencies, bin_intervals = np.histogram(values, bins = n_bins)
    print(bin_intervals)
    print(frequencies)
    bin_dict = bins_to_dict(name, frequencies, bin_intervals, mapping,\
                            restriction, 'distribution')
    #plt.hist(values, bins = n_bins)
    #plt.gca().set(title='Frequency Histogram', ylabel='frequency', xlabel=feature)
    #plt.show()
    return bin_dict



def bins_to_dict(name, frequencies, bin_intervals, mapping, restriction, bin_type):

    bin_dict = dict()
    bin_dict[name] =  {
    'type' : bin_type,
    'mapping' : mapping,
    'bins' : [],
    'frequencies' : [int(f) for f in list(frequencies)],
    'restriction' : restriction
    }


    for n, i in enumerate(bin_intervals):
        if n != len(bin_intervals) - 1:
            bin_dict[name]['bins'].append((i, bin_intervals[n+1]))
        else:
            break
    return bin_dict




def str_to_bool(string):

    if string == 'True':
        return True
    elif string == 'False':
        return False
    elif string == 'None':
        return None
    else:
        print('input not converted')
        return string


def get_polysemy_info(concept_dict):

    word = concept_dict['word']
    mipvu_met = concept_dict['mipvu']
    polysemy_type = concept_dict['polysemy_type']

    if polysemy_type == 'mon':
        poly = 'mon'
    elif polysemy_type == 'homonyms_also_same_pos':
        poly = 'homonym'
    elif mipvu_met == 'True':
        poly = 'met'
    # Possibly metonymy if not metaphor and not homonym
    # caveat: the metaphor annotations are not exhaustive
    elif polysemy_type == 'poly':
        poly = 'poly_metonymy'
    else:
        poly = None
    return poly


def get_polysemy_bins(concept_dict_list):

    bin_dict = dict()
    bin_dict['polysemy'] = {
    'type' : 'categories',
    'mapping' : None,
    'bins' : [],
    'frequencies' : [],
    'restriction' :  None,
    }

    polysemy_counter = Counter()

    for d in concept_dict_list:
        polysemy_info = get_polysemy_info(d)
        polysemy_counter[polysemy_info] += 1

    for polysemy_info, c in polysemy_counter.items():
        if polysemy_info != None:
            bin_dict['polysemy']['bins'].append(polysemy_info)
            bin_dict['polysemy']['frequencies'].append(c)

    return bin_dict



def main():
    #feature = sys.argv[1]
    #n_bins = int(sys.argv[2])
    #log = str_to_bool(sys.argv[3])
    #restriction = str_to_bool(sys.argv[4])

    #all_concepts_path = '../data/concepts_additional_info/all_concepts.csv'
    vocab_path = '../data/vocab/all_lodce_mrc.csv'
    concept_dict_list = load_vocab(vocab_path)

    all_bins_dict = dict()

    name = 'wiki_frequency'
    n_bins = 3
    mapping = 'log'
    restriction = None

    bin_dict_freq = get_bins_from_distribution(concept_dict_list, name, n_bins, \
                                mapping = mapping, restriction = restriction)

    name = 'conc'
    n_bins = 3
    mapping = None
    restriction = None

    bin_dict_conc = get_bins_from_distribution(concept_dict_list, name, n_bins, \
                                mapping = False, restriction = None)

    name = 'fam'
    n_bins = 3
    mapping = None
    restriction = None

    bin_dict_fam = get_bins_from_distribution(concept_dict_list, name, n_bins, \
                                mapping = False, restriction = None)


    name = 'aoa'
    n_bins = 3
    mapping = None
    restriction = None

    bin_dict_aoa = get_bins_from_distribution(concept_dict_list, name, n_bins, \
                                mapping = False, restriction = None)


    bin_dict_poly = get_polysemy_bins(concept_dict_list)

    all_bins_dict.update(bin_dict_freq)
    all_bins_dict.update(bin_dict_conc)
    all_bins_dict.update(bin_dict_fam)
    all_bins_dict.update(bin_dict_aoa)
    all_bins_dict.update(bin_dict_poly)


    with open("bins.json", "w") as outfile:
        json.dump(all_bins_dict, outfile)


if __name__ == '__main__':
    main()
