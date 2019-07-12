
#concepts = collect_concepts_cslb_clean(search_term, label)


def collect_concepts_manual(search_term):

    path = f'../data/source_data/manual_seed_data/{search_term}.txt'
    with open(path) as infile:
        concepts = infile.read().strip().split('\n')
    return concepts, []


def main():

    search_term = 'grow'
    concepts = collect_concepts_manual(search_term)
    print(concepts)


if __name__ == '__main__':
    main()
