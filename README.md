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

## Scripts

- `python3 scripts/rank_similar_words.py --term <TERM> --aspect <ASPECT>`
  - Retrieves words similar to `<TERM>` and ranks them by `<ASPECT>` (descending).
  - Requires `output.json`.
- `./scripts/generate_ordered_list.sh <ASPECT> <OUTPUT_FILE>`
  - Outputs a list ordered by `<ASPECT>` (descending) to `<OUTPUT_FILE>`.
  - Requires `output.json`.
