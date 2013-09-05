#!/usr/bin/python
'''
This script finds phage tax discrepancies via panda dataframes
'''
#print __doc__
import os
import datetime
import pconfig
import pandas
from pandas import *
from datetime import datetime
from dateutil import parser

def main():

    wepay = pandas.read_csv("./csvFiles/wepay.csv")
    phage = pandas.read_csv("./csvFiles/phage.csv")
    
#    phage.index = phage["Entry Date"]
    wepay["Purchase Date"] = wepay["Purchase Date"].apply(lambda d: parser.parse(d))
    wepay.index = wepay["Purchase Date"]
    wepay = wepay.drop("Purchase Date", axis=1)

    wepay_taxcount =  wepay["Ticket"].value_counts()
    wepay_total = wepay_taxcount.sum()

    phage_taxcount = phage["Phage Camp Taxes"].value_counts()
    phage_taxindex = phage["Phage Camp Taxes"].unique()
    phage_sum = phage_taxcount['regular'] + phage_taxcount['TaxTransfer'] + phage_taxcount['Exemption Code']
    phage_paid= phage_taxcount['regular'] + phage_taxcount['TaxTransfer'] 

    print "ThePhage.org total attendees (including exempt): %s\n" % phage_sum    
    print "WePay Total Paid: %s" % wepay_total
    print "ThePhage.org total paid tax: %s \n" % phage_paid
    print "ThePhage.org Status Breakdown:\n%s\n" % phage_taxcount
    print "WePay Taxes:\n%s\n"  % wepay_taxcount

    if (wepay_total != phage_paid):
        if wepay_total > phage_paid:
            print "Entries on Wepay, but not on ThePhage.org: %s" % (wepay_total-phage_paid)
        else:
            print "Entries on ThePhage.org not on Wepay: %s" % (phage_paid-wepay_total)
    elif (wepay_total == phage_paid): 
        print "numbers reconciled on both Wepay and ThePhage.org"

    # find entries which are not registered on either site
    try:
        TaxTransfers = phage[phage["Phage Camp Taxes"].apply(lambda e: "TaxTransfer" in e)]
        regular = phage[phage["Phage Camp Taxes"].apply(lambda e: "regular" in e)]
        paid = phage[phage["Phage Camp Taxes"].apply(lambda e: "TaxTransfer" in e or "regular" in e)]

    except:
        pass


if __name__ == "__main__":
    main()



