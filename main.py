import sqlite3
import requests
import json
import urllib.parse
from flask import Flask, request, render_template
from google.cloud.sql.connector import Connector
from scripts.sql import get_pool

from pymongo import MongoClient


_DB_SRC = "output.db"


app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    # get query
    args = request.args
    query = args.get("q", None)
    if not query or query.strip() == "":
        query = None
    encoded_query = None if not query else urllib.parse.quote(query)

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
        encoded_query=encoded_query,
        funniest=funniest,
        unfunniest=unfunniest,
        error=error,
    )


@app.route("/about", methods=["GET"])
def about():
    return render_template("about.html")


@app.route("/how-it-works", methods=["GET"])
def how_it_works():
    return render_template("how_it_works.html")


def get_rankings(db, term):
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

    client = MongoClient(
        "mongodb+srv://dbUser:XW3e3DEkplfqhBYy@cluster0.rnwa7.mongodb.net/?retryWrites=true&w=majority"
    )
    ratings = {
        item["term"]: item["score"]
        for item in client.funnybone.terms.find({"term": {"$in": similar_terms}})
    }

    # connector = Connector()
    # pool = get_pool(connector)
    # with pool.connect() as c:
    #     c.execute(f'SELECT * FROM Terms WHERE term IN ({", ".join(similar_terms)});')
    # connector.close()

    # ratings = {key: val for key, val in c.fetchall()}

    unranked_terms = list(filter(lambda t: not (t in ratings), similar_terms))
    ranked_terms = list(filter(lambda t: t in ratings, similar_terms))
    ranked_terms = sorted(ranked_terms, key=lambda t: ratings[t], reverse=True)
    return (ranked_terms, unranked_terms)


def get_filter_words():
    with open("filter_words.txt") as f:
        return f.read().strip().split("\n")


if __name__ == "__main__":
    app.run()
