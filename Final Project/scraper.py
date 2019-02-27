from bs4 import BeautifulSoup
import requests

url = 'https://www.federalreserve.gov/newsevents/pressreleases/monetary20190130a.htm'
url2='https://www.federalreserve.gov/newsevents/pressreleases/monetary20181108a.htm'
url_new='https://www.federalreserve.gov/newsevents/pressreleases/monetary20141217a.htm'
url_oldest_new='https://www.federalreserve.gov/newsevents/pressreleases/monetary20060510a.htm'
url_old_2 = 'https://www.federalreserve.gov/boarddocs/press/monetary/2004/20040128/default.htm'
url_oldest = 'https://www.federalreserve.gov/boarddocs/press/general/2000/20000202/'

response = requests.get(url_oldest, timeout=5)



def parse_new(response):
   
    parsed_content = BeautifulSoup(response.content, "html.parser")

    text=parsed_content.find('div',attrs={'class':'col-xs-12 col-sm-8 col-md-8'})

    return text

def parse_old(response):

    parsed_content = BeautifulSoup(response.content, "html.parser")

    text=parsed_content.find_all('td','p')

    return text

text = parse_old(response)

#print(text.find_all('p'))
paragraphs = []
for i in text.find_all('p'):
    i=i.text
    paragraphs.append(i)

print(paragraphs)
