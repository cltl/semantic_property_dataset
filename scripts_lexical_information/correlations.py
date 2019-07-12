import csv
import sys
import os

sys.path.append(os.path.abspath('../utils/'))

from stats import get_correlations


def load_data():
    with open('wordlists/all_lodce.csv') as infile:
        reader = csv.DictReader(infile)
        word_dict_list = list(reader)
    return word_dict_list



def main():

    comparisons = [('n_senses_total', 'n_synsets'),
                    ('n_senses_total', 'n_navigli_clusters'),
                    ('n_senses_total', 'n_onto_senses_n_v'),
                    ('n_synsets', 'n_navigli_clusters'),
                    ('n_synsets', 'n_onto_senses_n_v'),
                    ('n_navigli_clusters', 'n_onto_senses_n_v')]

    word_dict_list = load_data()


    #print(f'{senses1} and {senses2} have a pearson correlation of {coeff} with a p-value of {pvalue}.')
    print('senses1,senses2,coeff,pvalue,coeff_sp, pvalue_sp')
    for senses1, senses2 in comparisons:
        coeff, pvalue, coeff_sp, pvalue_sp = get_correlations(word_dict_list, senses1, senses2)
        print(f'{senses1},{senses2},{coeff},{pvalue},{coeff_sp},{pvalue_sp}')

if __name__ == '__main__':
    main()
