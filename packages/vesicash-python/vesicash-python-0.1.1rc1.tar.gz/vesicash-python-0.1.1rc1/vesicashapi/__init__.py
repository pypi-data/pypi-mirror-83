import os

"""Script used to define constants"""

PRIVATE_KEY = os.getenv(
    'VESICASH_PRIVATE_KEY',
    'v_sandbox_rcFScqeBxChswiaiG3hfLwEFVq3j3jtzbLnbaQmTrRAwwSwyJE'
)
HEADERS = {'V-Private-Key': PRIVATE_KEY}
api_url = ''
mode = os.getenv('VESICASH_MODE')

if(mode == 'sandbox'):
    API_URL = 'https://sandbox.api.vesicash.com/v1/'
else:
    API_URL = 'https://api.vesicash.com/v1/'
