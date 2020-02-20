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

from pyecharts.charts import Bar
from pyecharts import options as opts
from pyecharts.charts import Calendar

#使用主题
from pyecharts.globals import ThemeType

import datetime
import random
def calendar_base() -> Calendar:
    begin = datetime.date(2017, 1, 1)
    end = datetime.date(2017, 12, 31)
    data = [
        [str(begin + datetime.timedelta(days=i)), random.randint(1000, 25000)]
        for i in range((end - begin).days + 1)
    ]

    c = (
        Calendar()
        .add("", data, calendar_opts=opts.CalendarOpts(range_="2017"))
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Calendar-2017年微信步数情况"),
            visualmap_opts=opts.VisualMapOpts(
                max_=20000,
                min_=500,
                orient="horizontal",
                is_piecewise=True,
                pos_top="230px",
                pos_left="100px",
            ),
        )
    )
    return c

c = calendar_base()
c.render()

from pyecharts import options as opts
from pyecharts.charts import Gauge, Page


def gauge_base() -> Gauge:
    c = (
        Gauge()
        .add("", [("完成率", 66.6)])
        .set_global_opts(title_opts=opts.TitleOpts(title="Gauge-基本示例"))
    )
    return c
g = gauge_base()
g.render()

bar = (
    Bar()
    #Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
    .add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
    .add_yaxis("商家A", [5, 20, 36, 10, 75, 90])
    .add_yaxis("商家B", [15, 6, 45, 20, 35, 66])
    .set_global_opts(title_opts=opts.TitleOpts(title="主标题", subtitle="副标题"))
)
bar.render()

from pyecharts.charts import Geo
from pyecharts.faker import Faker
from pyecharts import options as opts
from pyecharts.charts import Geo
from pyecharts.globals import ChartType, SymbolType
from pyecharts.charts import Map
def map_visualmap() -> Map:
    c = (
        Map()
        .add("商家A", [list(z) for z in zip(Faker.provinces, Faker.values())], "china")
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Map-VisualMap（连续型）"),
            visualmap_opts=opts.VisualMapOpts(max_=200),
        )
    )
    return c

g = map_visualmap()
g.render()