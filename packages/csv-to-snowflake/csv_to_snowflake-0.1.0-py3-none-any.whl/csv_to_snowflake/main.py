import argparse
import csv
import logging
import ntpath
from pathlib import Path

import snowflake.connector

log_levels = {
    'critical': logging.CRITICAL,
    'error': logging.ERROR,
    'warn': logging.WARNING,
    'warning': logging.WARNING,
    'info': logging.INFO,
    'debug': logging.DEBUG
}
logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def run():
    parser = argparse.ArgumentParser(
        description='Creates Snowflake table from CSV file.')
    parser.add_argument('--log-level', default="warning", help='Snowflake user')
    parser.add_argument(
        '--account', required=True,
        help='Snowflake account. For example, mf00000.eu-central-1')
    parser.add_argument('--user', required=True, help='Snowflake user')
    parser.add_argument('--role', required=True, help='Snowflake role')
    parser.add_argument('--db', required=True, help='Snowflake database')
    parser.add_argument('--schema', required=True, help='Snowflake schema')
    parser.add_argument('--table', required=True, help='Snowflake table')
    parser.add_argument('csv_file', type=str, help='Path to CSV file')

    args = parser.parse_args()

    cur_log_level = log_levels.get(args.log_level)
    print("setting log level", cur_log_level)
    logger.setLevel(cur_log_level)

    with open(args.csv_file) as csv_file:
        reader = csv.DictReader(csv_file)
        columns = reader.fieldnames

        ctx = snowflake.connector.connect(
            user=args.user,
            role=args.role,
            authenticator='externalbrowser',
            account=args.account
        )
        ctx.autocommit(True)
        cs = ctx.cursor()

        csv_abs_path = Path(args.csv_file).resolve()

        try:
            sql_use_schema = f"USE SCHEMA {args.db}.{args.schema}"
            logger.debug(sql_use_schema)
            cs.execute(sql_use_schema)

            column_defs = [f"{x} text" for x in columns]
            sql_create_table = f"CREATE TABLE IF NOT EXISTS {args.table}({', '.join(column_defs)})"
            logger.debug(sql_create_table)
            cs.execute(sql_create_table)

            stage = f"@%{args.table}"

            sql_put = f"PUT file://{csv_abs_path}* {stage}"
            logger.debug(sql_put)
            cs.execute(sql_put)

            if args.log_level == "debug":
                sql_list = f"LIST {stage}"
                logger.debug(sql_list)
                res = cs.execute(sql_list).fetchall()
                for r in res:
                    logger.debug(r)

            csv_filename = ntpath.basename(csv_abs_path)
            sql_copy = f"""COPY INTO {args.table} FROM '{stage}'
            FILES = ('{csv_filename}.gz')
            FILE_FORMAT = (TYPE=CSV, COMPRESSION=GZIP);"""
            logger.debug(sql_copy)
            cs.execute(sql_copy)

            sql_remove = f"REMOVE {stage}"
            logger.debug(sql_remove)
            cs.execute(sql_remove)

            logger.info("done")
        except Exception as err:
            logger.error("Failed to upload CSV:", err)
        finally:
            cs.close()
