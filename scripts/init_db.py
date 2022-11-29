import sqlite3
import json

_INPUT_SRC = "../output.json"
_OUTPUT_SRC = "../output.db"

if __name__ == "__main__":
    conn = sqlite3.connect(_OUTPUT_SRC)
    c = conn.cursor()

    c.execute(f"CREATE TABLE IF NOT EXISTS Terms (term TEXT, score REAL)")
    c.execute("CREATE INDEX IF NOT EXISTS index1 ON Terms (term)")
    c.execute("DELETE FROM Terms")

    with open(_INPUT_SRC, "r") as f:
        data = json.load(f)
        for entry in data:
            c.execute(
                "INSERT INTO Terms VALUES (?, ?)", (entry["term"], entry["score"])
            )

    conn.commit()
    conn.close()
