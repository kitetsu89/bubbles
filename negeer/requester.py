import requests
import os
import time as t

HOST1 = os.environ['TEST_OBJ_ACC']
HOST2 = os.environ['TEST_OBJ_PRD']

# mail information
username = os.environ['SMTP_USER']
password = os.environ['SMTP_PASS']
mail_host = os.environ['SMTP_SERV']
recipient = os.environ['SMTP_RECP']

def http_req():
        at = t.asctime(t.localtime((t.time())))
        r1 = requests.get(f"https://{HOST1}")
        r2 = requests.get(f"https://{HOST2}")
        u1 = r1.status_code
        u2 = r2.status_code
        st1 = f"HTTP test successful for {HOST1}, status_code: {u1} @ {at}"
        st2 = f"HTTP test successful for {HOST2}, status_code: {u2} @ {at}"

http_req()
