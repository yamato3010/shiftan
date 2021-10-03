import numpy as np
from ortoolpy import addbinvars
import pandas as pd
from flask import Flask, render_template
from flask_httpauth import HTTPBasicAuth
from pulp import *

app = Flask(__name__)
auth = HTTPBasicAuth()

days = 10 # 提出された表から日数を取得(10は仮) /2忘れない
member = 4 # 提出された表から人数取得(4は仮)
needNumberWeekday = [2, 1] # [前半, 後半]
needNumberHoliday = [3, 3] # [前半, 後半]

#ペナルティ定数の定義
C_needNumber = 10
C_noAssign =100

#変数の定義
V_shift = np.array(addbinvars(days * 2, member))
V_needNumber = np.array(addbinvars(days)) # 0,1を入れれる日数分のリストを作成、後でこのリストに0，1を記入するコードが必要
# V_noAssign = 

# 問題の定義
problem = LpProblem(name="penalty", sense=LpMinimize)

# 必要な条件
# ・×が提出されている人をアサインしてはいけない
# ・○のみでシフトを作る
# ・平日、前半は2人後半は1人
# 　休日、前半は3人後半3人
# ・給料の誤差少ないようにする

# 目的関数
problem += C_needNumber * lpSum(V_needNumber)
#    + C_noAssign * lpSum(V_noAssign)

# 制約関数
for i in range(days*2):
    if 平日:
        problem += V_needNumber >= (lpSum(V_shift[iの行]) - needNumberWeekday[0])
        problem += V_needNumber >= -(lpSum(V_shift[iの行]) - needNumberWeekday[0])
        problem += V_needNumber >= (lpSum(V_shift[iの行]) - needNumberWeekday[1])
        problem += V_needNumber >= -(lpSum(V_shift[iの行]) - needNumberWeekday[1])
    else:
        problem += V_needNumber >= (lpSum(V_shift[iの行]) - needNumberHoliday[0])
        problem += V_needNumber >= -(lpSum(V_shift[iの行]) - needNumberHoliday[0])
        problem += V_needNumber >= (lpSum(V_shift[iの行]) - needNumberHoliday[1])
        problem += V_needNumber >= -(lpSum(V_shift[iの行]) - needNumberHoliday[1])

# ベーシック認証のためのidとパスワード
# {"ユーザー名": "パスワード"}
id_list = {"test": "0000"}

#入力されたidに該当するパスワードを比較
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
