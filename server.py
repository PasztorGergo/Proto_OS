from flask import Flask, request,render_template
#from face_anim import set_emotion

app = Flask(__name__)

@app.route("/")
def index():
    print("Main page opened!")
    return render_template("index.html")

@app.route("/emotion", methods=["POST"])
def setEmtoion():
    id = int(request.get_json()["id"])
    #set_emotion(id)
    return ("", 204)

@app.route("/system", methods=["GET"])
def sendStatus():
    print("Received")
    return {"version":"1.0"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)