from flask import Flask
from flask_apscheduler import APScheduler
from .updateentityauto import Config

app = Flask(__name__)

from .webhook import app_updateentityauto as api_event_Blueprint
app.register_blueprint(api_event_Blueprint)


app.config.from_object(Config())
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()