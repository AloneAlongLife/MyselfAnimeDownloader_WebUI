from modules import Json
from os.path import isfile
from datetime import timedelta, timezone, time
from logging import getLevelName
from typing import Union

# CRITICAL
# ERROR
# WARNING
# INFO
# DEBUG
# NOTSET

class LoggingConfig:
    STREAM_LEVEL: int = 20
    FILE_LEVEL: int = 20
    BACKUP_COUNT: int
    FILE_NAME: str
    DIR_PATH: str
    def __init__(self, data: dict) -> None:
        if type(getLevelName(data["stream_level"])) == int:
            self.STREAM_LEVEL = data["stream_level"]
        if type(getLevelName(data["file_level"])) == int:
            self.FILE_LEVEL = data["file_level"]
        self.BACKUP_COUNT = abs(data["backup_count"])
        self.FILE_NAME = data["file_name"]
        self.DIR_PATH = data["dir_path"]

CONFIG = {
    "web": {
        "host": "0.0.0.0",
        "port": 5000,
        "debug": True,
    },
    "global": {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 OPR/92.0.0.0 (Edition GX-CN)",
        "connections": 10,
        "threads": 3,
        "retry": 3,
        "zerofill": 2
    },
    "myself": {
        "check_update": 5,
        "classify": True,
        "file_name": "[Myself]$NAME $NOTE $NUM集",
        "dir_name": "[Myself]$NAME",
        "download_path": "download/myself"
    },
    "sql": {
        "mysql": False, # 未提供支援
        "host": "",
        "port": 0,
        "user": "",
        "password": "",
        "database": "data"
    },
    "logging": {
        "main": {
            "stream_level": "INFO",
            "file_level": "INFO",
            "backup_count": 3,
            "file_name": "main",
            "dir_path": "logs",
        },
        "web": {
            "stream_level": "INFO",
            "file_level": "INFO",
            "backup_count": 3,
            "file_name": "web",
            "dir_path": "logs",
        },
    },
    "timezone": 8,
    "ffmpeg_args": "",
}

try:
    RAW_CONFIG: dict[str, Union[dict, str, int]] = Json.load("config.json")
    for key, value in RAW_CONFIG.items():
        if type(value) == dict:
            for s_key, s_value in value.items():
                CONFIG[key][s_key] = s_value
        else:
            CONFIG[key] = value
except: pass
finally:
    Json.dump("config.json", CONFIG)

WEB_HOST: str = CONFIG["web"]["host"]
WEB_PORT: int = CONFIG["web"]["port"]
WEB_DEBUG: bool = CONFIG["web"]["debug"]

UA: str = CONFIG["global"]["user-agent"]
CONS: int = CONFIG["global"]["connections"]
THRS: int = CONFIG["global"]["threads"]
RETRY: int = CONFIG["global"]["retry"]
ZFILL: int = CONFIG["global"]["zerofill"]

MYSELF_UPDATE: int = CONFIG["myself"]["check_update"]
MYSELF_CLASSIFY: bool = CONFIG["myself"]["classify"]
MYSELF_FILE: str = CONFIG["myself"]["file_name"]
MYSELF_DIR: str = CONFIG["myself"]["dir_name"]
MYSELF_DOWNLOAD: str = CONFIG["myself"]["download_path"]

SQL_MYSQL: bool = CONFIG["sql"]["mysql"]
SQL_CONFIG: dict = {}
if SQL_MYSQL:
    SQL_CONFIG = {
        "host": CONFIG["sql"]["host"],
        "port": CONFIG["sql"]["port"],
        "user": CONFIG["sql"]["user"],
        "password": CONFIG["sql"]["password"],
        "database": CONFIG["sql"]["database"],
        "charset": "utf-8"
    }
else:
    SQL_CONFIG = {
        "database": f"{CONFIG['sql']['database']}.db",
    }
    from sqlite3 import connect
    if not isfile("data.db"):
        db = connect(**SQL_CONFIG)
        cursor = db.cursor()
        cursor.execute("""
            CREATE TABLE "Users" (
                "discord_id" INTEGER NOT NULL UNIQUE,
                "account" TEXT NOT NULL UNIQUE,
                "password" TEXT NOT NULL,
                "token"	TEXT UNIQUE,
                PRIMARY KEY("discord_id")
            );
        """)
        db.commit()
        cursor.close()
        db.close()

LOGGING_CONFIG: dict[str, LoggingConfig] = {
    "main": LoggingConfig(CONFIG["logging"]["main"]),
    "web": LoggingConfig(CONFIG["logging"]["web"]),
}

TIMEZONE: timezone = timezone(timedelta(hours=CONFIG["timezone"]))
FFMPEG_ARGS: str = CONFIG["ffmpeg_args"]
        