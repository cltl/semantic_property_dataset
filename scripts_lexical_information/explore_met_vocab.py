import sys




def show_wn_dat(word, pos):

    with open(f'mip_met_vocab/{pos}-concepts-definitions.csv') as infile:
        for line in infile:
            #print(line)
            target_found = False
            word_lex = line.split('\t')[0].strip('"')
            if word_lex == word:
                print(line)
                target_found = True

            elif target_found:
                break




def main():

    word = sys.argv[1]
    pos = sys.argv[2]

    show_wn_dat(word, pos)



if __name__ == '__main__':
    main()
