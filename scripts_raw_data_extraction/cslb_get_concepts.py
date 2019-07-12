from collections import defaultdict
import pandas as pd
import glob
import os
import xlrd



# load cslb messy data set

def load_norms_df(path, cutoff_concepts = 0, cutoff_pf = 1):


    df = pd.read_csv(path, delimiter = '\t',\
            index_col = 'Vectors')

    #print(len(list(df.columns)), len(df))

    for feat, pf in df.items():

        pos = len([x for x in pf if x > cutoff_pf])
        if pos < cutoff_concepts:

            df.drop(feat, axis = 1, inplace = True)
            #print(dropped)

    #print(len(list(df.columns)), len(df))

    for c, pf in df.iterrows():
        pos = len([x for x in pf if x > cutoff_pf])
        if pos == 0.0:
            df.drop(c, axis = 0, inplace = True)

    #print(len(list(df.columns)), len(df))
    return df

def find_relevant_properties(df, target_property):

    # find correct property names:

    properties = df.columns
    possible_properties = []
    selected_properties = []

    for p in properties:
        if p == target_property:
            selected_properties.append(p)


    return selected_properties


def get_concepts(df, property):

    target_concepts = []

    for concept, value in df[property].items():

        if value > 0:
            target_concepts.append(concept)


    return target_concepts



    #return concepts


def collect_concepts_cslb(path, target_property):

    all_concepts = []

    df = load_norms_df(path)

    #print(df['is_yellow'], type(df['is_yellow']))

    selected_properties_list = find_relevant_properties(df, target_property)


    for prop in selected_properties_list:
        concepts = get_concepts(df, prop)
        all_concepts.extend(concepts)

    return all_concepts, selected_properties_list


def get_properties(df, target_concept):

    properties = df.columns
    selected_properties = []
    row = df.loc[target_concept]
    for prop, pf in zip(properties, row):

        if pf > 0.0:
            selected_properties.append(prop)
        #else:
            #print(pf, prop, 'not listed')
    return selected_properties


def get_inconsistant_concepts(df, prop1, prop2):

    inconsistant_concepts = []

    col1 = df[prop1]
    col2 = df[prop2]

    concepts = df.index
    count = 0

    for n, values in enumerate(zip(col1, col2)):
        val1, val2 = values
        concept = concepts[n]

        if val1 > 0.0:
            count += 1

            if val2 == 0.0:
                inconsistant_concepts.append(concept)
                print(concept, val1, val2)

    print(f'''There are {len(inconsistant_concepts)} concepts not labeled as {prop2} \
    out of a total of {count} concepts labeled as {prop1} ''')

    return inconsistant_concepts



def main():

    path = '../data/source_data/cslb_norms/feature_matrix.dat'

    target_property = 'yellow'
    target_concept = 'seagull'

    df = load_norms_df(path)

    prop1 = 'is_a_bird'
    prop2 = 'is_an_animal'
    inconsistant_concepts = get_inconsistant_concepts(df, prop1, prop2)
    print(inconsistant_concepts)


if __name__ == '__main__':
    main()
