import requests
import json
from random import choice

def getToken():
    url = "https://event.smarter.com.tw/api/simplybook/login"
    creds = {
        "account":"",
        "keygen":""
    }
    token = requests.post(url, json=creds)
    tokenObj = json.loads(token.text)
    # print(tokenObj["token"])
    return tokenObj["token"]


def getProtectData(apifunc):
    url = "https://event.smarter.com.tw/api/simplybook/" + apifunc
    token = getToken()
    headers = {'x-access-token': str(token)}
    result = requests.get(url, headers=headers)
    # print(result.json())
    return result.json()


def postProtectData(apifunc, data):
    url = "https://event.smarter.com.tw/api/simplybook/" + apifunc
    token = getToken()
    headers = {'x-access-token': str(token)}
    result = requests.post(url, json=data, headers=headers)
    # print(result.text)
    return result


def get_location_id(location_name):
    context = getProtectData("getStoreDict")
    for key, value in context.items():
        try:
            storeName = context[str(key)]['title'][3:6]
            if storeName == location_name:
                location_id = (context[str(key)]['id'])
        except:
            continue
    return location_id


def getAvailableUnits(event_id, reservation_time):
    creds = {
        "eventId": event_id,
        "dateTime": reservation_time,
        "count": 1
    }
    result = postProtectData("getAvailableUnits", creds)
    # print(result)
    return result


def random_unit(*unit_id, **AvailableUnits):
    filter_list = []
    for i in AvailableUnits["result"]:
        for j in unit_id:
            if str(i) == str(j):
                filter_list.append(i)
    random_unit = choice(filter_list)
    return random_unit


def book(event_id, unit_id, date, time, location_id, gender, **clientData):
    creds = {
        "eventId": event_id,
        "unitId": unit_id,
        "date": date,
        "time": time,
        "clientData": clientData,
        "additional": {
            "7e104497990f5d83f2132605d04b6014": "0000",
            "Location_id": location_id,
            "ed17391b6e5fdc37884ebc88c36fcd3d": gender
                    },
        "count": 1
    }
    result = postProtectData("book", creds)
    print(result.json())
    return result


