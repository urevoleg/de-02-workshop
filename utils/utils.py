import os
import re
import json
import datetime as dt
from dateutil.parser import parse
from pprint import pprint

import wget

from functools import wraps

import logging
from logging import StreamHandler

from typing import List, Dict, Optional, Tuple
from urllib.parse import quote_plus as quote

import psycopg2
from psycopg2.extras import NamedTupleCursor

from airflow.hooks.base import BaseHook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.models.variable import Variable


def debug(func):
    @wraps(func)
    def wrapper_debug(*args, **kwargs):
        logger = get_logger(logger_name="debug")
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        logger.debug(f"Calling {func.__name__}({signature})")
        value = func(*args, **kwargs)
        logger.debug(f"{func.__name__!r} returned {value!r}")
        return value
    return wrapper_debug


def get_logger(logger_name="super_logger", handler=StreamHandler()):
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    super_logger = logging.getLogger(logger_name)
    super_logger.setLevel(logging.DEBUG)
    handler = handler

    handler.setFormatter(fmt=formatter)
    super_logger.addHandler(handler)
    return super_logger


class Config(object):
    STAGE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")
    BUSINESS_DT = '{{ ds }}'  # по-умолчанию, строка

    if re.match(BUSINESS_DT, "\d\d\d\d-\d\d-\d\d"):
        BUSINESS_DT = dt.datetime.strptime(BUSINESS_DT, "%Y-%m-%d")

    if not re.match(BUSINESS_DT, "\d\d\d\d-\d\d-\d\d"):
        BUSINESS_DT = dt.datetime.now().date()

    PG_WAREHOUSE_CONNECTION_CONN_ID = "pg_hackaton_con"
    PG_WAREHOUSE_CONNECTION = PostgresHook(PG_WAREHOUSE_CONNECTION_CONN_ID).get_uri()

    EVENTS_JSON_URL = "https://data.ijklmn.xyz/events/"


class SQLDdlScripts():
    CREATE_SCHEMAS = "migrations/create_schemas.sql"

    CREATE_CDM_DM_SETTLEMENT_REPORT = "migrations/cdm/dm_settlement_report.sql"


class FileEvent():
    def execute(self):
        """
        1. Upload ZIP
        2. Unzip json
        """
        pass

    def _get_file_attributes(self):
        file_date = dt.datetime.now() - dt.timedelta(days=1)
        file_name = f"events-{file_date.strftime('%Y')}-{file_date.strftime('%b')}-{file_date.strftime('%d')}-2134.json.zip"
        file_path = os.path.join(Config.STAGE_DIR, file_name)
        file_url = Config.EVENTS_JSON_URL + file_name
        return {
            "file_name": file_name,
            "file_path": file_path,
            "file_url": file_url
        }

    @staticmethod
    def get_file_url():
        return FileEvent()._get_file_attributes().get("file_url")

    def _is_file_exist(self):
        return 1 if os.path.exists(FileEvent.get_file_url().get("file_path")) else 0

    @staticmethod
    def is_file_exist():
        return FileEvent()._is_file_exist()


if __name__ == '__main__':
    print(FileEvent.get_file_url())
