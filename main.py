from flask import Flask, jsonify, redirect, request

flaskApp = Flask(__name__)
 
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