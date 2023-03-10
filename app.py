from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
client = MongoClient('몽고dbURL입력!!!!!!!!!!!!!!!!!!!')
db = client.dbsparta


@app.route('/')
def home():
   return render_template('index.html')

@app.route("/movie", methods=["POST"])
def movie_post():
    url_receive = request.form['url_give']
    star_receive = request.form['star_give']
    comment_receive = request.form['comment_give']

    test1_list = list(db.test1.find({}, {'_id': False}))
    count = len(test1_list) + 1

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    title = soup.select_one('meta[property="og:title"]')['content']
    image = soup.select_one('meta[property="og:image"]')['content']
    desc = soup.select_one('meta[property="og:description"]')['content']

    doc = {
        'num':count,
        'title':title,
        'image':image,
        'desc':desc,
        'star':star_receive,
        'comment':comment_receive
    }
    db.test1.insert_one(doc)


    return jsonify({'msg':'저장 완료!'})

@app.route("/movie", methods=["GET"])
def movie_get():
    movie_list = list(db.test1.find({}, {'_id': False}))
    return jsonify({'movies':movie_list})

@app.route("/movie/delete", methods=["POST"])
def movie_delete():
    num_receive = request.form['num_give']
    db.test1.delete_one({'num': int(num_receive)})
    return jsonify({'msg': '삭제 완료!'})

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)