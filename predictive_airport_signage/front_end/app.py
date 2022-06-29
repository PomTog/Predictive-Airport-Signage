from flask import Flask, jsonify
from back_end.processor import SignageDatas

app = Flask(__name__)
app.debug=True

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/arrivals")
def arrivals():
    return jsonify(SignageDatas.get("arrivals").dict())

@app.route("/departures")
def departures():
    return jsonify(SignageDatas.get("departures").dict())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port = 5000)