SCORE=$1

MRCPATH=../../../Data/psych_ling_data/mrc/1054
WORDSPATH=./../data/vocab/lemmas.txt
TARGET=./../data/mrc_data/$1.csv


java -classpath ./jmrc.jar jmrc.Example $MRCPATH $WORDSPATH $SCORE > $TARGET
