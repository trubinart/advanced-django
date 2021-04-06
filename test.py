import os
import json

# LOAD SECRETS KEY FOR AUTH
SOCIAL_SECRETS_FILE = 'geekshop/google.json'

SOCIAL = {}

if os.path.exists(SOCIAL_SECRETS_FILE):
    with open('geekshop/google.json', 'r') as file:
        SOCIAL = json.load(file)

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = SOCIAL['web'].get('client_id', '')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = SOCIAL['web'].get('client_secret', '')

print(SOCIAL)
print(SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET)
print(SOCIAL_AUTH_GOOGLE_OAUTH2_KEY)