import os

def get_concepts_simile(cat):

    if os.path.isfile('../data/source_data/veale_simile/'+cat+'.txt'):
        with open('../data/source_data/veale_simile/'+cat+'.txt') as infile:
            concepts = infile.readlines()
    else:
        concepts = []

    return concepts, []
