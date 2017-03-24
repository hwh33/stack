#!flask/bin/python
from flask import Flask, request, jsonify

app = Flask(__name__)

# TODO: read from settings file
root_dir = "data"

@app.route("/stacks", methods=["GET", "POST"])
def test_handler():
    if request.method == "GET":
        print("received get request")
    elif request.method == "POST":
        print("received post request")
    else:
        print("received unexpected request")
    return jsonify({"status" : 200})
