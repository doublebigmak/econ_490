"""
author: @michael mak
script to get fomc meeting/statement dates

"""

from bs4 import BeautifulSoup
import requests
import re

import pandas as pd

#url for currently 2014 onwards statements
new_url = 'https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm'

year = str(2013) # placeholder year 
historical_url = 'https://www.federalreserve.gov/monetarypolicy/fomchistorical'+year+'.htm'

response=requests.get(new_url, timeout=10)

parsed_content = BeautifulSoup(response.content, "html.parser")