#! /bin/sh

filename=$1
outputfile=$2
if [ -z $1 ]	
then
	echo Argumente fehlen
	exit 1;
fi
pfad='/mnt/ramdisk/'
in2csv $filename > $pfad/work.csv
#cp test.csv work.csv
vim -c ":d" +:wq $pfad/work.csv #für hinzugefügte abcde.. benennung#
vim -c ":d" +:wq $pfad/work.csv #für freeline
vim -c ":g/Praxis, Export/d" +:wq $pfad/work.csv
vim -c ":g/Vetera GmbH Eltville am Rhein/d" +:wq $pfad/work.csv
vim -c ":d" +:wq $pfad/work.csv
vim -c ":g/Banken (APO Bank), Forderungen/d" +:wq $pfad/work.csv
vim -c ":g/Seite : /d" +:wq $pfad/work.csv
vim -c ":g/erstellt am : /d" +:wq $pfad/work.csv
vim -c ":d" +:wq $pfad/work.csv
vim -c ":d" +:wq $pfad/work.csv
line=$(wc -l < $pfad/work.csv)
vim -c ":1,$((line))s/,,//" +:wq $pfad/work.csv
vim -c ":g/Datum,Beschreibung,,/d" +:wq $pfad/work.csv
csvcut -c 1,2,4,5 $pfad/work.csv > $pfad/anfang.csv
csvcut -c 6 $pfad/work.csv > $pfad/Konto.csv
csvcut -c 7 $pfad/work.csv > $pfad/GKonto.csv
csvcut -c 8 $pfad/work.csv > $pfad/Brutto.csv
vim -c ":d" +:wq $pfad/Konto.csv
vim -c ":d" +:wq $pfad/GKonto.csv
vim -c ":d" +:wq $pfad/Brutto.csv
csvjoin -I $pfad/anfang.csv $pfad/Konto.csv $pfad/GKonto.csv $pfad/Brutto.csv > $pfad/roh.work.csv 
vim -c ":1,1s/a,b,c,d,a2,a2_2,a2_3/Datum,Beschreibung,Belegfeld1,Gesamt,Konto,Gegenkonto,Brutto/" +:wq $pfad/roh.work.csv 
csvcut -x $pfad/roh.work.csv > $outputfile
#totalln=$(grep -n Total roh.csv | sed "s/[^[0-9]//g")
#vim -c ":$((totalln)),$((line))//"
#rm $pfad/roh.work.csv $pfad/anfang.csv $pfad/Konto.csv $pfad/GKonto.csv $pfad/Brutto.csv $pfad/work.csv
