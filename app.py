import numpy as np
import ortoolpy
import pandas as pd
from flask import Flask, render_template
from flask_httpauth import HTTPBasicAuth
from pulp import *

app = Flask(__name__)
auth = HTTPBasicAuth()

# idとパスワード
id_list = {"test": "0000"}

#入力されたidに該当するパスワードを
#比較のために取得する
@auth.get_password
def get_pw(id):
    if id in id_list:
        return id_list.get(id)
    return None

@app.route('/')
@auth.login_required #ここで認証が行われる
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app.debug = True
    app.run()
