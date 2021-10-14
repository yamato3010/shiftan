import os
import datetime
import jpholiday
import numpy as np
from ortoolpy import addbinvars
import pandas as pd
from flask import Flask, render_template
from flask import request
from flask_httpauth import HTTPBasicAuth
import pulp


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

    try:
        # csvファイルをデータフレームに
        chouseisan_csv = pd.read_csv(f.filename, encoding='cp932' ,header=1)
        chouseisan_csv['日程'].tolist()
        chouseisan_csv = chouseisan_csv.iloc[: , :-1]
        print("headerは１です")
    except:
        chouseisan_csv = pd.read_csv(f.filename, encoding='cp932' ,header=2)
        print("headerは２です")

    # ここから曜日を1 0 であらわす処理 ↓

    # csvファイルの日程の列をリスト化
    day_of_week_list = chouseisan_csv['日程'].tolist()
    
    # 日程のリストを0 1に変換
    for i,str in enumerate(day_of_week_list):
        # 10/1(金) 11:00～17:00という日程の形から日付を摘出
        target = '('
        idx = str.find(target)
        r = str[:idx]

        try:
            # 摘出した文字列(10/1)をdatetime型に変換
            dte = datetime.datetime.strptime(r, '%m/%d')
            today = datetime.date.today()
            # 調整さんには年は記述されていないので現在の年を追加
            dte = dte.replace(year = today.year)
            
            # もし土日、祝日(jpholidayを使用)だったら
            if dte.weekday() >= 5 or jpholiday.is_holiday(dte):
                day_of_week_list[i] = "1"
            else:
                day_of_week_list[i] = "0"

        except:
            """
            日程が
            10/1(金) 11:00～17:00
            17:00～22:00
            このように（2行）なっている場合、二つ目の行にも同じ値を追加
            """
            if day_of_week_list[i - 1] == "1":
                day_of_week_list[i] = "1"
            elif day_of_week_list[i - 1] == "0":
                day_of_week_list[i] = "0"
            else:
                continue

    # 作成したリストをdataflameに追加
    chouseisan_csv.insert(loc = 1, column= '曜日' ,value= day_of_week_list)

    print(chouseisan_csv) #デバッグ用

    # ここまで曜日を1 0 であらわす処理 ↑    

    # ここにシフトを作成する処理を書く？
    
    #daysとmemberの取得
    days = (len(chouseisan_csv.axes[0]) - 1) // 2 # 提出された表から日数を取得、各日2列なので2で割る
    member = len(chouseisan_csv.axes[1]) - 2 # 提出された表から人数取得
    #print(days)
    #print(member)
    #シフト希望の○×を0,1に変換
    shift_converted = np.ones((days * 2, member)) #シフトの0,1を格納する箱を作成、全て1が格納されている
    shift_hope = chouseisan_csv.iloc[0:days * 2, 2:] #調整さんのデータフレームから○×だけを取得
    shift_hope.to_string(header=False, index=False) #ヘッダーとインデックスの削除、○×だけの状態に

    for i in (range(days * 2)): #日程の分ループさせる
        for j in (range(member)): #従業員の分ループさせる
            if shift_hope.iat[i, j] != "○": #もしシフト希望表のあるマスが×ならそのマスに0を格納
                shift_converted[i, j] = 0
    
    print(shift_converted) #○×が1,0に書き換えられたシフト希望表の2次元配列を出力

    needNumberWeekday = [2, 1] # [前半, 後半]
    needNumberHoliday = [3, 3] # [前半, 後半]

    #ペナルティ定数の定義
    C_needNumber = 10

    # 問題の定義
    problem = pulp.LpProblem(name="penalty", sense=pulp.LpMinimize)

    #変数の定義
    V_shift = np.array(addbinvars(days*2, member))
    
    V_needNumber = np.array(addbinvars(days))

    # 必要な条件
    # ・×が提出されている人をアサインしてはいけない
    # ・○のみでシフトを作る
    # ・平日、前半は2人後半は1人
    # 　休日、前半は3人後半3人
    # ・給料の誤差少ないようにする

    # 目的関数
    problem += C_needNumber * pulp.lpSum(V_needNumber)
    #    + C_noAssign * lpSum(V_noAssign)

    weekday = "0"
    holiday = "1"
    
    no_shift_hope = 0.0
    yes_shift_hope = 1.0

    # 制約関数
    # シフト希望が×ならシフトに入れない
    for i in range(days * 2):
        for j in range(member):
            if shift_converted[i][j] == no_shift_hope:
                problem += V_shift[i][j] == 0
            elif shift_converted[i][j] == yes_shift_hope:
                continue
            else:
                print("155行目:×の人にはアサインしないようにするループでエラー発生")
                break

    # 人数が合うようにする制約式
    for i in range(0, days * 2, 2):
        # if chouseisan_csvが×ならそこに0を入れる制約式を作る
        if chouseisan_csv.iloc[i,1] == weekday:
            problem += V_needNumber[i//2] >= (pulp.lpSum(V_shift[i][j] for j in range(member)) - needNumberWeekday[0])
            problem += V_needNumber[i//2] >= -(pulp.lpSum(V_shift[i][j] for j in range(member)) - needNumberWeekday[0])
            problem += V_needNumber[i//2] >= (pulp.lpSum(V_shift[i+1][j] for j in range(member)) - needNumberWeekday[1])
            problem += V_needNumber[i//2] >= -(pulp.lpSum(V_shift[i+1][j] for j in range(member)) - needNumberWeekday[1])
        elif chouseisan_csv.iloc[i,1] == holiday:
            problem += V_needNumber[i//2] >= (pulp.lpSum(V_shift[i][j] for j in range(member)) - needNumberHoliday[0])
            problem += V_needNumber[i//2] >= -(pulp.lpSum(V_shift[i][j] for j in range(member)) - needNumberHoliday[0])
            problem += V_needNumber[i//2] >= (pulp.lpSum(V_shift[i+1][j] for j in range(member)) - needNumberHoliday[1])
            problem += V_needNumber[i//2] >= -(pulp.lpSum(V_shift[i+1][j] for j in range(member)) - needNumberHoliday[1])
        else:
            print("実行不可", chouseisan_csv.iloc[i,1])

    #解く
    status = problem.solve()
    print(pulp.LpStatus[status])


    result = np.vectorize(pulp.value)(V_shift).astype(int)
    print(type(result))
    print("result: ",result) # これが作成されたシフト？

    # 結果表示
    print("制約関数",pulp.value(problem.objective))

    # デバッグ用
    for i in range(days * 2):
        for j in range(member):
            if shift_converted[i][j] == no_shift_hope:
                if result[i][j] != 0:
                    print((i,j) , "シフト希望不可の部分にアサインしてしまっています")
            else:
                continue

    os.remove(f.filename) # 処理が終わった後、ダウンロードしたcsvを消す


    # 結果用のhtml
    return render_template("finished.html")

if __name__ == '__main__':
    app.debug = True
    
    app.run()