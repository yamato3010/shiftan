from os import remove
from flask.wrappers import Request
import numpy as np
from ortoolpy import addbinvars
import pandas as pd
from flask import Flask, render_template
from flask import request
from flask_httpauth import HTTPBasicAuth
import pulp


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
V_needNumber = np.array(addbinvars(days)) # 0,1を入れれる日数分のリストを作成、後でこのリストに0，1を記入するコードが必要、その日条件を満たすかどうかが入る
# V_noAssign = 

# 問題の定義
problem = pulp.LpProblem(name="penalty", sense=pulp.LpMinimize)

# 必要な条件
# ・×が提出されている人をアサインしてはいけない
# ・○のみでシフトを作る
# ・平日、前半は2人後半は1人
# 　休日、前半は3人後半3人
# ・給料の誤差少ないようにする

# 目的関数
problem += C_needNumber * pulp.lpSum(V_needNumber)
#    + C_noAssign * lpSum(V_noAssign)

# # 制約関数
# for i in range(0, days*2, 2):
#     if pd.read_csv('', usecols=['B']) == "平日":  # csvファイルの名前がどうなるかわからないから仮置き
#         problem += V_needNumber >= (pulp.lpSum(V_shift[i]) - needNumberWeekday[0])
#         problem += V_needNumber >= -(pulp.lpSum(V_shift[i]) - needNumberWeekday[0])
#         problem += V_needNumber >= (pulp.lpSum(V_shift[i+1]) - needNumberWeekday[1])
#         problem += V_needNumber >= -(pulp.lpSum(V_shift[i+1]) - needNumberWeekday[1])
#     else:
#         problem += V_needNumber >= (pulp.lpSum(V_shift[i]) - needNumberHoliday[0])
#         problem += V_needNumber >= -(pulp.lpSum(V_shift[i]) - needNumberHoliday[0])
#         problem += V_needNumber >= (pulp.lpSum(V_shift[i+1]) - needNumberHoliday[1])
#         problem += V_needNumber >= -(pulp.lpSum(V_shift[i+1]) - needNumberHoliday[1])

# #解く
# status = problem.solve()
# print(pulp.LpStatus[status])

# #結果表示
# print(V_shift)

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
