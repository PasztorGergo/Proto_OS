import time
import requests
import json

if __name__ == "__main__":
    while True:
        time.sleep(0.025)
        data = requests.get("https://proto-web-panel.vercel.app/api/synchronize").json()
        try:
            with open("/db.txt", "w") as fs:
                fs.write(f'{data["id"]}\t{data["mouth"]}\t{data["patriotism"]}\t1')
                fs.close()
        except:
            pass