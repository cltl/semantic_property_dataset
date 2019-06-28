import os
import glob
from collections import defaultdict, Counter
import sys
import json

sys.path.append('../utils/')
from data_utils import load_log



def load_concepts(category, timestamp, source):
    filepath = '../data/data_extracted/'+source+'/'+category+'-'+timestamp+'.txt'

    #source_concepts_dict = dict()

    if os.path.isfile(filepath):
        with open(filepath) as infile:
            concepts = infile.read().strip().split('\n')
        concepts = [c for c in concepts if c != '']
    else:
        concepts = []
            #[all_concepts.append(c) for c in concepts if c != '']
            #source_concepts_dict[source] = concepts
    return concepts




def assign_labels(search_dicts):

    # new dict to collect labels per concept (and not per category)
    correct_concept_label_dict = dict()
    concept_categories_dict = defaultdict(list)
    all_concepts_source_dict = defaultdict(list)
    concept_certainty_dict = dict()

    cat_label_dict_fixed = defaultdict(list)
    cat_label_dict_proposed = defaultdict(list)

    fixed_labels = ['cslb_crowd_neg',
                    'cslb_crowd_pos',
                    'cslb_implications_pos',
                    'cslb_implications_pos',
                    'qumcrae'
                     ]
    cat_concepts_dict = defaultdict(set)

    for search_dict in search_dicts:
        source = search_dict['source']
        proposed_label = search_dict['label']
        cat = search_dict['search_term']
        timestamp = search_dict['time']

        if source in fixed_labels:
            cat_label_dict_fixed[cat].append((source, proposed_label, timestamp))

        else:
            cat_label_dict_proposed[cat].append((source, proposed_label, timestamp))

    for cat, fixed_labels in cat_label_dict_fixed.items():
        if fixed_labels:
            for source, fixed_label, timestamp in fixed_labels:
                concepts = load_concepts(cat, timestamp, source)
                #concepts = source_concepts_dict[source]
                for concept in concepts:
                    print('concept with certain label: ', concept)
                    correct_concept_label_dict[concept] = fixed_label
                    all_concepts_source_dict[concept].append(source)
                    concept_categories_dict[concept].append(cat)
                    concept_certainty_dict[concept] = 'certain'

    for cat, proposed_labels in cat_label_dict_proposed.items():
        if proposed_labels:
            for source, proposed_label, timestamp in proposed_labels:
                concepts = load_concepts(cat, timestamp, source)
                for concept in concepts:
                    if concept not in correct_concept_label_dict:
                        correct_concept_label_dict[concept] = proposed_label
                        concept_certainty_dict[concept] = 'not_certain'
                    all_concepts_source_dict[concept].append(source)
                    concept_categories_dict[concept].append(cat)

    #print('concept categories dicts: ', concept_categories_dict)


    return correct_concept_label_dict, all_concepts_source_dict,\
            concept_categories_dict, concept_certainty_dict



def examples_to_file(collection_name, concept_categories_dict, \
                    correct_concept_label_dict, concept_source_dict,\
                    concept_certnainty_dict, property):

    # make a new directory for sorted examples:
    dir = '../data/data_extracted_sorted/'
    dir_collection = f'../data/data_extracted_sorted/{collection_name}/'
    if not os.path.isdir(dir):
        os.mkdir(dir)
    if not os.path.isdir(dir_collection):
        os.mkdir(dir_collection)

    lines = []
    header = 'concept,label,categories_str,sources_str,certainty'

    for concept, cats in concept_categories_dict.items():
        sources_str = ' '.join(set(concept_source_dict[concept]))
        categories_str = ' '.join(set(cats))
        certainty = concept_certnainty_dict[concept]
        label = correct_concept_label_dict[concept]
        line = ','.join([concept, label, categories_str, sources_str, certainty])
        lines.append(line)

    with open(dir_collection+property+'.csv', 'w') as outfile:
        outfile.write(header+'\n')
        outfile.write('\n'.join(lines))




def count_category_concepts(correct_concept_label_dict, concept_categories_dict):

    category_counts = dict()

    cat_concepts_dict = defaultdict(list)
    for concept, categories in concept_categories_dict.items():
        for cat in categories:
            cat_concepts_dict[cat].append(concept)


    for cat, concepts in cat_concepts_dict.items():
        cat_counter = Counter()
        for concept in concepts:
            label = correct_concept_label_dict[concept]
            cat_counter[label] += 1
        category_counts[cat] = cat_counter


    return category_counts


def clean_up():

    # load log
    with open('../scripts_raw_data_extraction/log.json') as infile:
        search_command_list = json.load(infile)

    relevant_filepaths = []

    for log_dict in search_command_list:
        category = log_dict['search_term']
        timestamp = log_dict['time']
        source = log_dict['source']
        filepath = '../data/data_extracted/'+source+'/'+category+'-'+timestamp+'.txt'
        relevant_filepaths.append(filepath)

    all_filepaths = glob.glob('../data/data_extracted/*/*-*.txt')

    for f in all_filepaths:
        if f not in relevant_filepaths:
            os.remove(f)



def main():
    collection_name = sys.argv[1]
    property_dict = load_log(collection_name)

    overview_lines = []

    for prop, search_dicts in property_dict.items():
        correct_concept_label_dict, concept_source_dict, concept_categories_dict,\
        concept_certnainty_dict = assign_labels(search_dicts)
        examples_to_file(collection_name, concept_categories_dict, \
        correct_concept_label_dict, concept_source_dict, concept_certnainty_dict, prop)
        total_concepts_pos = len([c for c, l in correct_concept_label_dict.items() if l == 'pos'])
        total_concepts_neg = len([c for c, l in correct_concept_label_dict.items() if l == 'neg'])
        total_concepts_mixed = len([c for c, l in correct_concept_label_dict.items() if l == 'pos/neg'])
        category_counts = count_category_concepts(correct_concept_label_dict, concept_categories_dict)

        for cat, counts_dict in category_counts.items():
            for label, counts in counts_dict.items():
                line = [prop, cat, label, str(counts)]
                overview_lines.append(','.join(line))

        overview_lines.append(','.join([prop, 'total', 'pos', str(total_concepts_pos)]))
        overview_lines.append(','.join([prop, 'total', 'neg', str(total_concepts_neg)]))
        overview_lines.append(','.join([prop, 'total', 'pos/neg', str(total_concepts_mixed)]))
        overview_lines.append(' ')

    target_dir = f'../data/data_extracted_sorted/overviews/'

    if not os.path.isdir(target_dir):
        os.mkdir(target_dir)

    with open(f'{target_dir}overview-{collection_name}.csv', 'w') as outfile:
        outfile.write('\n'.join(overview_lines))

    with open(f'{target_dir}properties-{collection_name}.csv', 'w') as outfile:
        outfile.write('\n'.join(property_dict.keys()))

    print('\n -- cleaning -- \n')
    clean_up()



if __name__ == '__main__':
    main()
