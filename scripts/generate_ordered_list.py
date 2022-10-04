import argparse
import sqlite3


_DB_SRC = "output.db"
_ASPECT_KEYS = ["overall", "snd", "scatc", "clq", "inslt", "juxt", "sexc"]


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--aspect",
        help=f'Which aspect to sort by. Can take the values: {", ".join(_ASPECT_KEYS)}',
        default="overall",
    )
    parser.add_argument(
        "--output_file",
        help="The output file for the list.",
        default="overall.words",
    )
    args = parser.parse_args()

    if args.aspect in _ASPECT_KEYS:
        db = sqlite3.connect(_DB_SRC)
        c = db.cursor()
        c.execute(
            f'SELECT term FROM terms ORDER BY {args.aspect + "_score"} DESC'
        )  # ? binding doesn't work

        ranked_terms = [item[0] for item in c.fetchall()]
        with open(args.output_file, "w") as f:
            print("\n".join(ranked_terms), file=f)
