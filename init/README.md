# README
- getImageMethodには使用手順があるため、準拠するように
- 以下の機能があり、手順も以下の通り
  - wikiから画像を取得する機能
  - アイドル名から、ある程度のアルファベット名を取得する機能
  - 画像が保存されたフォルダ名をアルファベットに戻す機能

## wikiから画像を取得する機能
- get_idol_image.py
  - get_image.pyがダウンロード機能

## アイドル名から、ある程度のアルファベット名を取得する機能
- kakasi.py
  - idol_name_base.ymlが作成される
  - 修正して、idol_name.ymlとする

## 画像が保存されたフォルダ名をアルファベットに戻す機能
- rename_idol_folder.py
  - idol_name.ymlを参照してフォルダ名を変換する