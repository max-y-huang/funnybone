# Humour Rating

Finds the humour scores of various words (both overall and in the 6 subcategories).

## Instructions

1. Download the data sources and place them under `data/`.
2. Run `main.ipynb` as deescribed in the file to generate `output.json`.
3. (Optional) view the rankings as described in the [Scripts](#Scripts) section.

### Data Sources

- Word vectors: `wiki-news-300d-1M-subword.vec.zip` from https://fasttext.cc/docs/en/english-vectors.html
- Cockamamie Gobbledegook data: https://github.com/limorigu/Cockamamie-Gobbledegook/blob/master/data/cockamamie_gobbledegook_us_data.json
- EH data: https://github.com/tomasengelthaler/HumorNorms/blob/master/humor_dataset.csv
- Datamuse data: https://drive.google.com/file/d/1qKyssIf0b8xoifxujPoU8TExWY8bH2jx/view?usp=sharing

## Scripts

**IMPORTANT**: All scripts must be called from `humour-rating/`.

- `python3 scripts/make_output_db.py`
  - Creates `output.db`.
  - Requires `output.json`.
- `python3 scripts/generate_ordered_list.py --aspect <ASPECT> --output_file <OUTPUT_FILE>`
  - Outputs a list ordered by `<ASPECT>` (descending) to `<OUTPUT_FILE>`.
  - Requires `output.db`.
- `streamlit run scripts/rank_similar_terms.py`
  - A streamlit app that retrieves similar terms and ranks them by an aspect of humour (descending).
  - Requires `output.db`

## Known Problems

- Not all words from `scripts/rank_similar_terms.py` get rated.
  - Casing problem.
