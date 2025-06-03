from __future__ import annotations

import os

from common.settings_utils import read_bool
from dotenv import load_dotenv

load_dotenv()

# asgi + app
APP_ENV = os.environ["APP_ENV"]
APP_HOST = os.environ["APP_HOST"]
APP_PORT = os.environ["APP_PORT"]
APP_LOG_LEVEL = os.environ["APP_LOG_LEVEL"]
APP_DEBUG = read_bool(os.environ["APP_DEBUG"])

# bancho.py folder
BANCHOPY_FOLDER = os.environ["BANCHOPY_FOLDER"]

# domain
DOMAIN = os.environ["DOMAIN"]

# database
READ_DB_SCHEME = os.environ["READ_DB_SCHEME"]
READ_DB_HOST = os.environ["READ_DB_HOST"]
READ_DB_PORT = int(os.environ["READ_DB_PORT"])
READ_DB_USER = os.environ["READ_DB_USER"]
READ_DB_PASS = os.environ["READ_DB_PASS"]
READ_DB_NAME = os.environ["READ_DB_NAME"]
READ_DB_CA_CERT_BASE64 = os.environ["READ_DB_CA_CERT_BASE64"]
READ_DB_MIN_POOL_SIZE = int(os.environ["READ_DB_MIN_POOL_SIZE"])
READ_DB_MAX_POOL_SIZE = int(os.environ["READ_DB_MAX_POOL_SIZE"])
READ_DB_USE_SSL = read_bool(os.environ["READ_DB_USE_SSL"])

WRITE_DB_SCHEME = os.environ["WRITE_DB_SCHEME"]
WRITE_DB_HOST = os.environ["WRITE_DB_HOST"]
WRITE_DB_PORT = int(os.environ["WRITE_DB_PORT"])
WRITE_DB_USER = os.environ["WRITE_DB_USER"]
WRITE_DB_PASS = os.environ["WRITE_DB_PASS"]
WRITE_DB_NAME = os.environ["WRITE_DB_NAME"]
WRITE_DB_CA_CERT_BASE64 = os.environ["WRITE_DB_CA_CERT_BASE64"]
WRITE_DB_MIN_POOL_SIZE = int(os.environ["WRITE_DB_MIN_POOL_SIZE"])
WRITE_DB_MAX_POOL_SIZE = int(os.environ["WRITE_DB_MAX_POOL_SIZE"])
WRITE_DB_USE_SSL = read_bool(os.environ["WRITE_DB_USE_SSL"])

# redis
REDIS_SCHEME = os.environ["REDIS_SCHEME"]
REDIS_USER = os.environ["REDIS_USER"]
REDIS_PASS = os.environ["REDIS_PASS"]
REDIS_HOST = os.environ["REDIS_HOST"]
REDIS_PORT = int(os.environ["REDIS_PORT"])
REDIS_DB = int(os.environ["REDIS_DB"])
