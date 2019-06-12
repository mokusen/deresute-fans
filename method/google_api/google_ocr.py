from pathlib import Path
from method.utils import handle_yaml, dele_logger
import requests
import json
import base64  # 画像はbase64でエンコードする必要があるため
import re
import io

token_path = Path(__file__).resolve().parents[0].joinpath("token.yml")
logger = dele_logger.set_logger(__name__)


def text_detection(image_path):
    API_KEY = handle_yaml.get_yaml(token_path)["api_key"]
    api_url = 'https://vision.googleapis.com/v1/images:annotate?key={}'.format(API_KEY)
    with io.open(image_path, "rb") as img:
        image_content = base64.b64encode(img.read())
        req_body = json.dumps({
            'requests': [{
                'image': {
                    'content': image_content.decode('utf-8')  # base64でエンコードしたものjsonにするためdecodeする
                },
                'features': [{
                    'type': 'TEXT_DETECTION'
                }]
            }]
        })
        res = requests.post(api_url, data=req_body).json()["responses"][0]["textAnnotations"][0]["description"][:-1]
        res_split = res.split("\n")
        print("Google Vision Return：", res_split)
        # よくある誤検知を修正する
        trans_res = res.translate(str.maketrans({'了': '7'}))

        re_res = re.sub(r'[^0-9\n万]*', '', trans_res)
        res_eight_five = re.sub(r'万([0-9]* *)*', '', re_res).split("\n")
        res_four_one = re.sub(r'([0-9]* *)*万', '', re_res).split("\n")

        # print(res_eight_five, res_four_one)
        if re.search(r'[a-zA-Z]', res):
            print("ERROR：Google Vision APIの返り値が不正です。DB構成の都合上、適当値で登録しています。")
            logger.error(f"GVAの返り値不正：{res_split}")

        fan_list = []
        for eight_five, four_one in zip(res_eight_five, res_four_one):
            try:
                if eight_five != four_one:
                    fan_list.append(int(eight_five) * 10000 + int(four_one))
                else:
                    fan_list.append(int(four_one))
            except:
                pass
        return fan_list
