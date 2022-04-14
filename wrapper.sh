#! /usr/bin/bash

infile=$1 # the raw unprocessed file to be converted
accountsFile=$2 # translation file from text accounts to numeric accounts
outfile=$3 # the final import ready file

if [ -f "$infile" ];
then
	if [ -f "$accountsFile" ];
	then
		./preprocess.sh "$infile" > "pre_""$infile" &&
		./completifier.py "pre_""$infile" "comp_""$infile" &&
		rm "pre_""$infile" &&
		./condenser.py "comp_""$infile" "cond_""$infile" &&
		rm "comp_""$infile" &&
		./preprocess.sh "$accountsFile" > "pre_""$accountsFile" &&
		./makeNumeric.sh "cond_""$infile" "pre_""$accountsFile" "num_""$infile" &&
		rm "cond_""$infile" && 
		rm "pre_""$accountsFile" &&
		rm "script_pre_""$accountsFile"".sh" &&
		echo "Done" # place holder for next command
	else
		echo "Accounts file does not exist"
	fi
else
	echo "Infile does not exist"
fi	
	

