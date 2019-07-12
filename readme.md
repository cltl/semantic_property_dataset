# Compiling a dataset of concepts and properties


This repository contains the code used to compile the dataset described in this paper:

@inproceedings{sommerauer2019,
title={Towards interpretable, data-derived distributional meaning representations for reasoning: A dataset of properties and concepts},
author={Sommerauer, Pia and Fokkens, Antske and Vossen, Piek},
booktitle={Proceedings of the 10th Global WordNet Conference (GWC 2019)},
year={2019}
}


## Code structure

.
├── data
├── readme.md
├── scripts_lexical_information
├── scripts_process_raw_data
├── scripts_raw_data_extraction
├── scripts_sample_candidates
├── utils
└── wikipedia_corpus_data

## Stepts taken to compile the corpus

[this is work in progress - the documentation will be updated]

1.) add **raw data** resources to data:

`mkdir data/source_data`

add the following resources

- CSLB norms
- McRae norms
- quanitfied McRae norms
- crowd annotated McRae norms
- TonyVeale simile data

2.) Extract raw data

use scripts in ./scripts/raw_data_extraction/

3.) Get lexical information

use scripts in scripts_lexical_information

(+ additional resources necessary)

4.) Process raw data

use scripts in scripts_process_raw_data (requires some lexical information)

5.) Sample

use scripts in scripts_sample_candidates


Contact: pia.sommerauer@vu.nl


