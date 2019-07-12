from analyze_polysemy import load_data

from polysemy_measure import load_truth
import matplotlib.pyplot as plt
#plt.style.use('seaborn-whitegrid')
import numpy as np
from collections import defaultdict

def get_polysemy_distribution(data_dict_list, noun = False):

    print(len(data_dict_list), 'all words')
    print('noun', noun)
    if noun == True:
        [data_dict_list.remove(d) for d in data_dict_list if d['wn_noun'] == 'False']
    print(len(data_dict_list), 'nouns only')

    #truth_dict = find_truth_from_data(data_dict_list)
    #split_truth_in_dev_test(truth_dict)
    if noun == True:
        targets = ['mon_n', 'poly_metonymy_n', 'met_n', 'homonym_n']
    else:
        targets = ['mon', 'poly_metonymy', 'met', 'homonym']
    targets.reverse()


    # truth

    #truth_hom = [w for w, l in truth_words.items() if l == 1]
    truth_target_dict = dict()
    for target in targets:
        truth_target_dict[target] = [w for w, l in load_truth(target).items() if l == 1 ]

    group_dict_syns = defaultdict(list)
    group_dict_sims = defaultdict(list)
    colors = ("red", "green", "blue", "black")

    for d in data_dict_list:
        word = d['word']
        if d['wn-abs-conc'].startswith('abs-conc'):
            abs_conc = 1
        else:
            abs_conc = 0

        sim = d['av_wup_sim']
        syn = d['n_synsets']
        if sim != '':

            for target, truth_list in truth_target_dict.items():
                if word in truth_list:
                    group_dict_sims[target].append(1-float(sim))
                    group_dict_syns[target].append(int(syn))


        #vecs.append([int(d['n_synsets']), float(d['av_wup_sim'])] #, float(d['min_wup_sim'], abs_conc)])
        #words.append(d['word'])
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, axisbg = '1.0')

    for color, target in zip(colors, targets):
        print(color, target)
        for sim, syn in zip(group_dict_sims[target], group_dict_syns[target]):
            ax.scatter(syn, sim, alpha=0.8, c=color, edgecolors='none', s=30, label = target)


    #plt.scatter(np.array(syns), np.array(sims))
    #ax.legend()
    plt.show()

def main():

    # explore
    path = 'wordlists/all_lodce_all_distances_pos.csv'

    # restrict to nouns:
    data_dict_list = load_data(path)
    get_polysemy_distribution(data_dict_list, noun = True)







if __name__ == '__main__':
    main()
