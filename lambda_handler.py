import json

from data_exporter import generate_html_table, send_email
from data_importer import fetch_apartment_list



def hello(event, context):
    result = send_email(generate_html_table(fetch_apartment_list()))

    response = {
        "statusCode": 200,
        "body": json.dumps(result)
    }

    return response

