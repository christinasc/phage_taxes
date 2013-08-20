#!/usr/bin/python
import csv, os, errno
import argparse

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

def read_header(aReader):  # get row 0
    a_rownum = 0
    a_header = []
    for row in aReader:        # Save header row.
        if a_rownum == 0:
            a_header = row
        a_rownum +=1
    return a_header

def gen_dict(aDict, aHeader): # identify columns we're interested in 
    header_colnum = 0
    for column in aHeader:
        for key in aDict: 
            if key in column:
                aDict[key] = header_colnum
        header_colnum +=1


def get_headerInfo(aDict, csvfile): # figure out where are the columns that matter
    ifile  = open(csvfile, "rb")
    reader = csv.reader(ifile)
    header = read_header(reader)
    gen_dict(aDict, header)
    ifile.close()


def create_cleanFile(aDict, csv_in, csv_out, param):  # grab regular camp tax entries only 
    taxType = ( "regular", "Exemption Code", "TaxTransfer", "Paid",  "")
    ifile  = open(csv_in, "rb")
    with ifile as source: 
        rdr = csv.reader(source)
        with open(csv_out, "wb") as result: 
            wtr= csv.writer(result)
#            print param
            if param == taxType[0]: #regular tax
                in_iter = ((r[int(aDict['First'])],
                            r[int(aDict['Last'])],                            
                            r[int(aDict['Email'])]) for r in rdr if param in r[int(aDict['Phage Camp Taxes'])]) 
            elif param == taxType[1]: # exempt
                in_iter = ((r[int(aDict['First'])],
                            r[int(aDict['Last'])],                           
                            r[int(aDict['Email'])]) for r in rdr if param in r[int(aDict['Phage Camp Taxes'])])
            elif param == taxType[2]: # tax transfer
                in_iter = ((r[int(aDict['First'])],
                            r[int(aDict['Last'])],                      
                            r[int(aDict['Email'])],
                            r[int(aDict['Tax Transfer'])]) for r in rdr if param in r[int(aDict['Phage Camp Taxes'])])
            elif param == taxType[3]: # invoice
                in_iter = ((r[int(aDict['Customer Name'])],
                            r[int(aDict['Email'])],
                            r[int(aDict['Status'])]) for r in rdr if param in r[int(aDict['Status'])])
            elif param == taxType[4]: # wepay
                in_iter = ((r[int(aDict['First'])],
                            r[int(aDict['Last'])],
                            r[int(aDict['Email'])]) for r in rdr if "First Name" not in r[int(aDict['First'])])
                           
            wtr.writerows(in_iter)
    
    ifile.close()


def wepay_invoice(csv_invoice, notPaid):
    ifile  = open(csv_invoice, "rb")
    invoice = csv.reader(ifile)
    invoice_list =[]
    for row in invoice:
        invoice_list.append(row)

        if invoice_list is not None:           
            invoice_names = []
            for row in invoice_list:
                (first_name, last_name) = row[0].split(" ")
                invoice_names.append([first_name, last_name])
            for each in notPaid:    # compare to notPaid, and remove from notPaid if match
                name_only = each[0:2]
                if name_only in invoice_names:                    
                    #print "match %s" % name_only
                    notPaid.remove(each)
    return notPaid



def tax_transfer(csv_transfer):
    ifile  = open(csv_transfer, "rb")
    transfer = csv.reader(ifile)
    tlist =[]
    for row in transfer:
        tlist.append(row)
    return tlist

    
def tax_exempt(csv_exempt):
    ifile  = open(csv_exempt, "rb")
    exempt = csv.reader(ifile)
    total_exempt =0
    for row in exempt:
        total_exempt +=1
    ifile.close()
    return total_exempt
    

def tax_missing(csv_phage, csv_wepay):
    ifile  = open(csv_phage, "rb")
    phage = csv.reader(ifile)
    wfile  = open(csv_wepay, "rb")
    wepay = csv.reader(wfile)
    
    firstname = []
    lastname = []
    emails = []
    notPaid = []

    for row in wepay:         
        # print row
        firstname.append(row[0].title().strip())
        lastname.append(row[1].title().strip())
        emails.append(row[2])

    a_rownum = 0
    for row in phage:
        if row[0].title().strip() not in firstname:
            if row[1].title().strip() not in lastname:
                notPaid.append(row)
        a_rownum += 1
                
    ifile.close()
    wfile.close()
    return notPaid


def reg_missing(csv_phage, csv_wepay):
    ifile  = open(csv_phage, "rb")
    phage = csv.reader(ifile)
    wfile  = open(csv_wepay, "rb")
    wepay = csv.reader(wfile)
    
    firstname = []
    lastname = []
    emails = []

    notRegistered = []
    notPaid = []

    for row in phage:         
        # print row
        firstname.append(row[0].title().strip())
        lastname.append(row[1].title().strip())
        emails.append(row[2])

    a_rownum = 0
    for row in wepay:
        if row[0].title().strip() not in firstname:
            if row[1].title().strip() not in lastname:
                notRegistered.append(row)
        a_rownum += 1        

    ifile.close()
    wfile.close()
    return notRegistered


def duplicate_reg(csv_phage, csv_wepay):
    ifile  = open(csv_phage, "rb")
    phage = csv.reader(ifile)
    emails = []
    for row in phage:
        emails.append(row[2])
    ifile.close()
    diff, total = test_distinct(emails)
    dup_emails = get_duplicate_entry(emails)
    ifile.close()
    return diff, total, dup_emails
    

def get_duplicate_entry(input):
  unique_output = []
  output = []
  for x in input:
    if x not in unique_output:
        unique_output.append(x)
    else:
        output.append(x)
  return output


## identify duplicates in phage csv
def test_distinct(mylist): 
    distinct = list(set(mylist))
    d_num = len(distinct)
    l_num = len(mylist)
    diff = l_num-d_num
    return (diff, l_num)


def main(): 

    phageDict = { 'First': 'X', 
                  'Last': 'X', 
                  'Email':'X', 
                  'Phage Camp Taxes': 'X'
                  }

    exemptDict = { 'First': 'X', 
                  'Last': 'X', 
                  'Email':'X', 
                  'Phage Camp Taxes': 'X',
                  'Exemption Code': 'X'
                  }

    transferDict = { 'First': 'X', 
                     'Last': 'X', 
                     'Email':'X', 
                     'Phage Camp Taxes': 'X',
                     'Tax Transfer': 'X'
                     }

    invoiceDict = { 'Customer Name': 'X', 
                    'Email':'X',
                    'Status':'X'
                    }


    parser = argparse.ArgumentParser()

#  "Usage: mtax_comparator.py [--inv=invoice_csv] phage_csv wepay_csv "

    parser.add_argument("phage_csv")
    parser.add_argument("wepay_guest_csv")

    parser.add_argument("--inv", dest="wepay_invoice_csv", required=False)

    args = parser.parse_args() 

    phage_csv = args.phage_csv
    wepay_csv = args.wepay_guest_csv
    
    wepayinv_csv = args.wepay_invoice_csv
    
    dir_csv = "csv/"
    mkdir_p(dir_csv)

    new_phage_csv = dir_csv + 'new_phage.csv'
    new_wepay_csv = dir_csv + 'new_wepay.csv'
    new_exempt_csv = dir_csv + 'new_exempt.csv'
    new_transfer_csv = dir_csv + 'new_transfer.csv'
    new_invoice_csv = dir_csv + 'new_invoice.csv'


    get_headerInfo(invoiceDict, wepayinv_csv)
    # print "Invoice Dict: %s" %  invoiceDict
    create_cleanFile(invoiceDict, wepayinv_csv, new_invoice_csv, "Paid")

    get_headerInfo(phageDict, phage_csv)
    create_cleanFile(phageDict, phage_csv, new_phage_csv, "regular")
    # print "Phage Dict: %s" %  phageDict

    # tax transfers
    get_headerInfo(transferDict, phage_csv)
    create_cleanFile(transferDict, phage_csv, new_transfer_csv, "TaxTransfer")
    #    print "Transfer Dict: %s" %  transferDict

    # this line must go before getHeaderInfo for wepay, because it uses phageDict from phage
    get_headerInfo(exemptDict, phage_csv)
    #    print "Exempt Dict: %s" %  exemptDict
    create_cleanFile(exemptDict, phage_csv, new_exempt_csv, "Exemption Code")

    get_headerInfo(phageDict, wepay_csv) # update phageDict for WePay
    create_cleanFile(phageDict, wepay_csv, new_wepay_csv, "")
    ## print "Wepay Dict: %s" %  phageDict

    transfers = tax_transfer(new_transfer_csv)

    ## who is tax exempt?  
    exempt = tax_exempt(new_exempt_csv)

    ## who hasn't paid tax?  - case independent
    notPaid = tax_missing(new_phage_csv, new_wepay_csv)

    ## check invoices against notPaid
    if wepayinv_csv is not None:
        #print "NOT Paid array %s" % str(notPaid)
        notPaid = wepay_invoice(new_invoice_csv, notPaid)

    # print "cleaned Not Paid array %s :" % str(notPaid)        

    ## who has not registered but paid tax?  - case independent
    notRegistered = reg_missing(new_phage_csv, new_wepay_csv)
    rnum = len(notRegistered)

    ## find and show any duplicate registration on ThePhage.org
    dupNum, total_entries, dup_emails  = duplicate_reg(new_phage_csv, new_wepay_csv)

    regularTax = total_entries - dupNum

    regular_transfers = regularTax + len(transfers)

    totalCampers =  exempt + regular_transfers


    print "\n ****** This is an Automatically Generated Email. *******\n " 

    # print number of campers
    print "=============================="
    print "Total Number of Campers: %s " % totalCampers
    print "Exempt: %s " % exempt
    print "Regular + Transfers: %s " % regular_transfers
    ### TODO: Add persons to total head count if "paid tax, not registered, 
    ### but omit them if they are a tax transfer"

    # print thephage.org stats
    print "=============================="
    print "Regular Camp Tax Entries on ThePhage.org : %s" % total_entries
    print "Tax Transfers: %s " % len(transfers)
    print "Registered on The Phage, not Paid : %s" % len(notPaid)
    print "Paid Tax, not Registered : %s" % rnum
    print "==============================\n"

    # print unpaid tax
    print "Camp Tax Not Paid, but Registered on ThePhage.org"
    print "Go here to pay tax: https://www.wepay.com/events/phagecamp"
    print "Total: %s " % len(notPaid)

    print "=============================="
    for row in notPaid:
        print "%s %s, %s" % (row[0], row[1], row[2])
    print ""


    print "=============================="
    # print tax transfer stats
    print "Tax Transfers: %s" % str(len(transfers))
    for row in transfers:
        print "%s %s, %s --Source->  %s" % (row[0].strip(), row[1].strip(), row[2].strip(), row[3].strip())
    print "=============================="


    # print not registered on thephage.org
    print "\n"
    print "Not Registered on http://ThePhage.org, but paid on WePay"
    print "Total: %s " % len(notRegistered)
    print "=============================="
    for row in notRegistered:
        print "%s %s, %s" % (row[0], row[1], row[2])
    print "\n"

    # print duplicate entries on thephage.org
    if (dupNum != 0):
        print "ThePhage.org directory has the following Duplicate Entries:"
        print "============================================================"
        print " %s " %  dup_emails
        print "\nDistinct Entries on ThePhage.org for Regular Tax: %s" % d_num    
    else: 
        print "ThePhage.org directory has No Duplicates. Yay!"
        print "================================================"

    
    print "\n"
    os.system('date')
    print "\n"


    # print csv file usage
'''
    print "\n"
    print "Using the following CSV files:"
    print(phage_csv)
    print(wepay_csv)
    if wepayinv_csv is None:
        print "No invoice file, that's OK. "
    else:
        print(wepayinv_csv)
'''





if __name__ == '__main__':
    main()


