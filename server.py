from flask import Flask, request,render_template
from fan_control import set_fan_speed

app = Flask(__name__)
hs = True
emotion = 0
hu = False
server_state = 1
default_db_values = "0\tTrue\tFalse\t0"

def write_change():
    global emotion
    global hs
    global hu
    global server_state

    fp = open("db.txt","w")
    fp.write(f"{emotion}\t{hs}\t{hu}\t{server_state}")
    fp.close()

@app.route("/")
def index():
    print("Main page opened!")
    with open("db.txt") as fp:
        spltied = fp.readline().split("\t")
        return render_template("index.html", title="controls", hall_effect=eval(spltied[1]), patriotism=eval(spltied[2]))

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
    return ("", 204)

@app.route("/hungary", methods=["POST"])
def setPatroitism():
    global hu
    hu = request.get_json()["state"]
    write_change()
    print("Patroitism toggled")
    return("", 204)


@app.route("/fan", methods=["POST"])
def setFanSpeed():
    speed = int(request.get_json()["speed"])
    set_fan_speed(speed)
    return {"speed": speed}

if __name__ == "__main__":
    write_change()
    try:
        app.run(host="0.0.0.0", port=3000, debug=True)
    except:
        fp = open("db.txt", "w")
        fp.write(default_db_values)
        fp.close()