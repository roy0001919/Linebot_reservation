from flask import Flask

app = Flask(__name__)

from .webhook import app_book as api_event_Blueprint
app.register_blueprint(api_event_Blueprint)