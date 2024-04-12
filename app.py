from flask import Flask, request, render_template
import asyncio
from websockets.sync.client import connect
import json
from flask_socketio import SocketIO
from flask_cors import CORS
from time import time
from seleniumConnect import dl_file
from threading import Thread

app=Flask(__name__)
CORS(app)  # Enable CORS for all routes
socketio = SocketIO(app)

#main page
@app.route("/")
def index():
	return render_template('index.html')



# global wifiOn, espIP
wifiOn=False
espIP=""
start=time()
last=start
#manage message from esp
@app.route("/batt", methods=["POST"])
def batt():
    global espIP
    global start, last
    espIP=request.remote_addr
    last=time()
    data=request.get_data()
    mess=data.decode('utf-8').split(',')
    batt=int(mess[0])/100
    bWifi=int(mess[1])
    print(f"{espIP} -- batt : {batt}V, wifi = {bWifi}")
    if wifiOn != bWifi:
        print("sending wifi")
        with connect(f"ws://{espIP}/ws") as websocket:
            websocket.send("wifi")
            print("sent wifi")
            message = websocket.recv()
            print(f"Received: {message}")
    if wifiOn and bWifi:
        print("threading to connect")
        bg=Thread(target=dl_file, args=(espIP,), daemon=True)
        bg.start()


    print(wifiOn, bWifi)
    if wifiOn:
        return ("4")
    else:
         return("0")


@app.route("/flaskJSON", methods=["POST"])
def flaskJSON():
    data=request.get_data().decode('utf-8')
    data_json=json.loads(data)
    print(type(data),data)
    print(type(data_json), data_json)
    return ("3")


@socketio.on("last")
def handle_message(msg):
    global start, last
    print("last",last)
    socketio.emit("last", time()-last)

#manage messages from client
@socketio.on('message')
def handle_message(msg):
    print('Message: ' + msg)
    socketio.emit('response', msg + "response")

#manage messages from client
@socketio.on('wifi')
def handle_message(msg):
    global wifiOn, espIP
    wifiOn = not wifiOn
    print(f"wifi : {wifiOn}")
    socketio.emit('wifi', json.dumps({"wifi":wifiOn, "ip":espIP}))


socketio.run(app, allow_unsafe_werkzeug=True)