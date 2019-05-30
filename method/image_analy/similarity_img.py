#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""hist matching."""

from pathlib import Path
import cv2
import re
import concurrent.futures

image_folder_path = Path(__file__).resolve().parents[2].joinpath("image")


def similarity(target_file, img_dir, output_switch, cal_mode):
    """
    Parameters
    ----------
    target_file : str
        filename.png(.jpg)等の拡張子付きファイル名

    img_dir : str
        探索フォルダパス

    output_switch : int
        0:出力しない
        1:検索画像名、各類似度を出力する
        2:TOP10を出力する

    cal_mode : int
        0:（default）AKAZEモード
        1:ORBモード

    Returns
    -------
    idol_name : str
        検索画像のアイドル名
    """
    # 初期設定
    IMG_SIZE = (200, 200)
    similarity_dict = {}

    # 検索画像の情報
    target_img_path = str(img_dir.joinpath(target_file))
    target_img = cv2.imread(target_img_path)
    target_img = cv2.resize(target_img, IMG_SIZE)

    # 特徴量の類似度
    bf = cv2.BFMatcher(cv2.NORM_HAMMING)
    if cal_mode == 0:
        detector = cv2.AKAZE_create()
    elif cal_mode == 1:
        detector = cv2.ORB_create()
    else:
        return
    (target_kp, target_des) = detector.detectAndCompute(target_img, None)

    if output_switch == 1:
        print(f'TARGET_FILE: {target_file}')

    for index, image_folders in enumerate(image_folder_path.iterdir()):
        image_folder_name = image_folders.name
        if image_folder_name == "gPhoto":
            continue
        # ../image/{idol_name}/を探索する
        search_folder_path = image_folder_path.joinpath(image_folder_name)
        for file_path in search_folder_path.iterdir():
            if file_path.name == '.DS_Store':
                continue
            comparing_img_path = str(file_path)
            try:
                comparing_img = cv2.imread(comparing_img_path)
                comparing_img = cv2.resize(comparing_img, IMG_SIZE)
                (comparing_kp, comparing_des) = detector.detectAndCompute(comparing_img, None)
                matches = bf.match(target_des, comparing_des)
                dist = [m.distance for m in matches]
                ret = sum(dist) / len(dist)
            except cv2.error:
                ret = 1000000
            except ZeroDivisionError:
                ret = 1000000
            finally:
                similarity_dict[file_path] = float(f"{ret:.1f}")
                if output_switch == 1:
                    print(f"{index:>3}: {comparing_img_path:>30}: {ret:>5.1f} %")

    # 最小値算出
    min_img_path = min(similarity_dict, key=similarity_dict.get)
    min_value = similarity_dict[min_img_path]
    # 結果出力
    if output_switch != 0:
        print(f"\nRESULT\npath: {min_img_path}, values: {min_value}")

    # 出力（TOP10等）
    if output_switch == 2:
        print("\nTOP10")
        count = 0
        for key, value in sorted(similarity_dict.items(), key=lambda x: x[1]):
            if count == 10:
                break
            print(f"path: {key:>30}, values: {value}")
            count += 1

    return min_img_path, min_value


def __output_mode(min_img_path, output_mode, idol_name_list):
    """
    アイドル名をモードによってはリストに追加して返却する

    Parameters
    ----------
    output_mode : int
        0:最適画像パスと類似度を出力する
        1:最適画像のアイドル名を返却する

    Returns
    -------
    idol_name_list : list
        idol_name_listに追加して返却する
    """
    if output_mode == 1:
        idol_name = min_img_path.parent.name
        idol_name_list.append(idol_name)
    return idol_name_list


def start_similarity_images(output_switch, output_mode):
    """
    画像の類似度検索を行い、output_modeによって返却する内容を変更する

    Parameters
    ----------
    output_switch : int
        0:出力しない
        1:検索画像名、各類似度を出力する
        2:TOP10を出力する

    output_mode : int
        0:最適画像パスと類似度を出力する
        1:最適画像のアイドル名を返却する
    """
    t_list = ['r-0.png', 'r-1.png', 'r-2.png', 'r-3.png', 'r-4.png']
    IMG_DIR = image_folder_path.joinpath('gPhoto')
    idol_name_list = []
    for target in t_list:
        akaze_image_path, akaze_min_value = similarity(target, IMG_DIR, output_switch, cal_mode=0)
        # 閾値100を与え、超えた場合はORB方式で再度類似度を求める
        if akaze_min_value >= 100:
            orb_image_path, orb_min_value = similarity(target, IMG_DIR, output_switch, cal_mode=1)
            # 両方式で同一画像が選択され、最小値がともに規定値の1000000でなければ採択する
            if akaze_image_path == orb_image_path and akaze_min_value != 1000000 and orb_min_value != 1000000:
                idol_name_list = __output_mode(akaze_image_path, output_mode, idol_name_list)
            else:
                print("there is no similar image")
                break
        else:
            idol_name_list = __output_mode(akaze_image_path, output_mode, idol_name_list)
    if output_mode == 1:
        return idol_name_list


def __multi_process_similarity(image_path, output_switch, idol_index):
    IMG_DIR = image_folder_path.joinpath('gPhoto')
    akaze_image_path, akaze_min_value = similarity(image_path, IMG_DIR, output_switch, cal_mode=0)
    # 閾値100を与え、超えた場合はORB方式で再度類似度を求める
    if akaze_min_value >= 100:
        orb_image_path, orb_min_value = similarity(image_path, IMG_DIR, output_switch, cal_mode=1)
        # 両方式で同一画像が選択され、最小値がともに規定値の1000000でなければ採択する
        if akaze_image_path == orb_image_path and akaze_min_value != 1000000 and orb_min_value != 1000000:
            idol_name = akaze_image_path.parent.name
        else:
            print(f"there is no similar image index: {image_path}")
            idol_name = ""
    else:
        idol_name = akaze_image_path.parent.name
    return [idol_index, idol_name]


def multi_process_similarity_main(output_switch):
    image_list = ['r-0.png', 'r-1.png', 'r-2.png', 'r-3.png', 'r-4.png']
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=5)
    submit_list = [executor.submit(__multi_process_similarity, image_path, output_switch, index) for index, image_path in enumerate(image_list)]
    result_list = sorted([submit.result() for submit in concurrent.futures.as_completed(submit_list)])
    idol_name_list = [idol_info_list[1] for idol_info_list in result_list if idol_info_list[1] != ""]
    executor.shutdown()
    print(f"Result idol list: {idol_name_list}")
    return idol_name_list


if __name__ == "__main__":
    import time
    start = time.time()
    # start_similarity_images(output_switch=2, output_mode=0)
    multi_process_similarity_main(output_switch=0)
    print(f"実行時間:{time.time()-start:.1f}[s]")
