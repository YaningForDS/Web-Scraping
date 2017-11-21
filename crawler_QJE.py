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

linklist = ['http://www.jstor.org/stable/i40063217','http://www.jstor.org/stable/i23015682','http://www.jstor.org/stable/i23015661',
'http://www.jstor.org/stable/i23015660','http://www.jstor.org/stable/i40043038','http://www.jstor.org/stable/i27867500',
'http://www.jstor.org/stable/i27867486','http://www.jstor.org/stable/i40022098','http://www.jstor.org/stable/i40022097',
'http://www.jstor.org/stable/i40022096','http://www.jstor.org/stable/i40022095','http://www.jstor.org/stable/i40022094',
'http://www.jstor.org/stable/i40022093','http://www.jstor.org/stable/i25098918','http://www.jstor.org/stable/i25098905',
'http://www.jstor.org/stable/i25098891','http://www.jstor.org/stable/i25098876','http://www.jstor.org/stable/i25098862',
'http://www.jstor.org/stable/i25098848','http://www.jstor.org/stable/i25098834','http://www.jstor.org/stable/i25098820',
'http://www.jstor.org/stable/i25098807','http://www.jstor.org/stable/i25098794','http://www.jstor.org/stable/i25098781',
'http://www.jstor.org/stable/i25098767','http://www.jstor.org/stable/i25098754','http://www.jstor.org/stable/i25098741',
'http://www.jstor.org/stable/i25098728','http://www.jstor.org/stable/i25098713','http://www.jstor.org/stable/i25098700',
'http://www.jstor.org/stable/i25098687','http://www.jstor.org/stable/i25098674','http://www.jstor.org/stable/i25053934',
'http://www.jstor.org/stable/i25053921','http://www.jstor.org/stable/i25053908','http://www.jstor.org/stable/i25053895',
'http://www.jstor.org/stable/i388072','http://www.jstor.org/stable/i388070','http://www.jstor.org/stable/i346041',
'http://www.jstor.org/stable/i346040','http://www.jstor.org/stable/i346039','http://www.jstor.org/stable/i346038',
'http://www.jstor.org/stable/i346037','http://www.jstor.org/stable/i346036','http://www.jstor.org/stable/i324122',
'http://www.jstor.org/stable/i324121','http://www.jstor.org/stable/i324120','http://www.jstor.org/stable/i324119',
'http://www.jstor.org/stable/i324118','http://www.jstor.org/stable/i324117','http://www.jstor.org/stable/i324116',
'http://www.jstor.org/stable/i324115','http://www.jstor.org/stable/i324114','http://www.jstor.org/stable/i324113',
'http://www.jstor.org/stable/i324112','http://www.jstor.org/stable/i324111','http://www.jstor.org/stable/i352639',
'http://www.jstor.org/stable/i352638','http://www.jstor.org/stable/i352637','http://www.jstor.org/stable/i352636',
'http://www.jstor.org/stable/i352578','http://www.jstor.org/stable/i352577','http://www.jstor.org/stable/i352576',
'http://www.jstor.org/stable/i352575','http://www.jstor.org/stable/i352574','http://www.jstor.org/stable/i352573',
'http://www.jstor.org/stable/i337103','http://www.jstor.org/stable/i337102','http://www.jstor.org/stable/i337101',
'http://www.jstor.org/stable/i337100','http://www.jstor.org/stable/i337099','http://www.jstor.org/stable/i337098',
'http://www.jstor.org/stable/i337097','http://www.jstor.org/stable/i337096','http://www.jstor.org/stable/i337095',
'http://www.jstor.org/stable/i337094','http://www.jstor.org/stable/i337093','http://www.jstor.org/stable/i337092',
'http://www.jstor.org/stable/i337091','http://www.jstor.org/stable/i337090','http://www.jstor.org/stable/i352312',
'http://www.jstor.org/stable/i352311','http://www.jstor.org/stable/i352310','http://www.jstor.org/stable/i352309',
'http://www.jstor.org/stable/i352308','http://www.jstor.org/stable/i352307','http://www.jstor.org/stable/i352302',
'http://www.jstor.org/stable/i352301']


class crawler_QJE():
    def __init__(self, mycsv):
        import csv
        self.csvfile = codecs.open(mycsv+'.csv','w', encoding = 'utf-8')
        self.fieldnames = ['Title','Abstract','topics', 'Authors','Publication Date','Volumne, Number','Page Number','stable URL']
        self.writer = csv.DictWriter(self.csvfile,fieldnames=self.fieldnames)
        self.writer.writeheader()

    def crawler(self):
        print 'start crawling...'
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
                Bitext = self.get_Bitext(hyperlink)
                print Bitext
                Volume_number = self.get_volume_number(Bitext)
                abstract = self.get_abstract(Bitext)
                authors = self.get_author(Bitext)
                pages = self.get_pages(Bitext)
                title = self.get_title(Bitext)
                stable = self.get_stable_url(Bitext)
                self.writer.writerow({'Title': title, 'Abstract': abstract, 'topics': topics, 'Authors': authors, 'Publication Date': date, 'Volumne, Number': Volume_number, 'Page Number': pages, 'stable URL': stable})
                print date



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
    
    def get_Bitext(self,links):
        try:
            text = ''
            codes = links.split('/')[-1]
            pre = 'http://www.jstor.org/citation/text/10.2307/'
            filelink = pre + codes
            text = self.download_page(filelink)
            text_list = text.split('\n')
            return text_list
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



crawler = crawler_QJE('QJE_res')
crawler.crawler()

