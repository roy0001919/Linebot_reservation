import requests
import json


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


def unitsQuery(infoStore):
    context = getProtectData("getStoreDict")
    for key, value in context.items():
        try:
            storeName = context[str(key)]['title'][3:6]
            if storeName == infoStore:
                units = (context[str(key)]['units'])
        except:
            continue
    return units


def getStartTimeMatrix(datefrom, dateto, eventid, unitid):
    creds = {
        "dateFrom": datefrom,
        "dateTo": dateto,
        "eventId": eventid,
        "unitId": unitid,
        "count": 1
    }
    result = postProtectData("getStartTimeMatrix", creds)
    return result




