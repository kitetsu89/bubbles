#!/usr/bin/env python3

import socket, ssl
import requests
#import openSSL




c = int(input("""
\nWelcome to the CONNECTIVITY TESTING script
Choose one of the following options:
 \n(1) HTTP status-code check
 \n(2) TCP Test
 \n(3) DNS look-up
 \n(4) TLS/SSL Test
\n> """))

# to be done: TLS/SSL wrapper etc


HOST = str(input("\nProvide IP-address or domainname> "))

# Input information




if c == 1 or c == 2 or c == 4:
    PORT = int(input("Please, specify port> "))

if c == 1:
# HTTP-test
    print(f"""
        *** HTTP TEST ***\n

        testing: {HOST}:{PORT}\n

        loading.....
        """)
    try:
        r = requests.get(f"https://{HOST}")
        u = r.status_code
        b = r.text
        print(f"Test succesvol! Status_code: {u}")
    except:
        print('Unable to Connect with HTTP-server')

elif c == 2:

# TCP TEST
    print(f"""
    *** TCP TEST ***\n
    Creating stream socket on \"{HOST}:{PORT}\"
    """)

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Connecting....this can take a few seconds...")
        s.connect((HOST, PORT))
        s.send(b'')
        s.settimeout(100)
        data = s.recv(1024)
        print(f"Result: TCP-connection successful!, received byte string: {data}")
    except:
        print("Unable to connect....")
    finally:
        s.close()

elif c == 3:

    print(f"""
    \n*** DNS-query ***\n
    \nloading DNS query for {HOST}
    """)
    try:
        host = socket.gethostbyname(HOST)
        print(f"Result: {HOST} 'maps to' {host}\n")
    except:
        print(f"Unable to query, please check if host {HOST} is defined correctly")

elif c == 4:

    #context = ssl.create_default_context()
    #sock = socket.create_connection((HOST, PORT))

# secure socket creation
    #ssock = context.wrap_socket(sock, server_hostname = HOST)
    #print("TLS/SSL version: {}".format(ssock.version()))

    cr = ssl.get_server_certificate(('nu.nl', 443))
    print(f"{cr}")

        #hier moet ie dan terug naar de host question...
