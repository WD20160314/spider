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

url_tmp = 'https://book.douban.com/subject/1084336/comments/hot?p={}'
#data = requests.get(url)
#print(data.status_code) #//418 说明需要header
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"}
htmls = []
for i in range(0,100):
    url = url_tmp.format(i)
    r = requests.get(url, headers=headers)
    #print(r.status_code) # 200说明请求正常
    htmls.append(r.text)  #把爬取的数据存到data变量里

datas = []
for html in htmls:
    soup = BeautifulSoup(html, 'html.parser') #将数据用beautifuksoup进行解析
    filmename = soup.find_all('a', class_='comment-info')
    #print(filmename) #返回为空， 说明找不到标签为a，类为'comment-info'的数据

    comments = soup.find_all('div', class_='comment')
    #print(filmename) #这个能找到数据，但是包含了多余的信息
    #print(comments)

    for comment in comments:
        comment_info = comment.find('span', class_='comment-info')
        date = comment_info.find('span',class_='').text
        link = comment_info.find('a')['href']
        name = comment_info.find('a').text
        content = comment.find('span', class_='short').text[:100].strip()
        print('{} {} {} {}'.format(link, name, date, content))
        datas.append({
            'link':link,
            'name':name,
            'last_time':date,
            'content':content
        })

#创建dataframe用来储存字典datas到excel
df = pd.DataFrame(datas)
df.to_excel('豆瓣影评.xlsx',index=False)


