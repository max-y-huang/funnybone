#!/usr/bin/env python3

_COCKAMAMIE_DATA_SRC = "data/cockamamie_gobbledegook_us_data.json"
_DATAMUSE_DATA_SRC = "data/ol_gte2.2022-09-26.words"
_EH_DATA_SRC = "data/humor_dataset.csv"

_VEC_SRC = "data/crawl-300d-2M-subword.bin"  # FastText subword model
_PKL_SRC = "data/crawl-300d-2M-subword.pkl"

_OUTPUT_SRC = "output.json"

_COMPONENT_KEYS = ["snd", "scatc", "clq", "inslt", "juxt", "sexc"]


import json
import numpy as np
import pickle as pkl

from collections import defaultdict
from sklearn.linear_model import LinearRegression
import fasttext


"""
Predict the humour score of all words.
Outputs (word, humour score) pairs (.json) and ordered list (by humour) (.txt).
"""


def append_predictions_to_output_data(acc, output_key, training_data):
    """
    ``acc``: The "running sum" of all data given by append_to_output_data (similar to the accumulator in tail recursion).
    ``output_key``: the key in ``acc`` to store the predictions made (for this call).
    ``training_data``: The data used to fit the linear regression model.
    """
    with open(_PKL_SRC, "rb") as f:
        E = pkl.load(f)

    clr = LinearRegression()
    clr.fit([E[w] for w in training_data], [training_data[w] for w in training_data])
    predictions = {
        w: float(v)
        for (w, v) in zip(testing_words, clr.predict([E[w] for w in testing_words]))
    }
    humour_order = [
        w for w in sorted(testing_words, key=lambda x: predictions[x], reverse=True)
    ]

    for word, score in predictions.items():
        acc[word][output_key] = score

    return acc


def export_output_data(data):
    with open(_OUTPUT_SRC, "w") as f:
        print(json.dumps(data), file=f)


def vec_file2dict(vec_filename, pkl_filename):

    model = fasttext.load_model(vec_filename)

    def get_word(w):
        try:
            v = model[w.replace("_", " ")]
            return v / np.linalg.norm(v)  # normalize v
        except:
            return 0.0 * model["cat"]

    e_dict = {w: get_word(w) for w in testing_words}
    with open(pkl_filename, "wb") as f:
        pkl.dump(e_dict, f)

    non_zero_vectors = [v for v in e_dict.values() if not np.allclose(v, 0)]
    print(
        f'Loaded "{vec_filename}" and wrote {len(non_zero_vectors):,} non-zero vectors to "{pkl_filename}"'
    )


if __name__ == "__main__":

    """
    Load sample_words from Datamuse data.
    """

    with open(_DATAMUSE_DATA_SRC, "r") as f:
        sample_words = f.read().splitlines()

    """
    Load training data for overall score from the EH dataset.
    """

    with open(_EH_DATA_SRC, "r") as f:
        cells = [line.strip().split(",") for line in f.readlines()]
        headings = cells[0][1:]
        entries = {
            row[0]: {feat: float(v) for v, feat in zip(row[1:], headings)}
            for row in cells[1:]
        }
    overall_training_data = {w: entries[w]["mean"] for w in entries}

    """
    Load training data for component scores from the Cockamamie Gobbledegook dataset.
    """
    with open(_COCKAMAMIE_DATA_SRC, "r") as f:
        component_training_data = json.load(f)["word_features"]

    overall_training_words = list(overall_training_data)
    component_training_words = list(
        component_training_data["snd"]
    )  # contains the same words for all keys in component_training_data -> random key chosen

    testing_words = (
        overall_training_words + component_training_words + sample_words
    )  # combine all seen words
    testing_words = list(set(testing_words))  # remove duplicates

    vec_file2dict(_VEC_SRC, _PKL_SRC)
    output_data = defaultdict(lambda: dict())

    output_data = append_predictions_to_output_data(
        output_data, "overall", overall_training_data
    )
    for key in _COMPONENT_KEYS:
        output_data = append_predictions_to_output_data(
            output_data, key, component_training_data[key]
        )

    export_output_data(output_data)
