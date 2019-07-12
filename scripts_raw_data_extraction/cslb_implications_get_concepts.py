# get crowd annotations
import glob



def collect_concepts_implications(property_name, label):


    #crowd1 = glob.glob('../crowd1/*.txt')
    implications = glob.glob('../data/source_data/cslb_implications/*'+property_name+'-'+label+'*.txt')




    if implications:

        all_concepts = []

        for f in implications:
            with open(f) as infile:
                concepts = infile.read().strip().split('\n')
                all_concepts.extend(concepts)
    else:
        concepts = []

    return concepts, implications


def main():


    concepts, selection_list = collect_concepts_implications(property_name)


if __name__ == '__main__':
    main()
