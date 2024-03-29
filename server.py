from flask import Flask, request,render_template
from tests import ani

app = Flask(__name__)
hs = True
emotion = 0
hu = False

def write_change():
    global emotion
    global hs
    global hu

    fp = open("db.txt","w")
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
    global emotion
    id = int(request.get_json()["id"])
    emotion = id
    write_change()
    return ("", 204)

@app.route("/system", methods=["GET"])
def sendStatus():
    print("Received")
    return {"version":"1.0"}

@app.route("/hall-effect", methods=["POST"])
def setMouthSync():
    global hs
    hs = request.get_json()["state"]
    write_change()
    print("Mouth sync toggled")
    return("", 204)

@app.route("/hungary", methods=["POST"])
def setPatroitism():
    global hu
    hu = request.get_json()["state"]
    write_change()
    print("Patroitism toggled")
    return("", 204)


if __name__ == "__main__":
    write_change()
    app.run(host="0.0.0.0", port=3000, debug=True)
    fp = open("db.txt", "w")
    fp.write("0\tTrue\tFalse")
    fp.close()