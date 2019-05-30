import os
import yaml

idol_image_path = '../image/'
files = os.listdir(idol_image_path)

with open('../idol_name.yml', encoding='utf-8') as bdi:
    yml = yaml.load(bdi, Loader=yaml.FullLoader)

for file in files:
    os.rename(f"{idol_image_path}{file}", f"{idol_image_path}{yml[file]}")
