#! /usr/bin/bash

infile=$1 # the raw unprocessed file to be converted
outfile=$2 # the final import ready file

if [ -f "$infile" ];
then
	./preprocess.sh "$infile" > "pre_""$infile" &&
	./completifier.py "pre_""$infile" "comp_""$infile" &&
	rm "pre_""$infile" &&
	echo "Done" # place holder for next command
else
	echo "Infile does not exist"
fi	
	

