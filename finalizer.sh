infile=$1
outfile=$2

echo "0,00;;;;;;000;0;;0;0;;;FEHLERZEILE" >> "$outfile" &&
cat "$infile" | 
	sed "/^.*;;;0,00;0,00;;0,00$/d" |
	awk -F\; '{print $10";;;;;;"$8";"$9";;"$3";"$6";;;"$4}' |
	sed -r "s/;;([0-9]{1,2})\.([0-9]{1,2})\.[0-9]{4};/;;\1\2;/" |
	tee >> "$outfile" &&
	echo "0,00;;;;;;000;0;;0;0;;;FEHLERZEILE" >> "$outfile"
