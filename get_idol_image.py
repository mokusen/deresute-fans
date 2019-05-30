import requests
from method.utils import get_image
from pathlib import Path
from bs4 import BeautifulSoup

image_folder_path = Path(__file__).resolve().parents[0].joinpath('image')


def get_idol_img_scraping():
    base_url = 'https://imascg-slstage.boom-app.wiki'
    target_url = base_url + '/entry/idol-kanalist'
    r = requests.get(target_url)
    soup = BeautifulSoup(r.text, 'lxml')

    for div_tag in soup.find_all("div", class_="basic"):
        for td_tag in div_tag.find_all("td", class_="text-center"):
            # アイドル専用ページへの遷移URLを取得する
            idol_url = base_url + td_tag.find("a").get('href')
            idol_name = td_tag.find("small").string

            # アイドル専用ページから、カードアイコンを取得する
            rr = requests.get(idol_url)
            rr_soup = BeautifulSoup(rr.text, 'lxml')
            count = 1
            for idol_div_tag in rr_soup.find_all("div", class_="basic"):
                for idol_td_tag in idol_div_tag.find_all("td", class_="text-center"):
                    for idol_img in idol_td_tag.find_all("img", attrs={"style": "margin: 1px;"}):
                        idol_src = idol_img.get("src")
                        idol_folder_path = image_folder_path.joinpath(idol_name)
                        get_image.download_img(idol_src, idol_folder_path, f"{count}.jpg")
                        count += 1


if __name__ == '__main__':
    get_idol_img_scraping()
