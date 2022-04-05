#! /usr/bin/bash

infile=$1 # the raw unprocessed file to be converted
outfile=$2 # the final import ready file

./preprocess.sh $infile > $infile_pre &&
	./completifier.py $infile_pre $infile_comp &&
	rm $infile_pre &&
	echo "Done" # place holder for next command
	

