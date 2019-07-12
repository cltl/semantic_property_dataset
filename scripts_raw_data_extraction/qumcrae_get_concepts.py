from collections import defaultdict
from collections import Counter
import os



def load_quantified_mcrea():

    prop_concept_dict = defaultdict(list)

    # load txt file of features for which there is a majority
    path = '../data/source_data/McRae-quantified/mcrae-quantified-majority.txt'
    with open(path) as infile:
        lines = infile.read().split('#')[-1].strip().split('\n')

    for line in lines:
        line_list = line.split('\t')
        concept = line_list[1]
        feature = line_list[2]
        annotations = line_list[3:]
        annotation_count = Counter(annotations)
        majority_voting, cnt = list(annotation_count.most_common(1))[0]

        concept_dict = dict()
        concept_dict[concept] = majority_voting
        prop_concept_dict[feature].append(concept_dict)

    return prop_concept_dict


def get_concepts_qumcrae(feature, label):

    prop_concept_dict = load_quantified_mcrea()
    #print(prop_concept_dict[feature])
    selected_concepts = []

    if label == 'pos':
        target_annotations = ['all', 'most', 'some']
    elif label == 'neg':
        target_annotations = ['few', 'no']

    for concepts_dict in prop_concept_dict[feature]:
        concept, annotation = list(concepts_dict.items())[0]
        if annotation in target_annotations:
            selected_concepts.append(concept)

    return selected_concepts, []



def main():

    feature = 'is_black'
    label = 'neg'

    selected_concepts = get_concepts_qumcrae(feature, label)
    print(selected_concepts)

if __name__ == '__main__':

    main()
