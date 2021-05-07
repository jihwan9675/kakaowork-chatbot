import os
import json
from flask import render_template
from flask import Flask, Blueprint, request, render_template, flash, redirect, url_for
from flask import current_app as app
import requests
from models import db, Complement


app = Flask(__name__)
conversation_id_unique = ''  # 단톡 ID

# Modal Json 파일 읽어오기
with open('modal.json', 'r') as f:
    json_data = json.load(f)


# 칭찬 내역 DB에 Insert
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        res = json.loads(request.data.decode('utf-8'))
        #print(res['actions'])

        # 원래면 여기에 예외처리 조건문
        complement = Complement()
        complement.id = 3
        complement.senderid = 1
        complement.complement_value = '칭찬'
        complement.complement_content = '얘는 착하다.'
        #complement.id = res['actions']['userName']
        #complement.senderid = res['message']['user']['user_id']
        ##complement.complement_value = res['message']['complement_value']
        ##complement.complement_content = res['message']['complement_content']

        db.session.add(complement)
        db.session.commit()

        # sendMessage(complement.message_notify())
    return "s"


# modal 요청이 오면 json 파일 리턴
@app.route('/modal', methods=['GET', 'POST'])
def modal():
    if request.method == 'POST':
        print(request.data['type'])
        # 첫번째 옵션에 워크스페이스 인원들을 추가
        json_data['blocks'][1]['options'] = get_userNames()
        ass = {'body': json_data}
    return {'view': json_data}


# 칭찬 횟수 조회
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        my_complement_count = Complement.query.filter_by(
            id=1).count()  # 칭찬받은 횟수
        complemented = Complement.query.filter_by(senderid=1)  # 칭찬한 횟수
        complemented_array = []
        for p in complemented:
            complemented_array.append(p.complement_value)
        print('칭찬받은 횟수 : %s 칭찬한 횟수 : %s 내용 : %s' %
              (my_complement_count, complemented.count(), complemented_array))

    return json_data

# 유저 중 한명이 칭찬을 했을 경우 단톡에 결과 메시지를 보냄


# 단톡 생성
def makeConversations():
    userids = get_userIds()
    URL = 'https://api.kakaowork.com/v1/conversations.open'
    headers = {
        'Authorization': 'Bearer c856d570.9901b06a691f4c3da28d3ad830a4e658', 'Content-Type': 'application/json;'}
    data = {'user_ids': userids}
    res = requests.post(URL, headers=headers, data=json.dumps(data))
    res = res.json()
    global conversation_id_unique
    conversation_id_unique = res['conversation']['id']
    inviteUsers()


# 생성된 단톡에 유저들 초대 (Update)
def inviteUsers():
    URL = 'https://api.kakaowork.com/v1/conversations/{conversation_id}/invite'.format(
        conversation_id=conversation_id_unique)
    headers = {
        'Authorization': 'Bearer c856d570.9901b06a691f4c3da28d3ad830a4e658', 'Content-Type': 'application/json;'}
    data = {'user_ids': get_userIds()}
    res = requests.post(URL, headers=headers, data=json.dumps(data))


# 단톡에 메시지 보내기
def sendMessage(message):
    URL = 'https://api.kakaowork.com/v1/messages.send'
    headers = {
        'Authorization': 'Bearer c856d570.9901b06a691f4c3da28d3ad830a4e658', 'Content-Type': 'application/json;'}
    data = {'conversation_id': conversation_id_unique, 'text': message}
    res = requests.post(URL, headers=headers, data=json.dumps(data))


# 유저 이름과 인덱스를 매칭한 딕셔너리를 담는 배열 생성
def get_userNames():
    URL = 'https://api.kakaowork.com/v1/users.list'
    headers = {'Content-Type': 'application/json; charset=utf-8',
               'Authorization': 'Bearer c856d570.9901b06a691f4c3da28d3ad830a4e658'}
    res = requests.get(URL, headers=headers)

    users = []
    for i, user in enumerate(res.json()['users']):
        users.append({"text": user['name'], "value": i})

    return users


# 유저 id 배열 생성
def get_userIds():
    URL = 'https://api.kakaowork.com/v1/users.list'
    headers = {'Content-Type': 'application/json; charset=utf-8',
               'Authorization': 'Bearer c856d570.9901b06a691f4c3da28d3ad830a4e658'}
    res = requests.get(URL, headers=headers)

    userids = []
    for user in res.json()['users']:
        userids.append(user['id'])
    return userids


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

if __name__ == '__main__':
    makeConversations()
    app.run(host='127.0.0.1', port=5000, debug=True)
