# importing requests modules
import requests
import os

# import scheduler and time modules
import schedule
import time as t

# import modules for mail
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

print("Welcome to Bubbles v0.4_for_Heroku")

print("""
Running....
""")

# test object information
HOST = "nu.nl"

# mail information
username = os.environ.get['SMTP_USER']
password = os.environ.get['SMTP_PASS']
mail_host = 'smtp.gmail.com'

recipient = os.environ.get['SMTP_RECP']

# function for requesting HTTP-statuscode
def http_req():
        try:
            at = t.asctime(t.localtime((t.time())))
            r = requests.get(f"https://{HOST}")
            u = r.status_code
            st = f"HTTP test succesvol for {HOST}, status_code: {u} @ {at}"
        except:
            st = f"Unable to Connect with {HOST} @ {at}"
        finally:
            print(st)
            return st

# function of mail_login
def mail_login():
        try:
            s = smtplib.SMTP_SSL(mail_host)
            print(f"Successfully connected to {mail_host}")
            return s
        except:
            print(f"Not connected to {mail_host}")

# function for composing mail
def mail_compose():
    s = mail_login()
    msg_text = http_req()
    msg = MIMEMultipart()
    msg.attach(MIMEText(msg_text, 'plain'))
    msg['From'] = username
    msg['To'] = recipient
    msg['Subject'] = f'Log for {HOST}'
    try:
        s.login(username, password)
        s.sendmail(msg['From'], msg['To'], msg.as_string())
        print(f"successfully sent to {recipient}")
    except:
        print(f"unable to sent to {recipient}")
    finally:
        s.quit()

# Scheduler
# use function reference!!!!
schedule.every(5).minutes.do(mail_compose)

# Runner
while True:
# current time, EPOCH -> Struct -> ASCII
    schedule.run_pending()
    t.sleep(1)
