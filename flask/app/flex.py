from .httpOpt import getProtectData


def eventInfo(event_dict):
    event_list = event_dict
    context = getProtectData("getEventDict")
    content = {
        "type": "carousel",
        "contents": [

        ]
    }
    for key, value in context.items():
        for event_id in event_list:
            if event_id == key:
                content["contents"].append(event_carousel_column(**value))
    return content


def event_carousel_column(**event_dict):
    content = {
        "type": "bubble",
        "hero": {
            "type": "image",
            "url": "https://simplybook.asia" + event_dict["picture_path"],
            "size": "full",
            "aspectRatio": "20:13",
            "aspectMode": "cover",
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": event_dict["name"],
                    "weight": "bold",
                    "size": "xl"
                },
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
                {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                        "type": "message",
                        "label": event_dict["name"],
                        "text": event_dict["name"]
                    }
                },
                {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                        "type": "message",
                        "label": "回上一頁",
                        "text": "回上一頁"
                    }
                },
                {
                    "type": "spacer",
                    "size": "sm"
                }
            ],
            "flex": 0
        }
    }
    return content


def categoryInfo():
    context = getProtectData("getCategoriesDict")
    content = {
        "type": "carousel",
        "contents": [

        ]
    }
    for key, value in context.items():
        content["contents"].append(category_carousel_column(**value))
    return content


def chg_categoryInfo():
    context = getProtectData("getCategoriesDict")
    content = {
        "type": "carousel",
        "contents": [

        ]
    }
    for key, value in context.items():
        content["contents"].append(chg_category_carousel_column(**value))
    return content


def category_carousel_column(**column_dict):
    content = {
        "type": "bubble",
        "hero": {
            "type": "image",
            "url": "https://simplybook.asia" + column_dict["picture_path"],
            "size": "full",
            "aspectRatio": "20:13",
            "aspectMode": "cover",
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": column_dict["name"],
                    "weight": "bold",
                    "size": "xl"
                }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
                {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                        "type": "message",
                        "label": column_dict["name"],
                        "text": column_dict["name"]
                    }
                },
                {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                        "type": "message",
                        "label": "回上一頁",
                        "text": "回上一頁"
                    }
                },
                {
                    "type": "spacer",
                    "size": "sm"
                }
            ],
            "flex": 0
        }
    }
    return content


def chg_category_carousel_column(**column_dict):
    content = {
        "type": "bubble",
        "hero": {
            "type": "image",
            "url": "https://simplybook.asia" + column_dict["picture_path"],
            "size": "full",
            "aspectRatio": "20:13",
            "aspectMode": "cover",
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": column_dict["name"],
                    "weight": "bold",
                    "size": "xl"
                }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
                {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                        "type": "message",
                        "label": column_dict["name"],
                        "text": column_dict["name"]
                    }
                },
                {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                        "type": "message",
                        "label": "修改店家",
                        "text": "修改店家"
                    }
                },
                {
                    "type": "spacer",
                    "size": "sm"
                }
            ],
            "flex": 0
        }
    }
    return content


def storelocation(store):
    context = getProtectData("getStoreDict")
    content = {
        "type": "carousel",
        "contents": [

        ]
    }
    for key, value in context.items():
        if context[str(key)]['title'] == store:
            content["contents"].append(store_carousel_column(**value))
    return content


def storeInfo(lineText):
    context = getProtectData("getStoreDict")
    content = {
        "type": "carousel",
        "contents": [

        ]
    }
    for key, value in context.items():
        if context[str(key)]['title'][0:2] == lineText:
            content["contents"].append(store_carousel_column(**value))
    return content


def store_carousel_column(**column_dict):
    content = {
        "type": "bubble",
        "hero": {
            "type": "image",
            "url": "https://simplybook.asia" + column_dict["picture_path"],
            "size": "full",
            "aspectRatio": "20:13",
            "aspectMode": "cover",
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": column_dict["title"][3:6],
                    "weight": "bold",
                    "size": "xl"
                }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
                {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                        "type": "message",
                        "label": column_dict["title"][3:6],
                        "text": column_dict["title"][3:6]
                    }
                },
                {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                        "type": "message",
                        "label": "回上一頁",
                        "text": "回上一頁"
                    }
                },
                {
                    "type": "spacer",
                    "size": "sm"
                }
            ],
            "flex": 0
        }
    }
    return content


