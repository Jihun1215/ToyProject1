from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
import certifi

ca = certifi.where()

client = MongoClient('mongodb+srv://test:sparta@cluster0.dq4uizr.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/post')
def post():
    return render_template('index2.html')

@app.route('/rank')
def rank():
    return render_template('index3.html')

@app.route("/show", methods=["GET"])
def til_get():
    til_list = list(db.til.find({},{'_id':False}))
    return jsonify({'tils': til_list})

@app.route("/ranking", methods=["GET"])
def rank_get():
    rank_list = list(db.til.find({},{'_id':False}))
    return jsonify({'tils': rank_list})

@app.route("/til", methods=["POST"])
def blog_post():
    name_receive = request.form['name_give']
    vlog_url_receive = request.form['vlog_url_give']
    comment5_receive = request.form['comment5_give']
    count = list(db.til.find({},{'_id':False}))
    num = len(count) + 1
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    

    soup = BeautifulSoup(data.text, 'html.parser')
    
    naver_url = vlog_url_receive

    test = naver_url.split('.')

    if test[1] == "naver":
      naver_url_iframe = soup.select_one('iframe#mainFrame')['src']
      naver_blog_url = "http://blog.naver.com" + naver_url_iframe
      
      data = requests.get(naver_blog_url, headers=headers)

      title_receive = soup.select_one('meta[property="og:title"]')['content']
      img_receive = soup.select_one('meta[property="og:image"]')['content']
      desc_receive = soup.select_one('meta[property="og:description"]')['content']
    else:
      data = requests.get(vlog_url_receive, headers=headers)
      title_receive = soup.select_one('meta[property="og:title"]')['content']
      img_receive = soup.select_one('meta[property="og:image"]')['content']
      desc_receive = soup.select_one('meta[property="og:description"]')['content']

    doc = {
        'name': name_receive,
        'num': num,
        'like': 0,
        'title': title_receive,
        'vlog_url': vlog_url_receive,
        'comment5': comment5_receive,
        'img': img_receive,
        'desc': desc_receive
    }

    db.til.insert_one(doc)

    return jsonify({'msg': '등록 완료!'})

@app.route("/like", methods=["POST"])
def like():
    num_receive = request.form['num_give']

    db.til.update_one({'num': int(num_receive)}, {'$inc': {'like': 1}})
    return jsonify({'msg': '좋아요 완료!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5003, debug=True)