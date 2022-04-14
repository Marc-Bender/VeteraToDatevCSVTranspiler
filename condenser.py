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
    def __init__(self):
        pass
    def toCSV_String(self):
        returnValue = ";;"
        returnValue += self.date + ";"
        returnValue += self.label + ";;"
        returnValue += str(self.field1) + ";"
        returnValue += str(self.total).replace(".",",") + ";"
        returnValue += self.account + ";"
        returnValue += self.ref_account + ";"
        returnValue += str(self.brutto).replace(".",",") + ";"
        returnValue += str(self.VAT).replace(".",",") + ";;"
        returnValue += str(self.netto).replace(".",",")
        return returnValue
        
    def fromCSV_String(self,string):
        regexDate = "([0-9]{0,2}\.{0,1}[0-9]{0,2}\.{0,1}[0-9]{0,4})"
        regexLabel = "([^;]*)"
        regexField1 = "([^;]*)"
        regexTotal = "([0-9,]*)"
        regexAccount = "([^;]*)"
        regexRefAcc = "([^;]*)"
        regexBrutto = "([-]{0,1}[0-9,]*)"
        regexVAT = "([-]{0,1}[0-9,]*)"
        regexNetto = "([-]{0,1}[0-9,]*)"
        
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
            self.total       = matches.group(4).replace(",",".")
            self.account     = matches.group(5)
            self.ref_account = matches.group(6)
            self.brutto      = matches.group(7).replace(",",".")
            self.VAT         = matches.group(8).replace(",",".")
            self.netto       = matches.group(9).replace(",",".")
            if (self.brutto == ""):
                self.brutto = 0.00
            else:
                pass

            if (self.VAT == ""):
                self.VAT = 0.00
            else:
                pass

            if (self.netto == ""):
                self.netto = 0.00
            else:
                pass

            self.brutto = Decimal(float(str(self.brutto))).quantize(Decimal("0.01"))
            self.VAT    = Decimal(float(str(self.VAT))).quantize(Decimal("0.01"))
            self.netto  = Decimal(float(str(self.netto))).quantize(Decimal("0.01"))
        else:
            print("input line misformed (was " + string +" )")
            exit()

def condense(infileName, outfileName):
    infile = open(infileName,"r")
    outfile = open(outfileName, "w")
    linesOfInfile = infile.readlines()
    defaultInitializedAccountingLine = accountingLine() 
    previousAccountingLine = accountingLine() 
    lengthOfFile = len(linesOfInfile)
    i = 0
    while i < lengthOfFile:
        currentAccountingLine = [accountingLine()] 
        currentAccountingLine[0].fromCSV_String(linesOfInfile[i]) 
        continueBuffering = 1
        numOfBufferedLines = 0
        while (
                        (i<lengthOfFile-1)
                    and (continueBuffering == 1)
              ):
            buffer = accountingLine()
            buffer.fromCSV_String(linesOfInfile[i+1])
            if (
                        (buffer.date == currentAccountingLine[0].date)
                   and  (buffer.label == currentAccountingLine[0].label)
                   and  (buffer.field1 == currentAccountingLine[0].field1)
               ):
                currentAccountingLine.append(buffer)
                numOfBufferedLines += 1
                continueBuffering = 1
                i += 1
            else:
                continueBuffering = 0


        wasIndexMatched = [0]*(numOfBufferedLines+1)
        wasIndexMatched[0] = 1 # the first entry is always matched since it will be kept if nothing else matches it
        for j in range(0,numOfBufferedLines+1):
            for k in range(j,numOfBufferedLines+1):
                if (
                            (j != k)
                        and (wasIndexMatched[k] == 0)
                        and (currentAccountingLine[j].total == "")
                        and (currentAccountingLine[j].account == currentAccountingLine[k].account)
                        and (currentAccountingLine[j].ref_account == currentAccountingLine[k].ref_account)
                   ):
                    currentAccountingLine[j].brutto += currentAccountingLine[k].brutto
                    currentAccountingLine[j].netto += currentAccountingLine[k].netto
                    currentAccountingLine[j].VAT += currentAccountingLine[k].VAT
                    wasIndexMatched[k] = 1
                else:
                    pass 
            if (
                       (j == 0)
                    or (wasIndexMatched[j] == 0)
               ):
                outfile.write(currentAccountingLine[j].toCSV_String() + "\n")
        
        i += 1

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
