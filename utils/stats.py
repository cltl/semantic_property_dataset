from scipy.stats import pearsonr
from scipy.stats import spearmanr
import numpy as np


def get_correlations(word_dict_list, senses1, senses2):

    senses1_list = [int(wd[senses1]) for wd in word_dict_list]
    senses2_list = [int(wd[senses2]) for wd in word_dict_list]

    senses1_np = np.array(senses1_list)
    senses2_np = np.array(senses2_list)

    coeff, pvalue = pearsonr(senses1_np, senses2_np)
    coeff_sp, pvalue_sp = spearmanr(senses1_np, senses2_np)
    return coeff, pvalue, coeff_sp, pvalue_sp
