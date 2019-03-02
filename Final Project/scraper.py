from bs4 import BeautifulSoup
import requests
import re



url = 'https://www.federalreserve.gov/newsevents/pressreleases/monetary20190130a.htm'
url2='https://www.federalreserve.gov/newsevents/pressreleases/monetary20181108a.htm'
url_new='https://www.federalreserve.gov/newsevents/pressreleases/monetary20141217a.htm'
url_oldest_new='https://www.federalreserve.gov/newsevents/pressreleases/monetary20060510a.htm'
url_old_2 = 'https://www.federalreserve.gov/boarddocs/press/monetary/2004/20040128/default.htm'
url_oldest = 'https://www.federalreserve.gov/boarddocs/press/general/2000/20000202/'

url_base ='https://www.federalreserve.gov/' 

url_news=[url,url2,url_new,url_oldest_new]

url_olds = [url_old_2,url_oldest]

def parse_new(response):
   
    parsed_content = BeautifulSoup(response.content, "html.parser")

    text=parsed_content.find('div',attrs={'class':'col-xs-12 col-sm-8 col-md-8'})

    return text

def parse_old(response):

    parsed_content = BeautifulSoup(response.content, "html.parser")

    text=parsed_content.find_all('td')
    
    if len(text)==1:
        return text[0]

    else:
        return text[1]

#text = parse_old(response)
#text = parse_new(response)
def select_par(text):

    paragraphs = []
    for para in text.find_all('p'):
        para=para.text
        para=remove_escape(para)
        paragraphs.append(para)
    
    print(paragraphs)
    return paragraphs
    
def remove_escape(paragraph):
    
    regex = re.compile(r'[\n\r\t]')
    paragraph = regex.sub("", paragraph)
    
    return paragraph

#print(text.find_all('p'))

for i in url_news:
    print('\nScraping',i)
    response = requests.get(i, timeout=5)
    print('Parsing')
    text = parse_new(response)
    
    select_par(text)

print('\n Old')

for i in url_olds:
    print('\nScraping',i)
    response = requests.get(i, timeout=5)
    print('Parsing')
    text = parse_old(response)
    
    select_par(text)