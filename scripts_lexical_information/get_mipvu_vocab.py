from lxml import etree
from collections import defaultdict



def load_mipvu_metaphors(path):

    met_dict = defaultdict(set)
    pos_type_counts = defaultdict(set)

    tree = etree.parse(path)
    root = tree.getroot()
    text = root.find('{http://www.tei-c.org/ns/1.0}text')
    group = text.find('{http://www.tei-c.org/ns/1.0}group')
    documents = group.getchildren()
    for doc in documents:
        body = doc.find('{http://www.tei-c.org/ns/1.0}body')
        for part in body.getchildren():
            #print(part.tag)
            #print(len(part.getchildren()))
            for textpart in part.getchildren():
                #print(textpart.tag)
                #print(len(textpart.getchildren()))
                for sentence in textpart.getchildren():
                    for tok in sentence.getchildren():
                        if tok.getchildren():
                            for add in tok.getchildren():
                                if 'function' in add.attrib and 'type' in add.attrib:
                                    if add.attrib['function'] == 'mrw' and add.attrib['type'] == 'met':
                                        met_dict[tok.attrib['lemma']].add('met')
                                        if 'type' in tok.attrib:
                                            pos = tok.attrib['type']
                                            pos_mapped = pos_tag_mapping(pos)
                                            pos_type_counts[pos_mapped].add(tok.attrib['lemma'])


                        else:
                            if 'lemma' in tok.attrib:
                                met_dict[tok.attrib['lemma']].add('non-met')


    return met_dict, pos_type_counts

def met_voacb_to_file(met_vocab):

    with open('wordlists/mipvu_metaphor_words.csv', 'w') as outfile:
        outfile.write('word,annotations\n')
        for word, annotations in met_vocab.items():
            outfile.write(f'{word},{" ".join(sorted(list(annotations)))}\n')
    #       outfile.write('\n'.join(met_vocab))


def pos_tag_mapping(pos):

    if pos.startswith('N'):
        pos_mapped = 'n'
    elif pos.startswith('V'):
        pos_mapped = 'v'
    elif pos.startswith('AJ'):
        pos_mapped = 'a'
    else:
        pos_mapped = 'other'

    return pos_mapped

def main():
    path = '../../../Data/mipvu/corpus/VUAMC.xml'
    met_vocab, pos_type_counts = load_mipvu_metaphors(path)
    met_voacb_to_file(met_vocab)

    for pos, types in pos_type_counts.items():
        print(pos, len(types))





if __name__ == '__main__':
    main()
