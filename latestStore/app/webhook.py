from flask import Blueprint, request
from .lateststore import get_store
import geocoder

app_lateststore = Blueprint("webhook", __name__)


@app_lateststore.route("/lateststore", methods=['POST'])
def get_lateststore():
    reponse = request.get_json(force=True)
    g = geocoder.arcgis(u"%s" % reponse["address"])
    content = get_store(g.lat, g.lng)
    return content


@app_lateststore.route("/")
def testing():
    return "test"