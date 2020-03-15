import boto3
from botocore.exceptions import ClientError
from tabulate import tabulate

template_html = """
<html>
<head>
<style> 
  table, th, td {{ border: 1px solid black; border-collapse: collapse; }}
  th, td {{ padding: 5px; }}
</style>
</head>
    <body><p>Hello, There.</p>
    <p>Here is your data:</p>
    <p>This is 1bhk and 2 bhk under 3000 sorted by rate and then movein date</p>
    {table}
    <p>Regards,</p>
    <p>Deepanshu</p>
    </body>

</html>
"""


def send_email(body_html):
    # me == my email address
    # you == recipient's email address
    me = "deepanshu.lulla@gmail.com"
    priya = "priya.makhija24@gmail.com"
    you = "deepanshu.lulla@gmail.com"
    AWS_REGION = 'us-east-1'
    # Create a new SES resource and specify a region.
    client = boto3.client('ses', region_name=AWS_REGION)
    # The character encoding for the email.
    CHARSET = "UTF-8"
    # Try to send the email.
    try:
        # Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    you,priya
                ],
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
                    'Data': "Newport rentals Cron",
                },
            },
            Source=me,
        )
    # Display an error if something goes wrong.
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])
    return body_html


def generate_html_table(apartments_dictionary_list):
    headers = ['apt_num', 'building_name', 'address', 'unit_type', 'area', 'rent', 'availability']
    apt_list_flat = []
    for apt in apartments_dictionary_list:
        apt_tuple = []
        for header in headers:
            apt_tuple.append(apt[header])
        apt_list_flat.append(apt_tuple)
    table = tabulate(apt_list_flat, headers=headers, tablefmt="html", showindex="always", stralign="center")
    return template_html.format(table=table)
