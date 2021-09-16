from pymongo import MongoClient
import jwt
import datetime
import hashlib
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta


app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"

SECRET_KEY = 'SPARTA'

# client = MongoClient('mongodb://test:test@localhost', 27017)
client = MongoClient('mongodb://54.180.143.1', 27017, username="test", password="test")
db = client.dbsparta_plus_week4


@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        return render_template('index.html')
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))


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





# 메인페이지 카드 리스트
@app.route('/matjip', methods=['GET'])
def listing():
    matjip_list = list(db.matjips.find({}, {'_id': False}))

    return jsonify({'result': 'success', 'matjip_list': matjip_list})



#####여기서부터 디테일페이지

@app.route('/detail', methods=['GET'])
def comment_listing():
    comments= list(db.comment.find({}, {'_id': False}))

    return jsonify({'result': 'success', 'comment_list': comments})

@app.route('/detail/<post_name>')
def post(post_name):
    store_receive = request.args.get("store")
    result = list(db.matjips_post.find({},{'_id':False}))
    print(result)
    return render_template("detail.html", post_name=post_name,result=result, store=store_receive)



#코멘트 추가 제거
@app.route('/detail', methods=['post'])
def save_comment():

    name_receive = request.form["name_give"]
    comment_receive= request.form["comment_give"]

    today = datetime.now()
    mytime = today.strftime('%Y.%m.%d')

    doc = {
        "name":name_receive,
        "comment":comment_receive,
        "time":mytime

    }


    db.comment.insert_one(doc)

    return jsonify({'msg': '저장 완료!'})

@app.route('/detalil/delete_comment')
def delete_comment():

    comment_receive = request.form["comment_give"]
    db.comment.delete_one({"comment":comment_receive})
    return jsonify({'result': 'success', 'msg': f'댓글삭제'})



# @app.route('/detail/<post_name>', methods=['GET'])
# def detail(post_name):
#     store_receive = request.args.get("store")
#     result = request.form[db.comment["name","comment"]]
#     print(result)
#     return render_template("detail.html", post_name=post_name,result=result, store=store_receive)

# @app.route('/main', methods=['GET'])
# def listing():
#     walkPlace = list(db.walkPlace.find({}, {'_id': False, '_password': False}))
#
#     return jsonify({'all_post': walkPlace})


# @app.route('/detail')
# def detail():
#     return render_template("detail.html")


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
#
#     return jsonify({'msg': '저장이 완료되었습니다.'})
#

@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    username_receive = request.form['username_give']
    exists = bool(db.users.find_one({"username": username_receive}))
    return jsonify({'result': 'success', 'exists': exists})


# @app.route('/posting', methods=['POST'])
# def posting():
#     token_receive = request.cookies.get('mytoken')
#     try:
#         payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
#         # 포스팅하기
#         return jsonify({"result": "success", 'msg': '포스팅 성공'})
#     except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
#         return redirect(url_for("home"))
#
#
# @app.route("/get_posts", methods=['GET'])
# def get_posts():
#     token_receive = request.cookies.get('mytoken')
#     try:
#         payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
#         # 포스팅 목록 받아오기
#         return jsonify({"result": "success", "msg": "포스팅을 가져왔습니다."})
#     except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
#         return redirect(url_for("home"))


# @app.route('/update_profile', methods=['POST'])
# def save_img():
#     token_receive = request.cookies.get('mytoken')
#     try:
#         payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
#         # 프로필 업데이트
#         return jsonify({"result": "success", 'msg': '프로필을 업데이트했습니다.'})
#     except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
#         return redirect(url_for("home"))


# @app.route('/update_like', methods=['POST'])
# def update_like():
#     token_receive = request.cookies.get('mytoken')
#     try:
#         payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
#         # 좋아요 수 변경
#         return jsonify({"result": "success", 'msg': 'updated'})
#     except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
#         return redirect(url_for("home"))


# @app.route('/user/<username>')
# def user(username):
#     # 각 사용자의 프로필과 글을 모아볼 수 있는 공간
#     token_receive = request.cookies.get('mytoken')
#     try:
#         payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
#         status = (username == payload["id"])  # 내 프로필이면 True, 다른 사람 프로필 페이지면 False
#
#         user_info = db.users.find_one({"username": username}, {"_id": False})
#         return render_template('user.html', user_info=user_info, status=status)
#     except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
#         return redirect(url_for("home"))



if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)