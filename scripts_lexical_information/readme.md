## Vocabulary exploration (LODCE dictionary)

1.) Extract lexical data with `get_vocab_data.py`

Extracts:

* number of wn synsets
* metaphorical in mipvu
* number of ontonotes sense groups
* number of navigli clusters
*  senses, polysemy and homnymy in lodce
* min wup similarity in wordnet
* abstract-concrete shift in wordnet
* whether a word is part of a metonymy-entity set


2.) Add sense distance data with `add_space_distances.py` (using the script `synset_distances.py`)

Adds the average distance of the monosemous synset neighbors to the polysemous word in the wikipedia sgns load_model.


Other scripts for explorations

* `analyze_polysemy`:
  investigate the relation between the average mon-synset neighbor to polysemous word distances in relation to the different types of polysemy according to the lodce dict: polysemy, homonymy (same pos), homonymy (different pos), monosemy + metaphor (MIPVU corpus)

* `polysemy_measure.py`
  experiment with different ways of measuring the degree of polysemy.

  Current suggestion:

      ** from the general distribution of synset similarities of a polysemous word, create three bins: low distance, medium distance, high distance [TO DO: investigate if these distances correspond to the different polysemy types (see above) ]
      ** measure polysemy in the following way: weigh relations by bin and merge relations if in 'low' bin (weights: low: 1, medium: 2, high: 3)
      e.g. syn1-syn2: low, syn2-syn3: medium, syn1-syn3: medium: 1 * 1 + 1 * 2 (the relations between syn2-syn3 and syn1-syn3 are merged) [TO DO: implement measure]
