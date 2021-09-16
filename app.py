from flask import Flask, render_template, jsonify, request, redirect, url_for

app = Flask(__name__)

import config
import jwt
import hashlib
import requests
from bs4 import BeautifulSoup
from datetime import  datetime, timedelta


SECRET_KEY = config.SECRET_KEY
client = config.client
db = config.db


## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

## 로그인
@app.route('/sign_in', methods=['POST'])
def sign_in():
    # 로그인
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'username': username_receive, 'password': pw_hash})

    if result is not None:
        payload = {
         'id': username_receive,
         'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')

        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


##로그아웃
@app.route('/sign_out')
def sign_out():
    return jsonify({"result": "success"})


##회원가입
@app.route('/sign_up/save', methods=['POST'])
def sign_up():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    doc = {
        "username": username_receive,                               # 아이디
        "password": password_hash,                                  # 비밀번호
        "profile_name": username_receive,                           # 프로필 이름 기본값은 아이디
        "profile_pic": "",                                          # 프로필 사진 파일 이름
        "profile_pic_real": "profile_pics/profile_placeholder.png", # 프로필 사진 기본 이미지
        "profile_info": ""                                          # 프로필 한 마디
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})

@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    username_receive = request.form['username_give']
    exists = bool(db.users.find_one({"username": username_receive}))
    return jsonify({'result': 'success', 'exists': exists})




# 메인페이지 카드 리스트
@app.route('/matjip', methods=['GET'])
def listing():
    matjip_list = list(db.matjips.find({}, {'_id': False}))

    return jsonify({'result': 'success', 'matjip_list': matjip_list})

@app.route('/detail')
def detail():
    return render_template('detail.html')

@app.route('/detail/list', methods=['GET'])
def comment_listing():
    comments= list(db.comment.find({}, {'_id': False}))

    return jsonify({'result': 'success', 'comment_list': comments})


#코멘트 포스팅
@app.route('/detail/list', methods=['post'])
def save_comment():

    name_receive = request.form["name_give"]
    comment_receive= request.form["comment_give"]

    doc = {
        "name":name_receive,
        "comment":comment_receive

    }

    db.comment.insert_one(doc)

#



























# @app.route('/create', methods=['POST'])
# def saving():
#     area_receive = request.form['area_give']
#     time_receive = request.form['time_give']
#     title_receive = request.form['title_give']
#     comment_receive = request.form['comment_give']
#     map_url_receive = request.form['map_url_give']
#     file = request.files["file_give"]
#
#     extension = file.filename.split('.')[-1]
#
#     today = datetime.now()
#     mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
#     filename = f'file-{mytime}'
#
#     save_to = f'static/{filename}.{extension}'
#     file.save(save_to)
#
#     doc = {
#         'area': area_receive,
#         'time': time_receive,
#         'title': title_receive,
#         'comment': comment_receive,
#         'map_url': map_url_receive,
#         'file': f'{filename}.{extension}'
#
#     }
#
#     db.walkPlace.insert_one(doc)

    # return jsonify({'msg': '저장이 완료되었습니다.'})








if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)