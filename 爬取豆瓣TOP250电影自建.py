#!/usr/bin/python
#-*- encoding utf-8 -*-
# FILE_HEADER--------------------------------------------------------------------------------------
# ASB Copyright  (c)
# ASB Company Confidential
#--------------------------------------------------------------------------------------------------
# FILE NAME             : test.py
# DEPARTMENT            : ASB WSPD TD-LTE RRH
# AUTHOR                : Wudi
# AUTHOR'S EMAIL        : wudi.a.Cao@alcatel-sbell.com.cn
#--------------------------------------------------------------------------------------------------
# RELEASE HISTORY
# VERSION               : DATE              : AUTHOR            : DESCRIPTION
# 1.0                   : 2020-02-02        : Wudi      : 
#--------------------------------------------------------------------------------------------------
# KEYWORDS              :
#--------------------------------------------------------------------------------------------------
# PURPOSE               :
#--------------------------------------------------------------------------------------------------
# PARAMETERS            
# PARAM_NAME            : RANGE             : DESCRIPTION       : DEFAULT           : UNITS
#
#--------------------------------------------------------------------------------------------------
# REUSE ISSUES          :
# Reset Strategy        : 
# Clock  Domains        : 
# Asynchronous I/F      : 
# Scan Methodology      : 
# Instaniations         : 
# Synthesizable         : 
# Other                 : 
# END_HEADER----------------------------------------------------------------------------------------

import requests
from bs4 import BeautifulSoup
import pandas as pd

page_index = range(0,250,25)

#requests爬取
def download_all_htmls():
    htmls = []
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"}
    for idx in page_index:
        url = f'https://movie.douban.com/top250?start={idx}&filter='
        r = requests.get(url, headers=headers)
        if r.status_code != 200:
            raise Exception('error')
        htmls.append(r.text)
    return htmls


#beautifulsoup解析
def parse_single_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    filmsname = (soup.find_all('div', class_='info'))
    datas=[]
    for film in filmsname:
        name = film.find('span').text
        link = film.find('a')['href']
        rating = film.find('span',class_='rating_num').text
        comments = film.find('div',class_='star').find_all('span')[3].text.replace('人评价','')
        print('{} {} {} {}\n'.format(link, name, rating, comments))
        datas.append({
            'name':name,
            'link':link,
            'rating':rating,
            'comments':comments
        })
    return datas

all_datas = []
htmls = download_all_htmls()
for i, html in enumerate(htmls):
    all_datas.extend(parse_single_html(html))

df = pd.DataFrame(all_datas)
df.to_excel('电影自建TOP250.xlsx', index=False)

