import os

recipient = os.environ['SMTP_RECP']
recipient_list = recipient.split(',')

print(f"{recipient_list}")
