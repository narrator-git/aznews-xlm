import json
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from sklearn.metrics import classification_report

load_dotenv()
client = OpenAI()
LABELS = ["sports", "politics", "economy", "culture", "world"]
INPUT_USD_PER_M = 0.15
OUTPUT_USD_PER_M = 0.60

def load_jsonl(path):
    rows = []
    with Path(path).open(encoding="utf-8") as f:
        for line in f:
            line=line.strip()
            if line: rows.append(json.loads(line))
    return rows

def fewshot_examples(train):
    picked = {}
    for row in train:
        lab = row["label"]
        if lab not in picked: picked[lab] = row
        if len(picked) == 5: break
    return [picked[lab] for lab in LABELS if lab in picked]

def parse_label(text):
    token = (text or "").strip().lower().replace(".", "")
    token = token.split()[0] if token else ""
    return token if token in LABELS else None

train = load_jsonl("data/splits/train.jsonl")
test = load_jsonl("data/splits/test.jsonl")
shots = fewshot_examples(train)

shot_block = "\n".join(f"text: {row['text'][:400]}\nlabel: {row['label']}" for row in shots)
system = ("You classify Azerbaijani news. Reply with exactly one label: sports, politics, economy, culture, world. No other words.")

y_true = []
y_pred = []
for i, row in enumerate(test, start=1):
    user = (
        "Examples:\n"
        f"{shot_block}\n\n"
        "Now classify this article:\n"
        f"{row['text'][:1500]}"
    )
    r = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ]
    )
    raw = r.choices[0].message.content
    pred = parse_label(raw)
    if pred is None:
        pred = "world"
        print("unparsed", i, raw)
    y_true.append(row["label"])
    y_pred.append(pred)
    print(i, row["label"], "->", pred)

print(classification_report(y_true, y_pred, labels=LABELS, digits=3))