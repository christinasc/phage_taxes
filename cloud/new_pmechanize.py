#!/usr/bin/python
import mechanize 
import os, shutil, errno
from bs4 import BeautifulSoup
import pconfig

WP_LOGIN = 'https://www.wepay.com/session/login'
WP_EVENTPAGE = 'https://www.wepay.com/events/manage/155731/guests/tickets'
WP_GUESTLIST = 'https://www.wepay.com/events/manage/155731/guest_list_print'
WP_INVOICES = 'https://www.wepay.com/invoice/account/217550'

PHAGE_SITE = 'http://thephage.org/wp-login.php'
PHAGE_DIR = 'http://thephage.org/camp-directory/'

csvFiles = 'csvFiles/'
webFiles = 'webFiles/'

SAVE_PATH = pconfig.MAIN_PATH + webFiles
CSV_PATH = pconfig.MAIN_PATH+ csvFiles

wepaylist = SAVE_PATH +'wepay_list.html'
wepayinvoice = SAVE_PATH +'wepay_invoices.html'
phagedirectory = SAVE_PATH+'phage_dir.html'

phagecsv = CSV_PATH+'phage.csv'
wepaycsv = CSV_PATH+'wepay.csv'
wepayinvoicecsv = CSV_PATH+'wepay_invoice.csv'


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise


def getWepay_pages(browser): 
    browser.open(WP_LOGIN) 
    browser.select_form(nr=0)
    browser['email'] = pconfig.WP_USERNAME
    browser['password'] = pconfig.WP_PASSWORD
    res = browser.submit()

    page_info = browser.retrieve(WP_GUESTLIST)[0]
    fh = open(page_info)
    with open(wepaylist, 'wb') as f:
        f.write(fh.read())

    page_info = browser.retrieve(WP_INVOICES)[0]
    fh = open(page_info)
    with open(wepayinvoice, 'wb') as f:
        f.write(fh.read())


def getPhage_pages(browser):
    browser.open(PHAGE_SITE) 
    browser.select_form(nr=0)
    browser['log'] = pconfig.PHAGE_LOGIN
    browser['pwd'] = pconfig.PHAGE_PASSWORD
    res = browser.submit()

    page_info = browser.retrieve(PHAGE_DIR)[0]
    fh = open(page_info)
    with open(phagedirectory, 'wb') as f:
        f.write(fh.read())


def makePhageCSV(): 
    soup = BeautifulSoup(open(phagedirectory)) 
    table = soup.find_all('table',  attrs={'class': 'gf_directory widefat fixed'})
    #print table
    
    sortedList  = ""
    header_list = ""

    ## GET HEADER from table
    header = table[0]
    th =  header.findAll('th')
    for name in th:
        if len(name) > 0:
            eachlink = name.find('a')
            if eachlink is not None:
                each_title =  eachlink.find(text=True)
                each_title = "\"" + each_title.encode('utf-8').strip() + "\","
                header_list = header_list + each_title

    sortedList = sortedList + header_list + "\n"

    ## GET Table data
    for line in table:
        rows =  line.findAll('tr')
        for cols in rows:
            item = cols.findAll('td')
            #print len(item)
            if len(item) > 0:
                for i in item:
                    eachitem =  i.find(text=True)
                    sortedList = sortedList + "\"" +  eachitem.encode('utf-8').strip() + "\","
                sortedList = sortedList + "\n"

    with open(phagecsv, 'wb') as f:
        f.write(sortedList)


def makeWepayCSV(): 
    soup = BeautifulSoup(open(wepaylist)) 
    table = soup.find_all('table',  attrs={'class': 'print-table'})
    #print table
    
    sortedList  = ""
    header_list = ""

    ## GET HEADER from table
    header = table[0]
    th =  header.findAll('th')
    for name in th:
#        print name
        if len(name) > 0:
            each_title = name.find(text=True)
            each_title = "\"" + each_title.encode('utf-8').strip() + "\","
            header_list = header_list + each_title

    sortedList = sortedList + header_list + "\n"

    ## GET Table data
    for line in table:
        rows =  line.findAll('tr')
        for cols in rows:
            item = cols.findAll('td')
            #print len(item)
            if len(item) > 0:
                for i in item:
                    eachitem =  i.find(text=True)
                    sortedList = sortedList + "\"" + eachitem.encode('utf-8').strip() + "\","
                sortedList = sortedList + "\n"

    with open(wepaycsv, 'wb') as f:
        f.write(sortedList)


def makeWepayInvoiceCSV(): 
    soup = BeautifulSoup(open(wepayinvoice)) 
    table = soup.find_all('table',  attrs={'class': 'invoice-list'})
    #print table
    
    sortedList  = ""
    header_list = ""

    ## GET HEADER from table
    header = table[0]
    th =  header.findAll('th')
    for name in th:
#        print name
        if len(name) > 0:
            each_title = name.find(text=True)
            if each_title == 'Customer':
                # insert email in advance of customer
                each_title = "\"Email\",\"" +  each_title.encode('utf-8').strip() + " Name" + "\","
            else: 
                each_title = "\"" + each_title.encode('utf-8').strip() + "\","
            header_list = header_list + each_title

    sortedList = sortedList + header_list +  "\n"

    email = ""
    ## GET Table data
    for line in table:
        rows =  line.findAll('tr')
        for cols in rows:
            item = cols.findAll('td')
            #print len(item)
            if len(item) > 0:
                for i in item:
                    eachitem =  i.find(text=True)
                    email = i.find('div', attrs={'class':'email'})
#                    print eachitem
                    if email is not None:
                        email = email.find(text=True)
                        email = email.encode('utf-8').strip()
#                        print str(email)
                        sortedList = sortedList + "\"" + email + "\","
                    sortedList = sortedList + "\"" +eachitem.encode('utf-8').strip() + "\","
                sortedList = sortedList + "\n"

    with open(wepayinvoicecsv, 'wb') as f:
        f.write(sortedList)


def main():

#    if os.path.isdir(SAVE_PATH):
#        shutil.rmtree(SAVE_PATH)  # deletes old files, needs to check if exists first, todo  
#    if os.path.isdir(SAVE_PATH):
#        shutil.rmtree(CSV_PATH)          

    mkdir_p(SAVE_PATH)
    mkdir_p(CSV_PATH)

    browser = mechanize.Browser(factory=mechanize.RobustFactory())
    browser.set_handle_robots(False)   # ignore robots
    browser.set_handle_refresh(False)  # can sometimes hang without this
    browser.addheaders = [('User-agent', 'Firefox')]  

    getWepay_pages(browser)
    getPhage_pages(browser)

    makePhageCSV()
    makeWepayCSV()
    makeWepayInvoiceCSV()
    # Note: csv file has extra comma for entries, but not header

    if os.path.isdir(pconfig.MAIN_PATH):
        csv_compare = pconfig.MAIN_PATH + "new_comparator.py "
        runscript = 'python ' + csv_compare + phagecsv + " " + wepaycsv + " --inv=" + wepayinvoicecsv + " > output.txt"
#        print runscript
        os.system(runscript)
        

    
    
#############################################################################
 
if __name__ == "__main__":
    main()
