import urllib
import requests
import bs4
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import re

data = pd.DataFrame(columns=["Title","Location","Company","Salary", "Description"])
url_template = "https://id.indeed.com/jobs?q=fresh+graduate&l=Indonesia&start={}"
max = 5000 #determine max job posting would be scraped
results = []

for start in range(0, max, 10):
    url = url_template.format(start)        
    # Append to the full set of results
    html = requests.get(url)
    soup = BeautifulSoup(html.content, 'html.parser', from_encoding="utf-8")
    for each in soup.find_all(class_= "result" ):
        try: 
            title = each.find(class_='jobtitle').text.replace('\n', '')
            location = each.find(class_ = "location" ).text.replace('\n', '')
            company = each.find(class_='company').text.replace('\n', '')
            salary = each.find(class_= "no-wrap").text.replace('\n', '')
            li = each.find("a", "jobtitle turnstileLink").get("href")
        except:
            title = 'None'
            location = 'None'
            company = 'None'
            salary = 'None'
            li = "None"
        
        link = "https://id.indeed.com" + str(li)
        ur = requests.get(link)
        ur = ur.text
        soup = BeautifulSoup(ur, "lxml")
        try:
            stat = soup.find("div", "jobsearch-jobDescriptionText").get_text()
        except: 
            stat = "None"
        data = data.append({'Title':title, 'Location':location, 'Company':company, 'Salary':salary, 'Description':stat}, ignore_index=True)
        
data.to_csv("indeed_scraping.csv")
