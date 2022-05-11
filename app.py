
# 참고
# @app.route('/')
# def home():
#     return render_template('index.html')

# package import
from flask import Flask, render_template, request, jsonify, redirect, url_for
import requests

# flask setting
app = Flask(__name__)

# mongodb connect
# client = MongoClient('내AWS아이피', 27017, username="아이디", password="비밀번호")
# db = client.dbsparta_plus_week2

# mongodb connect
from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:test@cluster0.mai7p.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

import certifi

ca = certifi.where()
# 크롤링
import requests
from bs4 import BeautifulSoup

@app.route('/')
def home():
    return render_template('index.html')

url = 'https://www.skyscanner.co.kr/news/inspiration/top10-europe-destinations-where-koreans-love-to-go'

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get(url,headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

card_image = soup.select('#post-321 > div > div > div.entry-content > figure')
card_title = soup.select('#post-321 > div > div > div.entry-content > h2')
count = 0

for image,title in zip(card_image,card_title):
    count = + 1
    image = image.select_one('img')['src']
    title = title.select_one('a').text
    print(image, title)
    doc = {
        'post_num': count,
        'title': title,
        'image_link': image
        }
    db.countrys.insert_one(doc)

@app.route("/countrys", methods=["GET"])
def countrys_get():
    countrys = list(db.countrys.find({}, {'_id': False}))
    return jsonify({'countrys':countrys})

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/detail')
def detail():
    # (to-do) index, id받아서 넣고  return에 넘기기
    # index=1
    # id=1
    comments = list(db.comments.find({},{'_id':False}))
    return render_template("detail.html", comments=comments)


@app.route('/detail/save_comment', methods=['POST'])
def save_comment():
    # (to-do) 인덱스, id 변수로 가져오고 db에 넣어야함

    # index_receive = request.form["index_give"]
    # id_receive = request.form["id_give"]
    comment_receive = request.form["comment_give"]
    print (comment_receive)

    # doc = {"index": index_receive, "id":id_receive, "comment": comment_receive}
    doc = {"comment": comment_receive}
    print(doc)
    db.comments.insert_one(doc)

    return jsonify({'result': 'success', 'msg': '커멘트 저장'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5500, debug=True)