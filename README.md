# [しふたん（自動シフト表作成アプリ）](https://ninteen-shiftan.herokuapp.com/ )
![image](https://user-images.githubusercontent.com/84577532/203667854-5165996c-4016-4710-9648-535ccbd2c527.png)
![image](https://user-images.githubusercontent.com/84577532/203667870-a1a2de6a-6f6d-4442-a574-b3dd3f3b303f.png)

紹介動画（2021年10月時点）:https://youtu.be/EfO9MpHo35Q  
アプリURL:https://ninteen-shiftan.herokuapp.com/ 


## 概要
しふたんは飲食店等のシフト表を自動で作成するwebアプリです。  
もともとCODEGYM Academyにおけるチーム開発での制作物として何を開発するか考えていたところ、
知人のアルバイト先の店長がシフトの作成に1週間かかっているという課題があり、それを解決するために開発を行いました。
結果的にシフト表の作成時間が1時間にまで短縮されましたが、他サービスに依存していることなどが原因で店舗に導入できず課題の解決に至らなかったため
もう一度チームで[Shiftan（シフト管理業務補助アプリ）](https://github.com/nineteen2021/shiftan-v2)の開発を始めました。

## こだわり・特徴
- 数理最適化の使用  
→Numpy,Pandasによる数理最適化を使用し、自動で効率的なシフト表の作成を実現しています。  
- シンプルなUI・UXの構築  
→パソコンが苦手な人でも使いやすいように、ボタンの数を減らしそれそれを大きく表示することや、短い手順でシフト表が作成できることに注力しました。  

## 開発期間・人数
開発期間:1か月半（2021/9-2021/10)  
開発人数:3人  
- [＠JinA293](https://github.com/JinA293) 
- [＠koki-fore](https://github.com/koki-fore)
- [＠yamato3010](https://github.com/yamato3010)  
（アルファベット順）

## 使用技術
#### Front : HTML/CSS, BootStarap 
#### Back : Python(Flask), Numpy, Pandas  
#### DB : MySQL  
#### Infrastructure : Heroku
#### Task Management : Trello

## どのように動くか
### シフト自動作成機能
- 数理最適化を用いて事前に調整さんで要していたcsvを自動でシフト表に変換
- 人数が少ない場合はセルに色付け
- 希望を提出する側に配慮し、○ or × or △で勤務希望度もつけることが可能
- 出勤する回数から想定される給与を計算し表示

## 困難だった点とどう乗り越えたか
- PandasやNumpyを用いた数理最適化の実現 
→ ネット上のドキュメントを読み漁り、3人で考えながら実現。

## 改善点
- 他サービス（[調整さん](https://chouseisan.com/)）に依存している問題  
→導入できない理由の主なもの。具体的になにが問題かというと、シフト収集の際に締切日をつけられないことや、他人のシフト希望を見ながら自分のシフト希望を提出できてしまうことがある。
- 数理最適化によるシフト作成の不具合  
→ 全員が均等な出勤回数になるように処理を組んでいるが、その中で正しくシフトが組まれていない場合がある。
