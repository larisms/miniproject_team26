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

    today = datetime.now()
    mytime = today.strftime('%Y.%m.%d')

    doc = {
        "name":name_receive,
        "comment":comment_receive,
        "time":mytime

    }


    db.comment.insert_one(doc)

    return jsonify({'msg': '저장 완료!'})



@app.route('/like_matjip', methods=["POST"])
def like_matjip():
    title_receive = request.form["title_give"]
    address_receive = request.form["address_give"]
    action_receive = request.form["action_give"]
    print(title_receive, address_receive, action_receive)

    if action_receive == "like":
        db.matjips.update_one({"title": title_receive, "address": address_receive}, {"$set": {"liked": True}})
    else:
        db.matjips.update_one({"title": title_receive, "address": address_receive}, {"$unset": {"liked": False}})
    return jsonify({'result': 'success'})





























if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
