import time
import requests
import json
import pandas as pd
import os
import datetime as dt
from dateutil.relativedelta import relativedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator, ShortCircuitOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator

from airflow.operators.empty import EmptyOperator
from airflow.utils.trigger_rule import TriggerRule
from airflow.models import Variable
from airflow.providers.postgres.hooks.postgres import PostgresHook

import psycopg2

# для импортов из utils
import sys
sys.path.append(os.path.abspath(os.path.dirname(os.path.abspath(__file__))))

from utils.utils import Config, FileEvent
from utils.utils import get_logger
logger = get_logger(logger_name=f"{__file__[:-3]}")


args = {
    "owner": "urev",
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=1)
}


with DAG(
        dag_id='Super-Puper-DAG',
        default_args=args,
        catchup=False,
        start_date=dt.datetime.today() - dt.timedelta(days=8),
        end_date=dt.datetime.today() + dt.timedelta(days=1),
) as dag:

    begin = EmptyOperator(task_id="begin")
    end = EmptyOperator(task_id="end")

    upload_and_unzip_files = BashOperator(
        task_id="upload_and_unzip_files",
        bash_command=f"""wget -N {FileEvent.get_file_url()} -P {Config.STAGE_DIR} && unzip -o {FileEvent.get_file_attributes().get('zip_file_path')} -d {Config.STAGE_DIR} && rm {FileEvent.get_file_attributes().get('zip_file_path')}"""
    )

    check_event_files_exist = ShortCircuitOperator(
        task_id="check_event_files_exist",
        python_callable=FileEvent.is_file_exist,
    )

    begin >> upload_and_unzip_files >> check_event_files_exist >> end


if __name__ == '__main__':
    pass

