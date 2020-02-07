import json

DB_PATH = 'db.sqlite'
LOG_CONFIG_PATH = 'logging.conf'

_creds = json.load(open('tmp/cred.json', 'r'))
LOGIN = _creds['LOGIN']
PASSWORD = _creds['PASSWORD']
POSTS_AMOUNT = 100
POSTS_DOWNLOAD_MAX = float('inf')
UPDATE_GROUP_INFO = True
UPDATE_COUNTERS = True
UPDATE_POSTS_INFO = False
