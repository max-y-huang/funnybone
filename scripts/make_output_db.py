from google.cloud.sql.connector import Connector
from sql import get_pool

if __name__ == "__main__":
    connector = Connector()
    pool = get_pool(connector)
    with pool.connect() as c:
        c.execute("DROP TABLE IF EXISTS Terms;")
        c.execute(
            "CREATE TABLE IF NOT EXISTS Terms (term VARCHAR(255) NOT NULL, score FLOAT NOT NULL, PRIMARY KEY (term));"
        )
    connector.close()
