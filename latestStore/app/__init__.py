from flask import Flask

app = Flask(__name__)

from .webhook import app_lateststore as api_lateststore_Blueprint
app.register_blueprint(api_lateststore_Blueprint)





