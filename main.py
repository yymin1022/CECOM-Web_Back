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
        postFile = open("/home/server/CECOM-Web_Back/Posts/%s.md"%(inputPostID), "r", encoding="utf-8")
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
    inputPostPassword = ""
    inputPostTitle = ""

    try:
        inputData = request.get_json()
        inputPostAuthor = inputData["postAuthor"]
        inputPostContent = inputData["postContent"]
        inputPostPassword = inputData["postPassword"]
        inputPostTitle = inputData["postTitle"]
    except Exception as errContent:
        errCode = 200
        errMessage = repr(errContent)

        dicResult = dict([("RESULT", dict([("RESULT_CODE", errCode), ("RESULT_MSG", errMessage)]))])

        return jsonify(dicResult)

    postID = datetime.datetime.now().strftime("%y%m%d-%H%M%S")

    try:
        uploadPostDB(inputPostAuthor, inputPostContent, postID, inputPostPassword, inputPostTitle)
        uploadPostFile(postID)
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
        deletePost(inputPostID)
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
    inputPostPassword = ""
    inputPostTitle = ""

    try:
        inputData = request.get_json()
        inputPostAuthor = inputData["postAuthor"]
        inputPostContent = inputData["postContent"]
        inputPostID = inputData["postID"]
        inputPostPassword = inputData["postPassword"]
        inputPostTitle = inputData["postTitle"]
    except Exception as errContent:
        errCode = 200
        errMessage = repr(errContent)

        dicResult = dict([("RESULT", dict([("RESULT_CODE", errCode), ("RESULT_MSG", errMessage)]))])

        return jsonify(dicResult)

    try:
        uploadPostDB(inputPostAuthor, inputPostContent, inputPostID, inputPostPassword, inputPostTitle)
        uploadPostFile(inputPostID)
    except Exception as errContent:
        errCode = 100
        errMessage = repr(errContent)

    dicResult = dict([("RESULT", dict([("RESULT_CODE", errCode), ("RESULT_MSG", errMessage)]))])

    return jsonify(dicResult)

def deletePost(postID):
    doc_ref = db.collection(u"Board").document(postID).delete()

    blob = bucket.blob("Posts/%s.md"%(postID))
    blob.delete()

def uploadPostDB(postAuthor, postContent, postID, postPassword, postTitle):
    doc_ref = db.collection(u"Board").document(postID)
    doc_ref.update({
        u"author": postAuthor,
        u"content": postContent,
        u"password": postPassword,
        u"title": postTitle
    })

def uploadPostFile(postID):
    postFile = open("/home/server/CECOM-Web_Back/Posts/%s.md"%(postID), "w", encoding="utf-8")
    postFile.write(inputPostContent)
    postFile.close()

    blob = bucket.blob("Posts/%s.md"%(postID))
    new_token = uuid4()
    metadata = {"firebaseStorageDownloadTokens": new_token}
    blob.metadata = metadata

    blob.upload_from_filename(filename="/home/server/CECOM-Web_Back/Posts/%s.md"%(postID))

if __name__ == "__main__":
    flaskApp.run(host="0.0.0.0", port=8080)