#FLASK
from flask import Flask, jsonify, render_template, request, redirect, flash, session, abort, url_for
import requests
import json
import pyrebase
app = Flask(__name__)
import os,optparse

config = {
  "apiKey": "AIzaSyAkUg7mNxW-W1Oqe_Mn_F6wogH6wlz3lRc",
  "authDomain": "covid-relief-1d6c0.firebaseapp.com",
  "databaseURL": "https://covid-relief-1d6c0.firebaseio.com",
  "storageBucket": "covid-relief-1d6c0.appspot.com"
}

#initialize firebase
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

#Initialze person as dictionary
person = {"is_logged_in": False, "email": "", "uid": ""}

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/signup')
def signup():
    return render_template("signup.html")

#Welcome page
@app.route("/welcome")
def welcome():
    if person["is_logged_in"] == True:
        return render_template("welcome.html", email = person["email"])
    else:
        return redirect(url_for('login'))

#If someone clicks on login, they are redirected to /result
@app.route("/result", methods = ["POST", "GET"])
def result():
    if request.method == "POST":        #Only if data has been posted
        result = request.form           #Get the data
        email = result["email"]
        password = result["pass"]
        try:
            #Try signing in the user with the given information
            user = auth.sign_in_with_email_and_password(email, password)
            #Insert the user data in the global person
            global person
            person["is_logged_in"] = True
            person["email"] = user["email"]
            person["uid"] = user["localId"]
            #Get the name of the user
            data = db.child("users").get()
            person["email"] = data.val()[person["uid"]]["email"]
            #Redirect to welcome page
            return redirect(url_for('welcome'))
        except:
            #If there is any error, redirect back to login
            return redirect(url_for('login'))
    else:
        if person["is_logged_in"] == True:
            return redirect(url_for('welcome'))
        else:
            return redirect(url_for('login'))

#If someone clicks on register, they are redirected to /register
@app.route("/register", methods = ["POST", "GET"])
def register():
    if request.method == "POST":        #Only listen to POST
        result = request.form           #Get the data submitted
        email = result["email"]
        password = result["pass"]
        #name = result["name"]
        try:
            #Try creating the user account using the provided data
            auth.create_user_with_email_and_password(email, password)
            #Login the user
            user = auth.sign_in_with_email_and_password(email, password)
            #Add data to global person
            global person
            person["is_logged_in"] = True
            person["email"] = user["email"]
            person["uid"] = user["localId"]
            #person["name"] = name
            #Append data to the firebase realtime database
            data = {"email": email}
            db.child("users").child(person["uid"]).set(data)
            #Go to welcome page
            return redirect(url_for('welcome'))
        except:
            #If there is any error, redirect to register
            return redirect(url_for('register'))

    else:
        if person["is_logged_in"] == True:
            return redirect(url_for('welcome'))
        else:
            return redirect(url_for('register'))

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