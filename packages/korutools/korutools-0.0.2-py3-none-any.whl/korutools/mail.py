# -*- coding: utf-8 -*-
"""
This script allows you to send emails to a mailing list using AWS SES.

For more information, refer to documentation on Notion.
"""

import boto3
from botocore.exceptions import ClientError

def send_report(item_list, maillist, subject):
    
    SENDER = "Email Bot <argusmailbot@gmail.com>"
    AWS_REGION = "us-west-2"
    CHARSET = "UTF-8"
    
    SUBJECT = subject
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