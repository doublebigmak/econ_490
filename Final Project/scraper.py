from bs4 import BeautifulSoup
import requests

url = 'https://www.federalreserve.gov/newsevents/pressreleases/monetary20190130a.htm'

response = requests.get(url, timeout=5)

parsed_content = BeautifulSoup(response.content, "html.parser")

text=parsed_content.find('div',attrs={'class':'col-xs-12 col-sm-8 col-md-8'})

#print(text.find_all('p'))
paragraphs = []
for i in text.find_all('p'):
    i=i.text
    paragraphs.append(i)

print(paragraphs)
