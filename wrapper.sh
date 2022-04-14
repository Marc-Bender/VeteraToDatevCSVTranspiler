#! /usr/bin/bash

infile=$1 # the raw unprocessed file to be converted
accountsFile=$2 # translation file from text accounts to numeric accounts
outfile=$3 # the final import ready file

if [ -f "$infile" ];
then
	if [ -f "$accountsFile" ];
	then
		if [ -f "$outfile" ];
		then
			echo "Overwriting the outfile is not supported"
		else
			echo "Preprocessing..." &&
			./preprocess.sh "$infile" > "pre_""$infile" &&
			echo "    ... done" &&
			echo "Completing..." &&
			./completifier.py "pre_""$infile" "comp_""$infile" &&
			echo "    ... done" &&
			rm "pre_""$infile" &&
			echo "Condensing..." &&
			./condenser.py "comp_""$infile" "cond_""$infile" &&
			echo "    ... done" &&
			rm "comp_""$infile" &&
			echo "Preparing Accountsfile ..." &&
			./preprocess.sh "$accountsFile" > "pre_""$accountsFile" &&
			echo "    ... done" &&
			echo "Making Accounts numeric..." &&
			./makeNumeric.sh "cond_""$infile" "pre_""$accountsFile" "num_""$infile" &&
			echo "    ... done" &&
			rm "cond_""$infile" && 
			rm "pre_""$accountsFile" &&
			echo "Finalizing..." &&
			./finalizer.sh "num_""$infile" "$outfile" &&
			echo "    ... done" &&
			rm "num_""$infile"
		fi
	else
		echo "Accounts file does not exist"
	fi
else
	echo "Infile does not exist"
fi	
	

