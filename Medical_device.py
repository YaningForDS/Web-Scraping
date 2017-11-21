import sqlite3
import urllib2
from bs4 import BeautifulSoup
import copy
import csv
import re
from time import sleep
import requests
from datetime import datetime
from threading import Timer
import os
from urllib import urlretrieve
#create a folder
current_file_path = __file__
foldername = os.path.dirname(os.path.realpath(__file__))
print foldername

# if not os.path.exists('Medical_Device'):
#     os.makedirs('Medical_Device')


#Medical_folder = os.path.join(foldername, 'Medical_Device')
#print Medical_folder

# today = datetime.today()
# y = today.replace(day=today.day+7, hour=16, minute=0, second=0, microsecond=0)
# seconds = (y-today).total_seconds()

# link = 'http://www.fda.gov/MedicalDevices/DeviceRegulationandGuidance/HowtoMarketYourDevice/RegistrationandListing/ucm134495.htm'
# class Medical_Devices():

#     def download_page(self, url):
#         ## change IP address
#         headers = {
#             'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) '
#                           'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
#         }
#         proxies = {
#               'http://65.151.185.117:80',
#         }
#         try:
#             data = requests.get(url, headers=headers, proxies = proxies, timeout = 335).content
#             return data
#         except requests.ConnectionError:
#             sleep(30)
#             data = requests.get(url, headers=headers,proxies = proxies, timeout = 335).content
#             return data

#     def get_date(self):
#         today = datetime.today()
#         year = str(today.year)
#         month = str(today.month)
#         day = str(today.day)
#         if len(month) == 1:
#             month = '0'+month
#         if len(day) == 1:
#             day = '0' + day
#         return year+month+day

#     def crawler(self):
#         date = self.get_date()
#         path = 'Medical_Device/{}'.format(date)
#         if not os.path.exists(path):
#             os.makedirs(path)  
#         html = self.download_page(link)
#         soup = BeautifulSoup(html, 'html.parser')
#         for i in soup.find_all('a',href=re.compile("zip")):
#             url = i.get('href')
#             filename = url.split('/')[-1][:-4]
#             di = date+'/'+filename+'.zip'
#             dirc = os.path.join(foldername,di)
#             urlretrieve(url, dirc)
#         print 'finish for {}... Next crawling is 7 days later'.format(date)
    
#     def main(self):
#         t = Timer(seconds, self.crawler())
#         t.start()


# ob = Medical_Devices()
# ob.main()







# # def hello_world():
# #     print "hello world"
# #     #...

# #t = Timer(secs, hello_world)
# #t.start()