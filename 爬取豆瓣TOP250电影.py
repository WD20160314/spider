import requests
from bs4 import BeautifulSoup
import pandas as pd
import pprint

#1.下载HTML页面
page_index = range(0,250,25)
print(list(page_index))

def download_all_htmls():
    htmls = []
    for idx in page_index:
        url = f'https://movie.douban.com/top250?start={idx}&filter='
        print('craw html:', url)
        r = requests.get(url,
                         headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"})
        if r.status_code != 200:
            raise Exception('error')
        htmls.append(r.text)
    return htmls

#2.解析HTML数据
def parse_single_html(html):
    soup = BeautifulSoup(html,'html.parser')
    article_items = (
        soup.find('div', class_='article')
        .find('ol', class_='grid_view')
        .find_all('div', class_='item')
    )
    datas = []

    for article_item in article_items:
        rank = article_item.find('div', class_='pic').find('em').get_text()
        info = article_item.find('div', class_='info')
        title = info.find('div', class_='hd').find('span', class_='title').get_text()
        stars = (
            info.find('div', class_='bd')
            .find('div', class_='star')
            .find_all('span')
        )
        rating_star = stars[0]['class'][0]
        rating_num = stars[1].get_text()
        comments = stars[3].get_text()

        datas.append({
            "rank": rank,
            "title": title,
            "rating_star": rating_star.replace("rating", "").replace("-t", ""),
            "rating_num": rating_num,
            "comments": comments.replace("人评价", "")
        })
    return datas



htmls = download_all_htmls()
# 执行所有的HTML页面的解析
all_datas = []
for html in htmls:
    all_datas.extend(parse_single_html(html))

#将结果存入dataFrame
df = pd.DataFrame(all_datas)
df.to_excel(f'豆瓣电影TOP250.xlsx', index=False)
