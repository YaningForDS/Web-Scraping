import sqlite3
import urllib2
from bs4 import BeautifulSoup
import copy
import csv

from time import sleep
import requests
def download_page(url):
    ## change IP address
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
    }
    proxies = {
          'http://65.151.185.117:80',
    }
    try:
        data = requests.get(url, headers=headers, proxies = proxies, timeout = 335).content
        return data
    except requests.ConnectionError:
        sleep(30)
        data = requests.get(url, headers=headers,proxies = proxies, timeout = 335).content
        return data

myfile = open('result_mach.csv','wb')
wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
namelist = ['Manufacturer','Address','Authorised Representative','Address','Date Registered','MHRA Reference Number']
devicename = ''
for i in xrange(1,51):
    devicename = 'Device {}'.format(i)
    namelist.append(devicename)

wr.writerow(namelist)
current = download_page('http://aic.mhra.gov.uk/era/pdr.nsf/name?openpage&start=1&count=200')
b = 'http://aic.mhra.gov.uk/era/pdr.nsf/'
soup = BeautifulSoup(current, 'html.parser')
pre_html_list = soup.find('div',class_ = 'textbox').find_all('a')
html_list = []
for i in pre_html_list:
    a = i.get('href')
    fhtml = b + a
    html_list.append(fhtml)

for html in html_list:
    pointer = download_page(html)
    soup = BeautifulSoup(pointer,'html.parser')
    table2 = soup.find_all('table')[0]
    for tr in table2.find_all('tr')[1:]:
        mylist = []
        tds = tr.find_all('td')
        mylist = [elem.text.encode('utf-8') for elem in tds]
        st = mylist[-1].split(',')
        mylist = mylist[:-1]
        mylist.extend(st)
        wr.writerow(mylist)


