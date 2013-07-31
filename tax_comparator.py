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


def create_cleanFile(aDict, csv_in, csv_out, isphage):  # grab regular camp tax entries only 
    ifile  = open(csv_in, "rb")
    with ifile as source: 
        rdr = csv.reader(source)
        with open(csv_out, "wb") as result: 
            wtr= csv.writer(result)
            if isphage:
                in_iter = ((r[int(aDict['First'])],
                            r[int(aDict['Last'])],
                            r[int(aDict['Email'])]) for r in rdr if "regular" in r[int(aDict['Phage Camp Taxes'])]) 
            else:
                in_iter = ((r[int(aDict['First'])],
                            r[int(aDict['Last'])],
                            r[int(aDict['Email'])]) for r in rdr if "First Name" not in r[int(aDict['First'])])
            wtr.writerows(in_iter)
    
    ifile.close()
    


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
                
    print "\nCamp Tax Not Paid, but Registered on ThePhage.org"
    print "Total: %s " % len(notPaid)
    print "=============================="
    for row in notPaid:
        print "%s %s, %s" % (row[0], row[1], row[2])
    print "\n"
        
    ifile.close()
    wfile.close()


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
                
    print "Not Registered on ThePhage.org, but paid on WePay"
    print "Total: %s " % len(notRegistered)
    print "=============================="
    for row in notRegistered:
        print "%s %s, %s" % (row[0], row[1], row[2])
    print "\n"

    ifile.close()
    wfile.close()


def duplicate_reg(csv_phage, csv_wepay):
    ifile  = open(csv_phage, "rb")
    phage = csv.reader(ifile)
    emails = []
    for row in phage:
        emails.append(row[2])
    ifile.close()
    test_distinct(emails)
    ifile.close()


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
    if (d_num != l_num):
        print "ThePhage.org directory has the following Duplicate Entries:"
        print "=============================="
        print " %s " %  get_duplicate_entry(mylist)
        print "\nDistinct Entries on ThePhage.org for Regular Tax: %s" % d_num
        print "Total Listed Entries : %s" % l_num
    else: 
        print "ThePhage.org directory has No Duplicates. Yay!"


def main(): 

    phageDict = { 'First': 'X', 
                  'Last': 'X', 
                  'Email':'X', 
                  'Phage Camp Taxes': 'X' }

    parser = argparse.ArgumentParser()
    parser.add_argument("phage_csv")
    parser.add_argument("wepay_csv")

    args = parser.parse_args() 

    print "Using the following CSV files:"
    print(args.phage_csv)
    print(args.wepay_csv)

    phage_csv = args.phage_csv
    wepay_csv = args.wepay_csv

    dir_csv = "csv/"
    mkdir_p(dir_csv)

    new_phage_csv = dir_csv + 'new_phage.csv'
    new_wepay_csv = dir_csv + 'new_wepay.csv'

    get_headerInfo(phageDict, phage_csv)
    create_cleanFile(phageDict, phage_csv, new_phage_csv, True)
    ## print "Phage Dict: %s" %  phageDict

    get_headerInfo(phageDict, wepay_csv)
    create_cleanFile(phageDict, wepay_csv, new_wepay_csv, False)
    ## print "Wepay Dict: %s" %  phageDict

    ## who hasn't paid tax?  - case independent
    tax_missing(new_phage_csv, new_wepay_csv)

    ## who has not registered but paid tax?  - case independent
    reg_missing(new_phage_csv, new_wepay_csv)

    ## find and show any duplicate registration on ThePhage.org
    duplicate_reg(new_phage_csv, new_wepay_csv)



if __name__ == '__main__':
    main()


