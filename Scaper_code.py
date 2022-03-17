# -*- coding: utf-8 -*-
"""
Created on Tue Jan 25 17:51:57 2022

@author: aryam
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
url="https://in.indeed.com/jobs?q={}&l={}&&start={}&vjk=949929f74a1aba6a"

job=input("Enter Job Title:")
country=input("Enter your location:")
p=int(input('Enter number of pages you want to scrap:'))
def S_Creator(job,country,url,page):
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.81 Safari/537.36'}
    url=url.format( job,country,page)
    r=requests.get(url,headers)
    soup=BeautifulSoup(r.content,'html.parser')
    return soup    
def transform(soup):
    divs=soup.find_all('div',class_='job_seen_beacon')
    for tags in divs:
        h2=tags.find('h2',class_='jobTitle')
        try:    
            company=tags.find('span',class_='companyName').text.strip()
        except:
            company=''
        spans=h2.find_all('span')
        title=''
        for span in spans:
            if(span.text!='new'):
                title=span.text
        try:
            title.replace(";","")
        except:
           title.strip()   
        try:
            location=tags.find('div',class_='companyLocation').text.strip()
        except:
            location=''    
        try:
            Salary=tags.find('div',class_='salary-snippet').text.strip()
        except:
            Salary='Not Disclosed'  
        Summary=tags.find('tr',class_='underShelfFooter').text.strip() 
        job={
        'Title':title,
        'Company Name':company,
        'Location':location,
        'Salary':Salary,
        'Summary':Summary
        }
        jobList.append(job)                 
        #print("Title:{}\nCompany:{} \nLocation:{}\nSalary:{}\nSummary:{}".format(title,company,location,Salary,Summary))
        #print()
        #print()
        
jobList=[]      
for i in range(0,p):
    soup=S_Creator(job,country,url,p*10)
    transform(soup)
df=pd.DataFrame(jobList)
print(df)
df.to_csv('Jobs.csv',index=False)
#print(jobList)