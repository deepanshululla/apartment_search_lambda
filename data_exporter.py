import boto3
from botocore.exceptions import ClientError
from tabulate import tabulate

from config import template_html, HEADERS, reciepients_list, sender_email, CHARSET


def send_email(body_html):
    AWS_REGION = 'us-east-1'
    # Create a new SES resource and specify a region.
    client = boto3.client('ses', region_name=AWS_REGION)
    # The character encoding for the email.

    # Try to send the email.
    try:
        # Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': reciepients_list,
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': body_html,
                    },

                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': "Newport Rentals Cron",
                },
            },
            Source=sender_email,
        )
    # Display an error if something goes wrong.
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])
    return body_html


def generate_html_table(apartments_dictionary_list):
    apt_list_flat = []
    for apt in apartments_dictionary_list:
        apt_tuple = []
        for header in HEADERS:
            apt_tuple.append(apt[header])
        apt_list_flat.append(apt_tuple)
    table = tabulate(apt_list_flat, headers=HEADERS, tablefmt="html", showindex="always", stralign="center")

    return template_html.format(table=table)
