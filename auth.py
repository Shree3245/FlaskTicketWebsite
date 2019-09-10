import requests
import json
import db

def authenticate(username,password):
    #insert url api for authentication purpose
    url = 'x'
    test = requests.post(url,auth=(username,password))
    json_data = json.loads(test.text)
    output =  json_data['status'].lower()

    global uID
    uID = '0'
    try:
        uID=str(json_data['data']['userId'])
    except KeyError:
        pass
    return output,uID,json_data