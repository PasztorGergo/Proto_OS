import time
import requests
import json

"""
    Polling Redis cache will be substituted with creating a websocket.
    Need a host other than Vercel because pure backend is unsupported
"""

if __name__ == "__main__":
    while True:
        time.sleep(0.025)
        data = requests.get("https://proto-web-panel.vercel.app/api/synchronize").json()
        try:
            if data["id"]:
                with open("/db.txt", "w") as fs:
                    fs.write(f'{data["id"]}\t{data["mouth"]}\t{data["patriotism"]}\t1')
                    fs.close()
        except:
            pass