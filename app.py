from os import remove
from flask.wrappers import Request
import numpy as np
import ortoolpy
import pandas as pd
from flask import Flask, render_template
from flask import request
from flask_httpauth import HTTPBasicAuth
from pulp import *


app = Flask(__name__)
auth = HTTPBasicAuth()

# ベーシック認証のためのidとパスワード
# {"ユーザー名": "パスワード"}
id_list = {"test": "0000"}

#入力されたidに該当するパスワードを比較
@auth.get_password
def get_pw(id):
    if id in id_list:
        return id_list.get(id)
    return None

@app.route('/', methods=['POST', 'GET'])
@auth.login_required #ここで認証が行われる
def index():
    if request.method == "GET":
        print("GETでした！")# デバッグ用
        return render_template("index.html",note = 0)

    print("POSTでした！")# デバッグ用
    # index.htmlの<input type="file" name="csv" class="form-control" id="customFile" accept=".csv">から取得
    f = request.files['csv']

    # もし、ファイル選択に何も指定されなかったら
    if f.filename == "":
        return render_template("index.html",note = 1)

    f.save(f.filename) # ファイルを保存(ファイルを選択して「シフト作成」ボタンを押すとstudio codeの左のファイルマネージャにcsvファイルが表示されるはず)
    


    # ここにシフトを作成する処理を書く？


    # os.remove(f.filename) # 処理が終わった後、ダウンロードしたcsvを消す

    # 結果用のhtml
    return render_template("finished.html")


    

if __name__ == '__main__':
    app.debug = True
    app.run()
