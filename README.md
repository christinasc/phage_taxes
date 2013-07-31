Python script to check if people registered on ThePhage.org and paid camp tax. 
Does a comparison between thephage.org csv download and wepay guest list csv file

usage: tax_comparator.py [-h] phage_csv wepay_csv

positional arguments:
  phage_csv
  wepay_csv


HowTo:

1. Download a copy of this repository 
2. Export camp directory from thephage.org
3. Export guestlist from wepay.com

4. Run script, e.g.

  % python tax_comparator.py the-phage-2013-2013-07-31.csv tickets_guests_155731_2013-07-31.csv


