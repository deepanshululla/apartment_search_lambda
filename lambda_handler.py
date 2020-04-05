import json

from data_exporter import generate_html_table, send_email
from data_importer import fetch_apartment_list



def hello(event, context):
    apt_list = fetch_apartment_list()
    apt_dict_list = [x.to_dict() for x in apt_list]
    result = send_email(generate_html_table(apt_dict_list))

    response = {
        "statusCode": 200,
        "body": json.dumps(result)
    }

    return response

