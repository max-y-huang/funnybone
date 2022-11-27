import os
import sqlalchemy


def get_conn(connector):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "../config/gcp_credentials.json"
    conn = connector.connect(
        "funnybone-369322:us-east1:humour-rankings",
        "pg8000",
        user="postgres",
        password='A^E@%"d>iT2s2g+g',
        db="postgres",
    )
    return conn


def get_pool(connector):
    pool = sqlalchemy.create_engine(
        "postgresql+pg8000://",
        creator=lambda: get_conn(connector),
    )
    return pool
