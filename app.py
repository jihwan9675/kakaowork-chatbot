import os, json
from flask import render_template
from flask import Flask, Blueprint, request, render_template, flash, redirect, url_for
from flask import current_app as app


app = Flask(__name__)

with open('modal.json','r') as f:
    json_data = json.load(f)

@app.route('/', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        print("hi")
        print(request.data.decode('utf-8'))
        ss = json.loads(request.data.decode('utf-8'))
        print(ss['action_time'], type(ss))
    else:
        print("no hi")
    return json_data

@app.route('/modal', methods=['GET', 'POST'])
def test():
    if request.method == "POST":
        print("hi")
        print(request.data['type'])
    else:
        print("no hi")
    return json_data


if __name__ == '__main__':
    app.run(host='127.0.0.1',port=5000,debug=True)