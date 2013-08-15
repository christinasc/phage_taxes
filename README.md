Python script to check if people registered on ThePhage.org and paid camp tax. 

The files in the cloud directory were uploaded to picloud.com and run as a daily cron job that sends an email out with the parsed and cross checked results. 

========
Example csv files included in the csv directory here.

Does a comparison between thephage.org csv download and wepay guest list csv file

example:

  <code>
  python tax_comparator.py the-phage-2013-2013-07-31.csv tickets_guests_155731_2013-07-31.csv
  </code>

usage: tax_comparator.py [-h] phage_csv wepay_csv

positional arguments:
  phage_csv
  wepay_csv


HowTo:
<ul>

<li> Step 1. Download a copy of this repository 
<li> Step 2. Export camp directory from thephage.org

<li> (click on image to view bigger) <br/>
<a href="https://raw.github.com/christinasc/phage_taxes/master/images/thephage.org_csv.png">
<img src="https://raw.github.com/christinasc/phage_taxes/master/images/thephage.org_csv.png" width="300"/>
</a>

<li> Step 3. Export guestlist from wepay.com 

<li> Login to event: <br/>
<a href="https://raw.github.com/christinasc/phage_taxes/master/images/phage_wepay1.png">
<img src="https://raw.github.com/christinasc/phage_taxes/master/images/phage_wepay1.png" width="300" /> 
</a>
<li> Visit Guestlist page: <br/>
<a href="https://raw.github.com/christinasc/phage_taxes/master/images/phage_wepay2.png">
<img src="https://raw.github.com/christinasc/phage_taxes/master/images/phage_wepay2.png" width="300"/>
</a>

<li> Step 4. Run script in shell, e.g.<br/>
  % python tax_comparator.py the-phage-2013-2013-07-31.csv tickets_guests_155731_2013-07-31.csv


</ul>
