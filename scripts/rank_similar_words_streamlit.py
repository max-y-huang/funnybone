import streamlit as st
import os

_CSS_SRC = "styles/rank_similar_words_streamlit.css"
_COMPONENT_KEYS = ["snd", "scatc", "clq", "inslt", "juxt", "sexc"]


def format_to_li(word, is_error=False):
    return f'<li style="color: {"#f00" if is_error else "#000"}">{word}</li>'


def format_words_to_html(words):
    ranked = list(map(lambda w: format_to_li(w), words["rankings"]))
    unranked = list(map(lambda w: format_to_li(w, True), words["unranked"]))
    return "\n".join(ranked + unranked)


def app():
    st.title("Rank similar terms")

    term = st.text_input("Term to rank").lower()
    aspect = st.selectbox("Sort aspect", ["overall"] + _COMPONENT_KEYS)

    if term and aspect:
        script = (
            f'python3 scripts/rank_similar_words.py --term "{term}" --aspect "{aspect}"'
        )
        words = eval(os.popen(script).read().strip())
        fs_out = open("out.html", "w")
        if not words["rankings"]:
            st.text("Sorry, we don't have data for that word")
        else:
            html = f"""
                <style>
                    {open(_CSS_SRC).read()}
                </style>
                <div class="container">
                    <ol>{format_words_to_html(words)}</ol>
                </div>
            """
            print(html, file=fs_out)
            st.components.v1.html(html, height=400)


if __name__ == "__main__":
    app()
