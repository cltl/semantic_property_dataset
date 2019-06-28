COLLECTION=$1

python sort_examples.py $COLLECTION
python neighbor_extension.py $COLLECTION 
