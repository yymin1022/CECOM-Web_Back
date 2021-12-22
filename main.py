from firebase_admin import credentials
from firebase_admin import firestore
from flask import Flask, jsonify, redirect, request

import firebase_admin

flaskApp = Flask(__name__)

cred = credentials.Certificate("/home/server/CECOM-Web_Front/cecom-web-e268a5fa9a73.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
 
@flaskApp.route("/")
def main():
    return "Hello, CECOM! API Main Function!"
 
@flaskApp.route("/getPostList")
def getPostList():
    return "CECOM Web API : Get Post List Function"
 
@flaskApp.route("/getPost")
def getPost():
    return "CECOM Web API : Get Post Function"
 
@flaskApp.route("/writePost")
def writePost():
    return "CECOM Web API : Write Post Function"

if __name__ == "__main__":
    flaskApp.run(host="0.0.0.0", port=80)