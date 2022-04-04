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
    #define the constuctor which will construct such an object from the parameters in their correct data type (should be unused in production)
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
        regex = "^;;([0-9]{2}\.[0-9]{2}\.[0-9]{4};.*$"
        self.date = re.compile(regex).match(string).group(1)

def completify(infileName, outfileName):
    infile = open(infileName,"r")
    outfile = open(outfileName, "w")


#Example for class definition and testing of the types
#line = accountingLine("01.01.22",\
#        "label",\
#        123456,\
#        12.34,\
#        "account",\
#        "ref_account",\
#        56.78,\
#        90.12,\
#        34.56)
#print(line.netto);
def main():
    if(len(sys.argv) != 3):
        print("Calling convention: completifier.py infile outfile")
    elif not os.path.isfile(sys.argv[2]):
        print("infile not found")
    else:
        infile = sys.argv[2]
        outfile = sys.argv[3]
        completify(infile,outfile)

