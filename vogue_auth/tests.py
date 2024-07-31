from django.test import TestCase

# Create your tests here.

'''import smtplib

try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('dhirugamingxon@gmail.com', 'wdil hidw mqde jmlg')
    server.sendmail('dhirugamingxo@gmail.com', 'jayeshpagar070@example.com', 'Test email')
    server.quit()
    print("Email sent successfully!")
except Exception as e:
    print(f"Failed to send email: {e}")
'''

import ssl
import socket

def check_ssl_cert(hostname, port):
    context = ssl.create_default_context()
    with socket.create_connection((hostname, port)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            cert = ssock.getpeercert()
            print(cert)

check_ssl_cert('smtp.gmail.com', 587)

