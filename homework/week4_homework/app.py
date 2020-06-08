from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

import requests


from pymongo import MongoClient           
client = MongoClient('localhost', 27017)  
db = client.dbsparta                      

## HTML을 주는 부분
@app.route('/')
def home():
   return render_template('index.html')

@app.route('/orders', methods=['POST'])
def saving():
    name_receive = request.form['name_front']  
    quantity_receive = request.form['quantity_front']  
    address_receive = request.form['address_front']  
    phone_receive = request.form['phone_front'] 

    orders = {'name': name_receive, 'quantity': quantity_receive, 'address': address_receive,
               'phone': phone_receive}

    db.orders.insert_one(orders)

    return jsonify({'result': 'success'})

@app.route('/orders', methods=['GET'])
def listing():
    result = list(db.orders.find({},{'_id':0}))
    print(result)
    return jsonify({'result':'success', 'orders':result})
if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)