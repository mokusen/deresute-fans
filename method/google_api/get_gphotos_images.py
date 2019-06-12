from pathlib import Path
from method.utils import handle_yaml
import os
import requests
import yaml


token_path = Path(__file__).resolve().parents[0].joinpath("token.yml")
setting_path = Path(__file__).resolve().parents[2].joinpath("setting.yml")


def update_access_token():
    read_yml = handle_yaml.get_yaml(token_path)
    data = {
        'refresh_token': read_yml["refresh_token"],
        'client_id': read_yml["client_id"],
        'client_secret': read_yml["client_secret"],
        'grant_type': 'refresh_token'
    }
    access_token = requests.post('https://www.googleapis.com/oauth2/v4/token', data=data).json()["access_token"]
    read_yml["access_token"] = access_token
    handle_yaml.output_yaml(token_path, read_yml)


def get_gPhotos_images():
    token = handle_yaml.get_yaml(token_path)
    access_token = token["access_token"]
    api_key = token["api_key"]
    data_yml = handle_yaml.get_yaml(setting_path)["google_api"]
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-type': 'application/json',
    }
    data = str({
        "pageSize": data_yml['pageSize'],
        "filters":
        {"dateFilter":
            {"ranges":
                [
                    {"startDate":
                        {"year": data_yml["start"]["year"],
                         "month": data_yml["start"]["month"],
                         "day": data_yml["start"]["day"]
                         },
                     "endDate":
                        {"year": data_yml["end"]["year"],
                         "month": data_yml["end"]["month"],
                         "day": data_yml["end"]["day"]
                         }
                     }
                ]
             }
         }
    })
    response = requests.post(f'https://photoslibrary.googleapis.com/v1/mediaItems:search?key={api_key}', headers=headers, data=data)
    return response.json()


def get_images_info():
    """
    mediaItemsの情報をJSON形式で返却する
    Returns
    -------
    response: json
        mediaItems情報全て
    """
    response = get_gPhotos_images()
    if 'error' in response:
        update_access_token()
        response = get_gPhotos_images()
    return response
