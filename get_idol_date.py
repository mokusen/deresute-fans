import requests
from method.models import connect_mysql
from bs4 import BeautifulSoup

target_url = 'https://imascg-slstage.boom-app.wiki/entry/idol-kanalist'
r = requests.get(target_url)
soup = BeautifulSoup(r.text, 'lxml')

for div_tag in soup.find_all("div", class_="basic"):
    for td_tag in div_tag.find_all("td", class_="text-center"):
        idol_name = td_tag.find("small").string

        # アイドル情報を登録する
        connect_mysql.insert_idol_base([idol_name])
