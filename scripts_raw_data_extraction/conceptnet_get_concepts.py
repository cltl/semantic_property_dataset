# This is a test script to see if we can extract concepts
# associated with a property using the web api of conceptnet 5.0 as documented
# here: https://github.com/commonsense/conceptnet5/wiki/API


import requests
import pprint
import os
import datetime
import glob

pp = pprint.PrettyPrinter(indent=4)

#query = requests.get('http://api.conceptnet.io/query?other=/c/en/fly').json() # works
#query = requests.get('http://api.conceptnet.io/query?rel=/CapableOf/c/en/fly').json() - does not work



def collect_relations(prop):

    relations = set()
    edges = []

    pages = []
    # http://api.conceptnet.io/c/en/example
    page = 'http://api.conceptnet.io/c/en/'+ prop
    #page = 'http://api.conceptnet.io/query?node=/c/en/' + prop
    #page = 'http://api.conceptnet.io/query?rel=/r/CapableOf' - this return fewer
    # concepts for some reason
    pages.append(page)
    for page in pages:
        #query = requests.get(page)
        #query = requests.get(page).json()
        query = requests.get(page).json()
        if 'view' in query:
            if 'nextPage' in query['view']:
                next_page = query['view']['nextPage']
                pages.append('http://api.conceptnet.io'+next_page)
        #print('edges first iteration: ', query['edges'])
        for edge in query['edges']:
            relation = edge['rel']['label']
            relations.add(relation)
            edges.append(edge)

    return relations, edges


def get_terms(edges, relation):

    print('the relation used is ', relation)

    terms = dict()

    for edge in edges:
        if edge['rel']['label'] == relation:
            target_term = edge['start']['term']
            if target_term.split('/')[2] == 'en':
                term = edge['start']['term']
                terms[term] = [edge['start']['label'], term.split('/')[3], 'direct_rel']
    return terms


def collect_concepts_conceptnet(prop, selection_list):

    relations, edges = collect_relations(prop)

    if relations:

        print('Relations connecting the property to concepts:\n')

        pp.pprint(relations)

        # ask for target relation
        if not selection_list:
            relations_selected = input('Enter relation (if more than one is selected,\
            seperate by comma). If none is appropriate, enter "none": ')
            relations_list = relations_selected.split(',')
        else:
            relations_list = selection_list
            print('these properties have been preselected: ', relations_list)

        if relations_list != ['none']:
            print(relations_list)
            all_terms = []
            for relation in relations_list:
                print('working on extracting: ', relation)
                if relation in relations:
                    terms = get_terms(edges, relation)
                    all_terms.extend(list(terms.keys()))

            terms_final = [t.split('/')[-1] for t in all_terms]

        else:
            terms_final = []
            relations_list = []

    else:

        terms_final = []
        relations_list = ['none']

    return terms_final, relations_list



def main():

    prop = 'yellow'
    terms, selection_list = collect_concepts_conceptnet(prop, ['HasProperty'])
    print(terms)


if __name__ == '__main__':

    main()
    #count_words()
