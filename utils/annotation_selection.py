

def apply_selection(concept_dict_list):
    new_concept_dict_list = []
    positive_labels = ['1', '2']
    for n, concept_dict in enumerate(concept_dict_list):
        if 'selection' in concept_dict.keys():
            selection = concept_dict['selection']
            concept_dict.pop('selection')
            concept_dict['manual_coarse_grained'] = selection
            if selection in positive_labels:
                for concept_dict in concept_dict_list[n:]:
                    concept_dict['space_selection'] = True
                    if 'selection' in concept_dict.keys():
                        selection = concept_dict['selection']
                        concept_dict.pop('selection')
                        #print(concept_dict.keys())
                        concept_dict['manual_coarse_grained'] = selection
                        if selection == '':
                            concept_dict['manual_coarse_grained'] = '-'

                        new_concept_dict_list.append(concept_dict)
                    else:
                        concept_dict['manual_coarse_grained'] = selection
                        new_concept_dict_list.append(concept_dict)

                break
            else:
                concept_dict['space_selection'] = False
                concept_dict['manual_coarse_grained'] = selection
                new_concept_dict_list.append(concept_dict)
        else:
            concept_dict['manual_coarse_grained'] = '-'
            concept_dict['space_selection'] = False
            new_concept_dict_list.append(concept_dict)
    return new_concept_dict_list
