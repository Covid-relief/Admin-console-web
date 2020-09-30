#FLASK
from flask import Flask, jsonify, render_template, request
import requests
import json
app = Flask(__name__)
import os,optparse

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/data")
def data():
    url = "https://covid-relief-1d6c0.firebaseio.com/.json"
    params = dict(

    )
    #resp = requests.get(url=url, params=params)
    resp = requests.get(url=url)
    if (resp.status_code == 200):
        data = resp.json()
        return data
    else:
        print(str(resp.status_code) + " " + str(resp))
        print(result)
    return ""

@app.route("/approve")
def approve():
    idPost = request.args.get('post')
    category = request.args.get('category')
    url = "https://covid-relief-1d6c0.firebaseio.com/"
    params = dict(

    )
    print(url+category+"/"+idPost+".json")
    #resp = requests.get(url=url, params=params)
    resp = requests.get(url=url+category+"/"+idPost+".json")
    if (resp.status_code == 200):
        data = resp.json()
        data['Estado'] = "approved"
        resp_put = requests.put(url=url+category+"/"+idPost+".json", data=json.dumps(data))
        return {'response':str(resp_put.status_code), 'data':data, 'type':str(type(data))}
    else:
        print(str(resp.status_code) + " " + str(resp))
        print(result)
    return ""

if __name__ == "__main__":
    debug=False
    app.run(host="0.0.0.0",port=80,debug=debug)