from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

from datetime import  datetime
import hashlib
import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbhomework_week1


## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')




@app.route('/main', methods=['GET'])
def listing():
    walkPlace = list(db.walkPlace.find({}, {'_id': False, '_password': False}))

    return jsonify({'all_post': walkPlace})


# @app.route('/main', methods=['GET'])
# def searching():
#
#     walkPlace = list(db.walkPlace.find({}, {'_id': False, '_password': False}))
#
#
#     return jsonify({})


## API 역할을 하는 부분
@app.route('/create')
def create():
    return render_template("create.html")

@app.route('/create', methods=['POST'])
def saving():
    area_receive = request.form['area_give']
    time_receive = request.form['time_give']
    title_receive = request.form['title_give']
    comment_receive = request.form['comment_give']
    map_url_receive = request.form['map_url_give']
    file = request.files["file_give"]

    extension = file.filename.split('.')[-1]

    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
    filename = f'file-{mytime}'

    save_to = f'static/{filename}.{extension}'
    file.save(save_to)

    doc = {
        'area': area_receive,
        'time': time_receive,
        'title': title_receive,
        'comment': comment_receive,
        'map_url': map_url_receive,
        'file': f'{filename}.{extension}'

    }

    db.walkPlace.insert_one(doc)

    return jsonify({'msg': '저장이 완료되었습니다.'})








if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
