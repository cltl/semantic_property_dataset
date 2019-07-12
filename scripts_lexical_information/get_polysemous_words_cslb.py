import sys
import pandas as pd
from collections import defaultdict

def load_norms_df(path, cutoff_concepts = 0, cutoff_pf = 1):

    df = pd.read_csv(path, delimiter = '\t',\
            index_col = 'Vectors')

    for feat, pf in df.items():
        pos = len([x for x in pf if x > cutoff_pf])
        if pos < cutoff_concepts:

            df.drop(feat, axis = 1, inplace = True)
            #print(dropped)

    for c, pf in df.iterrows():
        pos = len([x for x in pf if x > cutoff_pf])
        if pos == 0.0:
            df.drop(c, axis = 0, inplace = True)

    #print(len(list(df.columns)), len(df))
    return df


def main():

    path = '../data/source_data/cslb_norms/feature_matrix.dat'

    cslb_df = load_norms_df(path)

    concept_property_dict = defaultdict(list)

    shift_concepts_dict = defaultdict(list)

    #print(cslb_df.keys())
    properties = list(cslb_df.keys())

    for p in properties:
        for concept, value in cslb_df[p].items():
            if value > 0:
                concept = concept.split('_(')[0]
                # get rid of disambiguation
                concept_property_dict[concept].append(p)


    property_pairs = []
    for p1 in properties:
        for p2 in properties:
            if p1 != p2:
                pair = set()
                pair.add(p1)
                pair.add(p2)
                if pair not in property_pairs:

                    for c, properties in concept_property_dict.items():
                        if (p1 in properties) and (p2 in properties):
                            shift_concepts_dict[p1+'-'+p2].append(c)
                    property_pairs.append(pair)

    


    shift_n_concepts_list = []
    for shift, concepts in shift_concepts_dict.items():

        shift_n_concepts_list.append((len(concepts), shift))

    print('shift,number of concepts')
    for n, shift in sorted(shift_n_concepts_list, reverse = True):
        print(shift+','+str(n))












if __name__ == '__main__':
    main()
