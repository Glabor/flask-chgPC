from flask import Flask, request, render_template
import asyncio
from websockets.sync.client import connect
import json
from flask_socketio import SocketIO
from flask_cors import CORS
from time import time
from seleniumConnect import dl_file, disp
from threading import Thread
import systClass 

app=Flask(__name__)
CORS(app)  # Enable CORS for all routes
socketio = SocketIO(app)

#main page
@app.route("/")
def index():
	return render_template('index.html')

# global wifiOn, espIP
wifiOn=True
# espIP=""
# start=time()
# last=start
#manage message from esp
@app.route("/batt", methods=["POST"])
def batt():
    espIP=request.remote_addr
    data=request.get_data().decode('utf-8')
    data_json=json.loads(data)
    disp(data)
    # batt=int(mess[0])/100
    # bWifi=int(mess[1])
    batt=data_json["batt"]
    bWifi=data_json["bWifi"]
    etrNum=data_json["etrNum"]

    systClass.update(etrNum,"last",time())
    systClass.update(etrNum,"ip",espIP)
    wifiOn=systClass.get(etrNum,"wifi")
    info=disp(f"{espIP} -- id : {etrNum}, batt : {batt}V, wifi = {bWifi}")
    with open("batt.txt", "a") as file:
        file.write(f"{info} \n")

    disp(f"{wifiOn}, {bWifi}")
    if wifiOn:
        return ("4")
    else:
         return("0")
    
#manage message from esp
@app.route("/rssi", methods=["POST"])
def rssi():
    espIP=request.remote_addr
    data=request.get_data().decode('utf-8')
    data_json=json.loads(data)
    # disp(data)
    disp(f"{data_json}")
    return("1")
 
@app.route("/sens", methods=["POST"])
def sens():
    # global espIP
    # global start, last
    espIP=request.remote_addr
    # last=time()
    data=request.get_data().decode('utf-8')
    data_json=json.loads(data)
    disp(data)
    # if wifiOn :
    disp("threading to connect")
    bg=Thread(target=dl_file, args=(espIP,data_json,), daemon=True)
    bg.start()

    if wifiOn:
        return ("4")
    else:
         return("0")

@app.route("/flaskJSON", methods=["POST"])
def flaskJSON():
    data=request.get_data().decode('utf-8')
    data_json=json.loads(data)
    disp(f"{type(data)},{data}")
    disp(f"{type(data_json)}, {data_json}")
    return ("3")

@socketio.on("last")
def handle_last(msg):
    t=systClass.get(msg,"last")
    lastTime= t if t!="undefined" else 0
    socketio.emit("last", time()-lastTime)

@socketio.on("list")
def handle_list(msg):
    with open("test.txt", 'r') as file:
        file_c=file.read()
    try:
        c_json=json.loads(file_c)
    except:
        c_json=json.loads("[{}]")
    dj=json.dumps(c_json, indent=4)
    socketio.emit("list", dj)

#manage messages from client
@socketio.on('wifi')
def handle_message(msg):
    ip=systClass.get(msg, "ip")
    w=systClass.get(msg, "wifi")
    systClass.update(msg, "wifi", not w)
    disp(f"wifi : {not w}")
    socketio.emit('wifi', json.dumps({"wifi":not w, "ip":ip}))

socketio.run(app, allow_unsafe_werkzeug=True)