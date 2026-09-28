# AzNews-XLM

Azerbaijani news topic classifier built on fine-tuned XLM-RoBERTa

## Status

Working: collector for apa.az football
To be done: other topics, train/test split, TF-IDF, XLM-RoBERTa, GPT-4o-mini

## Task

Classify each article from Azerbaijani news into one of five topics:
```
sports, politics, economy, culture, world
```

## Why

Despite serious AI progress in last years, there is still not enough work done on low-resource languages like Azerbaijani. The aim of this project is to find out whether a small encoder beats an API LLM on topic classification, and at what latency and cost.

## Comparison

All three systems are evaluated on the same test set:
- TF-IDF + logistic regression (baseline)
- XLM-RoBERTa, fine-tuned on this dataset
- GPT-4o-mini

Metrics: accuracy, macro-F1, latency, and cost per 1k articles.

## Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```