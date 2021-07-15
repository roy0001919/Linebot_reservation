from . import app, db, url
from linebot.exceptions import (
    InvalidSignatureError
)
from flask import request, abort, Blueprint, current_app
import time
from . import db, line_bot_api, handler, url
from linebot.models import MessageEvent, TextMessage, TextSendMessage, QuickReply, QuickReplyButton, MessageAction, FlexSendMessage
from .dialogflow import set_context, PersonalInfo, dialogflow, set_context2, old_cust_reset_context, new_cust_reset_context
from firebase import firebase
from .lineApi import back, location, store2, category, event2, date2, success, retry, new_cust_back, new_cust_retry, time, book, chg_category
from .commonTool import categoryQuery, existEvent, unitsQuery, eventQuery, getStartTimeMatrix, getAvailableUnits, get_location_id
import json
import threading

app_chatbot = Blueprint("webhook",__name__)
fb = firebase.FirebaseApplication(url, None)


@app_chatbot.route("/")
def home():
    return 'test'


@app_chatbot.route("/Infofulfillment", methods=['POST'])
def Infofulfillment():
    print("Infofulfillment!")
    result = request.get_json(silent=True, force=True)
    # print(result)
    user_id = result["queryResult"]["parameters"]["user_id"]
    # print("fullfillment: "+user_id)
    report = result["queryResult"]["parameters"]
    result["queryResult"]["parameters"]["date"] = result["queryResult"]["parameters"]["date"][0:10]
    # result["queryResult"]["parameters"]["time"] = result["queryResult"]["parameters"]["time"][11:19]
    # report.update({'user_id': user_id})
    # fb = firebase.FirebaseApplication(url, None)
    # fb.put('/test', 'PersonalInfo', report)
    # db = firestore.client()
    doc_ref = db.collection("PersonalInfo").document(user_id)
    result["queryResult"]["parameters"]["location"] = fb.get(user_id, "location")
    result["queryResult"]["parameters"]["store"] = fb.get(user_id, "store")
    result["queryResult"]["parameters"]["category"] = fb.get(user_id, "category")
    result["queryResult"]["parameters"]["service"] = fb.get(user_id, "event")
    result["queryResult"]["parameters"]["date"] = fb.get(user_id, "date")
    time.sleep(3)
    result["queryResult"]["parameters"]["time"] = fb.get(user_id, "time")
    doc_ref.set(report)
    # doc_ref = db.collection("PersonalInfo").document(user_id)
    doc_ref.set(report)
    doc_ref2 = db.collection("ReservationLog")
    if 'email' and 'phone' in result["queryResult"]["parameters"]:
        del result["queryResult"]["parameters"]['email']
        del result["queryResult"]["parameters"]['phone']
        del result["queryResult"]["parameters"]['gender']
        del result["queryResult"]["parameters"]['location']
    doc_ref2.add(result["queryResult"]["parameters"])
    return "ok3",200


@app_chatbot.route("/fulfillment", methods=['POST'])
def reservation_fulfillment():
    print("fulfillment!")
    # user_id = fb.get('/PersonalInfo', 'user_id')
    result = request.get_json(silent=True, force=True)
    # user_id = "U263e1fd8e813219face2500fb0dc5815"
    user_id = result["queryResult"]["parameters"]["user_id"]
    result["queryResult"]["parameters"]["date"] = result["queryResult"]["parameters"]["date"][0:10]
    # result["queryResult"]["parameters"]["time"] = result["queryResult"]["parameters"]["time"][11:19]
    # fb = firebase.FirebaseApplication(url, None)
    # fb.put('/test', 'PersonalInfo', result["queryResult"]["parameters"])
    # db = firestore.client()
    doc_ref2 = db.collection("PersonalInfo").document(user_id)
    result["queryResult"]["parameters"]["category"] = fb.get(user_id, "category")
    result["queryResult"]["parameters"]["service"] = fb.get(user_id, "event")
    result["queryResult"]["parameters"]["date"] = fb.get(user_id, "date")
    time.sleep(3)
    result["queryResult"]["parameters"]["time"] = fb.get(user_id, "time")
    doc_ref2.update(result["queryResult"]["parameters"])
    doc_ref = db.collection("ReservationLog")
    if 'email' and 'phone' in result["queryResult"]["parameters"]:
        del result["queryResult"]["parameters"]['email']
        del result["queryResult"]["parameters"]['phone']
        # del result["queryResult"]["parameters"]['gender']
        # del result["queryResult"]["parameters"]['location']
    doc_ref.add(result["queryResult"]["parameters"])
    return "ok22",200


@app_chatbot.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK1'


from . import db, line_bot_api, handler, url
from .httpOpt import getProtectData
from linebot.models import MessageEvent, TextMessage, TextSendMessage, QuickReply, QuickReplyButton, MessageAction, FlexSendMessage
from .dialogflow import set_context, PersonalInfo, dialogflow, set_context2, old_cust_reset_context, new_cust_reset_context
from .flex import categoryInfo,  eventInfo,  storeInfo, storelocation
# from .commonTool import globalUid
from datetime import datetime, timedelta
from random import choice
from .commonTool import categoryQuery, existEvent, unitsQuery, eventQuery
from firebase import firebase
import requests
from requests import get


datefrom = str(datetime.now())[0:10]
end_date = datetime.now() + timedelta(days=14)
dateto = str(end_date)[0:10]
fb = firebase.FirebaseApplication(url, None)


def set_value():
    # global _global_dict
    _global_dict = {}
    # _global_dict["user_id"] = user_id
    # return _global_dict["user_id"]


def new_cust_action(content):
    if content == "請問您的姓名是?":
        return 1
    elif content == "請問您的性別是?":
        return 2
    elif content == "請問您的電話是?":
        return 3
    elif content == "請問您的email是?":
        return 4
    elif content == "請問您要預約的地點是?":
        return 5
    elif content == "請問您要預約的店家是?":
        return 6
    elif content == "請問您要預約的課程分類是?":
        return 7
    elif content == "請問您要預約的服務是?":
        return 8
    elif content == "請問您要預約的日期是?":
        return 9
    elif content == "請問您要預約的時間是?":
        return 10
    elif content == "預約成功":
        return 11


def action_number(content):
    if content == "請問您要預約的課程分類是?":
        return 5
    elif content == "請問您要預約的服務是?":
        return 6
    elif content == "請問您要預約的日期是?":
        return 7
    elif content == "請問您要預約的時間是?":
        return 8
    elif content == "預約成功":
        return 9
    else:
        return 4


def random_unit(*unit_id, **AvailableUnits):
    filter_list = []
    for i in AvailableUnits["result"]:
        for j in unit_id:
            if str(i) == str(j):
                filter_list.append(i)
    random_unit = choice(filter_list)
    return random_unit


def gen_quick_btn(content, **available_time):
    context = []
    context.append(
        QuickReplyButton(action=MessageAction(label="回上一頁", text="回上一頁"))
    )
    for key, value in available_time["result"].items():
        if value == []:
            continue
        else:
            context.append(QuickReplyButton(action=MessageAction(label=key, text=key)))
    if int(len(context)) > 13:
        context = context[0:13]
    text_message = TextSendMessage(text=content,
               quick_reply=QuickReply(items=
                                      context
                                      ))
    return text_message


def gen_quick_btn2(content, lineText, user_id):
    context = []
    context.append(
        QuickReplyButton(action=MessageAction(label="回上一頁", text="回上一頁"))
    )
    available_time = fb.get(user_id, 'available_time')
    for key, value in available_time["result"].items():
        if key == lineText:
            for i in value:
                context.append(QuickReplyButton(action=MessageAction(label=i, text=i)))
        else:
            continue
    if int(len(context)) > 13:
        context = context[0:13]
    text_message = TextSendMessage(text=content,
                                   quick_reply=QuickReply(items=
                                                          context
                                                          ))
    return text_message


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    lineText = event.message.text
    set_value()
    # user_id = globalUid(uid)
    doc_ref = db.collection("PersonalInfo").document(event.source.user_id)
    doc = doc_ref.get()
    # reservation_time = []
    stored_id = None if doc.to_dict() is None else doc.to_dict()['user_id']
    # print(event.source.user_id)
    # print(stored_id)
    try:
        if event.source.user_id == stored_id:
            fb.put(event.source.user_id, 'user_id', event.source.user_id)
            if lineText == "預約":
                old_cust_reset_context(event.source.user_id)
                # store = doc.to_dict()['store']
                set_context(event.source.user_id)
                content = PersonalInfo(lineText, event.source.user_id)
                text_message = TextSendMessage(text=content,
                   quick_reply=QuickReply(items=[
                       QuickReplyButton(action=MessageAction(label="名字", text="名字")),
                       QuickReplyButton(action=MessageAction(label="電話", text="電話")),
                       QuickReplyButton(action=MessageAction(label="信箱", text="信箱")),
                       QuickReplyButton(action=MessageAction(label="店家", text="店家")),
                       QuickReplyButton(action=MessageAction(label="不改變", text="不改變")),
                   ]))
                line_bot_api.reply_message(event.reply_token, text_message)
            else:
                try:
                    content = PersonalInfo(lineText, event.source.user_id)
                    if lineText == "回上一頁":
                        back(content, lineText, event, doc, doc_ref)
                    else:
                        if lineText == "是":
                            text_message = TextSendMessage(text=content,
                               quick_reply=QuickReply(items=[
                                   QuickReplyButton(action=MessageAction(label="名字", text="名字")),
                                   QuickReplyButton(action=MessageAction(label="電話", text="電話")),
                                   QuickReplyButton(action=MessageAction(label="信箱", text="信箱")),
                                   QuickReplyButton(action=MessageAction(label="店家", text="店家")),
                                   QuickReplyButton(action=MessageAction(label="不改變", text="不改變")),
                               ]))
                            line_bot_api.reply_message(event.reply_token, text_message)
                        elif content == "請問您要預約的地點是?":
                            location(event)
                        elif content == "請問您要預約的店家是?":
                            print(lineText)
                            content2 = dialogflow(lineText, event.source.user_id)
                            store2(content2, lineText, event)
                            if lineText == "台北" or lineText == "新北" or lineText == "新竹" or lineText == "台中" or lineText == "高雄" or lineText == "最近店家":
                                fb.put(event.source.user_id, 'location', lineText)
                        elif content == "名字已改好囉，請問您還有想改的項目嗎?" or content == "電話已改好囉，請問您還有想改的項目嗎?" or content == "信箱已改好囉，請問您還有想改的項目嗎?" :
                            text_message = TextSendMessage(text=content,
                                                           quick_reply=QuickReply(items=[
                                                               QuickReplyButton(action=MessageAction(label="是", text="是")),
                                                               QuickReplyButton(action=MessageAction(label="不改變", text="不改變")),
                                                           ]))
                            line_bot_api.reply_message(event.reply_token, text_message)
                        elif content =="店家已改好囉，請問您還有想改的項目嗎?":
                            fb.put(event.source.user_id, 'store', lineText)
                            # store = lineText
                            unit_id = unitsQuery(lineText)
                            fb.put(event.source.user_id, 'unit_id', unit_id)
                            text_message = TextSendMessage(text=content,
                                                           quick_reply=QuickReply(items=[
                                                               QuickReplyButton(action=MessageAction(label="是", text="是")),
                                                               QuickReplyButton(action=MessageAction(label="不改變", text="不改變")),
                                                           ]))
                            line_bot_api.reply_message(event.reply_token, text_message)
                        elif content == "請問您要預約的課程分類是?":
                            # category_entity("6c2d786b-9a20-4190-9d2c-8dfd1e6b903a")
                            text_message = FlexSendMessage(
                                alt_text='請問您要預約的課程分類是?',
                                contents=categoryInfo(),
                            )
                            line_bot_api.reply_message(event.reply_token, text_message)
                        elif content == "請問您要預約的服務是?":
                            # event_entity("48adf339-9b16-48c5-af75-bec4f9ac91e8")
                            cate_id = categoryQuery(lineText)
                            event_list = existEvent(cate_id)
                            fb.put(event.source.user_id, 'event_list', event_list)
                            # context = getProtectData("getEventDict")
                            text_message = FlexSendMessage(
                                alt_text='請問您要預約的服務是?',
                                contents=eventInfo(event_list),
                            )
                            line_bot_api.reply_message(event.reply_token, text_message)
                            fb.put(event.source.user_id, 'category', lineText)
                        elif content == "請問您要預約的日期是?":
                            # global event_id
                            event_id = eventQuery(lineText)
                            fb.put(event.source.user_id, 'event_id', event_id)
                            store = fb.get(event.source.user_id, 'store')
                            unit_id = unitsQuery(store)
                            content2 = getStartTimeMatrix(datefrom, dateto, event_id, unit_id)
                            # global available_time
                            available_time = content2.json()
                            fb.put(event.source.user_id, 'available_time', available_time)
                            text_message = gen_quick_btn("請問您要預約的日期是?", **available_time)
                            line_bot_api.reply_message(event.reply_token, text_message)
                            fb.put(event.source.user_id, 'event', lineText)
                        elif content == "請問您要預約的時間是?":
                            text_message = gen_quick_btn2("請問您要預約的時間是?", lineText, event.source.user_id)
                            line_bot_api.reply_message(event.reply_token, text_message)
                            # global select_date
                            select_date = lineText
                            fb.put(event.source.user_id, 'select_date', select_date)
                            fb.put(event.source.user_id, 'date', lineText)
                        elif content == "預約成功":
                            select_date = fb.get(event.source.user_id, 'select_date')
                            reservation_time = str(select_date) + " " + lineText
                            event_id = fb.get(event.source.user_id, 'event_id')
                            Units = getAvailableUnits(event_id, reservation_time)
                            AvailableUnits = Units.json()
                            unit_id = fb.get(event.source.user_id, 'unit_id')
                            random_one = random_unit(*unit_id, **AvailableUnits)
                            clientData = {}
                            clientData.update({"name": doc.to_dict()['name'], "email": doc.to_dict()['email'], "phone": doc.to_dict()['phone']})
                            store = fb.get(event.source.user_id, 'store')
                            location_id = get_location_id(store)
                            gender = doc.to_dict()['gender']
                            success_msg = event_id + location_id + gender
                            # content3 = book(event_id, random_one, select_date, lineText, location_id, gender, **clientData)
                            print(success_msg)
                            line_bot_api.reply_message(
                                event.reply_token,
                                TextSendMessage(text="預約成功"))
                            fb.put(event.source.user_id, 'time', lineText)
                            # doc_ref.update({"time": lineText})
                            select_date = fb.get(event.source.user_id, 'date')
                            # gender = fb.get(event.source.user_id, 'gender')
                            service = fb.get(event.source.user_id, 'event')
                            store = fb.get(event.source.user_id, 'store')
                            if store == "西華店":
                                phone_num = "02-2547-2638"
                            elif store == "仁愛店":
                                phone_num = "02-2755-5233"
                            elif store == "南京店":
                                phone_num = "02-2523-3688"
                            elif store == "南西店":
                                phone_num = "02-2531-0666"
                            elif store == "忠孝店":
                                phone_num = "02-2778-6267"
                            elif store == "頂好店":
                                phone_num = "02-2772-2123"
                            elif store == "站前店":
                                phone_num = "02-2381-0298"
                            elif store == "復北店":
                                phone_num = "02-2718-7123"
                            elif store == "公館店":
                                phone_num = "02-2366-1177"
                            elif store == "永和店":
                                phone_num = "02-8921-2299"
                            elif store == "新莊店":
                                phone_num = "02-2277-0970"
                            elif store == "樹林店":
                                phone_num = "02-8675-1043"
                            elif store == "光復店":
                                phone_num = "03-666-2989"
                            elif store == "忠明店":
                                phone_num = "04-2372-2288"
                            elif store == "文心店":
                                phone_num = "04-2311-6688"
                            elif store == "東寧店":
                                phone_num = "06-276-2595"
                            elif store == "崇學店":
                                phone_num = "06-336-0199"
                            elif store == "永康店":
                                phone_num = "06-312-7728"
                            elif store == "三多店":
                                phone_num = "07-339-3525"
                            else:
                                phone_num = "0800-500080"

                            # reservation_time = str(select_date) + " " + lineText
                            # event_id = fb.get(event.source.user_id, 'event_id')
                            # unit_id = fb.get(event.source.user_id, 'unit_id')
                            c_name = fb.get(event.source.user_id, 'name')
                            line_bot_api.reply_message(
                                event.reply_token,
                                TextSendMessage(
                                    text=c_name + '您好~謝謝您的預約,' + '\n' + '以下是您的預約資訊:' + '\n' + '\n' + '分店:' + store + '\n' + '療程:'
                                         + service + '\n' + '日期:' + select_date + '\n' + '時間:' + lineText + '\n' + '\n'
                                         + '再請您當天依預約時段前來,如有任何問題,請至電' + phone_num + '\n' + '謝謝~'))
                        else:
                            if lineText =="名字" or "電話" or "信箱" or "店家":
                                line_bot_api.reply_message(
                                    event.reply_token,
                                    TextSendMessage(text=content))
                except:
                    retry(content, lineText, event, doc, doc_ref)
        else:
            fb.put(event.source.user_id, 'user_id', event.source.user_id)
            if lineText == "預約":
                new_cust_reset_context(event.source.user_id)
                set_context2(event.source.user_id)
                content = dialogflow(lineText, event.source.user_id)
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=content))
            else:
                try:
                    content = dialogflow(lineText, event.source.user_id)
                    print(content)
                    if lineText == "回上一頁":
                        new_cust_back(content, lineText, event, doc, doc_ref, fb)
                    else:
                        if content == "請問您的電話是?":
                            gender = lineText
                            fb.put(event.source.user_id, 'gender', gender)
                            line_bot_api.reply_message(
                                event.reply_token,
                                TextSendMessage(text=content))
                        elif content == "請問您的性別是?":
                            # global name
                            name = lineText
                            fb.put(event.source.user_id, 'name', name)
                            text_message = TextSendMessage(text=content,
                                                           quick_reply=QuickReply(items=[
                                                               QuickReplyButton(action=MessageAction(label="男", text="男")),
                                                               QuickReplyButton(action=MessageAction(label="女", text="女")),
                                                           ]))
                            line_bot_api.reply_message(event.reply_token, text_message)
                        elif content == "請問您要預約的地點是?":
                            location(event.source.user_id, event.reply_token)
                            if "@" in lineText and ".com" in lineText:
                                fb.put(event.source.user_id, 'email', lineText)
                        elif content == "請問您要預約的店家是?":
                            content2 = PersonalInfo(lineText, event.source.user_id)
                            store2(content2, lineText, event.source.user_id, event.reply_token)
                            if lineText == "台北" or lineText == "新北" or lineText == "新竹" or lineText == "台中" or lineText == "高雄" or lineText == "最近店家":
                                fb.put(event.source.user_id, 'location', lineText)
                        elif content == "請問您的email是?":
                            # global phone
                            phone = lineText
                            fb.put(event.source.user_id, 'phone', phone)
                            line_bot_api.reply_message(
                                event.reply_token,
                                TextSendMessage(text=content))
                        elif content == "請問您要預約的課程分類是?":
                            # category_entity2("33b0dbc3-291e-4123-8b1b-5a5d8ffc6bd6")
                            store = lineText
                            unit_id = unitsQuery(lineText)
                            fb.put(event.source.user_id, 'unit_id', unit_id)
                            fb.put(event.source.user_id, 'store', store)
                            text_message = FlexSendMessage(
                                alt_text='請問您要預約的課程分類是?',
                                contents=categoryInfo(),
                            )
                            line_bot_api.reply_message(event.reply_token, text_message)
                        elif content == "請問您要預約的服務是?":
                            # event_entity2("c48e6174-0232-4aa7-86a8-a8bf3a53019a")
                            cate_id = categoryQuery(lineText)
                            event_list = existEvent(cate_id)
                            fb.put(event.source.user_id, 'event_list', event_list)
                            # context = getProtectData("getEventDict")
                            text_message = FlexSendMessage(
                                alt_text='請問您要預約的服務是?',
                                contents=eventInfo(event_list),
                            )
                            line_bot_api.reply_message(event.reply_token, text_message)
                            fb.put(event.source.user_id, 'category', lineText)
                        elif content == "請問您要預約的日期是?":
                            # global event_id
                            event_id = eventQuery(lineText)
                            fb.put(event.source.user_id, 'event_id', event_id)
                            unit_id = fb.get(event.source.user_id, 'unit_id')
                            # unit_id = []
                            # for i in range(0, 4):
                            #     unit_id.append(get(url).json()['dialogflow']['unit_id'][str(i)])
                            # print(unit_id)
                            content2 = getStartTimeMatrix(datefrom, dateto, event_id, unit_id)
                            available_time = content2.json()
                            fb.put(event.source.user_id, 'available_time', available_time)
                            text_message = gen_quick_btn(content, **available_time)
                            line_bot_api.reply_message(event.reply_token, text_message)
                            fb.put(event.source.user_id, 'event', lineText)
                        elif content == "請問您要預約的時間是?":
                            text_message = gen_quick_btn2(content, lineText, event.source.user_id)
                            # print(text_message)
                            line_bot_api.reply_message(event.reply_token, text_message)
                            # print(text_message)
                            # global select_date
                            select_date = lineText
                            fb.put(event.source.user_id, 'select_date', select_date)
                            fb.put(event.source.user_id, 'date', lineText)
                        elif content == "預約成功":
                            select_date = fb.get(event.source.user_id, 'select_date')
                            reservation_time = str(select_date) + " " + lineText
                            event_id = fb.get(event.source.user_id, 'event_id')
                            Units = getAvailableUnits(event_id, reservation_time)
                            AvailableUnits = Units.json()
                            unit_id = fb.get(event.source.user_id, 'unit_id')
                            random_one = random_unit(*unit_id, **AvailableUnits)
                            clientData = {}
                            name = fb.get(event.source.user_id, 'name')
                            email = fb.get(event.source.user_id, 'email')
                            phone = fb.get(event.source.user_id, 'phone')
                            clientData.update({"name": name, "email": email, "phone": phone})
                            store = fb.get(event.source.user_id, 'store')
                            location_id = get_location_id(store)
                            gender = fb.get(event.source.user_id, 'gender')
                            # content3 = event_id + location_id + gender
                            success_msg = book(event_id, random_one, select_date, lineText, location_id, gender, **clientData)
                            print(success_msg)
                            line_bot_api.reply_message(
                                event.reply_token,
                                TextSendMessage(text="預約成功"))
                            fb.put(event.source.user_id, 'time', lineText)
                            doc_ref.update({"time": lineText})

                            select_date = fb.get(event.source.user_id, 'date')
                            # gender = fb.get(event.source.user_id, 'gender')
                            service = fb.get(event.source.user_id, 'event')
                            store = fb.get(event.source.user_id, 'store')
                            if store == "西華店":
                                phone_num = "02-2547-2638"
                            elif store == "仁愛店":
                                phone_num = "02-2755-5233"
                            elif store == "南京店":
                                phone_num = "02-2523-3688"
                            elif store == "南西店":
                                phone_num = "02-2531-0666"
                            elif store == "忠孝店":
                                phone_num = "02-2778-6267"
                            elif store == "頂好店":
                                phone_num = "02-2772-2123"
                            elif store == "站前店":
                                phone_num = "02-2381-0298"
                            elif store == "復北店":
                                phone_num = "02-2718-7123"
                            elif store == "公館店":
                                phone_num = "02-2366-1177"
                            elif store == "永和店":
                                phone_num = "02-8921-2299"
                            elif store == "新莊店":
                                phone_num = "02-2277-0970"
                            elif store == "樹林店":
                                phone_num = "02-8675-1043"
                            elif store == "光復店":
                                phone_num = "03-666-2989"
                            elif store == "忠明店":
                                phone_num = "04-2372-2288"
                            elif store == "文心店":
                                phone_num = "04-2311-6688"
                            elif store == "東寧店":
                                phone_num = "06-276-2595"
                            elif store == "崇學店":
                                phone_num = "06-336-0199"
                            elif store == "永康店":
                                phone_num = "06-312-7728"
                            elif store == "三多店":
                                phone_num = "07-339-3525"
                            else:
                                phone_num = "0800-500080"

                            # reservation_time = str(select_date) + " " + lineText
                            # event_id = fb.get(event.source.user_id, 'event_id')
                            # unit_id = fb.get(event.source.user_id, 'unit_id')
                            c_name = fb.get(event.source.user_id, 'name')
                            line_bot_api.reply_message(
                                event.reply_token,
                                TextSendMessage(
                                    text=c_name + '您好~謝謝您的預約,' + '\n' + '以下是您的預約資訊:' + '\n' + '\n' + '分店:' + store + '\n' + '療程:'
                                         + service + '\n' + '日期:' + select_date + '\n' + '時間:' + lineText + '\n' + '\n'
                                         + '再請您當天依預約時段前來,如有任何問題,請至電' + phone_num + '\n' + '謝謝~'))
                        else:
                            line_bot_api.reply_message(
                                event.reply_token,
                                TextSendMessage(text=content))
                except:
                    new_cust_retry(content, lineText, event, doc, doc_ref)
    except:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="error"))
