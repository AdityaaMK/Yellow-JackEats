# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = "ACca1ee556b359ebfb6da84b0ee54efbdf"
auth_token = "2c5be667b816d2b1c7a5520124b0d578"
client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body="Join Earth's mightiest heroes. Like Kevin Bacon.",
                     from_='+13204002975',
                     to='+16692558316'
                 )

print(message.sid)