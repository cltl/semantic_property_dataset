import glob


def create_metonymy_list(data_dir_path):

    metonymy_set = set()
    met_files = glob.glob(f'{data_dir_path}/*metonymic*.txt')

    for f in met_files:
        with open(f) as infile:
            lines = infile.read().strip().split('\n')
        for line in lines:
            met = line.split('<SEP>')[0]
            metonymy_set.add(met)

    return metonymy_set


def main():

    data_dir_path = '../../../Data/metonymy/Minimalist-Location-Metonymy-Resolution/data'
    metonymy_set = create_metonymy_list(data_dir_path)
    print(len(metonymy_set))

    with open('../../../Data/metonymy/voc_from_minimalist.txt', 'w') as outfile:
        outfile.write('\n'.join(metonymy_set))


if __name__ == '__main__':
    main()
