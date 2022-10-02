import sqlite3
import requests
import json
import streamlit as st


_DB_SRC = "output.db"
_CSS_SRC = "styles/rank_similar_terms.css"
_ASPECT_KEYS = ["overall", "snd", "scatc", "clq", "inslt", "juxt", "sexc"]


def format_words_to_html(ranked_terms, unranked_terms):
    ranked = list(map(lambda t: f"<li>{t}</li>", ranked_terms))
    unranked = list(map(lambda t: f'<li style="color: #f00">{t}</li>', unranked_terms))
    return "\n".join(ranked + unranked)


def get_rankings(db, term, aspect):
    response_API = requests.get(f"https://api.datamuse.com/words?ml={term}")
    similar_terms = [item["word"].lower() for item in json.loads(response_API.text)]

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


if __name__ == "__main__":

    db = sqlite3.connect(_DB_SRC)
    st.title("Rank similar terms")

    term = st.text_input("Term to rank")
    aspect = st.selectbox("Sort aspect", _ASPECT_KEYS)

    if term and aspect:
        ranked_terms, unranked_terms = get_rankings(db, term, aspect)
        fs_out = open("out.html", "w")
        if not ranked_terms:
            st.text("Sorry, we don't have data for that word")
        else:
            html = f"""
                <style>
                    {open(_CSS_SRC).read()}
                </style>
                <div class="container">
                    <ol>{format_words_to_html(ranked_terms, unranked_terms)}</ol>
                </div>
            """
            print(html, file=fs_out)
            st.components.v1.html(html, height=400)
