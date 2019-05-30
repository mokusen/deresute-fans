from pathlib import Path
import cv2
import numpy as np


def idol_trimming(image_folder_path, image_path):
    # 設定値
    b_height = 50
    b_width = 50
    height_list = [78] * 5
    width_list = [72, 151, 230, 309, 388]

    # 画像サイズを統一する
    img = cv2.imread(str(image_folder_path.joinpath(image_path)))
    re_img = cv2.resize(img, (512, 288))

    # 5人のアイドルがいるため、5人分のアイコンを出力する
    for index in range(len(height_list)):
        height = height_list[index]
        width = width_list[index]
        dst = re_img[height: height + b_height, width: width + b_width]
        cv2.imwrite(f'{str(image_folder_path)}/r-{index}.png', dst)


def fans_trmiming(image_folder_path, image_path):
    # 設定値
    b_height = 11
    b_width = 70
    height_list = [213] * 5
    width_list = [62, 141, 220, 299, 378]
    unit_img_list = []

    # 画像サイズを統一する
    img = cv2.imread(str(image_folder_path.joinpath(image_path)))
    re_img = cv2.resize(img, (512, 288))

    # 意図的に5つ目の下にグレー画像を追加する
    # これを入れないとOCRしたとき、誤認識が多いため導入した
    base = cv2.imread(str(image_folder_path.joinpath("base.png")))

    # 5人のアイドルがいるため、ファン人数を1つの画像にまとめる
    for index in range(len(height_list)):
        height = height_list[index]
        width = width_list[index]
        dst = re_img[height: height + b_height, width: width + b_width]
        unit_img_list.append(dst)
        unit_img_list.append(base)

    # 5つのデータを合体させる
    unit_dst = cv2.vconcat(unit_img_list)
    cv2.imwrite(f'{str(image_folder_path.joinpath("r-fans.png"))}', unit_dst)


if __name__ == "__main__":
    path = Path(__file__).resolve().parents[2].joinpath("image/gPhoto")
    image_path = "gphoto.jpg"
    idol_trimming(path, image_path)
    fans_trmiming(path, image_path)
