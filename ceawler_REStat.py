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

linklist = ['http://www.jstor.org/stable/i40064284', 'http://www.jstor.org/stable/i23016057', 'http://www.jstor.org/stable/i23015914',
'http://www.jstor.org/stable/i23015904', 'http://www.jstor.org/stable/i40044303','http://www.jstor.org/stable/i27867549',
'http://www.jstor.org/stable/i27867531', 'http://www.jstor.org/stable/i25651384', 'http://www.jstor.org/stable/i25651367',
'http://www.jstor.org/stable/i25651349','http://www.jstor.org/stable/i25651333', 'http://www.jstor.org/stable/i25651312',
'http://www.jstor.org/stable/i40002308', 'http://www.jstor.org/stable/i40002311','http://www.jstor.org/stable/i40002310',
'http://www.jstor.org/stable/i40002309','http://www.jstor.org/stable/i40002307','http://www.jstor.org/stable/i40002304',
'http://www.jstor.org/stable/i40002305','http://www.jstor.org/stable/i40002306','http://www.jstor.org/stable/i40002303',
'http://www.jstor.org/stable/i40002302','http://www.jstor.org/stable/i40002301','http://www.jstor.org/stable/i40002299',
'http://www.jstor.org/stable/i40002295', 'http://www.jstor.org/stable/i40002298','http://www.jstor.org/stable/i40002296',
'http://www.jstor.org/stable/i40002297', 'http://www.jstor.org/stable/i40002300','http://www.jstor.org/stable/i361239',
'http://www.jstor.org/stable/i361238','http://www.jstor.org/stable/i361237','http://www.jstor.org/stable/i361236',
'http://www.jstor.org/stable/i361235','http://www.jstor.org/stable/i361234','http://www.jstor.org/stable/i361233',
'http://www.jstor.org/stable/i361232','http://www.jstor.org/stable/i361231','http://www.jstor.org/stable/i361230',
'http://www.jstor.org/stable/i361229','http://www.jstor.org/stable/i361228','http://www.jstor.org/stable/i361227',
'http://www.jstor.org/stable/i361226','http://www.jstor.org/stable/i345522','http://www.jstor.org/stable/i345521',
'http://www.jstor.org/stable/i345520','http://www.jstor.org/stable/i345519','http://www.jstor.org/stable/i345518',
'http://www.jstor.org/stable/i345517','http://www.jstor.org/stable/i345516', 'http://www.jstor.org/stable/i345515',
'http://www.jstor.org/stable/i345514','http://www.jstor.org/stable/i345513','http://www.jstor.org/stable/i345512',
'http://www.jstor.org/stable/i345511','http://www.jstor.org/stable/i345510','http://www.jstor.org/stable/i352647',
'http://www.jstor.org/stable/i352646','http://www.jstor.org/stable/i352645','http://www.jstor.org/stable/i352644',
'http://www.jstor.org/stable/i336990','http://www.jstor.org/stable/i336989','http://www.jstor.org/stable/i336988',
'http://www.jstor.org/stable/i336987','http://www.jstor.org/stable/i336986','http://www.jstor.org/stable/i336985',
'http://www.jstor.org/stable/i336984','http://www.jstor.org/stable/i336983','http://www.jstor.org/stable/i336982',
'http://www.jstor.org/stable/i336981','http://www.jstor.org/stable/i336980','http://www.jstor.org/stable/i336979',
'http://www.jstor.org/stable/i336978','http://www.jstor.org/stable/i336977','http://www.jstor.org/stable/i336976',
'http://www.jstor.org/stable/i336975','http://www.jstor.org/stable/i336974','http://www.jstor.org/stable/i336973',
'http://www.jstor.org/stable/i336972','http://www.jstor.org/stable/i336971','http://www.jstor.org/stable/i336970',
'http://www.jstor.org/stable/i336969','http://www.jstor.org/stable/i336968','http://www.jstor.org/stable/i336967',
'http://www.jstor.org/stable/i336966','http://www.jstor.org/stable/i336965','http://www.jstor.org/stable/i336964',
'http://www.jstor.org/stable/i336963']



class crawler_REStat():
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



crawler = crawler_REStat('REStat_res')
crawler.crawler()

