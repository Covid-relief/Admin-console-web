#FLASK
from flask import Flask, jsonify, render_template, request
app = Flask(__name__)
import os,optparse

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    debug=False
    app.run(host="0.0.0.0",port=80,debug=debug)