PDF結合ツール 実行手順
=======================

必要環境
--------
- Windows 10 / 11
- Python 3.10以上（3.11または3.12推奨）
- Pythonインストール時に「Add Python to PATH」を有効化
- tkinterは通常のWindows版Pythonに同梱されています

ファイル構成
------------
merge.py
requirements.txt
setup_and_run.bat
run.bat

初回実行
--------
1. 上記4ファイルを同じフォルダに置きます。
2. setup_and_run.bat をダブルクリックします。
3. .venv仮想環境を作成し、必要ライブラリをインストールした後、アプリが起動します。

2回目以降
----------
run.bat をダブルクリックします。

コマンドプロンプトから手動実行する場合
--------------------------------------
py -3 -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python merge.py

補足
----
- PDFを画面へドラッグ＆ドロップし、順番を調整して結合します。
- 各ページ左上に元PDFのファイル名が追加されます。
- パスワード付きPDFなど、一部のPDFは読み込めない場合があります。
