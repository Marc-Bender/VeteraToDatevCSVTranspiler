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
    def toCSV_String(self):
        returnValue = ";;"
        returnValue += self.date + ";"
        returnValue += self.label + ";;"
        returnValue += self.field1 + ";"
        returnValue += self.total + ";"
        returnValue += self.account + ";"
        returnValue += self.ref_account + ";"
        returnValue += self.brutto + ";"
        returnValue += self.VAT + ";;"
        returnValue += self.netto 
        return returnValue
        
    def fromCSV_String(self,string):
        regexDate = "([0-9]{0,2}\.{0,1}[0-9]{0,2}\.{0,1}[0-9]{0,4})"
        regexLabel = "([^;]*)"
        regexField1 = "([^;]*)"
        regexTotal = "([0-9,]*)"
        regexAccount = "([^;]*)"
        regexRefAcc = "([^;]*)"
        regexBrutto = "([0-9,]*)"
        regexVAT = "([0-9,]*)"
        regexNetto = "([0-9,]*)"
        
        regex = "^;;" + \
                regexDate + ";"+\
                regexLabel+";;"+\
                regexField1+";"+\
                regexTotal+";"+\
                regexAccount+";"+\
                regexRefAcc+";"+\
                regexBrutto+";"+\
                regexVAT+";;"+\
                regexNetto+\
                ".*$"
        matches = re.compile(regex).match(string)

        if matches:
            self.date        = matches.group(1)
            self.label       = matches.group(2)
            self.field1      = matches.group(3)
            self.total       = matches.group(4)
            self.account     = matches.group(5)
            self.ref_account = matches.group(6)
            self.brutto      = matches.group(7)
            self.VAT         = matches.group(8)
            self.netto       = matches.group(9)
        else:
            print("input line misformed (was " + string +" )")
            exit()

def completify(infileName, outfileName):
    infile = open(infileName,"r")
    outfile = open(outfileName, "w")
    linesOfInfile = infile.readlines()
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
        currentAccountingLine = accountingLine("01.01.22",\
            "label",\
            123456,\
            12.34,\
            "account",\
            "ref_account",\
            56.78,\
            90.12,\
            34.56) # default initialization should be overwritten asap by algorithm only for defining an object of known type
        currentAccountingLine.fromCSV_String(line) # fill the previously created currentaccountingLine object from the current line so that we can afterwards check if any fields are empty and then need to be reused from the previous line
        if (
                    (currentAccountingLine.date != "")
                and (currentAccountingLine.label != "")
                and (currentAccountingLine.field1 != "")
           ):
            # is start of new accounting line... the old line must be replaced with this one
            previousAccountingLine = currentAccountingLine
            # also there is obviously nothing to complete here
        else:
            # line with decomposition of existing accounting line
            # information from above lines can be reused
            currentAccountingLine.date = previousAccountingLine.date
            currentAccountingLine.label = previousAccountingLine.label
            currentAccountingLine.field1 = previousAccountingLine.field1
            currentAccountingLine.total = ""
        outfile.write(currentAccountingLine.toCSV_String()+"\n")

def main():
    if(len(sys.argv) != 3):
        print("Calling convention: completifier.py infile outfile")
        exit()
    else:
        pass

    if  (
                (not os.path.isfile(sys.argv[1]))
            or  (
                       (os.path.isfile(sys.argv[1]))
                    and(re.compile("^.*\.(.*)$").match(sys.argv[1]).group(1) != "csv")
                )
        ):
        print("infile not found or invalid (was "+sys.argv[1]+")")
        exit()
    else:
        pass

    if os.path.isfile(sys.argv[2]):
        print("outfile would be overwritten, can not do that yet")
        exit()
    else:
        pass

    #if everything ok (program did not prematurely terminate
    infile = sys.argv[1]
    outfile = sys.argv[2]
    completify(infile,outfile)

main() # use call to main in production anything else otherwise
#Example for class definition and testing of the types
#line = accountingLine("01.01.22",\
#       "label",\
#       123456,\
#       12.34,\
#       "account",\
#       "ref_account",\
#       56.78,\
#       90.12,\
#       34.56)
#line.fromCSV_String(";;03.01.2022;Musterfrau, Marianne, Musterhausen, 17155/03.01.2022 (MED_ABG_0% );;171552;28,62;;;;;;")
#print("date = " + line.date)
#print("label = " + line.label)
#print("field1 = " + line.field1)
#print("total = " + line.total)
#print("account = " + line.account)
#print("ref_account = " + line.ref_account)
#print("brutto = " + line.brutto)
#print("VAT = " + line.VAT)
#print("netto = " + line.netto)


