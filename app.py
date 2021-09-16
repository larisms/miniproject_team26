from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

from datetime import  datetime
import hashlib
import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient

client = MongoClient('15.164.170.238', 27017, username="test", password="test")
db = client.dbhomework_week1


## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')


# 메인페이지 카드 리스트
@app.route('/matjip', methods=['GET'])
def listing():
    matjip_list = list(db.matjips.find({}, {'_id': False}))

    return jsonify({'result': 'success', 'matjip_list': matjip_list})



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
@app.route('/detail/save_commnet', methods=['post'])
def save_comment():

    name_receive = request.form["name_give"]
    comment_receive= request.form["comment_give"]

    doc = {
        "name":name_receive,
        "comment":comment_receive

    }

    db.comment.insert_one(doc)
#
# @app.route('/detalil/delete_comment')
# def delete_comment():
#
#     name_recieve = request.form["name_give"]
#     db.comment.delete_one({"name":name_recieve})
#     return jsonify({'result': 'success', 'msg': f'댓글삭제'})



























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
