from flask import Blueprint, request
from .date import unitsQuery, getStartTimeMatrix
from datetime import datetime, timedelta

app_date = Blueprint("webhook", __name__)


datefrom = str(datetime.now())[0:10]
end_date = datetime.now() + timedelta(days=14)
dateto = str(end_date)[0:10]


@app_date.route("/date", methods=['POST'])
def get_date():
    reponse = request.get_json(force=True)
    unit_id = unitsQuery(reponse["store"])
    content2 = getStartTimeMatrix(datefrom, dateto, reponse["event_id"], unit_id)
    available_time = content2.json()
    return available_time


# @app_date.route("/")
# def testing():
#     return "test"