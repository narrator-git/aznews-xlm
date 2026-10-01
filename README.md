# AzNews-XLM

Azerbaijani news topic classifier built on fine-tuned XLM-RoBERTa

## Status

Working: collector, frozen split, TF-IDF baseline (test accuracy 0.944, macro-F1 0.942)

To be done: XLM-RoBERTa, GPT-4o-mini

## Task

Classify each article from Azerbaijani news into one of five topics:
```
sports, politics, economy, culture, world
```

## Why

Despite serious AI progress in last years, there is still not enough work done on low-resource languages like Azerbaijani. The aim of this project is to find out whether a small encoder beats an API LLM on topic classification, and at what latency and cost.

## Comparison

All three systems are evaluated on the same test set (54 articles):

| System | accuracy | macro-F1 | latency | cost / 1k docs |
|---|---|---|---|---|
| TF-IDF + logistic regression | 0.944 | 0.942 | TBD | 0 |
| XLM-RoBERTa, fine-tuned | TBD | TBD | TBD | 0 |
| GPT-4o-mini, few-shot via the API | TBD | TBD | TBD | TBD |

## Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```