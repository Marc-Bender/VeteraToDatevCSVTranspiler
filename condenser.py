#! /usr/bin/python3

import subprocess as sub
import re
import sys
import os.path
from decimal import *

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
        returnValue += str(self.field1) + ";"
        returnValue += str(self.total) + ";"
        returnValue += self.account + ";"
        returnValue += self.ref_account + ";"
        returnValue += str(self.brutto) + ";"
        returnValue += str(self.VAT) + ";;"
        returnValue += str(self.netto)
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

def condense(infileName, outfileName):
    infile = open(infileName,"r")
    outfile = open(outfileName, "w")
    linesOfInfile = infile.readlines()
    defaultInitializedAccountingLine = accountingLine("01.01.22",\
        "label",\
        123456,\
        12.34,\
        "account",\
        "ref_account",\
        56.78,\
        90.12,\
        34.56) # default initialization should be overwritten asap by algorithm only for defining an object of known type
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
                    (currentAccountingLine.date == previousAccountingLine.date)
                and (currentAccountingLine.label == previousAccountingLine.label)
                and (currentAccountingLine.field1 == previousAccountingLine.field1)
           ):
            if (
                        (currentAccountingLine.total == "")
                    and (currentAccountingLine.account == previousAccountingLine.account)
                    and (currentAccountingLine.ref_account == previousAccountingLine.ref_account)
               ):
                if (currentAccountingLine.brutto == ""):
                    currentAccountingLine.brutto = 0.00
                else:
                    pass

                if (previousAccountingLine.brutto == ""):
                    previousAccountingLine.brutto = 0.00
                else:
                    pass

                currentAccountingLine.brutto = float(str(currentAccountingLine.brutto).replace(",",".")) + float(str(previousAccountingLine.brutto).replace(",","."))
                currentAccountingLine.brutto = Decimal(str(currentAccountingLine.brutto)).quantize(Decimal("0.01"))
                
                if (currentAccountingLine.VAT == ""):
                    currentAccountingLine.VAT = 0.00
                else:
                    pass

                if (previousAccountingLine.VAT == ""):
                    previousAccountingLine.VAT = 0.00
                else:
                    pass

                currentAccountingLine.VAT = float(str(currentAccountingLine.VAT).replace(",",".")) + float(str(previousAccountingLine.VAT).replace(",","."))
                currentAccountingLine.VAT = Decimal(float(currentAccountingLine.VAT)).quantize(Decimal("0.01"))

                if (currentAccountingLine.netto == ""):
                    currentAccountingLine.netto = 0.00
                else:
                    pass

                if (previousAccountingLine.netto == ""):
                    previousAccountingLine.netto = 0.00
                else:
                    pass

                currentAccountingLine.netto = float(str(currentAccountingLine.netto).replace(",",".")) + float(str(previousAccountingLine.netto).replace(",","."))
                currentAccountingLine.netto = Decimal(float(currentAccountingLine.netto)).quantize(Decimal("0.01"))
                previousAccountingLine = currentAccountingLine
            else:
                if (previousAccountingLine != defaultInitializedAccountingLine):
                    outfile.write(previousAccountingLine.toCSV_String() + "\n")
                else:
                    pass
                previousAccountingLine = currentAccountingLine
        else:
            if (previousAccountingLine != defaultInitializedAccountingLine):
                outfile.write(previousAccountingLine.toCSV_String()+"\n")
            else:
                pass
            previousAccountingLine = currentAccountingLine

def main():
    if(len(sys.argv) != 3):
        print("Calling convention: condenser.py infile outfile")
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
        overwrite=input("Overwrite Outfile? (y/n) : ")
        if (
                (overwrite != "y")
             and(overwrite != "n")
           ):
            print("invalid answer, terminating")
            exit()
        elif (overwrite == "y"):
            pass
        else:
            print("Outfile exists and is not allowed to be overwritten, call again with different outfile")
    else:
        pass

    #if everything ok (program did not prematurely terminate
    infile = sys.argv[1]
    outfile = sys.argv[2]
    condense(infile,outfile)

main() # use call to main in production anything else otherwise
