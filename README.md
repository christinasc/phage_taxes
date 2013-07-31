Python script to check if people registered on ThePhage.org and paid camp tax. Example csv files included.
Does a comparison between thephage.org csv download and wepay guest list csv file

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
<b>
  % python tax_comparator.py the-phage-2013-2013-07-31.csv tickets_guests_155731_2013-07-31.csv
</b>

</ul>
