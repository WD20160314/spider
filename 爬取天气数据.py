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
import demjson

year = 2018
months = ['%d%02d' %(year, month) for month in range(1,13)]
print(months)

urls = [
    f'http://tianqi.2345.com/t/wea_history/js/{month}/54511_{month}.js' for month in months
]
print(urls)
all_datas = []
datas = []
for url in urls:
    r = requests.get(url)
    if r.status_code!=200:
        print(r.status_code)
        raise Exception()
    data = r.text.lstrip("var weather_str=").rstrip(";")
    datas.append(data)

for d in datas:
    tqInfos = demjson.decode(d)['tqInfo']
    #print(tqInfos)
    #print([x for x in tqInfos if len(x)>0])
    all_datas.extend([x for x in tqInfos if len(x)>0])
    # for tqInfo in tqInfos:
    #     data.append({
    #         'ymd':tqInfo['ymd'],
    #         'bWendu':tqInfo['bWendu'],
    #         'yWendu':tqInfo['yWendu'],
    #         'tianqi':tqInfo['tianqi'],
    #         'fengxiang':tqInfo['fengxiang'],
    #         'fengli':tqInfo['fengli'],
    #         'aqi':tqInfo['aqi'],
    #         'aqiInfo':tqInfo['aqiInfo'],
    #         'aqiLevel':tqInfo['aqiLevel'],
    #     })
print(len(all_datas))
df = pd.DataFrame(all_datas)
df.to_excel('2018天气数据.xlsx', index=False)
