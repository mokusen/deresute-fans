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
    b_height = 29
    b_width = 180
    height_list = [553] * 5
    width_list = [165, 370, 575, 780, 985]
    unit_img_list = []

    # 画像サイズを統一する
    img = cv2.imread(str(image_folder_path.joinpath(image_path)))
    re_img = cv2.resize(img, (1334, 750))

    # 5人のアイドルがいるため、ファン人数を1つの画像にまとめる
    for index in range(len(height_list)):
        height = height_list[index]
        width = width_list[index]
        dst = re_img[height: height + b_height, width: width + b_width]
        unit_img_list.append(dst)

    # 5つのデータを合体させる
    unit_dst = cv2.vconcat(unit_img_list)
    kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]], np.float32)
    # kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], np.float32)
    near_dst = cv2.filter2D(unit_dst, -1, kernel)
    re_img = cv2.resize(near_dst, (700, 650))

    cv2.imwrite(f'{str(image_folder_path.joinpath("r-fans.png"))}', re_img)


if __name__ == "__main__":
    path = Path(__file__).resolve().parents[2].joinpath("image/gPhoto")
    # image_path = "gphoto.jpg"
    # image_path = "miss_1.png"
    # image_path = "miss_2.png"
    # image_path = "miss_3.png"
    # image_path = "miss_4.png"
    # image_path = "miss_5.png"
    # image_path = "miss_6.png"
    # image_path = "miss_7.png"
    # image_path = "miss_8.png"
    # image_path = "miss_9.png"
    # image_path = "miss_10.png"
    # image_path = "inclued_A_1.png"
    # image_path = "inclued_A_2.png"
    # image_path = "inclued_A_3.png"
    # image_path = "inclued_A_4.png"
    # image_path = "inclued_A_5.png"
    image_path = "inclued_A_6.png"
    # image_path = "1.jpg"
    # image_path = "1.png"
    # image_path = "2.jpg"
    # image_path = "3.png"
    # image_path = "4.png"
    # image_path = "5.jpg"
    # image_path = "7.jpg"
    # image_path = "8.jpg"
    # image_path = "8.png"
    idol_trimming(path, image_path)
    fans_trmiming(path, image_path)
