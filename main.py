# from method.analy.imageAnaly import google_ocr
from method.google_api import get_gphotos_images, google_ocr
from method.utils import get_image, dele_logger
from method.image_analy import trimming_img, similarity_img
from method.sql import connect_mysql
from pathlib import Path
import datetime

logger = dele_logger.set_logger(__name__)

# 写真データを取得する
images_info = get_gphotos_images.get_images_info()

# 写真のurlと、creationTimeリストを作成する
try:
    images_info_list = list(reversed(images_info["mediaItems"]))
    image_url_list = [url["baseUrl"] for url in images_info_list]
    creation_list = [url["mediaMetadata"]["creationTime"] for url in images_info_list]
except:
    import sys
    sys.exit()
finally:
    print(f"対象件数：{len(image_url_list)}件")

# creation_listを日本語時間に変更する
jpn_creation_list = []
for c_time in creation_list:
    trans_time = c_time.translate(str.maketrans({'T': ' ', 'Z': ''}))
    jpn_time = datetime.datetime.strptime(trans_time, '%Y-%m-%d %H:%M:%S') + datetime.timedelta(hours=9)
    jpn_creation_list.append(jpn_time.strftime('%Y-%m-%d %H:%M:%S'))
print(jpn_creation_list)

# debug
# import pprint
# pprint.pprint(image_url_list)
# exit()

# 取得した画像分実行する
gphoto_folder_path = Path(__file__).resolve().parents[0].joinpath("image/gPhoto")
gphoto_name = 'gphoto.jpg'
for count in range(len(image_url_list)):
    print(f"{count+1}枚目：{jpn_creation_list[count]}")
    logger.info(f"{count+1}枚目：{jpn_creation_list[count]}")
    # Photosから取得した画像を保存する
    get_image.download_img(image_url_list[count], gphoto_folder_path, gphoto_name)

    # アイドル画像をトリミングして出力する
    trimming_img.idol_trimming(gphoto_folder_path, gphoto_name)

    # アイドル画像から類似度検索を行い、アイドル名を取得する
    idol_list = similarity_img.multi_process_similarity_main(output_switch=0)

    # 類似度判定において、全アイドルを返却しない場合は類似しないアイドルがいるため、強制終了とする
    if len(idol_list) != 5:
        continue

    # ファン人数をトリミングして出力する
    trimming_img.fans_trmiming(gphoto_folder_path, gphoto_name)

    # ファン人数画像をVision APIを使用して文字列化する
    fans_list = google_ocr.text_detection(str(gphoto_folder_path.joinpath("r-fans.png")))

    # 登録アイドル、ファン人数の重複を削除する
    unique_idol_list = list(dict.fromkeys(idol_list))
    unique_fans_list = list(dict.fromkeys(fans_list))
    if len(unique_idol_list) != len(unique_fans_list):
        logger.warning(f"GVA返り値不正が疑われます：idol：{unique_idol_list} fans：{unique_fans_list}")
    print(unique_idol_list)
    print(unique_fans_list)

    # アイドル名（アルファベット）を取得する
    idol_id_list = connect_mysql.select_idol_base()

    # データベースへ登録作業を行う
    for index in range(len(unique_idol_list)):
        connect_mysql.insert_idol_fans(idol_id_list.index(unique_idol_list[index])+1, unique_fans_list[index], jpn_creation_list[count])
