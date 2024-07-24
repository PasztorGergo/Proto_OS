from flask import Flask, request,render_template
from fan_control import set_fan_speed
from i2c_comm import send_emotion, send_blink, send_feature
from bluetooth_functions import req_to_astro, update_to_astro

app = Flask(__name__)
emotion = 0
rave = False
hu = False
eye = False
mouth = False
speed = 0
default_db_values = f"{emotion}\t{rave}\t{hu}\t{eye}\t{mouth}\{speed}"

def write_change():
    global emotion
    global rave
    global hu
    global eye
    global mouth

    with open("db.txt", "w") as fp:
        fp.write(f"{emotion}\t{rave}\t{hu}\t{eye}\t{mouth}\t{speed}")

@app.route("/")
def index():
    with open("db.txt") as fp:
        spltied = fp.readline().replace("\n", "").split("\t")
        return render_template("index.html", 
        title="controls", 
        rave_mode=eval(spltied[1]), 
        patriotism=eval(spltied[2]), 
        eye=eval(spltied[3]),
        mouth=eval(spltied[4]),
        speed=int(speed))

@app.route("/scans")
def scan_data():
    return render_template("scans.html", title="scans")

@app.route("/status")
def status_data():
    req_to_astro()
    return render_template("status.html", title="status")

@app.route("/static-emotion", methods=["POST"])
def setEmtoion():
    global id
    if int(request.get_json()["id"]) != 8:
        try:
            id = int(request.get_json()["id"])
            send_emotion(id)
            rave = False
            write_change()
            update_to_astro()
            return {"id": id}
        except:
            return {"id": id}, 500

@app.route("/system", methods=["GET"])
def sendStatus():
    print("Received")
    return {"version":"1.2"}

@app.route("/rave-mode", methods=["POST"])
def toggleRaveMode():
    global rave
    try:
        rave = request.get_json()["state"]
        send_feature(eval(rave), 0b10)
        print("Rave mode toggled")
        write_change()
        update_to_astro()
        return {"state": eval(rave)}
    except:
        return {"state": eval(rave)}, 500

@app.route("/hungary", methods=["POST"])
def setPatroitism():
    global hu
    try:
        hu = request.get_json()["state"]
        send_feature(eval(hu), 0b11)
        write_change()
        update_to_astro()
        print("Patroitism toggled")
        return {"state": eval(hu)}
    except:
        return {"state": eval(hu)}, 500

@app.route("/eye", methods=["POST"])
def toggleEyeTracking():
    global eye
    try:
        eye = request.get_json()["state"]
        send_feature(eval(eye), 0b00)
        write_change()
        update_to_astro()
        return {"state": eval(eye)}
    except:
        return {"state": eval(eye)}, 500

@app.route("/mouth", methods=["POST"])
def toggleMouthSynch():
    global mouth
    try:
        mouth = request.get_json()["state"]
        send_feature(eval(mouth), 0b01)
        write_change()
        update_to_astro()
        return {"state": eval(mouth)}
    except:
        return {"state": eval(mouth)}, 500

@app.route("/fan", methods=["POST"])
def setFanSpeed():
    global speed
    try:
        speed = int(request.get_json()["speed"])
        set_fan_speed(speed)
        update_to_astro()
        return {"speed": speed}
    except:
        return {"speed": speed}, 500

if __name__ == "__main__":
    write_change()
    try:
        app.run(host="0.0.0.0", port=3000, debug=True)
    except:
        with open("db.txt", "w") as fp:
            fp.write(default_db_values)