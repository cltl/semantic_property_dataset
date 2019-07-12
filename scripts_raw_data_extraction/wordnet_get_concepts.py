from nltk.corpus import wordnet as wn

import glob
import os


def get_all_hyponyms(syn):

    hyponyms = syn.hyponyms()
    lemma_dict = dict()

    # Include lemmas in the hypernym synset - activated
    lemma_dict[syn] = [str(l.name()) for l in syn.lemmas()]


    for hyp in hyponyms:
        for hyp2 in hyp.hyponyms():
            if hyp2 not in hyponyms:
                hyponyms.append(hyp2)
    # get all lemmas
    for hyp in hyponyms:
        lemmas =[str(l.name()) for l in hyp.lemmas()]
        lemma_dict[hyp] = set(lemmas)
    return lemma_dict


def select_correct_synsets(word, selection_list):

    syns = wn.synsets(word)
    if syns:
        if selection_list:
            if not str(selection_list[0]).startswith('Synset('):
                print('this is the selection_list', selection_list[0])
                indices_list = [int(i) for i in selection_list]
                target_synsets = [syns[i] for i in indices_list]
            else:
                target_synsets = []
                for syn in syns:
                    if str(syn) in selection_list:
                        target_synsets.append(syn)

        else:
            for n, syn in enumerate(syns):
                print(n)
                print(syn)
                print(syn.definition())
                print(syn.examples())
                print('\n')

            indices = input('Which synsets should be kept? (Seperate indices by a comma) ')
            indices_list = [int(i) for i in indices.split(',')]
            target_synsets = [syns[i] for i in indices_list]

    else:
        target_synsets = []

    return target_synsets


def get_all_parts(synset):

    hyponyms = get_all_hyponyms(synset)

    # include target_synset:
    hyponyms[synset] = set([str(l.name()) for l in synset.lemmas()])

    parts = []

    for hyp in hyponyms:

        parts1 = synset.part_holonyms()
        parts2 = synset.substance_holonyms()
        parts3 = synset.member_holonyms()

        parts.extend(parts1)
        parts.extend(parts2)
        parts.extend(parts3)

    parts_hyponyms = []

    for part in parts:
        hyponyms = get_all_hyponyms(part)
        parts_hyponyms.extend(hyponyms)

    all_parts = parts + parts_hyponyms

    all_lemmas = set()

    for syn in all_parts:
        lemmas = [str(l.name()) for l in syn.lemmas()]
        all_lemmas.update(set(lemmas))

    return all_lemmas




def collect_concepts_wn(category, selection_list):
    target_synsets = select_correct_synsets(category, selection_list)

    if target_synsets:

        all_lemma_dict = dict()

        for syn in target_synsets:
            lemma_dict = get_all_hyponyms(syn)
            all_lemma_dict.update(lemma_dict)

        all_lemmas_list = []

        [all_lemmas_list.extend(lemmas) for lemmas in all_lemma_dict.values()]

    else:
        all_lemmas_list = []
        target_synsets = []


    return all_lemmas_list, selection_list

def collect_negative_concepts_wn(category, negated_category):

    category_concepts, selected_list_category = collect_concepts_wn(category)

    negated_category_concepts, selected_list_negated_category = collect_concepts_wn(negated_category)

    target_concepts = set(category_concepts).difference(set(negated_category_concepts))

    return list(target_concepts), selected_list_category+selected_list_negated_category



def collect_concepts_wn_parts(category, selection_list):
    target_synsets = select_correct_synsets(category, selection_list)
    all_parts = []
    for syn in target_synsets:
        parts = get_all_parts(syn)
        all_parts.extend(parts)

    return sorted(set(all_parts)), selection_list


def collect_negative_parts_wn(category, negated_category):

    category_concepts, selected_list_category = collect_concepts_wn_parts(category)

    negated_category_concepts, selected_list_negated_category = collect_concepts_wn_parts(negated_category)

    target_concepts = set(category_concepts).difference(set(negated_category_concepts))

    return list(target_concepts), selected_list_category+selected_list_negated_category


def main():

    category = 'wing'
    selection_list = ['0']
    meronyms, selection_list = collect_concepts_wn_parts(category, selection_list)

    for mer in meronyms:
        print(mer)


if __name__ == '__main__':
    main()
