import time
import requests
import json
import pandas as pd
import os
import datetime as dt
from dateutil.relativedelta import relativedelta

from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator, ShortCircuitOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.sql import SQLCheckOperator
from airflow.operators.empty import EmptyOperator
from airflow.utils.trigger_rule import TriggerRule
from airflow.models import Variable
from airflow.providers.postgres.hooks.postgres import PostgresHook

import psycopg2

# для импортов из utils
import sys
sys.path.append(os.path.abspath(os.path.dirname(os.path.abspath(__file__))))

from utils.utils import Config
from utils.utils import get_logger
logger = get_logger(logger_name=f"{__file__[:-3]}")


def insert_values_to_db(list_of_values, pg_table, table_columns, conn_args):
    ''' load data to postgres '''
    cols = ','.join(list(table_columns))
    insert_stmt = f"INSERT INTO {pg_table} ({cols}) VALUES %s"

    uri = PostgresHook(conn_args).get_uri()
    with psycopg2.connect(uri) as conn:
        with conn.cursor() as cur:
            psycopg2.extras.execute_values(cur, insert_stmt, list_of_values)
            conn.commit()


def load_data_to_staging(date, pg_table, table_columns, conn_args):
    with open(os.path.join(Config.STAGE_DIR, f"transformed_rates_{date}.json")) as f:
        transformed_data = json.loads(f.read())

    insert_values_to_db(list_of_values=transformed_data, pg_table=pg_table, table_columns=table_columns, conn_args=conn_args)


args = {
    "owner": "urev",
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=1)
}


with DAG(
        dag_id='template_dag',
        default_args=args,
        catchup=False,
        start_date=dt.datetime.today() - dt.timedelta(days=8),
        end_date=dt.datetime.today() + dt.timedelta(days=1),
) as dag:

    is_table_created = SQLCheckOperator(
        task_id="is_table_created",
        conn_id=Config.LOCAL_DB_CONN_ID,
        sql="migrations/test.staging.table_is_created.sql",
        params={'table_name': 'table_name'}
    )

    load_data_to_staging = PythonOperator(
        task_id='load_data_to_staging',
        python_callable=load_data_to_staging,
        op_kwargs={
            'date': Config.BUSINESS_DT,
            "pg_table": 'staging.daily_rates',
            "table_columns": ['date', 'rub_to_usd', 'eur_to_usd'],
            "conn_args": Config.LOCAL_DB_CONN_ID
        }
    )

    is_table_created >> get_last_date


if __name__ == '__main__':
    pass

