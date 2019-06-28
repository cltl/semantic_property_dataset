How to clean the extracted data:

For all scripts: use the name of the collection you want to process as input argument. Possible collection names are:

* perceptual
* activities
* parts
* complex

Run the scripts in the following sequence:

1.) `sort_examples.py [collection name]`
XXX merged with 3 2.) `exclude_oov.py [collection name]`
3.) `neighbor_extension.py [collection name]`
5.) Manually annotate the furthest positive example from the centroid in the files `../data/data_for_concept_selection_cosine_centroid/[collection]/[properity].csv`:
(a) copy file and save new file under `../data/data_for_concept_selection_cosine_centroid/[collection]/[properity]_selected.csv`
(b) Go through farthest examples from the centroid and look for the first positive one. Label it as 'pos' in the column entitled 'selection'. Save the changes and move on to the next file.
6.) `get_word_data.py [collection name]`
8.)  [`create_crowd_input.py [collection name]`] --> moved to sampling step 
