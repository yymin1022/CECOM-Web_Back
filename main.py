from firebase_admin import credentials
from firebase_admin import firestore
from flask import Flask, jsonify, redirect, request

import firebase_admin

flaskApp = Flask(__name__)

cred = credentials.Certificate("/home/server/CECOM-Web_Back/cecom-web-e268a5fa9a73.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
board_ref = db.collection(u'Board')
posts = board_ref.stream()
 
@flaskApp.route("/")
def mainPage():
    return "Hello, CECOM! API Main Function!"
 
@flaskApp.route("/getPostList")
def getPostList():
    dicPosts = {}

    for post in posts:
        dicPosts[post.id] = post.to_dict()
    
    dicResult = {}
    dicResult["Result"] = "OK"
    dicResult["Posts"] = dicPosts

    return jsonify(dicResult)
 
@flaskApp.route("/getPost")
def getPost():
    postID = "211222-193005"

    dicPostData = {}

    for post in posts:
        if postID == post.id:
            dicPostData = post.to_dict()
    
    dicResult = {}
    dicResult["Result"] = "OK"
    dicResult["PostData"] = dicPostData

    return jsonify(dicResult)
 
@flaskApp.route("/writePost")
def writePost():
    return "CECOM Web API : Write Post Function"

if __name__ == "__main__":
    flaskApp.run(host="0.0.0.0", port=80)