mkNum_infile=$1
mkNum_accountsFile=$2
mkNum_outFile=$3

if [ -f "$mkNum_infile" ];
then
	if [ -f "$mkNum_accountsFile" ];
	then
		cat "$mkNum_accountsFile" |
			sed "s/^/sed \"s\/;/ " |
			sed "s/;;/\/;/" |
			sed "s/$/\/g\"/" |
			sed "s/$/ \|/" > "script_""$mkNum_accountsFile"".sh" &&
				echo tee >> "script_""$mkNum_accountsFile"".sh" &&
				cat "$mkNum_infile" |
					./"script_""$mkNum_accountsFile"".sh" > "$mkNum_outFile" &&
				rm "script_""$mkNum_accountsFile"".sh"
	else
		echo Accountsfile not existing
	fi
else
	echo Infile not existing
fi
