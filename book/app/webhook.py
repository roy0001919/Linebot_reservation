from flask import Blueprint, request
from .book import get_location_id, getAvailableUnits, random_unit, book

app_book = Blueprint("webhook", __name__)


@app_book.route("/book", methods=['POST'])
def get_date():
    reponse = request.get_json(force=True)
    location_id = get_location_id(reponse['store'])
    content2 = getAvailableUnits(reponse['event_id'], reponse['reservation_time'])
    AvailableUnits = content2.json()
    random_one = random_unit(*reponse['unit_id'], **AvailableUnits)
    # content3 = book(reponse['event_id'], random_one, reponse['select_date'], reponse['select_time'], location_id, reponse['gender'], **reponse['clientData'])
    content3 = reponse['event_id'] + location_id + reponse['gender']
    print(content3)
    return content3


@app_book.route("/")
def testing():
    return "test"