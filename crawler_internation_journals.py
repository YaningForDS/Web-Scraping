import urllib2
from bs4 import BeautifulSoup
import copy
import csv
import requests
import re
import codecs
import sys

reload(sys)  
sys.setdefaultencoding('utf8')
#f = codecs.open('dfads.csv','w',encoding='utf-8')

class ScienceDirect_crawl():
	##initial a csv file to store data
	def __init__(self,mycsv):
		import csv
		self.csvfile = codecs.open(mycsv+'.csv','w', encoding = 'utf-8')
		self.fieldnames = ['Title','Abstract','Keywords','JEL Codes','Authors','DOI Link','Publication Date','Volumne, Issue','Page Number']
		self.writer = csv.DictWriter(self.csvfile,fieldnames=self.fieldnames)
		self.writer.writeheader()

	## define the logic of crawl	
	def crawl(self):
		print 'starting crawling...'
		terminate = False
		url = 'http://www.sciencedirect.com/science/journal/00221996/31/1-2'
		webpage = self.download_page(url)
		soup = BeautifulSoup(webpage,'html.parser')
		while terminate == False:
			#url = 'http://www.sciencedirect.com/science/journal/00221996/31/1-2'
			#webpage = self.download_page(url)
			#soup = BeautifulSoup(webpage,'html.parser')
			tag = soup.find_all('h4')
			inter, Publication_date = self.get_internation_date(soup)
			Volumne_issue = self.get_volumne_issue(soup)
			for i in xrange(0, len(tag)):
				title = self.get_article_name(tag[i])
				authors = self.get_authors(soup,i)
				page_number = self.get_page_numbers(soup, i)
				##get hyperlink
				hyperlink = self.get_hyperlink(tag[i])
				sub_page = self.download_page(hyperlink)
				sub_soup = BeautifulSoup(sub_page,'html.parser')
				abstract = self.get_abstract(sub_soup)
				keywords = self.get_keywords(sub_soup)
				JEL_code = self.get_JEL(sub_soup)
				DOI = self.get_doi(sub_page,sub_soup)
				#Publication_date = self.get_publicationDate(sub_soup)
				self.writer.writerow({'Title': title, 'Abstract': abstract, 'Keywords': keywords, 'JEL Codes': JEL_code, 'Authors': authors, 'DOI Link': DOI, 'Publication Date': Publication_date, 'Volumne, Issue': Volumne_issue,'Page Number':page_number})
			next_url = self.get_next_issue(soup)
			if next_url == 'http://www.sciencedirect.com/science/journal/00221996/101':
				#terminate = True
				break
			url = next_url
			webpage = self.download_page(url)
			soup = BeautifulSoup(webpage,'html.parser')


	def get_next_issue(self,text):
		try:
			c = text.find('ul',class_ = 'volumePage navigation')
			a = c.find_all("a")
			post = str(a[-1].get('href'))
			pre = 'http://www.sciencedirect.com'
			url = pre + post
			return url
		except:
			return ''


	def get_hyperlink(self,text):
		try:
			return str(text.a.get('href'))
		except:
			pass
	


	def download_page(self, url):
		headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) '
								  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
		}
		data = requests.get(url, headers = headers).content
		return data
	


	def get_article_name(self, text):
		try:
			res = str(text.a)[:-4]
			new = res.split('>')
			return new[-1]
			#return text.a.string
		except:
			print ""

	##under hyperlink to gey abstract
	def get_abstract(self, text):
		try:
			ab = text.find('h2',string='Abstract')
			ab_1 = ab.next_sibling.string
			return str(ab_1)
		except:
			return []

	

	def get_JEL(self, text):
		try:
			JEL = []
			key = text.find("h2", text = "JEL classification")
			for row in key.next_sibling.find_all('span'):
				JEL.append(str(row.string))
			return JEL
		except:
			return []




	def get_keywords(self, text):
		try:
			keywords = []
			key = text.find("h2", text = 'Keywords')
			for row in key.next_sibling.find_all('span'):
				keywords.append(str(row.string))
			return keywords
		except:
			return []

	def get_volumne_issue(self, text):
		try:
			res = text.find('h2')
			result = res.br.string
			result = result.split(',')
			volumne = str(result[0])
			issue = str(result[1])
			return volumne, issue
		except:
			return []

	def get_page_numbers(self, text, index):
		try:
			b = text.find_all('li',class_ = 'source')
			return str(b[index].string)
		except:
			return []


	#soup.find_all("li",class_ = "authors")
	
	def get_authors(self,text,index):
		try:
			the_author = []
			all_author = text.find_all("li",class_ = "authors")
			#content = str(all_author[index].string)
			l = all_author[index].string
			return l
		except:
			return ''




	def get_internation_date(self, text):
		title = text.find('h2')
		for inter in title.strings:
			inter = str(inter)
			break
		index = str(title.br.string).index('(')
		date = str(title.br.string)[index+1:-1]
		return inter, date

	#soup = BeautifulSoup(page)
	def get_publicationDate(self, text):
		for dl in text.find_all('dl',{'class':'articleDates'}):
			return dl.get_text()


	def get_doi(self, page, text):
		m = re.search(".doi = '(.+?)'", page.decode("utf-8"))
		doi = ''
		if m:
			found = m.group(1)
			doi = 'http://dx.doi.org/'+ found
		if doi == '':
			pre = text.find('p',class_ = 'article-doi')
			doi = str(pre.a.get('href'))
		return doi



 #page = download_page('http://www.sciencedirect.com/science/article/pii/S0891422214000067?np=y')

crawler = ScienceDirect_crawl('result')
crawler.crawl()



