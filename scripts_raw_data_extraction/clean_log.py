import json


# load_log

with open('log.json') as infile:
    search_dict_list = json.load(infile)

clean_list = []

for search_dict in search_dict_list:
    if search_dict['collection'] != 'perceptual' and search_dict['source'] == 'conceptnet':
        print('to remove')
        print(search_dict)
    else:
        clean_list.append(search_dict)

print(len(clean_list))
