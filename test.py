import requests, json
URL = 'https://api.kakaowork.com/v1/users.list' 

headers = {'Content-Type': 'application/json; charset=utf-8','Authorization':'Bearer c856d570.9901b06a691f4c3da28d3ad830a4e658'}
res = requests.get(URL, headers=headers)

users = []
for user in res.json()['users']:
    users.append({"text":user['name'],"value":user['id']})
    

with open('modal.json','r') as f:
    json_data = json.load(f)
    json_data['blocks'][1]['options']=users
    #print(json_data)

def get_userIds():
    URL = 'https://api.kakaowork.com/v1/users.list'
    headers = {'Content-Type': 'application/json; charset=utf-8',
               'Authorization': 'Bearer c856d570.9901b06a691f4c3da28d3ad830a4e658'}
    res = requests.get(URL, headers=headers)

    userids = []
    for i, user in enumerate(res.json()['users']):
        userids.append(int(user['id']))

    return userids


def getConversationId():
    URL = 'https://api.kakaowork.com/v1/messages.send'
    headers = {'Content-Type': 'application/json;',
               'Authorization': 'Bearer c856d570.9901b06a691f4c3da28d3ad830a4e658'}
    data = {'conversation_id':get_userIds()}
    print(data)
    res = requests.post(URL, headers=headers,data=data)

def send_result_message():
    userids = get_userIds()
    URL = 'https://api.kakaowork.com/v1/conversations.open'
    headers = {
               'Authorization': 'Bearer c856d570.9901b06a691f4c3da28d3ad830a4e658','Content-Type': 'application/json;'}
    for userid in userids:
        data = {'user_id':userid}
        res = requests.post(URL, headers=headers,data=json.dumps(data))
        print(res)

def conversation_list():
    URL = 'https://api.kakaowork.com/v1/conversations.list'
    headers = {'Authorization': 'Bearer c856d570.9901b06a691f4c3da28d3ad830a4e658'}
    res = requests.get(URL, headers=headers)
    conversationIds = []
    for conversation in res.json()['conversations']:
        conversationIds.append(conversation['id'])
    print(conversationIds)
print(send_result_message())