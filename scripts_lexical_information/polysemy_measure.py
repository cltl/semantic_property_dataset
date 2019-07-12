import sys
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
from collections import defaultdict
from add_av_wup_distances import load_wup_distances
from statistics import stdev

sys.path.append('../utils/')
from wordnet_data import get_all_wup_sims
from wordnet_data import get_synsets
from data_utils import load_full_ldoce_data


def get_lowest_sim_per_word(word_wup_sims):

    word_wup_dict = defaultdict(list)

    word_min_wup_sim_dict = dict()

    for word, sim in word_wup_sims:
        word_wup_dict[word].append(sim)

    for word, sims in word_wup_dict.items():
        min_sim = min(sims)
        word_min_wup_sim_dict[word] = min_sim

    return word_min_wup_sim_dict

def plot_distribution(data_points_list, name, n_bins):

    #values = [float(d[feature]) for d in ldoce_data_dict_list if d[feature] != 'None']
    frequency, bins = np.histogram(data_points_list, bins =  n_bins )

    plt.hist(data_points_list, bins = bins)
    plt.gca().set(title='Frequency Histogram', ylabel='frequency', xlabel=name)
    plt.show()

    return bins, frequency

def bins_to_file(wup_bins, frequency, name):

    with open(f'bins/{name}.txt', 'w') as outfile:
        outfile.write('scale = linear 3\n')
        for b, f in zip(wup_bins, frequency):
            outfile.write(f'{str(b)},{str(f)}\n')



def get_distriution(data_points, n_bins, name):


    bins, frequency = plot_distribution(data_points, name, n_bins)
    print(bins)
    print(frequency)

    bins_to_file(bins, frequency, name)


def load_bins(name):

    with open(f'bins/{name}.txt') as infile:
        lines = infile.read().strip().split('\n')

    bins = []
    boundaries = []
    for line in lines[1:]:
        bin, frequ = line.split(',')
        bins.append(bin)

    return bins

def sort_to_bins(bins, word_sim_tuples):

    word_bin_dict = defaultdict(list)
    # go from highest to lowest bin
    bins.reverse()
    for w, sim in word_sim_tuples:
        # ignore lowest boundary
        for n, b in enumerate(bins):
            if float(sim) > float(b):
                word_bin_dict[w].append(n)
                break
    return word_bin_dict




def load_abs_conc_predictions(data_dict_list):

    predictions_dict = dict()

    for d in data_dict_list:
        word = d['word']
        abs_conc = d['wn-abs-conc']
        mipvu_met = d['mipvu']

        if abs_conc == 'abs-conc':
            prediction_dict[word] = 1
        elif (abs_conc == 'conc') or (abs_conc == 'abs'):
            prediction_dict[word] = 0
        else:
            prediction_dict[word] = None
    return prediction_dict


def find_truth_from_data(data_dict_list, noun = True):

    truth_dict = defaultdict(list)

    for d in data_dict_list:
        word = d['word']
        mipvu_met = d['mipvu']
        polysemy_type = d['polysemy_type']

        if polysemy_type == 'mon':
            truth_dict[word] = 'mon'
        elif polysemy_type == 'homonyms_also_same_pos':
            truth_dict[word] = 'homonym'

        elif mipvu_met == 'True':
            truth_dict[word] = 'met'

        # Possibly metonymy if not metaphor and not homonym
        # caveat: the metaphor annotations are not exhaustive
        elif polysemy_type == 'poly':
            truth_dict[word] = 'poly_metonymy'

    if noun == True:
        noun_truth_dict = dict()
        for word, label in truth_dict.items():
            noun_truth_dict[word] = label+'_n'
        return noun_truth_dict
    else:
        return truth_dict



def load_distance_predictions(word_bin_dict, target_bin):

    prediction_dict = dict()
    print('target bin:', target_bin)

    for word, bins in word_bin_dict.items():
        if target_bin in bins:
            prediction_dict[word] = 1
        else:
            prediction_dict[word] = 0
            # print(bins)

    return prediction_dict




def evaluate(prediction_dict, truth_dict, feature, target):

    eval_dict = Counter()
    vocab = prediction_dict.keys()
    for word in vocab:
        if (word in truth_dict.keys()):
            p = prediction_dict[word]
            t = truth_dict[word]
            #print(p, t)
            if (p != None) and (t != None):

                if p == t == 1:
                    eval_dict['tp'] += 1
                elif p == t == 0:
                    eval_dict['tn'] += 1
                elif (p == 1) and (t == 0):
                    eval_dict['fp'] += 1
                elif (p == 0) and (t == 1):
                    eval_dict['fn'] += 1
    print(eval_dict)
    precision = eval_dict['tp'] / (eval_dict['tp'] + eval_dict['fp'])
    recall = eval_dict['tp'] / (eval_dict['tp'] + eval_dict['fn'])
    f1 = 2* ( (precision * recall)/(precision + recall))

    print(f'{feature} in wordnet predicts {target} with:')
    print(f'Precision: {precision}')
    print(f'Recall: {recall}')
    print(f'F1: {f1}')

def truth_to_file(truth_dict, noun = True):

    word_list_dict = defaultdict(list)

    for word, label in truth_dict.items():
        word_list_dict[label].append(word)

    vocab = set()
    for label, words in word_list_dict.items():
        with open(f'evaluation_polysemy_measure/{label}.txt', 'w') as outfile:
            outfile.write('\n'.join(words))
            vocab.update(set(words))

    if noun == True:
        vocab_path = 'evaluation_polysemy_measure/vocab_n.txt'
    else:
        vocab_path = 'evaluation_polysemy_measure/vocab.txt'

    with open(vocab_path, 'w') as outfile:
        outfile.write('\n'.join(vocab))

def load_truth(label):

    truth_dict = dict()

    with open(f'evaluation_polysemy_measure/vocab.txt') as infile:
        for word in infile.read().split('\n'):
            truth_dict[word] = 0
    with open(f'evaluation_polysemy_measure/{label}.txt') as infile:
        for word in infile.read().split('\n'):
            truth_dict[word] = 1

    return truth_dict

def split_truth_in_dev_test(truth_dict, noun = True):

    word_list_dict = defaultdict(list)

    for word, label in truth_dict.items():
        word_list_dict[label].append(word)

    vocab_test = set()
    vocab_dev = set()
    for label, words in word_list_dict.items():
        n = len(words)
        # 70-20 split
        n_dev = int(n * 0.7)
        dev_words = words[:n_dev]
        test_words = words[n_dev:]
        with open(f'evaluation_polysemy_measure/{label}_test.txt', 'w') as outfile:
            outfile.write('\n'.join(test_words))
            vocab_test.update(set(test_words))
        with open(f'evaluation_polysemy_measure/{label}_dev.txt', 'w') as outfile:
            outfile.write('\n'.join(dev_words))
            vocab_dev.update(set(dev_words))
    if noun == True:
        vocab_path = 'evaluation_polysemy_measure/vocab_n'
    else:
        vocab_path = 'evaluation_polysemy_measure/vocab'
    with open(vocab_path+'_dev.txt', 'w') as outfile:
        outfile.write('\n'.join(vocab_dev))
    with open(vocab_path+'_test.txt', 'w') as outfile:
        outfile.write('\n'.join(vocab_test))




def distribution_wup_sim_sum():
    word_wup_sims_dict = defaultdict(list)
    for word, sim in words_wup_sims:
        word_wup_sims_dict[word].append(float(sim))

    data_points = [sum(sims) for word, sims in word_wup_sims_dict.items()]
    print(data_points[:5])
    name = 'wup_sims_sum'
    n_bins = 4
    get_distriution(data_points, n_bins, name)


def evaluate_bin_based_measure():


    data_dict_list = load_full_lodce_data()
    words_wup_sims = load_wup_distances()

    lowest_wup_sim = get_lowest_sim_per_word(words_wup_sims)
    data_points = [float(sim) for word, sim in lowest_wup_sim.items()]
    name = 'lowest_wup_sim'
    n_bins = 4
    get_distriution(data_points, n_bins, name)


    #data_points = [float(sim) for word, sim in words_wup_sims]
    #print(data_points[:5])
    #name = 'wup_sims'
    #n_bins = 4
    #get_distriution(data_points, n_bins, name)

    #data_points = [float(d['av_wup_sim']) for d in data_dict_list if d['av_wup_sim'] != '']
    #print(data_points[:5])
    #name = 'av_wup_sims'
    #n_bins = 4
    #get_distriution(data_points, n_bins, name)

    #data_points = [(1 - float(d['av_wup_sim'])) * int(d['n_synsets']) for d in data_dict_list if d['av_wup_sim'] != '']
    #print(data_points[:5])
    #name = 'av_wup_sims_by_n_synsets'
    #n_bins = 4
    #get_distriution(data_points, n_bins, name)

    bins = load_bins(name)
    #from high to low similarity (i.e. from monosemy to homonymy)

    #print(bins)

    word_sim_tuples = [(d['word'], float(d['min_wup_sim'])) for d in data_dict_list if d['min_wup_sim'] != 'None']

    word_bin_dict = sort_to_bins(bins, word_sim_tuples)


    bin_words_dict = defaultdict(list)

    for word, bins in word_bin_dict.items():
        # only a single bin possible
        print(word, bins)
        bin = bins[0]
        bin_words_dict[bin].append(word)

    # predict monosemy :
    targets = ['homonym', 'met', 'poly_metonymy', 'mon']
    target_bins = [3, 2, 1, 0]
    for target, target_bin in zip(targets, target_bins):
        target_words = bin_words_dict[target_bin]
        vocab = load_truth('vocab')

        tuple_list = [(word, 0) if word not in target_words else (word, 1) for word in vocab.keys() ]
        prediction_dict = dict(tuple_list)
        truth_dict = load_truth(target)
        #print(mon_truth_dict)

        print('-------')
        print('evaluating', target)
        evaluate(prediction_dict, truth_dict, name, target)

def get_polysemy_indicators(data_dict_list, noun = False):

    print(len(data_dict_list), 'all words')
    print('noun', noun)
    if noun == True:
        [data_dict_list.remove(d) for d in data_dict_list if d['wn_noun'] == 'False']
    print(len(data_dict_list), 'nouns only')
    truth_dict = find_truth_from_data(data_dict_list, noun = noun)
    truth_to_file(truth_dict, noun = noun)
    #truth_dict = find_truth_from_data(data_dict_list)
    #split_truth_in_dev_test(truth_dict)
    if noun == True:
        targets = ['mon_n', 'poly_metonymy_n', 'met_n', 'homonym_n']
    else:
        targets = ['mon', 'poly_metonymy', 'met', 'homonym']
    targets.reverse()

    word_sim_dict = dict()

    word_sim_dict['cos'] = [(d['word'], float(d['av_cos_mon_synonyms_to_word'])) for d\
                        in data_dict_list if not d['av_cos_mon_synonyms_to_word'].startswith('OO')]
    word_sim_dict['min_wup'] = [(d['word'], float(d['min_wup_sim'])) for d in data_dict_list if d['min_wup_sim'] != 'None']
    word_sim_dict['av_wup'] = [(d['word'], float(d['av_wup_sim'])) for d in data_dict_list if d['av_wup_sim'] != ('')]
    word_sim_dict['n_syns'] = [(d['word'], float(d['n_synsets'])) for d in data_dict_list if int(d['n_synsets']) != 0]
    word_sim_dict['wiki_freq'] = [(d['word'], int(d['wiki_frequency'])) for d in data_dict_list if d['wiki_frequency'] != 'OOV']

    abs_conc_tuples = [(d['word'], d['wn-abs-conc']) for d in data_dict_list if (d['wn-abs-conc']).startswith('abs-conc') ]
    abs_conc_oov = [(d['word'], d['wn-abs-conc']) for d in data_dict_list if (d['wn-abs-conc']) == '-' ]
    print('no annotation for abs conc', len(abs_conc_oov))
    #word_sim_dict = dict(word_sim_tuples)

    for name, sim_tuples in word_sim_dict.items():
        print(name)
        word_sim_dict = dict(sim_tuples)

        for target in targets:
            truth_words = load_truth(target)
            pos_words = [w for w, l in truth_words.items() if l == 1]
            #vocab = load_truth('vocab_dev')

            sims = [word_sim_dict[word] for word in pos_words if word in word_sim_dict.keys()]
            av_sims = round(sum(sims)/len(sims), 2)
            print(f'{av_sims} ({round(stdev(sims), 2)})\t {target}')

            # percentage of abs-conc-shift
            #shifts = len([word_sim_dict[word] for word in pos_words if word in word_sim_dict.keys()])
            #percentage = shifts/len(pos_words)
    for target in targets:
        abs_conc_dict = dict(abs_conc_tuples)
        oov_dict = dict(abs_conc_oov)
        truth_words = load_truth(target)
        pos_words = [w for w, l in truth_words.items() if l == 1]
        #vocab = load_truth('vocab_dev')

        # percentage of abs-conc-shift
        shifts = len([abs_conc_dict[word] for word in pos_words if word in abs_conc_dict.keys()])
        oov = len([oov_dict[word] for word in pos_words if word in oov_dict.keys()])
        print('positive', len(pos_words), 'oov', oov)
        percentage = shifts/(len(pos_words) - oov)
        print(f'{target}  {round(percentage, 2)}')


def noun_check_for_debugging(data_dict_list):
    av_wup_sim_dict = defaultdict(list)
    for d in data_dict_list:
        word = d['word']
        n_syns = d['n_synsets']
        av_wup_sim = d['av_wup_sim']
        av_cos = d['av_cos_mon_synonyms_to_word']
        #if d['wn-abs-conc'] == '':
        #print(d['wn-abs-conc'] )


        if d['wn_noun'] == 'False':
            if av_wup_sim == '':
                av_wup_sim_dict['no value'].append(word)
            elif float(av_wup_sim) == 1.0:
                av_wup_sim_dict[1.0].append(word)
            else:
                av_wup_sim_dict['value'].append(word)

    for sim_value, words in av_wup_sim_dict.items():
        print(sim_value, len(words))


def main():

    # explore


    # restrict to nouns:
    data_dict_list = load_full_lodce_data()
    [data_dict_list.remove(d) for d in data_dict_list if d['wn_noun'] == 'False']
    #get_polysemy_indicators(data_dict_list)
    # check if only nouns have a similarity measure:
    #noun_check_for_debugging(data_dict_list)
    noun = True
    truth_dict = find_truth_from_data(data_dict_list, noun = noun)
    split_truth_in_dev_test(truth_dict, noun = noun)
    #get_polysemy_indicators(data_dict_list, noun = False)





if __name__ == '__main__':
    main()
