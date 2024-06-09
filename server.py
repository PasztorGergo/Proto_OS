from flask import Flask, request,render_template
#from fan_control import set_fan_speed
#from i2c_comm import send_static_emotion, send_dynamic_emotion, send_secondary_feature, send_primary_feature

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
        return render_template("index.html", title="controls", rave_mode=eval(spltied[1]), patriotism=eval(spltied[2]))

@app.route("/scans")
def scan_data():
    return render_template("scans.html", title="scans")

@app.route("/emotion", methods=["POST"])
def setEmtoion():
    id = int(request.get_json()["id"])
    #send_static_emotion(id)
    return ("", 204)

@app.route("/system", methods=["GET"])
def sendStatus():
    print("Received")
    return {"version":"1.0"}

@app.route("/rave-mode", methods=["POST"])
def setMouthSync():
    global hs
    state = request.get_json()["state"]
    write_change()
    #send_secondary_feature(eval(state), 0b0)
    print("Rave mode toggled")
    return ("", 204)

@app.route("/hungary", methods=["POST"])
def setPatroitism():
    global hu
    hu = request.get_json()["state"]
    write_change()
    #send_secondary_feature(eval(state), 0b1)
    print("Patroitism toggled")
    return("", 204)


"""
@app.route("/fan", methods=["POST"])
def setFanSpeed():
    speed = int(request.get_json()["speed"])
    set_fan_speed(speed)
    return {"speed": speed}
"""

if __name__ == "__main__":
    write_change()
    try:
        app.run(host="0.0.0.0", port=3000, debug=True)
    except:
        fp = open("db.txt", "w")
        fp.write(default_db_values)
        fp.close()