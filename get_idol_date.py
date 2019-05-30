from method.sql import connect_mysql
from method.utils import handle_yaml
from pathlib import Path
from bs4 import BeautifulSoup
import requests
import yaml

target_url = 'https://imascg-slstage.boom-app.wiki/entry/idol-kanalist'
r = requests.get(target_url)
soup = BeautifulSoup(r.text, 'lxml')

idol_image_path = Path(__file__).resolve().parents[0].joinpath('idol_name.yml')
yml = handle_yaml.get_yaml(idol_image_path)

for div_tag in soup.find_all("div", class_="basic"):
    for td_tag in div_tag.find_all("td", class_="text-center"):
        idol_name = td_tag.find("small").string

        # アイドル情報を登録する
        print([idol_name, yml[idol_name]])
        connect_mysql.insert_idol_base([idol_name, yml[idol_name]])
