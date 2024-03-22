from flask import Flask, request,render_template
#from face_anim import set_emotion

app = Flask(__name__)
global hs
global emotion
hs = True
emotion = 0

@app.route("/")
def index():
    print("Main page opened!")
    return render_template("index.html")

@app.route("/emotion", methods=["POST"])

def setEmtoion():
    id = int(request.get_json()["id"])
    emotion = id
    fp = open("db.txt", "w")
    fp.write(f"{emotion}\t{hs}")
    fp.close()
    #set_emotion(id)
    return ("", 204)

@app.route("/system", methods=["GET"])
def sendStatus():
    print("Received")
    return {"version":"1.0"}

@app.route("/hall-effect", methods=["POST"])
def setMotuhSync():
    hs = request.get_json()["state"]
    fp = open("db.txt", "w")
    fp.write(f"{emotion}\t{hs}")
    fp.close()
    print("Mouth sync toggled")
    return("", 204)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
    fp = open("db.txt", "w")
    fp.write(f"{0}\t{True}")
    fp.close()