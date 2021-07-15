from flask import Blueprint, request

app_updateentityauto = Blueprint("webhook", __name__)


@app_updateentityauto.route("/updateentityauto", methods=['POST'])
def get_date():
    reponse = request.get_json(force=True)
    return reponse


@app_updateentityauto.route("/")
def testing():
    return "test"