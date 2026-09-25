# AzNews-XLM

Azerbaijani news topic classifier built on fine-tuned XLM-RoBERTa

## Why

Despite serious AI progress in last years, there is still not enough work done on low-resource languages like Azerbaijani. The aim of this project is to find out whether a small encoder beats an API LLM on topic classification, and at what latency and cost.

## Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt