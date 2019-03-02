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
url_addon = 'newsevents/pressreleases/monetary'

url_addon_2='boarddocs/press/'


urls=[url,url2,url_new,url_oldest_new,url_old_2,url_oldest]



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

def check_404(response):
    
    parsed_content = BeautifulSoup(response.content, "html.parser")
    try:
        return parsed_content.find('h2').text=='Page not found'
    except AttributeError as e:
        return False

def is_new_page(response):
    
    parsed_content = BeautifulSoup(response.content, "html.parser")

    return parsed_content.find('meta', attrs={'content':'IE=edge'})!=None


for i in urls:
    print('\nScraping',i)
    response = requests.get(i, timeout=5)
    print('Parsing')
    if is_new_page(response):

        text = parse_new(response)
    else:
        print('old')
        text=parse_old(response)
    
    select_par(text)
