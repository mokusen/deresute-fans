from pathlib import Path
from method.utils import handle_yaml
import requests
import json
import base64  # 画像はbase64でエンコードする必要があるため
import re

token_path = Path(__file__).resolve().parents[0].joinpath("token.yml")


def text_detection(image_path):
    API_KEY = handle_yaml.get_yaml(token_path)["api_key"]
    api_url = 'https://vision.googleapis.com/v1/images:annotate?key={}'.format(API_KEY)
    with open(image_path, "rb") as img:
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
        print(res)
        res_eight_five = re.sub(r'万([0-9]* *)*|人| |　', '', res).split("\n")
        res_four_one = re.sub(r'([0-9]* *)*万|人| |　', '', res).split("\n")
        print(res_eight_five, res_four_one)
        fan_list = [int(eight_five)*10000 + int(four_one) if eight_five != four_one else int(four_one) for eight_five, four_one in zip(res_eight_five, res_four_one)]
        return fan_list
