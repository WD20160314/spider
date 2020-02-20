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

url_tmp = 'http://dianying.2345.com/top/'

#爬取url
def download_all_htmls():
    htmls = []
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"}
    url = url_tmp
    print(url)
    r = requests.get(url, headers=headers)
    r.encoding = "gbk"  ## 这里不设置编码为gdk，则显示乱码，所以需要添加这一行
    if r.status_code != 200:
        print(r.status_code)
        raise Exception('error')
    htmls.append(r.text)
    return htmls

#解析网页
def parse_one_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    movies_list = soup.find('ul', class_="picList clearfix")
    movies = movies_list.find_all('li')
    datas = []
    for content in movies:
        name = content.find('span',class_='sTit').text
        img = 'http:'+content.find('img',)['src']
        print(img)
        with open('.\\data\\' + str(name) + '.png', 'wb+') as f:
            f.write(requests.get(img).content)
        try:
            time = content.find('span',class_='sIntro').text.replace('上映时间：','')
        except:
            time = 'NA'
        actor_tmp =content.find('p',class_='pActor')
        actorlist = actor_tmp.find_all('a')
        actor = ''
        for actors in actorlist:
            actor += actors.text+' '
        desc = content.find('p',class_='pTxt pIntroShow').text.replace('展开全部','')
        print('{} {} {} {}\n'.format(name, time, actor, desc))
        datas.append({
            'name':name,
            'time':time,
            'actor':actor,
            'desc':desc,
        })
    return datas


#主函数
if __name__ == '__main__':
    all_datas = []
    #1.爬取url
    htmls = download_all_htmls()
    #2.解析html
    for html in htmls:
        all_datas.extend(parse_one_page(html))
    #3.生成dataframe
    df = pd.DataFrame(all_datas)
    df.to_excel('2345电影排行.xlsx', index=False)

