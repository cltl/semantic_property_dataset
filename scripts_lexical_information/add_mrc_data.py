import sys
import csv
sys.path.append('../utils/')
from data_utils import load_mrc_data
from data_utils import load_full_lodce_data
from data_utils import get_mrc_score

def vocab_data_to_file(new_dict_list):

    fieldnames = new_dict_list[0].keys()

    with open('../data/vocab/all_lodce_mrc.csv', 'w') as outfile:
        writer = csv.DictWriter(outfile, fieldnames = fieldnames)
        writer.writeheader()
        for d in new_dict_list:
            writer.writerow(d)



def main():

    word_conc_dict = load_mrc_data('conc')
    word_fam_dict = load_mrc_data('fam')
    word_aoa_dict = load_mrc_data('aoa')

    dict_list_vocab = load_full_lodce_data()
    new_dict_list_vocab = []

    for d in dict_list_vocab:
        word = d['word']

        d['conc'] = get_score(word, word_conc_dict)
        d['fam'] = get_score(word, word_fam_dict)
        d['aoa'] = get_score(word, word_aoa_dict)
        new_dict_list_vocab.append(d)
    vocab_data_to_file(new_dict_list_vocab)


if __name__ == '__main__':
    main()
