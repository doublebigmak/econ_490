from bs4 import BeautifulSoup
import requests
import re

import pandas as pd
import csv
import os



url_addon = 'newsevents/pressreleases/monetary'

url_addon_2='boarddocs/press/'

url_base ='https://www.federalreserve.gov/'



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
        try:
            return text[1]
        except IndexError as e:
            pass


def select_par(text):

    paragraphs = []
    for para in text.find_all('p'):
        para=para.text
        para=remove_escape(para)
        paragraphs.append(para)
    
    print(paragraphs)
    return paragraphs
    
def remove_escape(paragraph):
    
    regex = re.compile(r'[\n\r\t\xa0\u2003\u2011]')
    paragraph = regex.sub("", paragraph)
    
    return paragraph

def check_404(url):

    
    response = requests.get(url, timeout=10)
    parsed_content = BeautifulSoup(response.content, "html.parser")
    try:
        return parsed_content.find('h2').text=='Page not found'
    except AttributeError as e:
        return False

def is_new_page(response):
    
    parsed_content = BeautifulSoup(response.content, "html.parser")

    return parsed_content.find('meta', attrs={'content':'IE=edge'})!=None


def scrape_func(url,date):

    print('\nScraping',url)
    response = requests.get(url, timeout=10)
    print('Parsing')
    if is_new_page(response):

        text = parse_new(response)
    else:
        print('old')
        text=parse_old(response)
    
    if text==None:
        return None

    else:

        paragraph=select_par(text)
        paragraph.append(date)
        with open(date+'.csv','w') as file:
            wr = csv.writer(file, quoting=csv.QUOTE_ALL)
            wr.writerow(paragraph)


date1 = '2015-04-29'
date2 = '2015-04-29'
dates = pd.date_range(date1, date2,freq='B')
stringed_dates = dates.strftime('%Y%m%d')

def main():
    for date in stringed_dates:
        if check_404(url_base+'boarddocs/press/'+'general/'+date[:4]+'/'+date+'/')==False:
            url = url_base+'boarddocs/press/'+'general/'+date[:4]+'/'+date+'/'
            scrape_func(url,date)
        elif check_404(url_base+'boarddocs/press/'+'monetary/'+date[:4]+'/'+date+'/'+'default.htm')==False:
            url = url_base+'boarddocs/press/'+'monetary/'+date[:4]+'/'+date+'/'+'default.htm'
            scrape_func(url,date)
        elif check_404(url_base+'newsevents/pressreleases/monetary'+date+'a.htm')==False:
            url=url_base+'newsevents/pressreleases/monetary'+date+'a.htm'
            scrape_func(url,date)
        else:
            pass

main()