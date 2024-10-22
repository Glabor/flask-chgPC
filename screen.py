from gpiozero import Button
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from luma.core.render import canvas
from datetime import datetime
from time import time, sleep

serial = i2c(port=1, address=0x3C)
device = ssd1306(serial, width=128, height=32)

def display_number(number):
    # Clear the OLED screen
    with canvas(device) as draw:
        draw.rectangle(device.bounding_box, outline="white", fill="black")
        draw.text((50, 10), str(number), fill="white")

# Function to be called when button 1 is pressed
def on_button1_pressed():
    display_number(1)

# Function to be called when button 2 is pressed
def on_button2_pressed():
    display_number(2)

# Function to be called when button 3 is pressed
def on_button3_pressed():
    display_number(3)

def display(mode, dataSet):
    data=dataSet[mode-1] if len(dataSet)>0 else ""
    with canvas(device) as draw:
        draw.rectangle(device.bounding_box, outline="white", fill="black")
        if data!="":
            date=data.get("date")
            # if mode<3:
            draw.text((0, 10), f"syst. {data.get('id')} : {data.get('batt')}", fill="white")
            draw.text((0, 20), f"IP {data.get('ip')}", fill="white")
                # if mode <2:
            draw.text((0, 0), str(date.strftime("%x")), fill="white")
            draw.text((50, 0), str(date.strftime("%X")), fill="white")      
            draw.text((105, 0), f"{mode+1}/{len(dataSet)}", fill="white")      

        else:
            draw.text((40, 10), "no data yet !", fill="white")

def screenThread(q):
    serial = i2c(port=1, address=0x3C)
    device = ssd1306(serial, width=128, height=32)
    button1 = Button(5)
    button2 = Button(6)
    button3 = Button(12)
    global mode
    mode=0   
    data=""
    date=datetime.now()

    def on_button1_pressed():
        global mode
        # mode=1
        if len(dataSet)>0:
            mode=(mode+1)%len(dataSet)
        else:
            mode=0
        print(mode)
        display(mode, dataSet)

    def on_button2_pressed():
        global mode
        # mode=2
        # display(mode, data, date)

    def on_button3_pressed():
        global mode
        # mode=3
        # display(mode, data, date)

    button1.when_pressed = on_button1_pressed
    button2.when_pressed = on_button2_pressed
    button3.when_pressed = on_button3_pressed
    dataSet=[]
    with canvas(device) as draw:
        draw.rectangle(device.bounding_box, outline="white", fill="black") 
        draw.text((40, 10), f"SERVER ON", fill="white")    

    while True:
        sleep(0.1)
        qu=q.get()
        if qu is None:
            break
            
        # data=dataSet[mode]
        if qu.get("id") not in (d.get("id") for d in dataSet) and qu.get("id") is not None:
            qu["date"]=datetime.now()
            dataSet.append(qu)
        else:
            for d in dataSet:
                if d.get("id")==qu.get("id"):
                    d["date"]=datetime.now()
        # date=datetime.now()

        display(mode, dataSet)
        # with canvas(device) as draw:
        #     draw.rectangle(device.bounding_box, outline="white", fill="black")
        #     # if mode<3:
        #     draw.text((0, 10), f"syst. {data.get('id')} : {data.get('batt')}", fill="white")
        #     draw.text((0, 20), f"IP {data.get('ip')}", fill="white")
        #         # if mode <2:
        #     draw.text((0, 0), str(date.strftime("%x")), fill="white")
        #     draw.text((50, 0), str(date.strftime("%X")), fill="white")

if __name__=="__main__":
    # Define the I2C interface and OLED device
    serial = i2c(port=1, address=0x3C)
    device = ssd1306(serial, width=128, height=32)

    # Define the buttons connected to GPIO pins
    button1 = Button(5)
    button2 = Button(6)
    button3 = Button(12)

    # Assign the functions to button events
    button1.when_pressed = on_button1_pressed
    button2.when_pressed = on_button2_pressed
    button3.when_pressed = on_button3_pressed

    # Run the program
    try:
        while True:
            pass
    except KeyboardInterrupt:
        pass
    finally:
        # Clear the OLED screen and cleanup GPIO
        device.clear()
        device.cleanup()

