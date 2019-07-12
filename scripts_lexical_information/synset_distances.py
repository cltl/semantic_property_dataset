import sys
from collections import defaultdict

from nltk.corpus import wordnet as wn

sys.path.append('../utils/')

from load_models import load_model
from load_models import get_cosine
from load_models import represent
from load_models import create_centroid_wordlist

from wordnet_data import get_synsets_max_distance



def get_monosemous_words(word):

    synsets = wn.synsets(word)
    monosemous_words_dict = defaultdict(list)
    for syn in synsets:
        lemmas = [str(l.name()) for l in syn.lemmas()]
        for l in lemmas:
            syns = wn.synsets(l)
            if len(syns) == 1:
                monosemous_words_dict[syn].append(l)

    return monosemous_words_dict


def get_distance_to_centroid(model, wordlist):

    centroid = create_centroid_wordlist(model, wordlist)
    distances = []

    for word in wordlist:
        vec = represent(model, word)
        if vec != 'OOV':
            cos = get_cosine(centroid, vec)
            distances.append(cos)

    if distances:
        average_distance_to_centroid = sum(distances)/len(distances)
    else:
        average_distance_to_centroid  = None

    return average_distance_to_centroid


def get_average_distance_to_word(model, target_word, wordlist):

    target_word_vec = represent(model, target_word)
    distances = []

    if type(target_word_vec) != str:
        for word in wordlist:
            vec = represent(model, word)
            if type(vec) != str:
                cos = get_cosine(target_word_vec, vec)
                distances.append(cos)


    if distances:
        average_distance_to_centroid = sum(distances)/len(distances)
    else:
        average_distance_to_centroid  = None

    return average_distance_to_centroid


def main():

    word = 'walk'

    monosemous_words_dict = get_monosemous_words(word)

    all_mon_words = []
    [all_mon_words.extend(mon_words) for mon_words in monosemous_words_dict.values()]

    for syn, words in monosemous_words_dict.items():
        print(syn, words)

    path_wiki_sgns = '../../../Data/dsm/wikipedia_full/sgns_pinit1/sgns_pinit1/sgns_rand_pinit1'
    model = load_model(path_wiki_sgns, 'sgns')

    av_distance_centroid = get_distance_to_centroid(model, all_mon_words)
    av_distance_word = get_average_distance_to_word(model, word, all_mon_words)

    print(f'The average distance of the monosemous synonyms of {word} to the \
            centroid of all monosemous words is {av_distance_centroid}')
    print()
    print(f'The average distance of the monosemous synonyms of {word} to the \
            to the polysemous target word {word} is  {av_distance_word}')


if __name__ == '__main__':
    main()
