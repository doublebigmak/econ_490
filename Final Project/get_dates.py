"""
author: @michael mak
script to get fomc meeting/statement dates

"""

from bs4 import BeautifulSoup
import requests
import re
import numpy as np
import pandas as pd


#url for currently 2014 onwards statements
new_url = 'https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm'

year = str(2013) # placeholder year 
historical_url = 'https://www.federalreserve.gov/monetarypolicy/fomchistorical'+year+'.htm'

response=requests.get(new_url, timeout=10)

parsed_content = BeautifulSoup(response.content, "html.parser")

article = parsed_content.find(attrs={'id':'article'})
year_panels = article.find_all(attrs={'class':'panel panel-default'})
panel_headings = article.find_all(attrs={'class':'panel-heading'})
#print(article)
#print(panel_headings)


years=[]
for item in year_panels:

    years.append(item.find('a'))

print(years)
#print(year_panels)