import requests

url = f'https://book.douban.com/subject/1084336/comments/'
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"}
r = requests.get(url, headers=headers)
print(r.url)
print(r.text)
info = r.raise_for_status()
info = r.encoding
print(info)
info = r.apparent_encoding
print(info)