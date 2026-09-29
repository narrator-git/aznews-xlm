import json, random
from collections import defaultdict, Counter
from pathlib import Path

random.seed(100)

raw_path = Path("data/raw/apa.jsonl")
out_dir = Path("data/splits")
out_dir.mkdir(parents=True, exist_ok=True)
rows = []
seen_urls = set()

with raw_path.open(encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line: continue
        row = json.loads(line)
        url = row.get("url")
        text = (row.get("text") or "").strip()
        if url in seen_urls or len(text) < 50: continue
        seen_urls.add(url)
        row["text"] = text
        rows.append(row)

print("kept", len(rows))
categorize_by_label = defaultdict(list)
for row in rows:
    categorize_by_label[row["label"]].append(row)

train, val, test = [], [], []
for label, group in categorize_by_label.items():
    random.shuffle(group)
    n=len(group)
    n_test=max(1, round(n * 0.15))
    n_val=max(1, round(n * 0.15))
    n_train = n-n_test-n_val
    train.extend(group[:n_train])
    val.extend(group[n_train:n_train + n_val])
    test.extend(group[n_train + n_val:])

def write_jsonl(path, items):
    with path.open("w", encoding="utf-8") as f:
        for row in items: f.write(json.dumps(row, ensure_ascii=False) + "\n")
write_jsonl(out_dir/"train.jsonl", train)
write_jsonl(out_dir/"val.jsonl", val)
write_jsonl(out_dir/"test.jsonl", test)