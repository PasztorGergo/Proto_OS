from bluedot.btcomm import BluetoothServer
from signal import pause

#ENGINEAR_MAC = "2C:CF:67:1B:D9:91" 

def on_receive(astro_db):
    enginear_db = None
    with open("db.txt") as fp:
        enginear_db = fp.readline()
    with open("db.txt", "w") as fp:
        fp.write(f"{enginear_db}\n{astro_db}")

def astro_connected():
    print("Astro connected UwU")
    enginear_db = None
    astro_db = None
    with open("db.txt") as fp:
        enginear_db = fp.readline().replace("\n", "")
    server.send(f"{enginear_db}\tcon")

def astro_disconnected():
    print("Farewell, brother!")
    enginear_db = None
    with open("db.txt") as fp:
        enginear_db = fp.readline().replace("\n", "")
    with open("db.txt", "w") as fp:
        fp.write(f"{enginear_db}\n-1")

server = BluetoothServer(on_receive, when_client_connects=astro_connected, when_client_disconnects=astro_disconnected)

if __name__ == "__main__":
    server.start()
    try:
        pause()
    except:
        server.stop()