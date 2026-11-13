"""
Proverbs vs. Poetry: Testing the Anti-Conventional Hypothesis.

Folk proverbs are maximally compressed, conventional, and memorable.
They should sit at or below the prose-control end of the S2 spectrum
because they exploit stock phrases, shared idioms, and predictable structure.

We test: (a) proverb avg S2 vs prose control and poetry average,
(b) metaphorical vs literal proverb within-class variation.
"""

import sys, os, json, statistics
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import warnings
warnings.filterwarnings("ignore")

from engine import analyze_poem

# Famous English proverbs, labeled metaphorical or literal
PROVERBS = [
    # Metaphorical proverbs (use figurative language / imagery)
    {"title": "Bird in hand", "text": "A bird in the hand is worth two in the bush.", "type": "metaphorical"},
    {"title": "Rolling stone", "text": "A rolling stone gathers no moss.", "type": "metaphorical"},
    {"title": "Barking dog", "text": "A barking dog never bites.", "type": "metaphorical"},
    {"title": "Still waters", "text": "Still waters run deep.", "type": "metaphorical"},
    {"title": "Bite the hand", "text": "Don't bite the hand that feeds you.", "type": "metaphorical"},
    {"title": "Leopard spots", "text": "A leopard cannot change its spots.", "type": "metaphorical"},
    {"title": "Broken clock", "text": "A broken clock is right twice a day.", "type": "metaphorical"},
    {"title": "Stitch in time", "text": "A stitch in time saves nine.", "type": "metaphorical"},
    {"title": "Spilled milk", "text": "There is no use crying over spilled milk.", "type": "metaphorical"},
    {"title": "Glass houses", "text": "People who live in glass houses should not throw stones.", "type": "metaphorical"},
    {"title": "Silver lining", "text": "Every cloud has a silver lining.", "type": "metaphorical"},
    {"title": "One swallow", "text": "One swallow does not make a summer.", "type": "metaphorical"},
    # Literal proverbs (direct, non-figurative advice)
    {"title": "Waste not", "text": "Waste not, want not.", "type": "literal"},
    {"title": "Better safe", "text": "Better safe than sorry.", "type": "literal"},
    {"title": "Early bird", "text": "The early bird catches the worm.", "type": "literal"},
    {"title": "Many hands", "text": "Many hands make light work.", "type": "literal"},
    {"title": "Actions speak", "text": "Actions speak louder than words.", "type": "literal"},
    {"title": "Look before", "text": "Look before you leap.", "type": "literal"},
    {"title": "Too many cooks", "text": "Too many cooks spoil the broth.", "type": "literal"},
    {"title": "Better late", "text": "Better late than never.", "type": "literal"},
    {"title": "Honesty policy", "text": "Honesty is the best policy.", "type": "literal"},
    {"title": "No pain", "text": "No pain, no gain.", "type": "literal"},
    {"title": "Practice perfect", "text": "Practice makes perfect.", "type": "literal"},
    {"title": "Two wrongs", "text": "Two wrongs do not make a right.", "type": "literal"},
]

def analyze_tokens_clean(result):
    """Return artifact-free tokens (p_newline < 0.9)."""
    return [t for t in result["tokens"] if t.get("p_newline", 0) < 0.9]

def compute_stats(tokens):
    s2_vals = [t["s2"] for t in tokens]
    if not s2_vals:
        return {}
    return {
        "n": len(s2_vals),
        "mean_s2": round(statistics.mean(s2_vals), 4),
        "median_s2": round(statistics.median(s2_vals), 4),
        "std_s2": round(statistics.stdev(s2_vals) if len(s2_vals) > 1 else 0, 4),
        "pos_ratio": round(sum(1 for v in s2_vals if v > 0) / len(s2_vals), 4),
        "mean_surprisal": round(statistics.mean(t["surprisal"] for t in tokens), 4),
        "mean_entropy": round(statistics.mean(t["entropy"] for t in tokens), 4),
    }

print("Loading GPT-2 model...", flush=True)

results = []
for p in PROVERBS:
    r = analyze_poem(
        text=p["text"],
        title=p["title"],
        author="proverb",
        year=0,
        era="proverb",
    )
    clean = analyze_tokens_clean(r)
    stats = compute_stats(clean)
    stats["title"] = p["title"]
    stats["type"] = p["type"]
    stats["text"] = p["text"]
    results.append(stats)
    print(f"  {p['title']}: mean_s2={stats.get('mean_s2','N/A')}", flush=True)

# Aggregate stats
meta_stats = {}
for grp in ["metaphorical", "literal", "all"]:
    subset = [r for r in results if grp == "all" or r["type"] == grp]
    if subset:
        means = [r["mean_s2"] for r in subset if "mean_s2" in r]
        pos_rs = [r["pos_ratio"] for r in subset if "pos_ratio" in r]
        meta_stats[grp] = {
            "n_proverbs": len(subset),
            "mean_of_means_s2": round(statistics.mean(means), 4),
            "median_of_means_s2": round(statistics.median(means), 4),
            "mean_pos_ratio": round(statistics.mean(pos_rs), 4),
        }

# Reference values from corpus
# prose_control avg (artifact-free): -1.72
# poetry overall avg (artifact-free): ~-0.44
REFERENCE = {
    "prose_control_artifact_free": -1.72,
    "poetry_overall_artifact_free": -0.44,
    "german_modernist_best": 0.63,
    "cliche_control": -0.93,
}

output = {
    "proverb_results": results,
    "meta_stats": meta_stats,
    "reference": REFERENCE,
}

out_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "results", "proverb_s2.json")
with open(out_path, "w") as f:
    json.dump(output, f, indent=2)

print(f"\nSaved results to {out_path}")
print("\n=== SUMMARY ===")
for grp, s in meta_stats.items():
    print(f"  {grp}: mean S2 = {s['mean_of_means_s2']}, pos_ratio = {s['mean_pos_ratio']}")
print(f"  Reference: prose_control = -1.72, poetry = -0.44")
