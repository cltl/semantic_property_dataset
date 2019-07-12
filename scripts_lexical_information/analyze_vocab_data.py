import sys
import matplotlib.pyplot as plt
import numpy as np

sys.path.append('../utils/')
from data_utils import load_full_ldoce_data




def get_distribution(ldoce_data_dict_list, feature):

    values = [float(d[feature]) for d in ldoce_data_dict_list if d[feature] != 'None']
    frequency, bins = np.histogram(values, bins = 3, )
    print(bins)

    plt.hist(values, bins = 3)
    plt.gca().set(title='Frequency Histogram', ylabel='frequency', xlabel=feature)
    plt.show()

    #for b, f in zip(bins[1:], frequency):
    #    print(round(b, 1), ' '.join(np.repeat('*', f)))



def main():

    feature = sys.argv[1]

    ldoce_data_dict_list = load_full_ldoce_data()

    get_distribution(ldoce_data_dict_list, feature)

if __name__ == '__main__':
    main()
