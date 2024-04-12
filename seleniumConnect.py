import requests
import os

def dl_file(ip):
    with open("file.txt", "a") as file:
        file.write("trying")
    try:
        resp=requests.get(f"http://{ip}")
        if resp.ok:
            os.chdir("/home/gle/Desktop/flask-chg")
            with open("file.txt", "wb") as file:
                file.write(resp.content)
    except:
        with open("file.txt", "w") as file:
                file.write("failed dl")