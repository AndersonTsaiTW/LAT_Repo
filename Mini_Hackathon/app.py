# test Flask

from flask import Flask
app = Flask(__name__)
@app.route("/")
@app.route("/hello")
def hello():
    return "Hello, World!"