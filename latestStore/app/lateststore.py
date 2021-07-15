import requests
import json


def getToken():
    url = "https://event.smarter.com.tw/api/simplybook/login"
    creds = {
        "account":"",
        "keygen":""
    }
    token = requests.post(url, json = creds)
    tokenObj = json.loads(token.text)
    # print(tokenObj["token"])
    return tokenObj["token"]


def postProtectData(apifunc, data):
    url = "https://event.smarter.com.tw/api/simplybook/" + apifunc
    token = getToken()
    headers = {'x-access-token': str(token)}
    result = requests.post(url, json=data, headers=headers)
    # print(result.text)
    return result


def get_store(lat, lng):
    from collections import OrderedDict
    store_list = []
    creds = {
        "lat": lat,
        "lng": lng
    }
    content = postProtectData("storeLocate", creds)
    content = content.json()
    ordered = OrderedDict(sorted(content.items(), key=lambda i: i[1]['haversine'], reverse=False))
    for key, value in ordered.items():
        store_list.append(value["title"])
    return store_list[0]