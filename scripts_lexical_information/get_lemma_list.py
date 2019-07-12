import sys

sys.path.append('../utils/')
from data_utils import load_full_lodce_data


def get_lemmas(dict_list):

    lemmas = [d['word'] for d in dict_list]

    with open('../data/vocab/lemmas.txt', 'w') as outfile:
        outfile.write('\n'.join(lemmas))


def main():
    dict_list = load_full_lodce_data()
    get_lemmas(dict_list)

if __name__ == '__main__':
    main()
