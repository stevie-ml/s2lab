"""Run analysis only on new poems not yet in corpus_results.json."""
import sys
import json
import os

sys.path.insert(0, '/home/user/s2lab')

from engine import analyze_poem, get_model
from corpus.poems import POEMS

RESULTS_FILE = os.path.join(os.path.dirname(__file__), "results", "corpus_results.json")

with open(RESULTS_FILE) as f:
    existing = json.load(f)

# Build a set of already-analyzed (author, title) pairs
analyzed = {(e["metadata"]["author"], e["metadata"]["title"]) for e in existing}

new_poems = [
    p for p in POEMS
    if (p["author"], p["title"]) not in analyzed
]

print(f"Corpus: {len(POEMS)} poems total, {len(existing)} already analyzed, {len(new_poems)} new")

if not new_poems:
    print("Nothing to do.")
    sys.exit(0)

new_results = []
for i, poem in enumerate(new_poems):
    lang = poem.get("language", "en")
    print(f"  [{i+1}/{len(new_poems)}] [{lang}] {poem['author']} — {poem['title']}")
    result = analyze_poem(
        text=poem["text"],
        title=poem["title"],
        author=poem["author"],
        year=poem.get("year"),
        era=poem.get("era", ""),
        language=lang,
    )
    new_results.append(result)

all_results = existing + new_results
with open(RESULTS_FILE, "w") as f:
    json.dump(all_results, f, indent=2, default=str)
print(f"Saved {len(all_results)} results ({len(new_results)} new) to {RESULTS_FILE}")
