import urllib2
from bs4 import BeautifulSoup
from time import sleep
import copy
import csv
import requests
import re
import codecs
import sys

reload(sys)  
sys.setdefaultencoding('utf8')

class crawler_JPE():
    def __init__(self, mycsv):
        import csv
        self.csvfile = codecs.open(mycsv+'.csv','w', encoding = 'utf-8')
        self.fieldnames = ['Title','Abstract','Authors','DOI Link','Publication Date','Volumne, Number','Page Number']
        self.writer = csv.DictWriter(self.csvfile,fieldnames=self.fieldnames)
        self.writer.writeheader()

    def crawler(self):
        print 'starting crawling...'
        url = 'http://www.journals.uchicago.edu/loi/jpe'
        webpage = self.download_page(url)
        soup = BeautifulSoup(webpage,'html.parser')
        subcontent = soup.find_all('div',class_ = 'decade')
        content = subcontent[0:3]
        for row in content:
            year = self.get_Publication_year(row)
            sub = row.find_all('div',class_ = 'loiRow-layout')
            for index in xrange(len(sub)):
                date = self.get_date(sub,index)
                volume_number = self.get_volume_number(sub,index)
                hyperlink = self.get_hyperlink(sub, index)
                hyper = self.download_page(hyperlink)
                subsoup = BeautifulSoup(hyper, 'html.parser')
                all_article = subsoup.find_all('table', class_='articleEntry')
                for article in all_article:
                    title = self.get_article_name(article)
                    authors = self.get_author_name(article)
                    page_number = self.get_page_number(article)
                    abstract = self.get_abstract(article)
                    DOI = self.get_doi(article)
                    self.writer.writerow({'Title': title, 'Abstract': abstract, 'Authors': authors, 'DOI Link': DOI, 'Publication Date': date, 'Volumne, Number': volume_number, 'Page Number': page_number})
                    print date

    def download_page(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
        }
        try:
            sleep(30)
            data = requests.get(url, headers=headers, timeout = 335).content
            return data
        except requests.ConnectionError:
            sleep(30)
            data = requests.get(url, headers=headers, timeout = 335).content
            return data

    # text = content
    def get_Publication_year(self, text):
        try:
            year = text
            return str(year.div.a.string)
        except:
            return []

    #text = sub
    def get_volume_number(self, text, index):
        try:
            v = text[index].a.string
            return str(v)
        except:
            return []

    def get_date(self,text,index):
        try:
            date = text[index].find('span',class_ = 'loiIssueCoverDateText').string
            return str(date).replace('|','').lstrip()
        except:
            return []

    def get_hyperlink(self, text, index):
        try:
            hyper = text[index].span.a.get('href')
            return str(hyper)
        except:
            return []

    #text = article
    def get_article_name(self, text):
        try:
            title = text.find('span',class_='hlFld-Title').string
            return str(title.encode('utf-8'))
        except:
            return []

    def get_author_name(self, text):
        try:
            name = []
            b = text.find_all('span', class_= 'hlFld-ContribAuthor')
            for i in b:
                name.append(i.string.encode('utf-8'))
            return name
        except:
            return []


    def get_page_number(self, text):
        try:
            res = ''
            for i in text.find('span',class_= 'articlePageRange').stripped_strings:
                res = i
            page = res.replace('\u2013', '*').encode('utf-8').replace('\xe2\x80\x93','-')
            return page
        except:
            return []

    def get_abstract(self, text):
        try:
            pre = 'http://www.journals.uchicago.edu'
            l = str(text.find('a').get('href'))
            link = pre + l
            ab_link = self.download_page(link)
            ab_soup = BeautifulSoup(ab_link, 'html.parser')
            ab = ab_soup.find('p',class_= 'first last').string
            return str(ab)
        except:
            return []

    def get_doi(self, text):
        try:
            l = str(text.find('a').get('href'))
            l = l.split('/')
            l = l[-2:]
            doi = ''
            for i in l:
                doi = doi + i + '/'
            doi = doi[:-1]
            return doi
        except:
            return []

crawler = crawler_JPE('JPE')
crawler.crawler()
