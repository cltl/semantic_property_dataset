# get crowd annotations
import glob



def collect_concepts_cslb_clean(property_name, label):


    if label == 'neg':
        label = 'neg-all'
    crowd2 = glob.glob('../data/source_data/crowd2/'+property_name+'-'+label+'.txt')
    crowd1 = glob.glob('../data/source_data/crowd1/'+property_name+'-'+label+'.txt')
    imp = glob.glob('../data/source_data/cslb_implications/imp-'+property_name+'-'+label+'.txt')

    all_files = crowd2 + crowd1 + imp
    print('this is a list of all files:', all_files)
    all_concepts = []

    if all_files:
        for f in all_files:
            with open(f) as infile:
                concepts = infile.read().strip().split('\n')
                print('concepts: ', concepts)
                [all_concepts.append(c) for c in concepts]
                #all_concepts.extend(concepts)
    else:
        print('property not found')
        all_concepts = []

    return all_concepts, []


def main():

    concepts, selection_list = collect_concepts_crowd


if __name__ == '__main__':
    main()
