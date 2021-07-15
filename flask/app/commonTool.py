import io, json, os
from .httpOpt import getProtectData, postProtectData
from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument("headless")


def loadJson(filename):
    path = os.path.join('app/static/', filename)
    with io.open(path, encoding='utf-8') as json_file:
        data = json.load(json_file)
    return data


def categoryQuery(cateName):
    context = getProtectData("getCategoriesDict")
    for key, value in context.items():
        try:
            categoryName = (context[str(key)]['name'])
            if categoryName == cateName:
                categoryID = context[str(key)]['id']
        except:
            continue
    return categoryID


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


def eventQuery(eveName):
    context = getProtectData("getEventDict")
    for key, value in context.items():
        try:
            eventName = (context[str(key)]['name'])
            if eveName == eventName:
                eventID = context[str(key)]['id']
        except:
            continue
    return eventID


def getAvailableUnits(event_id, reservation_time):
    creds = {
        "eventId": event_id,
        "dateTime": reservation_time,
        "count": 1
    }
    result = postProtectData("getAvailableUnits", creds)
    # print(result)
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


def existEvent(categoryID):
    context = getProtectData("getEventDict")
    event_id = []
    for key, value in context.items():
        try:
            if context[str(key)]['categories'][0] == str(categoryID):
                content = (context[str(key)]['id'])
                event_id.append(content)
        except:
            continue
    return event_id


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
    return store_list[0:1]