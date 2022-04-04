#! /usr/bin/python3

import subprocess as sub
import re
import sys
import os.path

class accountingLine:
    date: str = ""
    label: str = ""
    field1: int = 0
    total: float = 0.0
    account: str = ""
    ref_account: str = ""
    brutto: float = 0.0
    VAT: float = 0.0
    netto: float = 0.0
    #define the constuctor which will construct such an object from the parameters in their correct data type (should be unused in production, apart from default initializations maybe)
    def __init__(self,date, label, field1, total, account, ref_account, brutto, VAT, netto):
        self.date = date
        self.label = label
        self.field1 = field1
        self.total = total
        self.account = account
        self.ref_account = ref_account
        self.brutto = brutto
        self.VAT = VAT
        self.netto = netto
    def fromCSV_String(self,string):
        #        ";;<DATE><DATE><DATE><DATE><DATE>;<Label>;;<field1>;<total><total> ; "
        regex = "^;;([0-9]{2}\.[0-9]{2}\.[0-9]{4});([^;]*);;([0-9]*);([0-9]*[,0-9]*);.*$"
        self.date = re.compile(regex).match(string).group(1)
        self.label = re.compile(regex).match(string).group(2)
        self.field1 = re.compile(regex).match(string).group(3)
        self.total = re.compile(regex).match(string).group(4)

def completify(infileName, outfileName):
    infile = open(infileName,"r")
    outfile = open(outfileName, "w")
    linesOfInfile = infile.readLines()
    previousAccountingLine = accountingLine("01.01.22",\
        "label",\
        123456,\
        12.34,\
        "account",\
        "ref_account",\
        56.78,\
        90.12,\
        34.56) # default initialization should be overwritten asap by algorithm only for defining an object of known type
    for line in linesOfInfile:
        currentAccountingLine = accountingLine.fromCSV_String(line) # create a new accountingLine object from the current line so that we can afterwards check if any fields are empty and then need to be reused from the previous line
        

def main():
    if(len(sys.argv) != 3):
        print("Calling convention: completifier.py infile outfile")
    elif not os.path.isfile(sys.argv[2]):
        print("infile not found")
    else:
        infile = sys.argv[2]
        outfile = sys.argv[3]
        completify(infile,outfile)

#main() # use call to main in production anything else otherwise
#Example for class definition and testing of the types
line = accountingLine("01.01.22",\
        "label",\
        123456,\
        12.34,\
        "account",\
        "ref_account",\
        56.78,\
        90.12,\
        34.56)
#print(line.netto);
line.fromCSV_String(";;03.01.2022;Musterfrau, Marianne, Musterhausen, 17155/03.01.2022 (MED_ABG_0% );;171552;28,62;;;;;;")
print(line.date)
print(line.label)
print(line.field1)
print(line.total)
