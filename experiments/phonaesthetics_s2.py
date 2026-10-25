"""
Phonaesthetics and S₂: Do Sound-Symbolic Word Classes Have Distinct
Information Signatures in Poetry?

Phonaesthemes are sub-morphemic sound clusters associated with consistent
meaning. English examples:
  gl- → light/vision (gleam, glimmer, glint, glow, glare, gloom)
  sl- → negative/slow (slime, slug, slouch, slur, sloppy)
  fl- → quick movement (flutter, flicker, flash, fly, flap)
  cr- → hard/breaking (crack, crash, creak, crunch, crush)
  sp- → energy/dispersion (spark, spin, spiral, splash, spring)
  sn- → contempt/nose (sneer, snicker, snob, snoop, sniff)
  dr- → slow/heavy (droop, drift, drag, drip, drone)
  wh- → air/quiet (whisper, whirl, whisk, whip)
  bl- → dark/strong (blaze, blast, blow, bleed, blind)
  gr- → rough/discontent (growl, groan, grind, grudge, grim)
  sw- → sweeping motion (sweep, swing, sway, swirl, swim)
  st- → solid/standing (stand, still, stone, stark, strong)

Hypothesis: Phonaesthetically marked words will have higher S₂ — poets
choose them deliberately for sound-meaning resonance, defying GPT-2's
prediction. Alternatively, GPT-2 may have learned these associations,
making phonaesthetic words MORE predictable (lower S₂) in their poetic
contexts.
"""

import json
import os
import re
from collections import defaultdict

RESULTS_PATH = os.path.join(os.path.dirname(__file__), "..", "results", "corpus_results.json")

# Phonaesthetic clusters with canonical semantic associations
CLUSTERS = {
    "gl-": ("light/vision", ["gleam", "glimmer", "glint", "glow", "glare", "gloom", "glamour",
                               "glisten", "glitter", "glance", "glaze", "glory", "glad"]),
    "sl-": ("negative/slow", ["slime", "slug", "slouch", "slur", "sloppy", "slack", "sloth",
                               "sleazy", "slant", "slump", "slash", "slave", "slaughter", "slip",
                               "slide", "slow", "sly", "slam", "slab"]),
    "fl-": ("quick movement", ["flutter", "flicker", "flash", "fly", "flap", "float", "flow",
                                "flame", "flit", "fling", "fleet", "flex", "flare", "flaw",
                                "fleck", "flesh", "flight"]),
    "cr-": ("hard/breaking", ["crack", "crash", "creak", "crunch", "crush", "crumble", "creep",
                               "crow", "cruel", "crisp", "crave", "crazy", "cry", "crime",
                               "create", "cross", "crown"]),
    "sp-": ("energy/dispersion", ["spark", "spin", "spiral", "splash", "spring", "spill", "spit",
                                   "spread", "spray", "sprint", "speck", "spell", "spend",
                                   "spirit", "spur", "speed"]),
    "sn-": ("contempt/nose", ["sneer", "snicker", "snob", "snoop", "sniff", "snare", "snap",
                               "snake", "snag", "snow", "sneak", "snarl"]),
    "dr-": ("slow/heavy", ["droop", "drift", "drag", "drip", "drone", "dream", "draw", "dread",
                            "drown", "dress", "drive", "drip", "drop", "dry", "drug"]),
    "wh-": ("air/quiet/quick", ["whisper", "whirl", "whisk", "whip", "whistle", "white",
                                  "wheat", "wheel", "where", "whole", "why", "who", "when",
                                  "what"]),
    "bl-": ("dark/strong", ["blaze", "blast", "blow", "bleed", "blind", "bleak", "blight",
                              "bloom", "blood", "black", "blade", "blank", "bliss", "blue",
                              "bless", "blur"]),
    "gr-": ("rough/discontent", ["growl", "groan", "grind", "grudge", "grim", "grave", "grief",
                                   "grip", "green", "grey", "great", "ground", "grace",
                                   "grain", "grass", "gray"]),
    "sw-": ("sweeping motion", ["sweep", "swing", "sway", "swirl", "swim", "swift", "sweet",
                                  "swell", "swan", "swear", "sweat", "sword", "swallow"]),
    "st-": ("solid/standing", ["stand", "still", "stone", "stark", "strong", "strike", "storm",
                                 "star", "stem", "steel", "stir", "stream", "stray", "steep",
                                 "step", "stern", "strain", "strange"]),
}

# Function words starting with some clusters (wh-, st-, dr-) to be treated with care
KNOWN_FUNCTION = {"where", "when", "what", "who", "while", "whether",
                   "the", "this", "that", "there", "their", "they", "them",
                   "draw", "drawn", "drew", "drove"}


def load_corpus():
    with open(RESULTS_PATH) as f:
        return json.load(f)


def clean_token_text(tok_text: str) -> str:
    """Strip whitespace/punctuation, lowercase."""
    return re.sub(r"[^\w]", "", tok_text).lower()


def classify_cluster(word: str) -> str | None:
    """Return the matching cluster prefix for a word, or None."""
    if len(word) < 3:
        return None
    for cluster in CLUSTERS:
        prefix = cluster.rstrip("-")
        if word.startswith(prefix):
            return cluster
    return None


def main():
    corpus = load_corpus()
    texts = corpus.get("texts", corpus) if isinstance(corpus, dict) else corpus
    if isinstance(texts, dict):
        texts = list(texts.values())

    # Corpus baseline (excluding newline-artifact tokens: p_newline > 0.9)
    baseline_s2 = []
    baseline_surp = []
    baseline_ent = []

    cluster_data = defaultdict(lambda: {"s2": [], "surp": [], "ent": [], "examples": []})
    token_total = 0

    # Track non-phonaesthetic tokens for better baseline
    non_phonaes_s2 = []

    for text in texts:
        title = text.get("title", "Unknown")
        author = text.get("author", "Unknown")
        tokens = text.get("tokens", [])
        for tok in tokens:
            s2 = tok.get("s2")
            surp = tok.get("surprisal")
            ent = tok.get("entropy")
            p_nl = tok.get("p_newline", 0)
            tok_text = tok.get("token", "")

            if s2 is None or surp is None or ent is None:
                continue

            # Skip newline-artifact positions
            if p_nl > 0.9:
                continue

            token_total += 1
            baseline_s2.append(s2)
            baseline_surp.append(surp)
            baseline_ent.append(ent)

            word = clean_token_text(tok_text)
            cluster = classify_cluster(word)

            if cluster:
                cluster_data[cluster]["s2"].append(s2)
                cluster_data[cluster]["surp"].append(surp)
                cluster_data[cluster]["ent"].append(ent)
                if len(cluster_data[cluster]["examples"]) < 30:
                    cluster_data[cluster]["examples"].append({
                        "token": tok_text, "word": word,
                        "s2": round(s2, 2), "surp": round(surp, 2), "ent": round(ent, 2),
                        "title": title, "author": author
                    })
            else:
                non_phonaes_s2.append(s2)

    # Compute stats
    def stats(vals):
        if not vals:
            return {}
        n = len(vals)
        mean = sum(vals) / n
        pos_ratio = sum(1 for v in vals if v > 0) / n
        sorted_v = sorted(vals)
        median = sorted_v[n // 2]
        return {"n": n, "mean": round(mean, 3), "median": round(median, 3),
                "pos_ratio": round(pos_ratio, 3)}

    baseline = stats(baseline_s2)
    print(f"Corpus baseline (artifact-free): n={baseline['n']}, mean_S2={baseline['mean']}, +S2={baseline['pos_ratio']*100:.1f}%")
    print(f"Token total (artifact-free): {token_total}\n")

    results = []
    for cluster, semantic in CLUSTERS.items():
        semantic_label = semantic[0]
        data = cluster_data[cluster]
        if not data["s2"]:
            continue
        st = stats(data["s2"])
        surp_st = stats(data["surp"])
        ent_st = stats(data["ent"])
        delta = round(st["mean"] - baseline["mean"], 3)
        results.append({
            "cluster": cluster,
            "semantic": semantic_label,
            "n": st["n"],
            "mean_s2": st["mean"],
            "delta_s2": delta,
            "pos_ratio": st["pos_ratio"],
            "mean_surp": surp_st["mean"],
            "mean_ent": ent_st["mean"],
            "examples": data["examples"]
        })

    # Sort by delta_s2 descending
    results.sort(key=lambda x: x["delta_s2"], reverse=True)

    # Top/bottom examples for each cluster
    print("="*70)
    print("PHONAESTHETIC CLUSTER ANALYSIS")
    print("="*70)
    print(f"\n{'Cluster':<10} {'Semantic':<25} {'n':>5} {'mean_S2':>8} {'Δ_S2':>8} {'+S2%':>6} {'Surp':>8} {'Ent':>8}")
    print("-"*80)
    for r in results:
        print(f"{r['cluster']:<10} {r['semantic']:<25} {r['n']:>5} {r['mean_s2']:>8.3f} "
              f"{r['delta_s2']:>8.3f} {r['pos_ratio']*100:>5.1f}% "
              f"{r['mean_surp']:>8.3f} {r['mean_ent']:>8.3f}")

    print(f"\n{'CORPUS BASELINE':<36} {baseline['n']:>5} {baseline['mean']:>8.3f} "
          f"{'0.000':>8} {baseline['pos_ratio']*100:>5.1f}%")

    # High-S2 examples for most divergent clusters
    print("\n\n--- High S₂ tokens for 'gl-' cluster ---")
    gl = [r for r in results if r["cluster"] == "gl-"]
    if gl:
        ex = sorted(gl[0]["examples"], key=lambda x: x["s2"], reverse=True)[:8]
        for e in ex:
            print(f"  token={e['token']!r:15} S2={e['s2']:+.2f}  [{e['author']}: {e['title']!r}]")

    print("\n--- High S₂ tokens for 'sl-' cluster ---")
    sl = [r for r in results if r["cluster"] == "sl-"]
    if sl:
        ex = sorted(sl[0]["examples"], key=lambda x: x["s2"], reverse=True)[:8]
        for e in ex:
            print(f"  token={e['token']!r:15} S2={e['s2']:+.2f}  [{e['author']}: {e['title']!r}]")

    print("\n--- High S₂ tokens for 'fl-' cluster ---")
    fl = [r for r in results if r["cluster"] == "fl-"]
    if fl:
        ex = sorted(fl[0]["examples"], key=lambda x: x["s2"], reverse=True)[:8]
        for e in ex:
            print(f"  token={e['token']!r:15} S2={e['s2']:+.2f}  [{e['author']}: {e['title']!r}]")

    return results, baseline


if __name__ == "__main__":
    results, baseline = main()
    print("\nDone.")
