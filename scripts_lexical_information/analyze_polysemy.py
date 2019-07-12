import csv
from synset_distances import get_average_distance_to_word

sys.path.append('../utils/')

from data_utils import load_full_ldoce_data# Compare wn distances to ldoce senses


# Compare MIPVU metaphoricity to wn abs conc




def get_cosines(dict_list, header, target_value):

    cosines = []
    for d in dict_list:
        cos = d['av_cos_mon_synonyms_to_word']
        if (cos.replace('.','',1).isdigit()) and (d[header] == target_value):
            cosines.append(float(cos))

    return cosines



def analyze_distance_type_correlations(dict_list):

    """Analyze the relation between the average distance of the monosemous
     synset neighbors to the polysemous word and the polysemy type"""

    metonymic_in_wn = [d for d in dict_list if d['metonymy_entities'] == str(True) \
                        and int(d['n_synsets']) > 0]

    metaphoric_in_wn = [d for d in dict_list if (d['mipvu'] == str(True)) and int(d['n_synsets']) > 0]

    homonyms_same_pos = [d for d in dict_list if d['polysemy_type'] == 'homonymous_also_same_pos']
    homonyms_different_pos = [d for d in dict_list if d['polysemy_type'] == 'homonymous_only_different_pos']
    poly = [d for d in dict_list if d['polysemy_type'] == 'poly']

    #print(len(metonymic_in_wn))
    #print(len(metaphoric_in_wn))

    # see how much overlap there is:

    words_metonymic = set([d['word'] for d in metonymic_in_wn])
    words_metaphoric = set([d['word'] for d in metaphoric_in_wn])


    overlap = words_metonymic.intersection(words_metaphoric)

    print('overlap between metaphoric and metonymic: ', len(overlap))
    print('metaphoric: ', len(words_metaphoric))
    print('metonymic: ', len(words_metonymic))

    # no overlap

    # compare spatial distances


    data_dict = dict()

    data_dict['cos_metaphoric'] = get_cosines(dict_list, 'mipvu', 'True')
    data_dict['cos_metonymic'] = get_cosines(dict_list, 'metonymy_entities', 'True')
    print(len(data_dict['cos_metonymic']))

    data_dict['cos_polysemous'] = get_cosines(dict_list, 'polysemy_type', 'poly')
    data_dict['cos_monosemous'] = get_cosines(dict_list, 'polysemy_type', 'mon')
    data_dict['cos_homonym_same_pos'] = get_cosines(dict_list, 'polysemy_type', 'homonyms_also_same_pos')
    data_dict['cos_homonym_different_pos'] = get_cosines(dict_list, 'polysemy_type', 'homonyms_only_different_pos')


    for name, cosines in data_dict.items():
        if cosines:
            av_cosine = sum(cosines)/len(cosines)
        else:
            av_cosine = None
        print(f'{name} has an average cos of {av_cosine} using {len(cosines)} data points.')







def main():

    # explore

    dict_list = load_full_lodce_data()


    analyze_distance_type_correlations(dict_list)








if __name__ == '__main__':
    main()
