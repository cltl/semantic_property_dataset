import glob
from collections import defaultdict
import os

def get_property_overview():

    data_files = glob.glob('../data/concepts_additional_info/*/*.csv')
    category_property_dict = defaultdict(list)
    for f in data_files:
        category = f.split('/')[-2]
        property = os.path.basename(f).split('.')[0]
        category_property_dict[category].append(property)

    return category_property_dict


def files_for_manual_addition(category_property_dict):

    with open('../data/manually_included/properties_overview.csv', 'w') as outfile:
        outfile.write('category,property,pos, pos_met, neg, neg_met\n')
        for cat, prop_list in category_property_dict.items():
            for prop in prop_list:
                outfile.write(f'{cat},{prop}\n')


def overview_to_file(category_property_dict):

    #lenght, longest_prop_list = max([(len(prop_list), prop_list) for prop_list in category_property_dict.values()])
    with open('../statistics/property_overivew.csv', 'w') as outfile:
        outfile.write('category,properties\n')
        for cat, prop_list in category_property_dict.items():
            outfile.write(f'{cat},{" ".join(prop_list)}\n')






def main():

    category_property_dict = get_property_overview()
    #properties = []
    overview_to_file(category_property_dict)
    files_for_manual_addition(category_property_dict)
    #properties_to_file(properties)




if __name__ == '__main__':
    main()
