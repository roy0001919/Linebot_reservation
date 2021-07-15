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



class Config(object):
    JOBS = [
        {
            'id':'job1',
            'func':'app.updateentityauto:updateLocalJson',
            'trigger':'cron',
            'hour':10,
            'minute': 00,
            'second': 0
        },
        {
            'id': 'job2',
            'func': 'app.updateentityauto:updateLocalJson2',
            'trigger':'cron',
            'hour':11,
            'minute': 00,
            'second': 0
        }
    ]

def personalinfo_creat_entity(entity_id, key, value):
    import dialogflow_v2 as dialogflow
    import os
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "app/static/-660c1a8bd25d.json"
    entity_type_UUID = entity_id
    entity_type_client = dialogflow.EntityTypesClient()
    parent = entity_type_client.entity_type_path("", entity_type_UUID)
    entities = [
        {
            "value": key,
            "synonyms": [
                value
            ]
        }
    ]
    response = entity_type_client.batch_create_entities(parent, entities)
    print(response)


def dialogflow_creat_entity(entity_id, key, value):
    import dialogflow_v2 as dialogflow
    import os
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "app/static/-2915db2b9d5e.json"
    entity_type_UUID = entity_id
    entity_type_client = dialogflow.EntityTypesClient()
    parent = entity_type_client.entity_type_path("", entity_type_UUID)
    entities = [
        {
            "value": key,
            "synonyms": [
                value
            ]
        }
    ]
    response = entity_type_client.batch_create_entities(parent, entities)
    print(response)


def category_entity2(category_entity_id):
    context = getProtectData("getCategoriesDict")
    for key, value in context.items():
        categoryName = (context[str(key)]['name'])
        dialogflow_creat_entity(category_entity_id, categoryName, categoryName)


def event_entity2(event_entity_id):
    context = getProtectData("getEventDict")
    for key, value in context.items():
        eventName = (context[str(key)]['name'])
        print(eventName)
        dialogflow_creat_entity(event_entity_id, eventName, eventName)


def store_entity2(event_entity_id):
    context = getProtectData("getStoreDict")
    for key, value in context.items():
        storeName = (context[str(key)]['title'][3:6])
        print(storeName)
        dialogflow_creat_entity(event_entity_id, storeName, storeName)


def location_entity2(event_entity_id):
    context = getProtectData("getStoreDict")
    for key, value in context.items():
        storeName = (context[str(key)]['title'][0:2])
        print(storeName)
        dialogflow_creat_entity(event_entity_id, storeName, storeName)


def category_entity(category_entity_id):
    context = getProtectData("getCategoriesDict")
    for key, value in context.items():
        categoryName = (context[str(key)]['name'])
        personalinfo_creat_entity(category_entity_id, categoryName, categoryName)


def event_entity(event_entity_id):
    context = getProtectData("getEventDict")
    for key, value in context.items():
        eventName = (context[str(key)]['name'])
        print(eventName)
        personalinfo_creat_entity(event_entity_id, eventName, eventName)


def store_entity(event_entity_id):
    context = getProtectData("getStoreDict")
    for key, value in context.items():
        storeName = (context[str(key)]['title'][3:6])
        print(storeName)
        personalinfo_creat_entity(event_entity_id, storeName, storeName)


def location_entity(event_entity_id):
    context = getProtectData("getStoreDict")
    for key, value in context.items():
        storeName = (context[str(key)]['title'][0:2])
        print(storeName)
        personalinfo_creat_entity(event_entity_id, storeName, storeName)


def updateLocalJson():
    category_entity("6c2d786b-9a20-4190-9d2c-8dfd1e6b903a")
    event_entity("48adf339-9b16-48c5-af75-bec4f9ac91e8")
    store_entity("c207e3b7-4a84-442a-8f51-5eb8480d5916")
    category_entity2("33b0dbc3-291e-4123-8b1b-5a5d8ffc6bd6")
    event_entity2("c48e6174-0232-4aa7-86a8-a8bf3a53019a")
    store_entity2("427d7773-7716-451e-964b-0f55ea0397d6")
    print("create finish")


def updateLocalJson2():
    location_entity("1480af02-62c7-4bb7-a497-b9d215bf2e17")
    location_entity2("f63277bd-01d4-44b0-b006-879963a0f0c5")
    print("create finish2")