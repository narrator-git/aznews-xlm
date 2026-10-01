import json
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

LABELS = ["sports", "politics", "economy", "culture", "world"]

def extract(path):
    rows = []
    with Path(path).open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line: rows.append(json.loads(line))
    return [i["text"] for i in rows], [i["label"] for i in rows]

x_train, y_train = extract("data/splits/train.jsonl")
x_val, y_val = extract("data/splits/val.jsonl")
x_test, y_test = extract("data/splits/test.jsonl")

vectorizer = TfidfVectorizer()
x_train = vectorizer.fit_transform(x_train)
x_val = vectorizer.transform(x_val)
x_test = vectorizer.transform(x_test)

clf = LogisticRegression(max_iter=1000)
clf.fit(x_train, y_train)

def predict(x, y):
    pred = clf.predict(x)
    print(classification_report(y, pred, labels=LABELS, digits=3))

print("Validation accuracy")
predict(x_val, y_val)
print("Test accuracy")
predict(x_test, y_test)