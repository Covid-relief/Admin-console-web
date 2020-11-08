from functools import wraps
import sys
import os
from flask import Flask, render_template, redirect, request, url_for, session
#coming from pyrebase4
import pyrebase
import requests
import json

#firebase config
config = {
    "apiKey": "AIzaSyAkUg7mNxW-W1Oqe_Mn_F6wogH6wlz3lRc",
    "authDomain": "covid-relief-1d6c0.firebaseapp.com",
    "databaseURL": "https://covid-relief-1d6c0.firebaseio.com",
    "storageBucket": "covid-relief-1d6c0.appspot.com",
    "projectId": "covid-relief-1d6c0",
    "messagingSenderId": "965781285698",
    "appId": "1:965781285698:android:9ce59d336ebb319d3036db"
  
}

#init firebase
firebase = pyrebase.initialize_app(config)
#auth instance
auth = firebase.auth()
#real time database instance
db = firebase.database();


#new instance of Flask
app = Flask(__name__)
#secret key for the session
app.secret_key = os.urandom(24)

#decorator to protect routes
def isAuthenticated(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        #check for the variable that pyrebase creates
        if not auth.current_user != None:
            return redirect(url_for('signup'))
        return f(*args, **kwargs)
    return decorated_function

#index route
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/test")
def test():
    business = db.child("business").get().val().values()
    medicina = db.child("medicina").get().val().values()
    psicologia = db.child("psicología").get().val().values()
    tecnologia = db.child("tecnología").get().val().values()
    approveBusiness = db.child("business").get()
    #print(allposts.val(), file=sys.stderr)
    return render_template("test.html", business = business, medicina = medicina, psicologia = psicologia, tecnologia = tecnologia,
                           approveBusiness = approveBusiness)

@app.route("/aprobar")
def aprobar():
    business = []
    business_keys = []
    business_response = db.child("business").get()
    counter=0
    for keys in business_response.val():
        print(type(keys))
        business_keys.append(keys)
    for dict_business in business_response.val().values():
        dict_business["ID"] = business_keys[counter]
        business.append(dict_business)
        counter+=1

    medicina = db.child("medicina").get().val().values()
    psicologia = db.child("psicología").get().val().values()
    tecnologia = db.child("tecnología").get().val().values()

    # print(allposts.val(), file=sys.stderr)
    return render_template("aprobar.html", business=business, medicina=medicina, psicologia=psicologia,
                           tecnologia=tecnologia)

@app.route("/estadisticas")
def estadisticas():
    return render_template("estadisticas.html")

#signup route
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
      #get the request form data
      email = request.form["email"]
      password = request.form["password"]
      try:
        #create the user
        auth.create_user_with_email_and_password(email, password);
        #login the user right away
        user = auth.sign_in_with_email_and_password(email, password)   
        #session
        user_id = user['idToken']
        user_email = email
        session['usr'] = user_id
        session["email"] = user_email
        return redirect("/")
      except:
        return render_template("login.html", message="The email is already taken, try another one, please" )  

    return render_template("signup.html")


#login route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
      #get the request data
      email = request.form["email"]
      password = request.form["password"]
      try:
        #login the user
        user = auth.sign_in_with_email_and_password(email, password)
        #set the session
        user_id = user['idToken']
        user_email = email
        session['usr'] = user_id
        session["email"] = user_email
        return redirect("/")
      
      except:
        return render_template("login.html", message="Wrong Credentials" )  

     
    return render_template("login.html")

#logout route
@app.route("/logout")
def logout():
    #remove the token setting the user to None
    auth.current_user = None
    #also remove the session
    #session['usr'] = ""
    #session["email"] = ""
    session.clear()
    return redirect("/")

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

@app.route("/deny")
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
        data['Estado'] = "denied"
        resp_put = requests.put(url=url+category+"/"+idPost+".json", data=json.dumps(data))
        return {'response':str(resp_put.status_code), 'data':data, 'type':str(type(data))}
    else:
        print(str(resp.status_code) + " " + str(resp))
        print(result)
    return ""


#run the main script
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
