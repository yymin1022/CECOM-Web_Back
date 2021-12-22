from firebase_admin import credentials
from firebase_admin import firestore
from flask import Flask, jsonify, redirect, request

import firebase_admin

flaskApp = Flask(__name__)

cred = credentials.Certificate("/home/server/CECOM-Web_Back/cecom-web-e268a5fa9a73.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
 
@flaskApp.route("/")
def mainPage():
    return "Hello, CECOM! API Main Function!"
 
@flaskApp.route("/getPostList")
def getPostList():
    board_ref = db.collection(u'Board')
    posts = board_ref.stream()

    listPosts = []

    for post in posts:
        listPosts.append([post.id, post.to_dict()])

    dictPosts = dict(["Result", listPosts])
    return dictPosts
 
@flaskApp.route("/getPost")
def getPost():
    return "CECOM Web API : Get Post Function"
 
@flaskApp.route("/writePost")
def writePost():
    return "CECOM Web API : Write Post Function"

if __name__ == "__main__":
    flaskApp.run(host="0.0.0.0", port=80)