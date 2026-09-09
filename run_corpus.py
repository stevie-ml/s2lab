"""Run GPT-2 analysis on the full poem corpus and save results."""
import sys
sys.path.insert(0, '/home/user/s2lab')

from engine import analyze_corpus, save_results
from corpus.poems import POEMS

print(f"Analyzing {len(POEMS)} poems (mixed languages, engine handles each)...")
results = analyze_corpus(POEMS)
save_results(results, "corpus_results.json")
print(f"Done. Saved {len(results)} results.")
