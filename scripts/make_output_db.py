import sqlite3
import json


_ASPECT_KEYS = ["overall", "snd", "scatc", "clq", "inslt", "juxt", "sexc"]


if __name__ == "__main__":
    conn = sqlite3.connect("output.db")
    c = conn.cursor()

    score_columns = [key + "_score REAL" for key in _ASPECT_KEYS]
    c.execute(
        f'CREATE TABLE IF NOT EXISTS terms (term TEXT, {", ".join(score_columns)})'
    )
    c.execute("CREATE INDEX IF NOT EXISTS index1 ON terms (term)")
    c.execute("DELETE FROM terms")
    with open("output.json", "r") as f:
        data = json.load(f)
        for key, val in data.items():
            row = [key] + [val[k] for k in _ASPECT_KEYS]
            c.execute("INSERT INTO terms VALUES (?, ?, ?, ?, ?, ?, ?, ?)", row)
    conn.commit()
    conn.close()
