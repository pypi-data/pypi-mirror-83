# -*- coding: utf-8 -*-
"""
This script allows you to send emails to a mailing list using AWS SES.

For more information, refer to documentation on Notion.
"""

import boto3
from botocore.exceptions import ClientError

#put the mailing list into a config.py file
maillist = ['recipient1@email.com','recipient2@email.com'] 

def send_report(item_list):
    
    SENDER = "Email Bot <mailbot@email.com>"
    AWS_REGION = "us-west-2"
    CHARSET = "UTF-8"
    
    SUBJECT = "Subject"
    client = boto3.client('ses',region_name=AWS_REGION)
    
    try:
        response = client.send_email(
            Destination={
                'ToAddresses': maillist,
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': ''.join(['<p>' + item + '</p>' for item in item_list]),
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])