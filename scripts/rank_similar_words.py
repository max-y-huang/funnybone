"""
README: Run from ``humour-rating`` directory, NOT from ``humour-rating/tests``
"""

import argparse
import requests
import json


def sort_func(word, ratings):
    word = word.lower()
    if not word in ratings:
        return -1
    return ratings[word][args.aspect]


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--term",
        help="Rank the humour scores of the synonyms of this word.",
        default="poo",
    )
    parser.add_argument(
        "--aspect",
        help="Which aspect to sort by. Can take the values: overall, snd, scatc, clq, inslt, juxt, sexc",
        default="overall",
    )
    args = parser.parse_args()

    response_API = requests.get(f"https://api.datamuse.com/words?ml={args.term}")
    # print(response_API.status_code)

    words = [item["word"] for item in json.loads(response_API.text)]
    with open("output.json", "r") as f:
        ratings = json.load(f)
        sorted_words = sorted(
            words,
            key=lambda x: sort_func(x, ratings),
            reverse=True,
        )

    print(sorted_words)
