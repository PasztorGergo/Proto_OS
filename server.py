from flask import Flask, request,render_template
#from fan_control import set_fan_speed
#from i2c_comm import send_static_emotion, send_dynamic_emotion, send_secondary_feature, send_primary_feature

app = Flask(__name__)
rave = False
emotion = 0
hu = False
dynamic_emotion = False
default_db_values = "0\tFalse\tFalse\False"

def write_change():
    global emotion
    global rave
    global hu
    global dynamic_emotion

    with open("db.txt", "w") as fp:
        fp.write(f"{emotion}\t{rave}\t{hu}\t{dynamic_emotion}")

@app.route("/")
def index():
    with open("db.txt") as fp:
        spltied = fp.readline().split("\t")
        return render_template("index.html", title="controls", rave_mode=eval(spltied[1]), patriotism=eval(spltied[2]))

@app.route("/scans")
def scan_data():
    return render_template("scans.html", title="scans")

@app.route("/dynamic-emotion", methods=["POST"])
def toggleDynamicEmotion():
    global dynamic_emotion
    dynamic_emotion = not dynamic_emotion
    return {"state": dynamic_emotion}


@app.route("/static-emotion", methods=["POST"])
def setEmtoion():
    if not dynamic_emotion:
        id = int(request.get_json()["id"])
        send_static_emotion(id)
        return {"id": id}
    else:
        return ("Dynamic emotions on", 403)

@app.route("/system", methods=["GET"])
def sendStatus():
    print("Received")
    return {"version":"1.1"}

@app.route("/rave-mode", methods=["POST"])
def toggleRaveMode():
    global rave
    rave = request.get_json()["state"]
    write_change()
    send_secondary_feature(eval(rave), 0b0)
    print("Rave mode toggled")
    return {"state": eval(rave)}

@app.route("/hungary", methods=["POST"])
def setPatroitism():
    global hu
    hu = request.get_json()["state"]
    write_change()
    send_secondary_feature(eval(hu), 0b1)
    print("Patroitism toggled")
    return {"state": eval(hu)}


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
        with open("db.txt", "w") as fp:
            fp.write(default_db_values)