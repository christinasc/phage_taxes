#!/usr/bin/python
import smtplib, datetime
import os, pconfig
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import pconfig
 
csv_result = pconfig.MAIN_PATH+"output.txt"
#csv_result = "output.txt"
# Writing the message (this message will appear in the email)
msg = 'Enter you message here'

def main():

    os.system(pconfig.runscr)
    now = datetime.datetime.now()
#    print str(now)

    body = ""

    if os.path.exists(csv_result):
        ifile  = open(csv_result, "rb")
        for line in ifile:
            body = body + line+"<br>"            
        ifile.close()
        body = str(body)
    else: 
        body = " Could not generate result; possible website connection problem "

    msg = MIMEMultipart()
    msg['From'] = pconfig.fromaddr
    msg['To'] = pconfig.toaddrs
    msg['Subject'] = " %d-%d-%d : Phage Tax Update" % (now.month, now.day,now.year)
    msg.attach(MIMEText(body, 'html'))
    
    text = msg.as_string()
#    print text
    
    # Sending the mail  
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(pconfig.username,pconfig.password)
    server.sendmail(pconfig.fromaddr, pconfig.toaddrs, text)
    server.quit()

    
# rm -rf csv csvFiles/ webFiles/ output.txt pconfig.pyc 


if __name__ == "__main__":
    main()
