import json

def init_db():
    c_json=None
    with open("test.txt", 'r') as file:
        file_c=file.read()
    try:
        c_json=json.loads(file_c)
    except:
        print("could not load file json")
    return c_json

def update(id, var, value):
    try:
        id=int(id)
    except:
        return("undefined")
    init_syst(id)
    with open("test.txt", 'r') as file:
        file_c=file.read()
    print("update",file_c)
    c_json=json.loads(file_c)
    for c in c_json:
        if c.get("id")==id:
            c[var]=value
    dj=json.dumps(c_json, indent=4)
    with open("test.txt","w") as file:
        file.write(dj)
    return(value)
