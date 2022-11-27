import os
import json
import sqlalchemy

__dir__ = os.path.dirname(os.path.realpath(__file__))


def get_conn(connector):
    with open(f"{__dir__}/../config/db_credentials.json") as f:
        cred = json.load(f)

    conn = connector.connect(
        cred["connection_name"],
        cred["db_driver"],
        user=cred["user"],
        password=cred["password"],
        db=cred["db"],
    )
    return conn


def get_pool(connector):
    pool = sqlalchemy.create_engine(
        "postgresql+pg8000://",
        creator=lambda: get_conn(connector),
    )
    return pool
