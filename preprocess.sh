infile=$1
cat "$infile" |
	sed '/^;*$/d' | # delete lines only containing semicolons (effectively blank lines)
       	sed '/^.*Praxis, Export nach Vetera, .*$/d' | # delete header lines
	sed '/^Banken (APO Bank), Forderungen (.*$/d' | # delete explanatory line with all kinds of virtual accounts (used in accounting)
	sed '/^.*Seite : .*$/d' | # delete pagenumbering
	sed '/^.*erstellt am : .*$/d' | # delete export date
	sed '/^.*Datum;Beschreibung;.*$/d' # delete header line

