from . import db, line_bot_api, handler, url
from linebot.models import MessageEvent, TextMessage, TextSendMessage, QuickReply, QuickReplyButton, MessageAction, FlexSendMessage
from .dialogflow import set_context, PersonalInfo, dialogflow, set_context2, old_cust_reset_context, new_cust_reset_context
from .flex import categoryInfo,  eventInfo,  storeInfo, storelocation, chg_categoryInfo
from datetime import datetime, timedelta
from random import choice
from .commonTool import categoryQuery, existEvent, unitsQuery, eventQuery
from firebase import firebase
import requests


datefrom = str(datetime.now())[0:10]
end_date = datetime.now() + timedelta(days=14)
dateto = str(end_date)[0:10]
fb = firebase.FirebaseApplication(url, None)


def category(user_id, reply_token):
    text_message = FlexSendMessage(
        alt_text='請問您要預約的課程分類是?',
        contents=categoryInfo(),
    )
    line_bot_api.reply_message(reply_token, text_message)


def chg_category(user_id, reply_token):
    text_message = FlexSendMessage(
        alt_text='請問您要預約的課程分類是?',
        contents=chg_categoryInfo(),
    )
    line_bot_api.reply_message(reply_token, text_message)


def event2(cate_name, user_id, reply_token, doc_ref):
    cate_id = categoryQuery(cate_name)
    event_list = existEvent(cate_id)
    fb.put(user_id, 'event_list', event_list)
    text_message = FlexSendMessage(
        alt_text='請問您要預約的服務是?',
        contents=eventInfo(event_list),
    )
    line_bot_api.reply_message(reply_token, text_message)
    fb.put(user_id, 'category', cate_name)


def date2(user_id, reply_token, content, eve_name):
    event_id = eventQuery(eve_name)
    fb.put(user_id, 'event_id', event_id)
    store = fb.get(user_id, 'store')
    url = "https://event.smarter.com.tw/chatbot/date"
    data = {
        "store": store,
        "event_id": event_id
    }
    content2 = requests.post(url, json=data)
    # unit_id = unitsQuery(store)
    # content2 = getStartTimeMatrix(datefrom, dateto, event_id, unit_id)
    available_time = content2.json()
    text_message = gen_quick_btn("請問您要預約的日期是?", **available_time)
    fb.put(user_id, 'available_time', available_time)
    line_bot_api.reply_message(reply_token, text_message)
    fb.put(user_id, 'event', eve_name)


def time(user_id, reply_token, content, select_date):
    text_message = gen_quick_btn2("請問您要預約的時間是?", select_date, user_id)
    line_bot_api.reply_message(reply_token, text_message)
    fb.put(user_id, 'date', select_date)


def success(app, user_id, lineText, c_name, c_gender, c_email, c_phone):
    with app.app_context():
        fb.put(user_id, 'time', lineText)
        print('success:' + lineText)
        PersonalInfo_data = {}
        category = fb.get(user_id, "category")
        select_date = fb.get(user_id, 'date')
        email = c_email
        gender = c_gender
        location = fb.get(user_id, 'location')
        name = c_name
        phone = c_phone
        service = fb.get(user_id, 'event')
        store = fb.get(user_id, 'store')
        PersonalInfo_data.update(
            {
                "category": category,
                "date": select_date,
                "email": email,
                "gender": gender,
                "location": location,
                "name": name,
                "phone": phone,
                "service": service,
                "store": store,
                "time": lineText,
                "user_id": user_id
            }
        )
        doc_ref = db.collection("PersonalInfo").document(user_id)
        doc_ref.set(PersonalInfo_data)
        print("PersonalInfo_data finish")
        ReservationLog_data = {}
        doc_ref2 = db.collection("ReservationLog")
        ReservationLog_data.update(
            {
                "category": category,
                "date": select_date,
                "name": name,
                "service": service,
                "store": store,
                "time": lineText,
                "user_id": user_id
            }
        )
        doc_ref2.add(ReservationLog_data)
        print("ReservationLog_data finish")

    # try:
    #     clientData.update(
    #         {"name": doc.to_dict()['name'], "email": doc.to_dict()['email'], "phone": doc.to_dict()['phone']})
    #     gender = doc.to_dict()['gender']
    # except:
    #     name = fb.get(user_id, 'name')
    #     email = fb.get(user_id, 'email')
    #     phone = fb.get(user_id, 'phone')
    #     clientData.update({"name": name, "email": email, "phone": phone})
    #     gender = fb.get(user_id, 'gender')
    # location_id = get_location_id(store)
    # content2 = getAvailableUnits(event_id, reservation_time)
    # AvailableUnits = content2.json()
    # random_one = random_unit(*unit_id, **AvailableUnits)
    # # content3 = book(event_id, random_one, select_date, lineText, location_id, gender, **clientData)
    # content3 = event_id + location_id + gender
    # print(content3)


def book(app, user_id, reply_token, lineText, c_name, c_gender):
    with app.app_context():
        print("booking")
        select_date = fb.get(user_id, 'date')
        gender = c_gender
        service = fb.get(user_id, 'event')
        store = fb.get(user_id, 'store')
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

        reservation_time = str(select_date) + " " + lineText
        event_id = fb.get(user_id, 'event_id')
        unit_id = fb.get(user_id, 'unit_id')
        clientData = {}
        url = "https://event.smarter.com.tw/chatbot/book"
        data = {
            "store": store,
            "event_id": event_id,
            "reservation_time": reservation_time,
            "unit_id": unit_id,
            "select_date": select_date,
            "select_time": lineText,
            "gender": gender,
            "clientData": clientData
        }
        content2 = requests.post(url, json=data)
        print(content2.text)
        line_bot_api.reply_message(
            reply_token,
            TextSendMessage(
                text=c_name + '您好~謝謝您的預約,' + '\n' + '以下是您的預約資訊:' + '\n' + '\n' + '分店:' + store + '\n' + '療程:'
                     + service + '\n' + '日期:' + select_date + '\n' + '時間:' + lineText + '\n' + '\n'
                     + '再請您當天依預約時段前來,如有任何問題,請至電' + phone_num + '\n' + '謝謝~'))


def location(user_id, reply_token):
    text_message = TextSendMessage(text="請問您要預約的地點是?",
                                   quick_reply=QuickReply(items=[
                                       QuickReplyButton(action=MessageAction(label="台北", text="台北")),
                                       QuickReplyButton(action=MessageAction(label="新北", text="新北")),
                                       QuickReplyButton(action=MessageAction(label="新竹", text="新竹")),
                                       QuickReplyButton(action=MessageAction(label="台中", text="台中")),
                                       QuickReplyButton(action=MessageAction(label="台南", text="台南")),
                                       QuickReplyButton(action=MessageAction(label="高雄", text="高雄")),
                                       QuickReplyButton(action=MessageAction(label="最近店家", text="最近店家"))
                                   ]))
    line_bot_api.reply_message(reply_token, text_message)


def store2(content2, lineText, user_id, reply_token):
    if lineText == "最近店家":
        line_bot_api.reply_message(
            reply_token,
            TextSendMessage(text=content2))
    else:
        if content2 == "已填完地址":
            # store = get_coordinate(lineText)
            url = "https://event.smarter.com.tw/chatbot/lateststore"
            data = {
                "address": lineText
            }
            store = requests.post(url, json=data)
            print(store.text)
            text_message = FlexSendMessage(
                alt_text='請問您要預約的店家是?',
                contents=storelocation(store.text),
            )
            line_bot_api.reply_message(reply_token, text_message)
        else:
            text_message = FlexSendMessage(
                alt_text='請問您要預約的店家是?',
                contents=storeInfo(lineText),
            )
            line_bot_api.reply_message(reply_token, text_message)
    if lineText == "台北" or lineText == "新北" or lineText == "新竹" or lineText == "台中" or lineText == "台南" or lineText == "高雄" or lineText == "最近店家":
        fb.put(user_id, 'location', lineText)


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


def new_cust_back(content, lineText, user_id, reply_token, doc, doc_ref, fb):
    action_numbers = int(new_cust_action(content))-1
    print(action_numbers)
    if action_numbers == 5:
        location(user_id, reply_token)
    if action_numbers == 6:
        location2 = fb.get(user_id, "location")
        store2(content, location2, user_id, reply_token)
    if action_numbers == 7:
        category(user_id, reply_token)
    elif action_numbers == 8:
        cate_name = fb.get(user_id, "category")
        event2(cate_name, user_id, reply_token, doc_ref)
    elif action_numbers == 9:
        eve_name = fb.get(user_id, "event")
        date2(user_id, reply_token, content, eve_name)
    elif action_numbers == 10:
        select_date = fb.get(user_id, "date")
        time(user_id, reply_token, content, select_date)
        pass


def new_cust_retry(content, lineText, user_id, reply_token, doc, doc_ref):
    action_numbers = int(new_cust_action(content))
    if action_numbers == 7:
        category(user_id, reply_token)
    elif action_numbers == 8:
        cate_name = fb.get(user_id, 'category')
        event2(cate_name, user_id, reply_token, doc_ref)
    elif action_numbers == 9:
        eve_name = fb.get(user_id, 'event')
        date2(user_id, reply_token, content, eve_name)
    elif action_numbers == 10:
        select_date = fb.get(user_id, 'date')
        time(user_id, reply_token, content, select_date)


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


def back(content, lineText, user_id, reply_token, doc, doc_ref):
    action_numbers = int(action_number(content))-1
    print(action_numbers)
    print(lineText)
    if action_numbers == 4:
        content = PersonalInfo("是", user_id)
        text_message = TextSendMessage(text=content,
                                       quick_reply=QuickReply(items=[
                                           QuickReplyButton(action=MessageAction(label="名字", text="名字")),
                                           QuickReplyButton(action=MessageAction(label="電話", text="電話")),
                                           QuickReplyButton(action=MessageAction(label="信箱", text="信箱")),
                                           QuickReplyButton(action=MessageAction(label="店家", text="店家")),
                                           QuickReplyButton(action=MessageAction(label="不改變", text="不改變")),
                                       ]))
        line_bot_api.reply_message(reply_token, text_message)
    elif action_numbers == 5:
        category(user_id, reply_token)
    elif action_numbers == 6:
        cate_name = fb.get(user_id, 'category')
        event2(cate_name, user_id, reply_token, doc_ref)
    elif action_numbers == 7:
        eve_name = fb.get(user_id, 'event')
        date2(user_id, reply_token, content, eve_name)
    elif action_numbers == 8:
        select_date = fb.get(user_id, 'date')
        time(user_id, reply_token, content, select_date)
        pass


def retry(content, lineText, user_id, reply_token, doc, doc_ref):
    action_numbers = int(action_number(content))
    print(action_numbers)
    print(lineText)
    if action_numbers == 5:
        category(user_id, reply_token)
    elif action_numbers == 6:
        cate_name = fb.get(user_id, 'category')
        event2(cate_name, user_id, reply_token, doc_ref)
    elif action_numbers == 7:
        eve_name = fb.get(user_id, 'event')
        date2(user_id, reply_token, content, eve_name)
    elif action_numbers == 8:
        select_date = fb.get(user_id, 'date')
        time(user_id, reply_token, content, select_date)
        pass


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
            # print(key, value)
            context.append(QuickReplyButton(action=MessageAction(label=key, text=key)))
    if int(len(context)) > 13:
        context = context[0:13]
        text_message = TextSendMessage(text=content,
                                       quick_reply=QuickReply(items=
                                                              context
                                                              ))
    elif int(len(context)) == 1:
        text_message = TextSendMessage(text="不好意思，該課程都已約滿!",
                                       quick_reply=QuickReply(items=
                                                              context
                                                              ))
    else:
        text_message = TextSendMessage(text=content,
                                       quick_reply=QuickReply(items=
                                                              context
                                                              ))
    return text_message


def gen_quick_btn2(content, lineText, user_id):
    context = []
    context.append(
        QuickReplyButton(action=MessageAction(label="回上一頁", text="*回上一頁"))
    )
    available_time = fb.get(user_id, 'available_time')
    for key, value in available_time["result"].items():
        if key == lineText:
            for i in value:
                context.append(QuickReplyButton(action=MessageAction(label=i, text="*"+i)))
        else:
            continue
    if int(len(context)) > 13:
        context = context[0:13]
        text_message = TextSendMessage(text=content,
                                       quick_reply=QuickReply(items=
                                                              context
                                                              ))
    elif int(len(context)) == 1:
        text_message = TextSendMessage(text="不好意思，該課程都已約滿!",
                                       quick_reply=QuickReply(items=
                                                              context
                                                              ))
    else:
        text_message = TextSendMessage(text=content,
                                       quick_reply=QuickReply(items=
                                                              context
                                                              ))
    return text_message
