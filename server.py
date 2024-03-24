from flask import Flask, request,render_template
from tests import ani

app = Flask(__name__)
global hs
global emotion
global hu
hs = 0
emotion = 0
hu = 0

def write_change():
    fp = open("db.txt")
    fp.write(f"{emotion}\t{hs}\t{hu}")
    fp.close()

@app.route("/")
def index():
    print("Main page opened!")
    return render_template("index.html", title="controls")

@app.route("/scans")
def scan_data():
    return render_template("scans.html", title="scans")

@app.route("/emotion", methods=["POST"])
def setEmtoion():
    id = int(request.get_json()["id"])
    emotion = id
    fp = open("db.txt", "w")
    write_change()
    fp.close()
    return ("", 204)

@app.route("/system", methods=["GET"])
def sendStatus():
    print("Received")
    return {"version":"1.0"}

@app.route("/hall-effect", methods=["POST"])
def setMouthSync():
    hs = request.get_json()["state"]
    fp = open("db.txt", "w")
    write_change()
    fp.close()
    print("Mouth sync toggled")
    return("", 204)

@app.route("/hungary", methods=["POST"])
def setPatroitism():
    hu = request.get_json()["state"]
    fp = open("db.txt", "w")
    write_change()
    fp.close()
    print("Patroitism toggled")
    return("", 204)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
    fp = open("db.txt", "w")
    fp.write("0\t1\t0")
    fp.close()