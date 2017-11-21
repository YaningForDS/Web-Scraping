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

pre_linklist = ['https://www.jstor.org/journal/jpoliecon?decade=2010','https://www.jstor.org/journal/jpoliecon?decade=2000',
'https://www.jstor.org/journal/jpoliecon?decade=1990']

class crawler_JPE():
    def __init__(self, mycsv):
        import csv
        self.csvfile = codecs.open(mycsv+'.csv','w', encoding = 'utf-8')
        self.fieldnames = ['Title','Abstract','topics', 'Authors','Publication Date','Volumne, Number','Page Number','DOI']
        self.writer = csv.DictWriter(self.csvfile,fieldnames=self.fieldnames)
        self.writer.writeheader()

    def crawler(self):
        print 'start crawling...'
        linklist = self.get_linklist()
        for url in linklist:
            webpage = self.download_page(url)
            soup = BeautifulSoup(webpage,'html.parser')
            date = self.get_publish_date(soup)
            sub = soup.find_all('div','stable')
            for index in xrange(1,len(sub)-1):
                hyperlink = self.get_hyperlink(sub, index)
                print hyperlink
                sub_page = self.download_page(hyperlink)
                sub_soup = BeautifulSoup(sub_page,'html.parser')
                #print soup.find('div', class_ = 'topics mtl')
                topics = self.get_topics(sub_soup)
                Bitext, doi = self.get_Bitext_doi(hyperlink)
                print Bitext
                Volume_number = self.get_volume_number(Bitext)
                abstract = self.get_abstract(Bitext)
                authors = self.get_author(Bitext)
                pages = self.get_pages(Bitext)
                title = self.get_title(Bitext)
                stable = self.get_stable_url(Bitext)
                self.writer.writerow({'Title': title, 'Abstract': abstract, 'topics': topics, 'Authors': authors, 'Publication Date': date, 'Volumne, Number': Volume_number, 'Page Number': pages, 'DOI': doi})
                print date

    def get_linklist(self):
        linklist = []
        for item in pre_linklist:
            html = self.download_page(item)
            soup = soup = BeautifulSoup(html, 'html.parser')
            dd = soup.find_all('dl',class_ = 'accordion')
            li_of_link = dd[2].find_all('a',text=re.compile('pp.'))
            for i in li_of_link:
                pre = 'http://www.jstor.org'
                linklist.append(pre + str(i.get('href')))
        return linklist




    def download_page(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
        }
        try:
            #sleep(1)
            data = requests.get(url, headers=headers, timeout = 335).content
            return data
        except requests.ConnectionError:
            sleep(30)
            data = requests.get(url, headers=headers, timeout = 335).content
            return data

    #an s = soup.find_all('div','stable')
    #soup
    def get_publish_date(self, soup):
        try:
            m = ''
            y = ''
            d = soup.find('div',class_ = 'issue')
            date = str(d.string).replace('\n','').strip().split(',')[-1].strip()
            if len(date) == 4:
                m = str(d.string).replace('\n','').strip().split(',')[-2].strip()
                y = str(d.string).replace('\n','').strip().split(',')[-1].strip()
                date = m + y
            return date
        except:
            return []

    def get_hyperlink(self, text, index):
        try:
            #h = soup.find_all('div','stable')
            hyperlink = 'http:' + (str(text[index].string.strip()).split(':'))[-1]
            return hyperlink
        except:
            return []
    
    ##soup = BeautfulSoup(hyperlink)
    def get_topics(self, soup):
        try:
            topics = []
            t = soup.find('div', class_ = 'topics mtl')
            for i in t.find_all('a'):
                topics.append(str(i.string))
            return topics
        except:
            return []
    
    def get_Bitext_doi(self,links):
        try:
            text = ''
            codes = links.split('/')[-1]
            pre = 'http://www.jstor.org/citation/text/10.1086/'
            filelink = pre + codes
            text = self.download_page(filelink)
            text_list = text.split('\n')
            doi = '10.1086/' + codes
            return text_list,doi
        except:
            return []
    #text = text_list
    
    def get_volume_number(self, text):
        number = ''
        volume = ''
        res = ''
        for row in text:
            row = row.lower()
            if 'number' in row:
                number =  (row.replace('=','').replace('{','').replace('}','').replace(',','')).strip()
            if 'volume' in row:
                volume =  row.replace('=','').replace('{','').replace('}','').replace(',','').strip()
            res = number + ', ' + volume
        return res

    def get_stable_url(self, text):
        stable = ''
        for row in text:
            row = row.lower()
            if 'url' in row:
                stable = row.replace('url','').replace('=','').replace('{','').replace('}','').replace(',','').strip()
        return stable

    def get_abstract(self, text):
        abstract = ''
        for row in text:
            row = row.lower()
            if 'abstract' in row:
                abstract = row.replace('abstract','').replace('=','').replace('{','').replace('}','').replace(',','').strip()
        return abstract

    def get_author(self, text):
        try:
            author = ''
            for row in text:
                row = row.lower()
                if 'author' in row:
                    author = row.replace('author','').replace('=','').replace('{','').replace('}','').replace(',','').strip().replace('and',',')
            return author
        except:
            return []

    def get_pages(self, text):
        try:
            pages = ''
            for row in text:
                row = row.lower()
                if 'pages' in row:
                    pages = row.replace('pages','pp.').replace('=','').replace('{','').replace('}','').replace(',','').strip()
            return pages
        except:
            return []
    
    def get_title(self,text):
        try:
            title = ''
            for row in text:
                row = row.lower()
                if 'title' in row:
                    title = row.replace('title','').replace('=','').replace('{','').replace('}','').replace(',','').strip()
            return title
        except:
            return []



crawler = crawler_JPE('JPE_res')
crawler.crawler()

