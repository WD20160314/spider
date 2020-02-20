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
import os
from hashlib import md5

url_tmp = 'https://www.mzitu.com/page/{}/'
page_index = range(0,1)

def download_all_htmls():
    htmls = []
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"}
    for idx in page_index:
        url = url_tmp.format(idx)
        print(url)
        r = requests.get(url, headers=headers)
        if r.status_code != 200:
            print(r.status_code)
            raise Exception('error')
        htmls.append(r.text)
    return htmls

def parse_one_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    r = (soup.find('ul', id='pins'))
    datas = []
    list = r.find_all('li')
    for l in list:
        link = l.find('a')['href']
        desc = l.find('img')['alt']
        pic =  l.find('img')['data-original']
        date = l.find('span', class_='time').text
        print('{} {} {} {} '.format(link, desc, date, pic))
        datas.append({
            'link':link,
            'desc':desc,
            'pic':pic,
            'date':date,
        })
    return datas

if __name__ == '__main__':
    all_data = []
    #1. 爬取url
    htmls = download_all_htmls()
    #2.解析html
    for html in htmls:
        all_data.extend(parse_one_page(html))
    #3 写入文件
    df = pd.DataFrame(all_data)
    df.to_excel('妹子图.xlsx',index=False)
