# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client
from twilio_tokens import account_sid, auth_token

def sendMessage(body, to):
    # Find your Account SID and Auth Token at twilio.com/console
    # and set the environment variables. See http://twil.io/secure
    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                        body=body,
                        from_='+18454156955',
                        to=to
                    )

    print(message.sid)