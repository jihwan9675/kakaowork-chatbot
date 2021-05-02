import os
import json
from flask import render_template
from flask import Flask, Blueprint, request, render_template, flash, redirect, url_for
from flask import current_app as app
import requests
from models import db, Complement


app = Flask(__name__)

with open('modal.json', 'r') as f:
    json_data = json.load(f)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        #print(request.data.decode('utf-8'))
        res = json.loads(request.data.decode('utf-8'))
        print(res['actions'])

        # 원래면 여기에 예외처리 조건문
        complement = Complement()
        complement.id = 1
        complement.senderid = 1
        complement.complement_value = '칭찬'
        complement.complement_content = '얘는 착하다.'
        #complement.id = res['actions']['userName']
        #complement.senderid = res['message']['userid']
        #complement.complement_value = res['message']['complement_value']
        ##complement.complement_content = res['message']['complement_content']
        db.session.add(complement)
        db.session.commit()

    return "s"


@app.route('/modal', methods=['GET', 'POST'])
def modal():
    if request.method == 'POST':
        print(request.data['type'])
        json_data['blocks'][1]['options'] = make_users_array()
    return json_data


def make_users_array():
    URL = 'https://api.kakaowork.com/v1/users.list'
    headers = {'Content-Type': 'application/json; charset=utf-8',
               'Authorization': 'Bearer c856d570.9901b06a691f4c3da28d3ad830a4e658'}
    res = requests.get(URL, headers=headers)

    users = []
    for i, user in enumerate(res.json()['users']):
        users.append({"text": user['name'], "value": i})

    return users

# DB Setting
basedir = os.path.abspath(os.path.dirname(__file__))
dbfile = os.path.join(basedir, 'db.sqlite')
 
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///"+dbfile
app.config['SQLALCHEMY_COMMIT_ON_TREEDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'sdafoiauyefhioauwefbnh'

db.init_app(app)
db.app = app
db.create_all()
# END DB Setting

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
