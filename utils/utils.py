import os
import re
import datetime as dt
from pprint import pprint
import json

import logging
from logging import StreamHandler

#from airflow.hooks.base import BaseHook


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
    BUSINESS_DT = '{{ ds }}' #по-умолчанию, строка

    if re.match(BUSINESS_DT, "\d\d\d\d-\d\d-\d\d"):
        BUSINESS_DT = dt.datetime.strptime(BUSINESS_DT, "%Y-%m-%d")

    if not re.match(BUSINESS_DT, "\d\d\d\d-\d\d-\d\d"):
        BUSINESS_DT = dt.datetime.now().date()

    #TODO перенести в Airflow.Connections
    LOCAL_SQL_URI = "postgresql+psycopg2://user:12345@localhost/localdb"
    LOCAL_DB_CONN_ID = "pg_db_local"


if __name__ == '__main__':
    with open("/home/urev/projects/de-02-workshop/src/events-2022-Sep-30-2134.json") as f:
        json_data = json.loads(f.read())

    for idx, row in enumerate(json_data):
        pprint(row)
        if idx > 5:
            break
