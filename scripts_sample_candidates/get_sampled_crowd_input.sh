

N=180


python get_bins.py

python sample.py perceptual None $N
python sample.py activities None $N
python sample.py complex None $N
python sample.py parts None $N


python create_crowd_input.py perceptual
python create_crowd_input.py activities
python create_crowd_input.py complex
python create_crowd_input.py parts
