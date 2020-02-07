from pathlib import Path
import json
_creds = json.load(open(Path('tmp', 'cred.json'), 'r'))  # load credentials

INPUTS_FOLDER = Path('inputs').absolute()
OUTPUTS_FOLDER = Path('outputs').absolute()

INPUT_LIST_LINE_SEPARATOR = ','

DB_PATH = Path('db.sqlite').absolute()
LOG_CONFIG_PATH = Path('logging.conf').absolute()

LOGIN = _creds['LOGIN']
PASSWORD = _creds['PASSWORD']

POSTS_AMOUNT = 100
POSTS_DOWNLOAD_MAX = float('inf')
UPDATE_GROUP_INFO = True  # update group info when re-running script (if group exists in db)
UPDATE_COUNTERS = True  # update counters for a group when re-running script (if group exists in db)
UPDATE_POSTS_INFO = False  # update wall posts for a group when re-running script (if posts exist in db) [False]
