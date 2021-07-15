from flask import Flask
from firebase_admin import firestore
import firebase_admin
from firebase_admin import credentials

from .commonTool import loadJson
from linebot import (
    LineBotApi, WebhookHandler
)

line_bot_api = LineBotApi('')
handler = WebhookHandler('')
url = ''



def firestore_init():
    if not firebase_admin._apps:
        cred = credentials.Certificate(loadJson(""))
        firebase_admin.initialize_app(cred)


firestore_init()
db = firestore.client()
app = Flask(__name__)
from .webhook import app_chatbot as api_chatbot_Blueprint
app.register_blueprint(api_chatbot_Blueprint)





