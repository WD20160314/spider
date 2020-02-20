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
import re

import requests
from bs4 import BeautifulSoup

url_city = f'https://www.lagou.com/jobs/allCity.html'

#requests爬取
def download_all_htmls():
    htmls = []
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"}
    url = url_city
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        raise Exception('error')
    htmls.append(r.text)
    return htmls

def download_all_htmls2(city_list):
    htmls = []
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"}
    for city in city_list:
        url = f"https://www.lagou.com/jobs/list_python?city={city}&cl=false&fromSearch=true&labelWords=&suginput="
        print(url)
        r = requests.get(url, headers=headers)
        if r.status_code != 200:
            raise Exception('error')
        htmls.append(r.text)
    return htmls

#beautifulsoup解析
def parse_single_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    positions = soup.find_all('ul',class_='city_list')
    datas = []
    for position in positions:
        citys = position.find_all('li')
        for city in citys:
            city_title = city.find('a').text
            city_link = city.find('a')['href']
            datas.append(city_title)
    print(datas)
    datas = ['长沙']
    htmls = download_all_htmls2(datas)

    # data2= []
    # city_search = re.compile(r'www\.lagou\.com\/.*\/">(.*?)</a>')
    # data2 = set(city_search.findall(html))
    # print(data2)



    # filmsname = (soup.find_all('div', class_='info'))
    # datas=[]
    # for film in filmsname:
    #     name = film.find('span').text
    #     link = film.find('a')['href']
    #     rating = film.find('span',class_='rating_num').text
    #     comments = film.find('div',class_='star').find_all('span')[3].text.replace('人评价','')
    #     print('{} {} {} {}\n'.format(link, name, rating, comments))
    #     datas.append({
    #         'name':name,
    #         'link':link,
    #         'rating':rating,
    #         'comments':comments
    #     })
    # return datas


if __name__=='__main__':
    htmls = download_all_htmls()
    for html in htmls:
        parse_single_html(html)