from functools import wraps
import sys
import os
from flask import Flask, render_template, redirect, request, url_for, session
#coming from pyrebase4
import pyrebase

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
    #print(allposts.val(), file=sys.stderr)
    return render_template("test.html", business = business, medicina = medicina, psicologia = psicologia, tecnologia = tecnologia)

@app.route("/aprobar")
def aprobar():
    business = db.child("business").get().val().values()
    medicina = db.child("medicina").get().val().values()
    psicologia = db.child("psicología").get().val().values()
    tecnologia = db.child("tecnología").get().val().values()
    # print(allposts.val(), file=sys.stderr)
    return render_template("test.html", business=business, medicina=medicina, psicologia=psicologia,
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


#run the main script
if __name__ == "__main__":
    app.run(debug=True)
