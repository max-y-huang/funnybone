import sqlite3
import json

_INPUT_SRC = "../output.json"
_OUTPUT_SRC = "../output.db"

_ASPECT_KEYS = ["overall", "snd", "scatc", "clq", "inslt", "juxt", "sexc"]


if __name__ == "__main__":
    conn = sqlite3.connect(_OUTPUT_SRC)
    c = conn.cursor()

    score_columns = [key + "_score REAL" for key in _ASPECT_KEYS]
    c.execute(
        f'CREATE TABLE IF NOT EXISTS terms (term TEXT, {", ".join(score_columns)})'
    )
    c.execute("CREATE INDEX IF NOT EXISTS index1 ON terms (term)")
    c.execute("DELETE FROM terms")

    with open(_INPUT_SRC, "r") as f:
        data = json.load(f)
        for key, val in data.items():
            row = [key] + [val[k] for k in _ASPECT_KEYS]
            c.execute("INSERT INTO terms VALUES (?, ?, ?, ?, ?, ?, ?, ?)", row)

    conn.commit()
    conn.close()
