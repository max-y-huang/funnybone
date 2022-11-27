import json
import sqlalchemy
from google.cloud.sql.connector import Connector
from sql import get_pool

_INPUT_SRC = "../output.json"

if __name__ == "__main__":
    connector = Connector()
    pool = get_pool(connector)

    with pool.connect() as c:
        # create table
        c.execute("DROP TABLE IF EXISTS Terms;")
        c.execute(
            "CREATE TABLE IF NOT EXISTS Terms (term VARCHAR(255) NOT NULL, score FLOAT NOT NULL, PRIMARY KEY (term));"
        )
        # add data to table
        insert_stmt = sqlalchemy.text("INSERT INTO Terms VALUES (:term, :score);")
        with open(_INPUT_SRC, "r") as f:
            data = json.load(f)
            for key, val in data.items():
                c.execute(insert_stmt, term=key, score=val["overall"])

        # res = c.execute("SELECT * FROM Terms").fetchall()
        # for row in res:
        #     print(row)

    connector.close()
