# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client
import netifaces as ni


ni.ifaddresses('wlan0')
ip = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']
print(ip)


# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = 'ACd3cf45089d440771cac793386a783249'
auth_token = 'e6ba06f4263331bdb6f5be7c6a2ca3c0'
client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body="Freelin it @ " + ip,
                     from_='+14132871478',
                     to='+14138002963'
                 )

print(message.sid)

