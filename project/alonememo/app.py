from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient           
client = MongoClient('localhost', 27017)  
db = client.dbsparta                      

## HTML을 주는 부분
@app.route('/')
def home():
   return render_template('index.html')

@app.route('/memo', methods=['POST'])
def saving():
    url_receive = request.form['url_front']  
    comment_receive = request.form['comment_front'] 

    # print(url_receive, comment_receive)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    og_image = soup.select_one('meta[property="og:image"]')

    if soup.select_one('meta[property="og:site_name"]') == None:
        og_title = soup.select_one('meta[property="og:title"]')
    else:
        og_title = soup.select_one('meta[property="og:site_name"]')

    if soup.select_one('meta[name="description"]') == None:
        og_description = soup.select_one('meta[property="og:description"]')
    else:
        og_description = soup.select_one('meta[name="description"]')
    
    # og_description = soup.select_one('meta[name="description"]')
    # og_description = soup.select_one('meta[property="og:description"]')

    url_image = og_image['content']
    url_title = og_title['content']
    url_description = og_description['content']

    article = {'url': url_receive, 'comment': comment_receive, 'image': url_image,
               'title': url_title, 'desc': url_description}

    db.articles.insert_one(article)

    return jsonify({'result': 'success'})

@app.route('/memo', methods=['GET'])
def listing():
    # 모든 document 찾기 & _id 값은 출력에서 제외하기
    result = list(db.articles.find({},{'_id':0}))
    print(result)
    # articles라는 키 값으로 영화정보 내려주기
    return jsonify({'result':'success', 'articles':result})
if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)