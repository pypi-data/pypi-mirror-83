#!/usr/bin/env python

MONGO_CONN_STR = "mongodb+srv://..."

ADMIN_COLLECTION = "info" # collection containing credentials and function parameters

ADMIN_DATABASES = ["admin", "local"] # databases to ignore when fetching customers

OS = 'UBUNTU'
# OS = 'MAC'

SAVE_LOGS = False

LOG_DIR = "logs/"

MAX_LOG_SIZE = 100000000 # 100Mb