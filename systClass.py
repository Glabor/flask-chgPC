import json
from time import time

def init_syst(id):
    with open("test.txt", 'r') as file:
        file_c=file.read()
    
    try:
        c_json=json.loads(file_c)
    except:
        c_json=json.loads("[{}]")

    s=id
    done=False
    for c in c_json:
        if c.get("id")==s:
            c["ip"]= "" if c.get("ip") == None else c["ip"]
            c["last"]= 0 if c.get("last") == None else c["last"]
            c["wifi"]= False if c.get("wifi") == None else c["wifi"]
            done=True
            break
    if not done:
        d={}
        d["id"]=s
        d["ip"]=""
        d["last"]=0
        d["wifi"]=True
        c_json.append(d)
    dj=json.dumps(c_json, indent=4)
    with open("test.txt","w") as file:
        file.write(dj)
    return ('ok')

def update(id, var, value):
    try:
        id=int(id)
    except:
        return("undefined")
    init_syst(id)
    with open("test.txt", 'r') as file:
        file_c=file.read()
    print("update")
    c_json=json.loads(file_c)
    for c in c_json:
        if c.get("id")==id:
            c[var]=value
    dj=json.dumps(c_json, indent=4)
    with open("test.txt","w") as file:
        file.write(dj)
    return(value)

def get(id, var):
    try:
        id=int(id)
    except:
        return("undefined")
    init_syst(id)       
    value="undefined"
    with open("test.txt", 'r') as file:
        file_c=file.read()
    # print("get")
    c_json=json.loads(file_c)
    for c in c_json:
        if c.get("id")==id:
            value=c[var] if c.get(var)!=None else value
    return(value)
