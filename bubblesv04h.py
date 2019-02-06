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
HOST1 = os.environ['TEST_OBJ_ACC']
HOST2 = os.environ['TEST_OBJ_PRD']

# mail information
username = os.environ['SMTP_USER']
password = os.environ['SMTP_PASS']
mail_host = os.environ['SMTP_SERV']
recipient = os.environ['SMTP_RECP']


# function for requesting HTTP-statuscode
def http_req():
        try:
            at = t.asctime(t.localtime((t.time())))
            r1 = requests.get(f"https://{HOST1}")
            r2 = requests.get(f"https://{HOST2}")
            u1 = r1.status_code
            u2 = r2.status_code
            st1 = f"HTTP test successful for {HOST1}, status_code: {u1} @ {at}"
            st2 = f"HTTP test successful for {HOST2}, status_code: {u2} @ {at}"
        except:
            st1 = f"Unable to Connect with {HOST1} @ {at}"
            st2 = f"Unable to Connect with {HOST2} @ {at}"
        finally:
            st = f"{st1}\n{st2}"
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
    print(type(msg_text))
    msg = MIMEMultipart()
    msg.attach(MIMEText(msg_text, 'plain'))
    msg['From'] = username
    msg['To'] = recipient
    msg['Subject'] = "Log for RCS-proxy"
    try:
        s.login(username, password)
        print("successfully logged in")
    except:
        print("unable to login")
    try:
        s.sendmail(msg['From'], msg['To'], msg.as_string())
        print(f"successfully sent to {recipient}")
    except:
        print(f"unable to send to {recipient}")
    finally:
        s.quit()

#mail_compose()

# Scheduler
# use function reference!!!!
schedule.every().day.at("08:30").do(mail_compose)

# Runner
#while True:
# current time, EPOCH -> Struct -> ASCII
    schedule.run_pending()
    t.sleep(1)
