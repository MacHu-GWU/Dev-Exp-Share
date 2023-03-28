# -*- coding: utf-8 -*-

import json
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pprint import pprint

import boto3

aws_profile = "eq_sanhe"
aws_region = "us-east-1"
boto_ses = boto3.session.Session(profile_name=aws_profile, region_name=aws_region)
ses_client = boto_ses.client("ses")

sender_email = "sender@email.com"
receiver_email_list = [
    "receiver1@email.com",
    "receiver2@email.com",
]
subject = "Sanhe AWS SES Test"
text_body = "Hello, this is a test email from AWS SES"
html_body = """
Hello, this is a <strong>test</strong> email from AWS SES
<ul>
    <li>first</li>
    <li>second</li>
    <li>third</li>
</ul>
"""

attachment_content = json.dumps({"email": "my@email.com", "password": "J2q3uZ@JkFSQ"}).encode("utf-8")
attachment_filename = "data.json"


def send_plain_text_email():
    params = dict(
        Source=sender_email,
        Destination={
            "ToAddresses": receiver_email_list
        },
        Message={
            "Subject": {
                "Data": subject,
            },
            "Body": {
                "Text": {
                    "Data": text_body,
                }
            }
        }
    )
    res = ses_client.send_email(**params)
    pprint(res)


# send_plain_text_email()

def send_html_email():
    params = dict(
        Source=sender_email,
        Destination={
            "ToAddresses": receiver_email_list
        },
        Message={
            "Subject": {
                "Data": subject,
            },
            "Body": {
                "Html": {
                    "Data": html_body,
                }
            }
        }
    )
    res = ses_client.send_email(**params)
    pprint(res)


# send_html_email()

def send_attachment_email():
    """
    If you want to send email with attachment, you have to use
    python email.mime.multipart library to encode it and send through
    ses.send_raw_email() api.
    """
    message = MIMEMultipart()
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = ",".join(receiver_email_list)

    # message body
    email_body = MIMEText(html_body, "html")
    message.attach(email_body)

    # attachment
    attachment = MIMEApplication(attachment_content)
    attachment.add_header("Content-Disposition", 'attachment', filename=attachment_filename)
    message.attach(attachment)

    params = dict(
        Source=sender_email,
        Destinations=receiver_email_list,
        RawMessage={
            "Data": message.as_bytes(),
        }
    )
    res = ses_client.send_raw_email(**params)
    pprint(res)

# send_attachment_email()
