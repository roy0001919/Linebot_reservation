from . import db
from datetime import datetime

def set_context(user_id, name, gender, phone, email):
    import os
    import dialogflow_v2 as dialogflow
    from google.api_core.exceptions import InvalidArgument

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = ""
    projectID = ""
    # client = dialogflow.IntentsClient()
    # parent = client.project_agent_path(projectID)

    DIALOGFLOW_LANGUAGE_CODE = 'zh-tw'
    now = datetime.now()
    SESSION_ID = user_id#str(user_id) + str(now)
    text_to_be_analyzed = "1"
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(projectID, SESSION_ID)
    text_input = dialogflow.types.TextInput(text=text_to_be_analyzed, language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dialogflow.types.QueryInput(text=text_input)
    parameters = dialogflow.types.struct_pb2.Struct()
    parameters["user_id"] = user_id
    parameters["name"] = name
    parameters["gender"] = gender
    parameters["phone"] = phone
    parameters["email"] = email
    doc_ref = db.collection("PersonalInfo").document(user_id)
    doc = doc_ref.get()
    context_1 = dialogflow.types.context_pb2.Context(
        name='',
        lifespan_count=15,
        parameters=parameters)
    query_params_1 = {"contexts": [context_1]}
    try:
        response = session_client.detect_intent(session=session, query_input=query_input, query_params=query_params_1)
    except InvalidArgument:
        raise
    # JsonType = pf.json_format.MessageToJson(response.query_result.fulfillment_messages,including_default_value_fields=False)
    content = response.query_result.fulfillment_text
    return content


def dialogflow_creat_entity(entity_id, key, value):
    import dialogflow_v2 as dialogflow
    import os

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = ""
    entity_type_UUID = entity_id
    entity_type_client = dialogflow.EntityTypesClient()
    parent = entity_type_client.entity_type_path("", entity_type_UUID)
    entities = [
        {
            "value": key,
            "synonyms": [
                value
            ]
        }
    ]
    response = entity_type_client.batch_create_entities(parent, entities)
    print(response)


def set_context2(user_id):
    import os
    import dialogflow_v2 as dialogflow
    from google.api_core.exceptions import InvalidArgument

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = ""
    projectID = ""
    # client = dialogflow.IntentsClient()
    # parent = client.project_agent_path(projectID)

    DIALOGFLOW_LANGUAGE_CODE = 'zh-tw'
    now = datetime.now()
    SESSION_ID = user_id#str(user_id) + str(now)
    text_to_be_analyzed = "1"
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(projectID, SESSION_ID)
    text_input = dialogflow.types.TextInput(text=text_to_be_analyzed, language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dialogflow.types.QueryInput(text=text_input)
    parameters = dialogflow.types.struct_pb2.Struct()
    parameters["user_id"] = user_id
    # parameters["name"] = "愈則"
    # parameters["gender"] = "男"
    # parameters["phone"] = "0987456764"
    # parameters["email"] = "roy0001919@gmail.com"
    doc_ref = db.collection("PersonalInfo").document(user_id)
    doc = doc_ref.get()
    parameters["location"] = None if doc.to_dict() is None else doc.to_dict()['location']
    parameters["store"] = None if doc.to_dict() is None else doc.to_dict()['store']
    context_1 = dialogflow.types.context_pb2.Context(
        name='',
        lifespan_count=15,
        parameters=parameters)
    query_params_1 = {"contexts": [context_1]}
    try:
        response = session_client.detect_intent(session=session, query_input=query_input, query_params=query_params_1)
    except InvalidArgument:
        raise
    # JsonType = pf.json_format.MessageToJson(response.query_result.fulfillment_messages,including_default_value_fields=False)
    content = response.query_result.fulfillment_text
    return content


def new_cust_reset_context(user_id):
    import dialogflow_v2 as dialogflow
    import os

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = ""
    client = dialogflow.ContextsClient()
    parent = client.session_path("", user_id)
    client.delete_all_contexts(parent)


def old_cust_reset_context(user_id):
    import dialogflow_v2 as dialogflow
    import os

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = ""
    client = dialogflow.ContextsClient()
    parent = client.session_path("", user_id)
    client.delete_all_contexts(parent)


def PersonalInfo(lineText, user_id):
    import os
    import dialogflow_v2 as dialogflow
    from google.api_core.exceptions import InvalidArgument
    import google.protobuf  as pf
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = ""
    projectID = ""
    # client = dialogflow.IntentsClient()
    # parent = client.project_agent_path(projectID)

    DIALOGFLOW_LANGUAGE_CODE = 'zh-tw'
    now = datetime.now()
    SESSION_ID = user_id
    text_to_be_analyzed = lineText
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(projectID, SESSION_ID)
    text_input = dialogflow.types.TextInput(text=text_to_be_analyzed, language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dialogflow.types.QueryInput(text=text_input)
    try:
        response = session_client.detect_intent(session=session, query_input=query_input)
    except InvalidArgument:
        raise
    # JsonType = pf.json_format.MessageToJson(response.query_result.fulfillment_messages,including_default_value_fields=False)
    content = response.query_result.fulfillment_text
    # content = JsonType
    return content


def dialogflow(lineText, user_id):
    import os
    import dialogflow_v2 as dialogflow
    from google.api_core.exceptions import InvalidArgument
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = ""
    projectID = ""
    # client = dialogflow.IntentsClient()
    # parent = client.project_agent_path(projectID)

    DIALOGFLOW_LANGUAGE_CODE = 'zh-tw'
    SESSION_ID = user_id
    text_to_be_analyzed = lineText
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(projectID, SESSION_ID)
    text_input = dialogflow.types.TextInput(text=text_to_be_analyzed, language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dialogflow.types.QueryInput(text=text_input)
    try:
        response = session_client.detect_intent(session=session, query_input=query_input)
    except InvalidArgument:
        raise
    content = response.query_result.fulfillment_text
    return content

