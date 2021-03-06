from flask import Flask, jsonify, render_template
from back_end.processor import SignageDatas

app = Flask(__name__)

@app.route("/api/arrivals")
def arrivals():
    return jsonify(SignageDatas.get("arrivals").dict())

@app.route("/api/departures")
def departures():
    return jsonify(SignageDatas.get("departures").dict())

@app.route("/")
@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/planes")
def planes():
    return render_template("planes.html")

@app.route("/signage")
def signage():
    return render_template("signage.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port = 5000)
