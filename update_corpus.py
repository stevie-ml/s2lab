"""
Incremental corpus updater: analyzes only poems not yet in corpus_results.json.
Appends new results and saves.
"""
import sys
sys.path.insert(0, '/home/user/s2lab')

import json
from engine import analyze_poem, load_results, save_results
from corpus.poems import POEMS

# Load existing results
existing = load_results("corpus_results.json")
analyzed_keys = set()
for r in existing:
    m = r.get('metadata', {})
    key = (m.get('title', ''), m.get('author', ''))
    analyzed_keys.add(key)

print(f"Existing analyzed poems: {len(existing)}")

# Find new poems
new_poems = []
for poem in POEMS:
    key = (poem['title'], poem['author'])
    if key not in analyzed_keys:
        new_poems.append(poem)

print(f"New poems to analyze: {len(new_poems)}")
for p in new_poems:
    print(f"  - {p['author']} — {p['title']}")

if not new_poems:
    print("No new poems to analyze.")
    sys.exit(0)

# Analyze new poems
results = []
for i, poem in enumerate(new_poems):
    lang = poem.get('language', 'en')
    print(f"\n  [{i+1}/{len(new_poems)}] {poem['author']} — {poem['title']}")
    result = analyze_poem(
        text=poem['text'],
        title=poem['title'],
        author=poem['author'],
        year=poem.get('year'),
        era=poem.get('era', ''),
        language=lang,
    )
    results.append(result)

# Merge and save
all_results = existing + results
save_results(all_results, "corpus_results.json")
print(f"\nDone. Total poems in corpus: {len(all_results)}")
