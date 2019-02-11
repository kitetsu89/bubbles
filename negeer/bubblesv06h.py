"""Script for HTTP servertesting"""

# importing environment variables
import os

# import modules for mail
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# import scheduler and time modules
import time as t
import schedule

# importing requests modules
import requests

print("Welcome to Bubbles v0.6_for_Heroku")

print("""
Running....
""")

# Objects to be tested
HOST1 = os.environ['HOST1'] # [HOST_NAME, HOST]
HOST2 = os.environ['HOST2'] # [HOST_NAME, HOST]
# split into HOST URL and HOST-name
HOST_LIST1 = HOST1.split(',')
HOST_LIST2 = HOST2.split(',')

# mail information
USERNAME = os.environ['SMTP_USER']
PASSWORD = os.environ['SMTP_PASS']
MAIL_HOST = os.environ['SMTP_SERV']

recipient = os.environ['SMTP_RECP']
recipient_list = recipient.split(',')

def http_requestor(HOST_NAME, HOST):
    """the function that triggers http-requests"""
    try:
        at = t.asctime(t.localtime((t.time())))
        r = requests.get(f"https://{HOST}")
        u = r.status_code
        st = f"{HOST_NAME}\nHTTP test successful for {HOST}, status_code: {u} @ {at}\n"
    except Exception as e:
        st = f"{HOST_NAME}\nUnable to connect with {HOST} @ {at}\nLog: {e}\n"
    finally:
        return st

def mail_login():
    try:
        s = smtplib.SMTP_SSL(MAIL_HOST)
        print(f"Successfully connected to {MAIL_HOST}")
        return s
    except:
        print(f"Not connected to {MAIL_HOST}")

# Message text is a string
def mail_compose():
    s = mail_login()
    msg_text = http_requestor(HOST_LIST1[0], HOST_LIST1[1]) + http_requestor(HOST_LIST2[0], HOST_LIST2[1])
    msg = MIMEMultipart()
    msg.attach(MIMEText(msg_text, 'plain'))
    msg['From'] = USERNAME
    msg['To'] = recipient
    msg['Subject'] = "Daily report RCS-proxy"

    try:
        s.login(USERNAME, PASSWORD)
        print("successfully logged in")
    except:
        print("unable to login")

    try:
        s.sendmail(msg['From'], recipient_list, msg.as_string())
        print(f"successfully sent to {recipient_list}")
    except:
        print(f"unable to send to {recipient_list}")
    finally:
        s.quit()

#mail_compose()
schedule.every().day.at("08:30").do(mail_compose)

# Runner
while True:
  schedule.run_pending()

t.sleep(1)
