"""
author: @michael mak
script to get fomc meeting/statement dates

"""
from bs4 import BeautifulSoup
import requests
import re
import numpy as np
import pandas as pd
from datetime import datetime

#url for currently 2014 onwards statements
new_url = 'https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm'

def getNewDates(url):
    
    #initialize lists
    years=[]
    dates=[]

    econ_proj_dates = []

    response=requests.get(new_url, timeout=10)
    parsed_content = BeautifulSoup(response.content, "html.parser")

    article = parsed_content.find(attrs={'id':'article'})
    year_panels = article.find_all(attrs={'class':'panel panel-default'})
    
    
    
    for item in year_panels:
    
        years.append(item.find('a').string.split()[0])
        year = item.find('a').string.split()[0]
        months = item.find_all(class_='fomc-meeting__month')
        days = item.find_all(class_='fomc-meeting__date')
    
        for i in range(len(months)):
            #unscheduled = 0
            econ_proj = 0
            month = months[i].string.split('/')[-1:][0]
        
            day = re.sub('\D',"", days[i].string.split('-')[-1:][0])

            try:
                date=datetime.strptime(year+month+day,'%Y%B%d')
            except ValueError:
                date=datetime.strptime(year+month+day,'%Y%b%d')
            dates.append(date.strftime("%Y%m%d"))
            if '*' in days[i].string.split('-')[-1:][0]:
                econ_proj = 1
            #if 'unscheduled' in days[i].string.split('-')[-1:][0]:
            #    unscheduled = 1
        
            #unscheduled_dates.append(unscheduled)
            econ_proj_dates.append(econ_proj)
        

    release_dates = pd.DataFrame({'Dates':dates,
                                  'Summary of Econ Projections':econ_proj_dates})
    return release_dates


def parse_state_date(panels):
    dates=[]
    for item in panels:
        for a in item.find_all('a', href=True):
            if "Statement" in a.string:
            
                #date_str = panel.find(attrs={'class':"panel-heading panel-heading--shaded"}).string
                if re.sub('\D',"", a['href'].split('/')[-1])=='':
                    
                    date=re.sub('\D',"", a['href'].split('/')[-2])
                else:
                    date=re.sub('\D',"", a['href'].split('/')[-1])
                dates.append(date)
    
    return dates


def parse_proj(panels):
    
    projection_dates=[]
    for item in panels:
        
        for a in item.find_all('a', href=True):
            econ_proj = 0
            if "Statement" in a.string:
                for i in item.find_all('a', href=True):
                    if "Individual Projections" in i.string:
                        econ_proj = 1
                
                projection_dates.append(econ_proj)

    return projection_dates

old_release_dates=pd.DataFrame(columns=['Dates','Summary of Econ Projections'])

for year in range(2000,2014,1):
    year = str(year)
    historical_url = 'https://www.federalreserve.gov/monetarypolicy/fomchistorical'+year+'.htm'
    response=requests.get(historical_url, timeout=10)

    parsed_content = BeautifulSoup(response.content, "html.parser")
    panels = parsed_content.find_all(class_='panel-default')

    
    old_dates = pd.DataFrame({'Dates':parse_state_date(panels),
                              'Summary of Econ Projections':parse_proj(panels)})
    old_release_dates = old_release_dates.append(old_dates)

release_dates = getNewDates(new_url)
all_dates = old_release_dates.append(release_dates)

all_dates.sort_values(by='Dates').to_csv(r'statement_dates.csv',index=None,header=True)