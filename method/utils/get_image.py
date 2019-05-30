from pathlib import Path
import shutil
import requests


def download_img(url, fold_path, file_name):
    if not fold_path.exists():
        fold_path.mkdir()
    input_file_name = fold_path.joinpath(file_name)
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(input_file_name, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
