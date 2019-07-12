# script that, given a property, retrieves all concepts associatied with
# it in a given dataset

from wordnet_get_concepts import collect_concepts_wn
from wordnet_get_concepts import collect_negative_concepts_wn
from wordnet_get_concepts import collect_concepts_wn_parts
from wordnet_get_concepts import collect_negative_parts_wn
from conceptnet_get_concepts import collect_concepts_conceptnet
from cslb_get_concepts import collect_concepts_cslb
from crowd_get_concepts import collect_concepts_cslb_clean
from cslb_implications_get_concepts import collect_concepts_implications
from regpol_get_concepts import collect_concepts_regpol
from simile_get_concepts import get_concepts_simile
from mcrae_get_concepts import collect_concepts_mcrae
from manual_get_concepts import collect_concepts_manual
#from qumcrae_get_concepts import get_concepts_qumcrae
import glob
import os
import datetime
import pprint
import sys
import json

pp = pprint.PrettyPrinter(indent=4)

# Create a directory for the selected data source

def create_dirs():
    extracted_dir = '../data/data_extracted/'
    dir_list = [
    extracted_dir+'wn_hypernym/',
    extracted_dir+'wn_parts/',
    #extracted_dir+'wn_negated/',
    #extracted_dir+'wn_parts_negated/',
    extracted_dir+'conceptnet/',
    extracted_dir+'cslb/',
    extracted_dir+'bats/',
    #extracted_dir+'cslb_implications_pos/',
    #extracted_dir+'cslb_implications_neg/',
    extracted_dir+'cslb_crowd_pos',
    extracted_dir+'cslb_crowd_neg',
    extracted_dir+'manual',
    extracted_dir+'regpol',
    extracted_dir+'veale_simile',
    extracted_dir+'mcrae',
    extracted_dir+'manual_seed_data'
    ]

    if not os.path.isdir(extracted_dir):
        os.mkdir(extracted_dir)
    for dir in dir_list:
        if not os.path.isdir(dir):
            os.mkdir(dir)



# Search for property/category in the data source

def search_concepts(data_source, search_term, path_dict, selection_list = []):


    if data_source == 'wn_hypernym':
        concepts = collect_concepts_wn(search_term, selection_list)
    elif data_source == 'wn_parts':
        concepts = collect_concepts_wn_parts(search_term, selection_list)
    elif data_source == 'wn_parts_negated':
        category, negated_category = search_term.split('/')
        concepts = collect_negative_parts_wn(category, negated_category)
    elif data_source == 'wn_negated':
        category, negated_category = search_term.split('/')
        concepts = collect_negative_concepts_wn(category, negated_category)
    elif data_source == 'conceptnet':
        concepts = collect_concepts_conceptnet(search_term, selection_list)
    elif data_source == 'cslb':
        path = path_dict['cslb']
        concepts = collect_concepts_cslb(search_term)
    elif data_source == 'mcrae':
        concepts = collect_concepts_mcrae(search_term)
    elif data_source == 'cslb_crowd_pos':
        print('crowd!')
        label = 'pos'
        concepts = collect_concepts_cslb_clean(search_term, label)
        print(concepts)
    elif data_source == 'cslb_crowd_neg':
        label = 'neg'
        concepts = collect_concepts_cslb_clean(search_term, label)
    elif data_source == 'cslb_implications_pos':
        label = 'pos'
        concepts = collect_concepts_implications(search_term, label)
    elif data_source == 'cslb_implications_neg':
        label = 'neg'
        concepts = collect_concepts_implications(search_term, label)
    elif data_source == 'regpol':
        concepts = collect_concepts_regpol(search_term)
    elif data_source == 'manual':
        concepts = [], []
    elif data_source == 'veale_simile':
        concepts = get_concepts_simile(search_term)
    elif data_source == 'manual_seed_data':
        concepts = collect_concepts_manual(search_term)
    return concepts

# Select appropriate one

# Retrieve concepts

# Write concepts to file in appropriate directoryg

def concepts_to_file(category_name, data_source, timestamp, concepts):

    with open('../data/data_extracted/'+data_source+'/'+category_name+'-'+timestamp+'.txt', 'w') as outfile:
        outfile.write('\n'.join(concepts))

# Create overview file of unique concepts

# Log all decisions + filename


def load_log():

    with open('log.json', 'r') as infile:
        log_search_commands = json.load(infile)

    return log_search_commands


def log_to_file(updated_search_log):

    with open('log.json', 'w') as outfile:
        json.dump(updated_search_log, outfile, indent = True)

def load_concept_search_file(collection_file):

    with open(collection_file) as infile:
        lines = infile.read().strip().split('\n')

    header_str = lines[0]
    if ',' in header_str:
        deli = ','
    elif '\t' in header_str:
        deli = '\t'
    headers = header_str.split(deli)

    search_commands = []
    for line in lines[1:]:
        search_dict = dict()
        for header, cell in zip(headers, line.split(deli)):
            #print(header, cell.strip('"'))
            search_dict[header.strip('"')] = cell.strip('"')
        search_commands.append(search_dict)

    return search_commands


def main():
    collection_name = sys.argv[1]
    extract_again_fixed = sys.argv[2]

    path_dict = dict()
    path_dict['cslb'] = '../data/source_data/cslb_norms/feature_matrix.dat'

    already_extracted_here = []

    create_dirs()
    timestamp = str(datetime.datetime.now()).replace(',', '-').replace(' ', '-')
    search_commands = load_concept_search_file(collection_name+'.csv')
    if os.path.isfile('log.json'):
        search_logs = load_log()
    else:
        search_logs = []
    extracted_categories = [(log['search_term'], log['source']) for log in search_logs]


    for search_command in search_commands:
        print(search_command)
        #skipping concept net for now
        #if search_command['source'] == 'conceptnet':
        #    continue
        source = search_command['source']
        search_term = search_command['search_term']
        property_name = search_command['property_name']
        #n_concepts = search_command['n_extracted']
        if 'selection' in search_command.keys():
                selection_list = search_command['selection'].split(',')

        else:
            selection_list = []
        #print(search_term, source)
        #print(extracted_categories)

        if (search_term, source) in already_extracted_here:
            print('extracted just now')
            new_search_log = dict()
            new_search_log.update(search_command)
            new_search_log['time'] = timestamp
            #new_search_log['n_extracted'] = n_concepts
            new_search_log['extracted_categories'] = selection_list
            new_search_log['collection'] = collection_name
            new_search_log['n_extracted'] = 's.o.'
            search_logs.append(new_search_log)
            continue
        else:
            already_extracted_here.append((search_term, source))

        if (search_term, source) in extracted_categories:
            print('category already extracted previously')
            # find entry to show extracted subcategories:
            for log in search_logs:
                if (log['search_term'] == search_term) and (log['source'] == source):
                    selection_list = log['extracted_categories']
                    print('these categories have already been extracted:')
                    print(selection_list)
                    log_to_update = log
                    break

            if extract_again_fixed == 'no':
                extract = False
            else:
                if extract_again_fixed == 'yes':
                    extract = True
                    search_logs.remove(log_to_update)
                elif extract_again_fixed == 'ask':
                    extract_again = input('do you want to extract it again?')
                    if extract_again == 'no':
                        extract = False
                    elif extract_again == 'yes':
                        extract = True
                        search_logs.remove(log_to_update)
                    # remove search log from logs, because it will be updated:

        else:
            print('not searched for yet')
            extract = True

        if extract == True:
            concepts, selection_list = search_concepts(source, search_term, path_dict, selection_list)
            selection_list = [str(item) for item in selection_list]
            n_concepts = len(concepts)
            print('extracted: ', concepts)
            concepts_to_file(search_term, source, timestamp, concepts)
            new_search_log = dict()
            new_search_log.update(search_command)
            new_search_log['time'] = timestamp
            new_search_log['n_extracted'] = n_concepts
            new_search_log['extracted_categories'] = selection_list
            new_search_log['collection'] = collection_name
            search_logs.append(new_search_log)


        else:
            print('already extracted - not extracting again')

    log_to_file(search_logs)





if __name__ == '__main__':
    main()
