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

#导入库
import requests
from bs4 import BeautifulSoup
import pandas as pd

url_tmp = 'https://www.buxiuse.com/?pager_offset={}'

#爬取url
def download_all_htmls():
    htmls = []
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"}
    for idx in range(0,3):
        url = url_tmp.format(idx)
        print(url)
        r = requests.get(url, headers=headers)
        #r.encoding = "gbk"  ## 这里不设置编码为gdk，则显示乱码，所以需要添加这一行
        if r.status_code != 200:
            print(r.status_code)
            raise Exception('error')
        htmls.append(r.text)
    return htmls

#解析网页
def parse_one_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    r = soup.find('ul', class_='thumbnails')
    lis = r.find_all('li')
    img_urls = []
    for li in lis:
        img_url = li.find('img')['src']
        img_urls.append({
            'url':img_url,
        })
    return img_urls

#主函数
if __name__ == '__main__':
    all_datas = []
    #1.爬取url
    htmls = download_all_htmls()
    # #2.解析html
    for html in htmls:
        all_datas.extend(parse_one_page(html))

    for idx, list in enumerate(all_datas):
        print('.\\data\\{}'.format(list['url'][-10:]))
        with open('.\\data\\{}'.format(list['url'][-10:]), 'wb+') as f:
            f.write(requests.get(list['url']).content)

    # #3.生成dataframe
    # df = pd.DataFrame(all_datas)