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
from pyecharts.charts import Page, Pie, Bar
import pyecharts.options as opts


url_tmp = 'https://movie.douban.com/cinema/later/{}/'
page_index = ['shamghai']

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
    r = (soup.find_all('div', class_='intro'))
    datas=[]
    for film in r:
        name = film.find('a',class_='').text
        link = film.find('a', class_='')['href']
        info = film.find_all('li')
        date = info[0].text
        type = info[1].text
        people = info[3].text.replace('人想看','')
        print('{} {} {} {} {}'.format(name, link, date, type, people))
        datas.append({
            'name':name,
            'link':link,
            'date':date,
            'type':type,
            'people': people,
        })
    return datas

if __name__ == '__main__':

    all_data = []
    #1. 爬取url
    htmls = download_all_htmls()
    #2.解析html
    for html in htmls:
        all_data.extend(parse_one_page(html))

    #3.生成dataframe
    df = pd.DataFrame(all_data)
    df.columns = ['电影名', '链接', '上映日期', '类型', '期待人数']
    #df.to_excel('影讯.xlsx', index=False)
    #df.to_html('影讯.html',encoding='gbk')

    # 绘制关注者排行榜图
    df['期待人数'] = df['期待人数'].astype('int32')
    sort_by_lovers = df.sort_values(by=['期待人数'])
    all_names = sort_by_lovers['电影名']
    all_lovers = sort_by_lovers['期待人数']

    bar = (
        Bar()
            .add_xaxis(all_names.values.tolist())
            .add_yaxis("关注数", all_lovers.values.tolist())
            .set_global_opts(
                xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-90))
    )
            .reversal_axis()
            .set_series_opts(label_opts=opts.LabelOpts(position="right"))
    )
    bar.render('bar.html')


    pie = Pie()
    pie.add("", [list(z) for z in zip(all_names.values.tolist()[:8], all_lovers.values.tolist()[:8])])
    pie.set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    pie.set_global_opts(title_opts=opts.TitleOpts(title="Pie-电影关注数"),legend_opts=opts.LegendOpts(pos_left="15%"),)
    pie.render('pie.html')

