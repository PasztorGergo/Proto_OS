#sudo rfcomm connect hci0 MAC-ADDR
import serial
import json

astro = serial.Serial("/dev/rfcomm0",115200)

while(True):
    astro_data = serial.readline().decode("ascii")
    enginear_db = None
    astro_db = None
    with open("db.txt") as fp:
        enginear_db = fp.readline().replace("\n", "")
        astro_db = fp.readline().replace("\n", "").split("\t")

        status = json.loads(astro_data)
        astro_db[0] = int(status["id"])
        astro_db[1] = eval(status["eye"])
        astro_db[2] = eval(status["lips"])
        astro_db[3] = eval(status["rave"])
        astro_db[4] = eval(status["patriotism"])
    with open("db.txt", "w") as fp:
        fp.write(f"{enginear_db}\n{"\t".join(astro_db)}")
