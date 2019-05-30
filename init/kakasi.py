from pykakasi import kakasi
import yaml
import os

com_img_path = '../image/'
files = os.listdir(com_img_path)

for file in files:
    k = kakasi()
    k.setMode("K", "a")
    k.setMode("H", "a")
    k.setMode("J", "a")
    k.setMode("r", "Hepburn")
    k.setMode("s", True)

    conv = k.getConverter()

    idol_name = conv.do(file)
    with open('../idol_name_base.yml', 'a', encoding='utf-8') as bdi:
        yaml.dump({file: idol_name}, bdi, encoding='utf-8', allow_unicode=True, default_flow_style=False)
