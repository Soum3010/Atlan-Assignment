from twilio.rest import Client
import json
import os

file_path = os.path.join('SMSservice', 'twilio.json')
with open(file_path) as f:
    twilio_keys = json.load(f)

twilio_client = Client(twilio_keys['account_sid'], twilio_keys['auth_token'])
