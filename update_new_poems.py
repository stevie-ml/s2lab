"""Analyze only poems not yet in corpus_results.json and append them."""
import json
import sys
sys.path.insert(0, '/home/user/s2lab')

from engine import analyze_corpus, save_results, load_results
from corpus.poems import POEMS

existing = load_results("corpus_results.json")
analyzed_titles = {r["metadata"]["title"] for r in existing}

new_poems = [p for p in POEMS if p["title"] not in analyzed_titles]
print(f"Already analyzed: {len(existing)} poems")
print(f"New poems to analyze: {len(new_poems)}")
for p in new_poems:
    print(f"  - {p['title']} by {p['author']}")

if not new_poems:
    print("Nothing to do.")
    sys.exit(0)

new_results = analyze_corpus(new_poems)
combined = existing + new_results
save_results(combined, "corpus_results.json")
print(f"Updated corpus: {len(combined)} total poems.")
