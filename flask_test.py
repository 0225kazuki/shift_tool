# Flask などの必要なライブラリをインポートする
from flask import Flask, render_template, request, redirect, url_for
import numpy as np
import shift_edit2 as st

# 自身の名称を app という名前でインスタンス化する
app = Flask(__name__)


# ここからウェブアプリケーション用のルーティングを記述
# index にアクセスしたときの処理
@app.route('/')
def index():
    title = "shift tool"
    cal_tag = ""
    day_data = st.get_day()
    mem_data = st.get_mem()
    time_data = st.get_time()
    req_data = st.get_req()
    id_data = [x[1] for x in st.get_id()]

    # index.html をレンダリングする
    return render_template('index.html',
                                id_data=id_data, day_data=day_data, mem_data=mem_data, title=title,time_data = time_data,req_data=req_data)

# /post にアクセスしたときの処理
@app.route('/post', methods=['GET', 'POST'])
def post():
    title = "こんにちは"
    if request.method == 'POST':
        day_data = st.get_day()
        mem_data = st.get_mem()
        time_data = st.get_time()
        id_data = [x[1] for x in st.get_id()]
        req_data = st.get_req()
        input_data = []

        for i in range(len(id_data)):
            for j in range(len(day_data)):
                key_str = str(i+1)+'/'+str(j+1)
                input_data.append(request.form[key_str])
        #insert
        for i in input_data:
            if i[0] == 'w':
                who_day = i[1:].split('/')
                print(who_day)
                st.insert(who=who_day[0],day=who_day[1])

        #delete
        for i in input_data:
            if i[0] == 'd':
                who_day = i[1:].split('/')
                print('who day',who_day)
                st.delete(memid=who_day[0],day=who_day[1])

        '''return render_template('index.html',
                               id_data=id_data, day_data=day_data, mem_data=mem_data,title=title,input_data = input_data,time_data = time_data)'''
        # エラーなどでリダイレクトしたい場合はこんな感じで
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.debug = True # デバッグモード有効化
    app.run(host='0.0.0.0') # どこからでもアクセス可能に
