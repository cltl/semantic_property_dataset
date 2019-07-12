from nltk.corpus import wordnet as wn



def check_wordnet_noun(syns):
    noun = False
    if syns:
        pos = [syn.pos() for syn in syns]
        if 'n' in pos:
            noun = True
    return noun


def get_synsets_max_distance(synsets):

    pairs = set()
    sims = []
    for syn1 in synsets:
        for syn2 in synsets:
            if all([((syn1, syn2) not in pairs), ((syn2, syn1) not in pairs),\
                    (syn1.pos() == syn2.pos()), (syn1 != syn2)]):
                pairs.add((syn1, syn2))
                sim = syn1.wup_similarity(syn2)
                sims.append((sim, (syn1, syn2)))
    sim_pairs = [(sim, pair) for sim, pair in sims if type(sim) == float]
    if sims:
        min_sim, min_pair = min(sims)
    else:
        min_sim, min_pair = str(None), (None, None)

    return min_sim, min_pair


def get_synsets(word):

    synsets = wn.synsets(word)
    return synsets

def get_all_wup_sims(synsets):

    pairs = set()
    sims = []

    if len(synsets) > 1:
        for syn1 in synsets:
            for syn2 in synsets:
                if all([((syn1, syn2) not in pairs), ((syn2, syn1) not in pairs),\
                        (syn1.pos() == syn2.pos()), (syn1 != syn2)]):
                    pairs.add((syn1, syn2))
                    sim = syn1.wup_similarity(syn2)
                    sims.append(sim)
    elif len(synsets) == 1:
        syn = synsets[0]
        sim = syn.wup_similarity(syn)
        sims.append(sim)
    sims = [sim for sim in sims if type(sim) == float]
    return sims


def get_min_wn_sense_sim(synsets):
    # use wu-palmer because it takes their lowest common subsumer into account
    # values can range between 0 and 1 (1 means same synset)
    # only works for same po

    sims = get_all_wup_sims(synsets)
    if sims:
        min_sim = min(sims)
    else:
        min_sim = str(None)

    return min_sim

def get_wordnet_data(word):
    syns = wn.synsets(word)
    min_wn_sense_sim = get_min_wn_sense_sim(syns)
    noun = check_wordnet_noun(syns)
    n_senses = len(syns)
    if syns:
        exists = True
    else:
        exists = False
    return exists, noun, n_senses, min_wn_sense_sim


def all_hypernyms(syn):

    hypernyms = []

    for hyp in syn.hypernyms():
        hypernyms.append(hyp)

    for hyp in hypernyms:
        for next_hyp in hyp.hypernyms():
            if next_hyp not in hypernyms:
                hypernyms.append(next_hyp)
    return hypernyms

def check_hyponyms(node_abs, node_conc, word):

    syns = wn.synsets(word, 'n')
    answers = set()
    if syns:
        # get hpyernyms and check if synset is in hypernyms
        for syn in syns:
            hypernyms = all_hypernyms(syn)
            if node_abs in hypernyms:
                answers.add('abs')
            elif node_conc in hypernyms:
                answers.add('conc')
            else:
                answers.add('n')
    else:
        answers.add('-')
    return answers


def get_abstract_concrete(word):

    node_abstract = wn.synsets('abstract_entity')[0]
    node_concrete = wn.synsets('physical_entity')[0]

    answers = check_hyponyms(node_abstract, node_concrete, word)
    answer_str = '-'.join(sorted(list(answers)))

    return answer_str






def main():

    word = 'lemon'
    synsets = get_synsets(word)
    noun = check_wordnet_noun(synsets)
    print(noun)
    #answer_str = get_abstract_concrete(word)


    #print(answer_str)

if __name__ == '__main__':
    main()
