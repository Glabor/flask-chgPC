import requests
import os
from datetime import datetime
import json

def disp(text):
    dispText=f"{datetime.now()} -- {text}"
    print(dispText)
    return(dispText)

def init_file(date, etrNum, type):
    fpath=f"bin/raw/{type}/{etrNum}/{date.strftime('%Y-%m-%d_%H-%M-%S')}.bin"
    fdir="/".join(fpath.split('/')[:-1])

    if not os.path.exists(fdir):
        os.makedirs(fdir)
    return fpath

def dl_file(ip, data):
    disp("dl started")
    with open("file.txt", "w") as file:
        json_object = json.dumps(data, indent=4)
        file.write(json_object)
    
    date=datetime.now()
    etrNum=-1
    type="other"
    if data.get("type") is not None:
        type=data.get("type")
    if data.get("etrNum") is not None:
        etrNum=data.get("etrNum")
    
    fpath=init_file(date, etrNum, type)
    try:
        disp("get file")
        resp=requests.get(f"http://{ip}/new")
        if resp.ok:
            disp("file ok")
            # os.chdir("/home/gle/Desktop/flask-chg")
            with open(f"{fpath}", "wb") as file:
                file.write(resp.content)
            disp("file written")
        else:
            disp("no file")
    except:
        disp("failed dl")
        with open("file.txt", "w") as file:
                file.write("failed dl")
    try:
        disp("stop")
        resp=requests.get(f"http://{ip}/stop")
        if resp.ok:
            disp(resp.content)
    except:
        disp("failed stop")