# Humour Rating

Finds the humour scores of various words (both overall and the 6 subcategories).

## Instructions

Download the data sources and place them under `data/`.
Run `main.ipynb` as deescribed in that file.

### Data Sources

- Word vectors: `wiki-news-300d-1M-subword.vec.zip` from https://fasttext.cc/docs/en/english-vectors.html
- Cockamamie Gobbledegook data: https://github.com/limorigu/Cockamamie-Gobbledegook/blob/master/data/cockamamie_gobbledegook_us_data.json
- EH data: https://github.com/tomasengelthaler/HumorNorms/blob/master/humor_dataset.csv
- Sample words (Datamuse): https://drive.google.com/file/d/1qKyssIf0b8xoifxujPoU8TExWY8bH2jx/view?usp=sharing

## Scripts (Must Run From `/`)

- `python3 scripts/make_output_db.py`
  - Creates `output.db`.
  - Requires `output.json`.
- `python3 scripts/generate_ordered_list.py --aspect <ASPECT> --output_file <OUTPUT_FILE>`
  - Outputs a list ordered by `<ASPECT>` (descending) to `<OUTPUT_FILE>`.
  - Requires `output.db`.
- `streamlit run scripts/rank_similar_terms.py`
  - A streamlit app that retrieves similar terms and ranks them by an aspect of humour (descending).
  - Requires `output.db`
