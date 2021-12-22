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
 
@flaskApp.route("/getPostList", methods = ["POST"])
def getPostList():
    errCode = 0
    errMessage = "RESULT OK"

    board_ref = db.collection(u'Board')
    posts = board_ref.stream()

    dicPosts = {}

    for post in posts:
        dicPosts[post.id] = post.to_dict()
    
    dicResult = dict([("RESULT", dict([("RESULT_CODE", errCode), ("RESULT_MSG", errMessage)])), ("DATA", dicPosts)])

    return jsonify(dicResult)
 
@flaskApp.route("/getPost", methods = ["POST"])
def getPost():
    errCode = 0
    errMessage = "RESULT OK"
    inputPostID = ""

    try:
        inputData = request.get_json()
        inputPostID = inputData["postID"]
    except Exception as errContent:
        errCode = 200
        errMessage = repr(errContent)

        dicResult = dict([("RESULT", dict([("RESULT_CODE", errCode), ("RESULT_MSG", errMessage)])), ("DATA", dict([("", "")]))])

        return jsonify(dicResult)

    board_ref = db.collection(u'Board')
    posts = board_ref.stream()

    dicPostData = {}

    for post in posts:
        if inputPostID == post.id:
            dicPostData = post.to_dict()
    
    dicResult = dict([("RESULT", dict([("RESULT_CODE", errCode), ("RESULT_MSG", errMessage)])), ("DATA", dicPostData)])

    return jsonify(dicResult)
 
@flaskApp.route("/writePost")
def writePost():
    return "CECOM Web API : Write Post Function"

if __name__ == "__main__":
    flaskApp.run(host="0.0.0.0", port=80)