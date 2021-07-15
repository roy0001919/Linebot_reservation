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


def getProtectData(apifunc):
    url = "https://event.smarter.com.tw/api/simplybook/" + apifunc
    token = getToken()
    headers = {'x-access-token': str(token)}
    result = requests.get(url, headers=headers)
    # print(result)
    # print(result.json())
    return result.json()


def postProtectData(apifunc, data):
    url = "https://event.smarter.com.tw/api/simplybook/" + apifunc
    token = getToken()
    headers = {'x-access-token': str(token)}
    result = requests.post(url, json=data, headers=headers)
    # print(result.text)
    return result
# print(getProtectData("getEventDict"))