from bluedot.btcomm import BluetoothServer
from signal import pause

def on_receive(astro_db):
    enginear_db = None
    with open("db.txt") as fp:
        enginear_db = fp.readline()
    if astro_db == "req":
        server.send(enginear_db)
    else:
        with open("db.txt", "w") as fp:
            fp.write(f"{enginear_db}\n{astro_db}")

def req_to_astro():
    client.send("req")

def astro_connected():
    print("Astro connected UwU")
    enginear_db = None
    astro_db = None
    with open("db.txt") as fp:
        enginear_db = fp.readline().replace("\n", "")
    server.send(f"{enginear_db}\tcon")

def astro_disconnected():
    print("Farewell, bro!")
    enginear_db = None
    with open("db.txt") as fp:
        enginear_db = fp.readline().replace("\n", "")
    with open("db.txt", "w") as fp:
        fp.write(f"{enginear_db}\n-1")

def update_to_astro():
    with open("db.txt") as fp:
        enginear_db = fp.readline().replace("\n", "")
        server.send(enginear_db)

server = BluetoothServer(on_receive, when_client_connects=astro_connected, when_client_disconnects=astro_disconnected)

if __name__ == "__main__":
    server.start()
    try:
        pause()
    except:
        server.stop()