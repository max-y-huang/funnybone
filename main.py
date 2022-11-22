import sqlite3
import requests
import json
from flask import Flask, request, render_template

_DB_SRC = "output.db"
_ASPECT_KEYS = ["overall", "snd", "scatc", "clq", "inslt", "juxt", "sexc"]


app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    # get query
    args = request.args
    query = args.get("q", None)
    if not query or query.strip() == "":
        query = None

    # get funniest and unfunniest matches
    db = sqlite3.connect(_DB_SRC)
    ranked_terms, _ = get_rankings(db, query)
    ranked_terms = list(map(lambda x: x.replace("_", " "), ranked_terms))
    funniest = ranked_terms[:3]
    unfunniest = ranked_terms[-1:]

    # get error state
    error = query == None or len(ranked_terms) == 0

    return render_template(
        "index.html",
        query=query,
        funniest=funniest,
        unfunniest=unfunniest,
        error=error,
    )


def get_rankings(db, term, aspect="overall"):
    if not term:
        return ([], [])  # throws error

    response_API = requests.get(f"https://api.datamuse.com/words?ml={term}")
    similar_terms = [
        item["word"].lower().replace(" ", "_") for item in json.loads(response_API.text)
    ]

    filter_words = get_filter_words()
    similar_terms = list(filter(lambda t: not t in filter_words, similar_terms))
    if term.lower().replace(" ", "_") in filter_words:
        return ([], [])  # throws error

    c = db.cursor()
    c.execute(
        f'SELECT * FROM terms WHERE term IN ({", ".join("?" * len(similar_terms))})',
        similar_terms,
    )

    ratings = {
        item[0]: {key: item[i] for i, key in enumerate(_ASPECT_KEYS, start=1)}
        for item in c.fetchall()
    }

    unranked_terms = list(filter(lambda t: not (t in ratings), similar_terms))
    ranked_terms = list(filter(lambda t: t in ratings, similar_terms))
    ranked_terms = sorted(ranked_terms, key=lambda t: ratings[t][aspect], reverse=True)
    return (ranked_terms, unranked_terms)


def get_filter_words():
    with open("filter_words.txt") as f:
        return f.read().strip().split("\n")


if __name__ == "__main__":
    app.run()
