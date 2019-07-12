from collections import defaultdict



def read_file(name):

    with open(name) as infile:
        lines = infile.read().strip().split('\n')

    property_dict = defaultdict(list)


    for line in lines:
        line_list = line.split('\t')

        concept = line_list[0]

        for cat in line_list[1:]:
            property_dict[cat].append(concept)


    return property_dict



def main():

    name = "../data/source_data/TonyVeale/TSV_lists/CategoryHierarchy.csv"

    property_dict = read_file(name)

    for prop, concepts in property_dict.items():
        print(prop)
        print(concepts)
        print()


if __name__ == '__main__':
    main()
