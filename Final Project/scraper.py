from bs4 import BeautifulSoup
import requests

url = 'https://www.federalreserve.gov/newsevents/pressreleases/monetary20190130a.htm'

test_url = 'https://www.michael-mak.ca'

response = requests.get(url, timeout=5)

print(response.content)