# Data

354 Azerbaijani news articles from apa.az (five topics, three list pages each)

Frozen split: `data/splits/train.jsonl`, `val.jsonl`, `test.jsonl`

## Task
Classify each Azerbaijani news article as one of: `{sports, politics, economy, culture, world}`

## Sources
Collected:
- https://apa.az

Planned:
- https://report.az
- https://oxu.az

## What one row looks like
- url
- title
- text
- date
- source (which site)
- label (one of the five topics)

## Split
Split by **article**
`random.seed(100)`, shuffle inside each label, then split 70% / 15% / 15%:
| split | rows |
|---|---|
| train | 246 |
| val | 54 |
| test | 54 |