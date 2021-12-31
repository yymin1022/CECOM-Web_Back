from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage
from flask import Flask, jsonify, redirect, request
from flask_cors import CORS, cross_origin
from uuid import uuid4

import datetime
import firebase_admin

flaskApp = Flask(__name__)
CORS(flaskApp)

cred = credentials.Certificate("/home/server/CECOM-Web_Back/cecom-web-e268a5fa9a73.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': f"cecom-web.appspot.com"
})

db = firestore.client()
bucket = storage.bucket()
 
@flaskApp.route("/")
def mainPage():
    return "Hello, CECOM! API Main Function!"
 
@flaskApp.route("/getPostList", methods = ["POST"])
def getPostList():
    dicPosts = {}
    errCode = 0
    errMessage = "RESULT OK"

    try:
        board_ref = db.collection(u"Board")
        posts = board_ref.stream()

        for post in posts:
            dicPosts[post.id] = post.to_dict()
    except Exception as errContent:
        errCode = 200
        errMessage = repr(errContent)

    dicResult = dict([("RESULT", dict([("RESULT_CODE", errCode), ("RESULT_MSG", errMessage)])), ("DATA", dicPosts)])

    return jsonify(dicResult)
 
@flaskApp.route("/getPost", methods = ["POST"])
def getPost():
    dicPostData = {}
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

    try:
        board_ref = db.collection(u"Board")
        posts = board_ref.stream()

        for post in posts:
            if inputPostID == post.id:
                dicPostData = post.to_dict()
        
        blob = bucket.blob("Posts/%s.md"%(inputPostID))
        new_token = uuid4()
        metadata = {"firebaseStorageDownloadTokens": new_token}
        blob.metadata = metadata

        blob.download_to_filename(filename="/home/server/CECOM-Web_Back/Posts/%s.md"%(inputPostID))

        postContent = ""
        postFile = open("/home/server/CECOM-Web_Back/Posts/%s.md"%(inputPostID), "r")
        for postFileLine in postFile.readlines():
            postContent = "%s\n%s"%(postContent, postFileLine)
            
        dicPostData["content"] = postContent
    except Exception as errContent:
        errCode = 100
        errMessage = repr(errContent)

    dicResult = dict([("RESULT", dict([("RESULT_CODE", errCode), ("RESULT_MSG", errMessage)])), ("DATA", dicPostData)])

    return jsonify(dicResult)
 
@flaskApp.route("/writePost", methods = ["POST"])
def writePost():
    errCode = 0
    errMessage = "RESULT OK"
    inputPostAuthor = ""
    inputPostContent = ""
    inputPostTitle = ""

    try:
        inputData = request.get_json()
        inputPostAuthor = inputData["postAuthor"]
        inputPostContent = inputData["postContent"]
        inputPostTitle = inputData["postTitle"]
    except Exception as errContent:
        errCode = 200
        errMessage = repr(errContent)

        dicResult = dict([("RESULT", dict([("RESULT_CODE", errCode), ("RESULT_MSG", errMessage)]))])

        return jsonify(dicResult)

    postID = datetime.datetime.now().strftime("%y%m%d-%H%M%S")

    try:
        doc_ref = db.collection(u"Board").document(postID)
        doc_ref.set({
            u"author": inputPostAuthor,
            u"content": inputPostContent,
            u"title": inputPostTitle
        })

        postFile = open("/home/server/CECOM-Web_Back/Posts/%s.md"%(postID), "w")
        postFile.write(inputPostContent)
        postFile.close()

        blob = bucket.blob("Posts/%s.md"%(postID))
        new_token = uuid4()
        metadata = {"firebaseStorageDownloadTokens": new_token}
        blob.metadata = metadata

        blob.upload_from_filename(filename="/home/server/CECOM-Web_Back/Posts/%s.md"%(postID))
    except Exception as errContent:
        errCode = 100
        errMessage = repr(errContent)
    
    dicResult = dict([("RESULT", dict([("RESULT_CODE", errCode), ("RESULT_MSG", errMessage)]))])

    return jsonify(dicResult)

@flaskApp.route("/deletePost", methods = ["POST"])
def deletePost():
    errCode = 0
    errMessage = "RESULT OK"
    inputPostID = ""

    try:
        inputData = request.get_json()
        inputPostID = inputData["postID"]
    except Exception as errContent:
        errCode = 200
        errMessage = repr(errContent)

        dicResult = dict([("RESULT", dict([("RESULT_CODE", errCode), ("RESULT_MSG", errMessage)]))])

        return jsonify(dicResult)

    try:
        doc_ref = db.collection(u"Board").document(inputPostID).delete()
    except Exception as errContent:
        errCode = 100
        errMessage = repr(errContent)

    dicResult = dict([("RESULT", dict([("RESULT_CODE", errCode), ("RESULT_MSG", errMessage)]))])

    return jsonify(dicResult)

@flaskApp.route("/updatePost", methods = ["POST"])
def updatePost():
    errCode = 0
    errMessage = "RESULT OK"
    inputPostAuthor = ""
    inputPostContent = ""
    inputPostID = ""
    inputPostTitle = ""

    try:
        inputData = request.get_json()
        inputPostAuthor = inputData["postAuthor"]
        inputPostContent = inputData["postContent"]
        inputPostID = inputData["postID"]
        inputPostTitle = inputData["postTitle"]
    except Exception as errContent:
        errCode = 200
        errMessage = repr(errContent)

        dicResult = dict([("RESULT", dict([("RESULT_CODE", errCode), ("RESULT_MSG", errMessage)]))])

        return jsonify(dicResult)

    try:
        doc_ref = db.collection(u"Board").document(inputPostID)
        doc_ref.update({
            u"author": inputPostAuthor,
            u"content": inputPostContent,
            u"title": inputPostTitle
        })

        postFile = open("/home/server/CECOM-Web_Back/Posts/%s.md"%(inputPostID), "w")
        postFile.write(inputPostContent)
        postFile.close()

        blob = bucket.blob("Posts/%s.md"%(inputPostID))
        new_token = uuid4()
        metadata = {"firebaseStorageDownloadTokens": new_token}
        blob.metadata = metadata

        blob.upload_from_filename(filename="/home/server/CECOM-Web_Back/Posts/%s.md"%(inputPostID))
    except Exception as errContent:
        errCode = 100
        errMessage = repr(errContent)

    dicResult = dict([("RESULT", dict([("RESULT_CODE", errCode), ("RESULT_MSG", errMessage)]))])

    return jsonify(dicResult)

if __name__ == "__main__":
    flaskApp.run(host="0.0.0.0", port=80)