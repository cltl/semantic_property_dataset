# Compiling a dataset of concepts and properties


This repository contains the code used to compile the dataset described in this paper:

@inproceedings{sommerauer2019,
title={Towards interpretable, data-derived distributional meaning representations for reasoning: A dataset of properties and concepts},
author={Sommerauer, Pia and Fokkens, Antske and Vossen, Piek},
booktitle={Proceedings of the 10th Global WordNet Conference (GWC 2019)},
year={2019}
}


## Code structure

Directories with data:

* `./data/`
* `./wirkipedia_corpus_data`

Directories with scripts for data extration:

* `./scripts_raw_data_extraction`
* `./scripts_process_raw_data`
* `./scripts_lexical_information/`
* `./scripts_sample_candidates`
* `./utils`



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


2.1 To extract data, run:
`cd scripts_raw_data_extraction/`
`get_concepts.py [collection_name] [extract_fixed_again (yes/no)]``

3.) Extract lexical data:

3.1 Get list of words in LDOCE dictionary and store in `'../data/vocab/all_lodce.csv'`
3.2 Run the following scripts to add information:

`cd scripts_lexical_information/`
* `get_mrc_data.sh`
* `python add_mrc_data.py`
* `python get_mipvu_vocab.py`

3.3 Add extracted data to vocab:

* `python get_vocab_data.py`

4.) Process the raw data and extend them with neighbors from the distributional space

4.1 To sort the extracted data and extend them with neighbors, run:
`cd scripts_process_raw_data/`
`sh process1.sh [collection]`


4.2 Annotate data:

`cd data/data_for_concept_selection_cosine_centroid/[collection]`

Annotate the concepts you want to keep by opening the file called `[property]_selection.csv`:
Add '1' for the first concept you want to include (you do not need to annotated the rest). The idea is to find the positive example furthest away from the centroid (which should be most difficult for a classifier). Everything closer to the centroid should be included, everything further away excluded.

4.3 Add lexical data to the selected data by running:

`cd scripts_process_raw_data/`
`sh process2.sh [collection]`


5.) Sample candidates for annotation

`cd scripts_sample_candidates/`
`sh get_sampled_crowd_input.sh`


Contact: pia.sommerauer@vu.nl
