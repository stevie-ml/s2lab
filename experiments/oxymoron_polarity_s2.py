"""
Oxymoron and Semantic Polarity Reversal vs S2
==============================================
Investigates whether oxymoronic substitutions — moments where a poet chooses a word
whose emotional/semantic valence opposes what the model expected — produce systematic
S2 spikes.

The "oxymoron as Straussian gap": when GPT-2 predicts positive-valence continuations
and the poet supplies a negative word (or vice versa), we get a polarity reversal.
High-polarity-reversal tokens should cluster at the extreme positive end of S2.

Method:
  1. Use a curated valence lexicon (ANEW-inspired simple positive/negative word lists).
  2. For each token in the corpus, determine:
       - Predicted valence: the predominant valence among the top-10 alternatives
       - Actual valence: the valence of the chosen token
  3. Flag "polarity reversals" (predicted positive → actual negative, or vice versa).
  4. Compare S2 distributions: reversal vs. non-reversal tokens, poetry vs. prose.
  5. Identify canonical examples of oxymoronic high-S2 moments in the corpus.
"""

import json
import os
import re
from collections import defaultdict
from statistics import mean, stdev

# ---------------------------------------------------------------------------
# Simple valence lexicon — enough for a first pass
# ---------------------------------------------------------------------------

POSITIVE_WORDS = {
    "love","lovely","light","bright","beauty","beautiful","sweet","joy","joyful",
    "peace","peaceful","hope","hopeful","grace","graceful","true","truth","good",
    "great","warm","warmth","life","living","dream","rise","spring","sun","shine",
    "shining","gold","golden","free","freedom","sing","song","music","pure","holy",
    "heaven","divine","gentle","tender","smile","laugh","laughter","happy","happiness",
    "delight","delightful","glory","glorious","noble","fair","rich","plenty","bloom",
    "blossom","soft","kind","kindness","clear","calm","serene","sacred","bliss",
    "blessed","praise","celebrate","triumph","win","victory","strong","strength",
    "safe","bright","brilliant","wonder","wonderful","glad","gift","care","heal",
    "fresh","alive","grow","grow","flourish","radiant","splendid","magnificent",
    "eternal","immortal","paradise","ecstasy","euphoria","rapture","elation",
    "content","fortunate","merry","vivid","vibrant","lively","jubilant",
    "exalt","exalted","sublime","perfect","harmony","harmonious","unity",
    "love","trust","faith","loyal","loyalty","courage","courageous","heroic",
}

NEGATIVE_WORDS = {
    "death","dead","die","dying","dark","darkness","shadow","cold","night","end",
    "fall","fallen","fear","grief","grieve","sad","sorrow","pain","suffer","loss",
    "lost","broken","break","destroy","destruction","hate","hatred","war","fight",
    "battle","wound","blood","tears","cry","weep","mourning","grave","tomb",
    "silence","silent","alone","lonely","empty","hollow","void","nothing","nothingness",
    "despair","desperation","decay","rot","ruin","ruined","ash","ashes","bitter",
    "bitterness","anger","rage","cruel","cruelty","evil","wicked","wrong","sin",
    "guilt","shame","regret","remorse","anguish","agony","misery","wretched",
    "horror","dread","terror","fear","panic","anxiety","doom","doom","fatal",
    "fatal","violent","violence","cruel","burden","heavy","weight","stone","grey",
    "gray","black","curse","cursed","poison","poisoned","blind","deaf","mute",
    "wound","wounds","scar","scars","storm","floods","flood","drown","drowning",
    "slavery","slave","prison","cage","trap","bound","chains","chained","forgotten",
    "forgetting","absence","absent","absence","void","nothing","null","naught",
    "barren","bleak","desolate","desolation","forsaken","abandon","abandoned",
    "hunger","starve","thirst","exhausted","weary","tired","fading","fade",
    "wither","withered","fallen","crumbling","crumble","vanish","vanished",
    "collapse","failure","fail","fell","sink","sinking","fell","crash",
}

def get_valence(token_text: str) -> str | None:
    """Return 'pos', 'neg', or None for unknown."""
    word = re.sub(r"[^a-zA-Z]", "", token_text.strip().lower())
    if word in POSITIVE_WORDS:
        return "pos"
    if word in NEGATIVE_WORDS:
        return "neg"
    return None

def predicted_valence(alternatives: list[dict]) -> str | None:
    """
    Compute the valence of the top predicted tokens (weighted by probability).
    Returns 'pos', 'neg', or None if inconclusive.
    """
    pos_mass = 0.0
    neg_mass = 0.0
    for alt in alternatives[:10]:
        v = get_valence(alt["token"])
        if v == "pos":
            pos_mass += alt["prob"]
        elif v == "neg":
            neg_mass += alt["prob"]
    total = pos_mass + neg_mass
    if total < 0.05:  # not enough valenced mass to call
        return None
    if pos_mass / total >= 0.65:
        return "pos"
    if neg_mass / total >= 0.65:
        return "neg"
    return None

def analyze_corpus(corpus_path: str):
    with open(corpus_path) as f:
        corpus = json.load(f)

    # Storage: collect token-level records
    reversal_tokens = []       # polarity reversal tokens
    concordant_tokens = []     # same valence as prediction
    unknown_tokens = []        # can't determine

    # Per-poem oxymoron scores
    poem_stats = []

    # Famous oxymoron catalog: actual token text patterns to watch for
    known_oxymorons = {
        ("sweet", "sorrow"), ("living", "death"), ("cold", "fire"),
        ("deafening", "silence"), ("bitter", "sweet"), ("dark", "light"),
        ("dead", "alive"), ("loving", "hate"), ("joyful", "pain"),
        ("gentle", "violence"), ("beautiful", "death"), ("silent", "scream"),
        ("bright", "darkness"), ("sweet", "bitter"), ("warm", "cold"),
    }

    catalog_hits = []

    for poem in corpus:
        meta = poem["metadata"]
        tokens = poem["tokens"]
        era = meta.get("era", "unknown")
        is_prose = (era == "control")

        poem_reversals = 0
        poem_total_valenced = 0
        poem_reversal_s2 = []
        poem_concordant_s2 = []

        for i, tok in enumerate(tokens):
            if tok.get("p_newline", 0) > 0.9:
                continue  # skip stanza-break artifact positions

            actual_v = get_valence(tok["token"])
            pred_v = predicted_valence(tok.get("alternatives", []))

            record = {
                "token": tok["token"],
                "s2": tok["s2"],
                "surprisal": tok["surprisal"],
                "entropy": tok["entropy"],
                "actual_valence": actual_v,
                "pred_valence": pred_v,
                "title": meta["title"],
                "author": meta.get("author", ""),
                "era": era,
                "is_prose": is_prose,
                "position": tok["position"],
                "rank": tok.get("rank", None),
            }

            if actual_v and pred_v:
                poem_total_valenced += 1
                if actual_v != pred_v:
                    record["reversal_type"] = f"{pred_v}→{actual_v}"
                    reversal_tokens.append(record)
                    poem_reversals += 1
                    poem_reversal_s2.append(tok["s2"])
                else:
                    record["reversal_type"] = "concordant"
                    concordant_tokens.append(record)
                    poem_concordant_s2.append(tok["s2"])
            else:
                unknown_tokens.append(record)

            # Check for known oxymoron bigrams
            if i > 0:
                prev_tok = re.sub(r"[^a-z]", "", tokens[i-1]["token"].strip().lower())
                curr_tok = re.sub(r"[^a-z]", "", tok["token"].strip().lower())
                for (w1, w2) in known_oxymorons:
                    if (prev_tok == w1 and curr_tok == w2) or (prev_tok == w2 and curr_tok == w1):
                        catalog_hits.append({
                            "bigram": f"{tokens[i-1]['token']} + {tok['token']}",
                            "s2_second": tok["s2"],
                            "s2_first": tokens[i-1]["s2"],
                            "title": meta["title"],
                            "author": meta.get("author", ""),
                        })

        if poem_total_valenced > 0:
            reversal_rate = poem_reversals / poem_total_valenced
            poem_stats.append({
                "title": meta["title"],
                "author": meta.get("author", ""),
                "era": era,
                "is_prose": is_prose,
                "reversal_rate": reversal_rate,
                "n_reversals": poem_reversals,
                "n_valenced": poem_total_valenced,
                "avg_reversal_s2": mean(poem_reversal_s2) if poem_reversal_s2 else None,
                "avg_concordant_s2": mean(poem_concordant_s2) if poem_concordant_s2 else None,
            })

    return {
        "reversal_tokens": reversal_tokens,
        "concordant_tokens": concordant_tokens,
        "poem_stats": poem_stats,
        "catalog_hits": catalog_hits,
    }

def compute_summary(results: dict) -> dict:
    rev = results["reversal_tokens"]
    conc = results["concordant_tokens"]
    poem_stats = results["poem_stats"]

    # S2 comparison
    rev_s2 = [t["s2"] for t in rev]
    conc_s2 = [t["s2"] for t in conc]

    # Poetry vs prose reversal rates
    poetry_stats = [p for p in poem_stats if not p["is_prose"]]
    prose_stats = [p for p in poem_stats if p["is_prose"]]

    poetry_rev_rates = [p["reversal_rate"] for p in poetry_stats if p["n_valenced"] >= 5]
    prose_rev_rates = [p["reversal_rate"] for p in prose_stats if p["n_valenced"] >= 5]

    # Top reversal types
    from collections import Counter
    rev_type_counts = Counter(t["reversal_type"] for t in rev)

    # By era
    era_reversals = defaultdict(list)
    for t in rev:
        if not t["is_prose"]:
            era_reversals[t["era"]].append(t["s2"])
    for t in conc:
        pass  # just tracking reversal tokens

    era_reversal_rates = {}
    for p in poetry_stats:
        if p["n_valenced"] >= 3:
            era = p["era"]
            if era not in era_reversal_rates:
                era_reversal_rates[era] = []
            era_reversal_rates[era].append(p["reversal_rate"])

    era_avg_rates = {era: mean(rates) for era, rates in era_reversal_rates.items() if rates}

    # Top reversal poems
    top_poems = sorted(
        [p for p in poetry_stats if p["n_valenced"] >= 5],
        key=lambda p: p["reversal_rate"],
        reverse=True
    )[:10]

    # Top S2 reversal tokens
    top_s2_reversals = sorted(rev, key=lambda t: t["s2"], reverse=True)[:20]

    return {
        "n_reversal_tokens": len(rev),
        "n_concordant_tokens": len(conc),
        "avg_s2_reversal": mean(rev_s2) if rev_s2 else 0,
        "avg_s2_concordant": mean(conc_s2) if conc_s2 else 0,
        "std_s2_reversal": stdev(rev_s2) if len(rev_s2) > 1 else 0,
        "std_s2_concordant": stdev(conc_s2) if len(conc_s2) > 1 else 0,
        "avg_reversal_rate_poetry": mean(poetry_rev_rates) if poetry_rev_rates else 0,
        "avg_reversal_rate_prose": mean(prose_rev_rates) if prose_rev_rates else 0,
        "reversal_type_counts": dict(rev_type_counts.most_common()),
        "era_avg_reversal_rates": era_avg_rates,
        "top_reversal_poems": top_poems,
        "top_s2_reversals": [
            {k: v for k, v in t.items() if k in ("token","s2","surprisal","title","author","reversal_type")}
            for t in top_s2_reversals
        ],
        "catalog_hits": results["catalog_hits"],
    }

if __name__ == "__main__":
    corpus_path = os.path.join(os.path.dirname(__file__), "..", "results", "corpus_results.json")
    out_path = os.path.join(os.path.dirname(__file__), "..", "findings", "oxymoron_polarity_s2.json")

    print("Analyzing polarity reversals in corpus...")
    results = analyze_corpus(corpus_path)
    summary = compute_summary(results)

    with open(out_path, "w") as f:
        json.dump(summary, f, indent=2)

    print(f"\n=== Polarity Reversal Summary ===")
    print(f"Reversal tokens: {summary['n_reversal_tokens']}")
    print(f"Concordant tokens: {summary['n_concordant_tokens']}")
    print(f"Avg S2 — reversal: {summary['avg_s2_reversal']:.3f}, concordant: {summary['avg_s2_concordant']:.3f}")
    print(f"Avg reversal rate — poetry: {summary['avg_reversal_rate_poetry']:.3f}, prose: {summary['avg_reversal_rate_prose']:.3f}")
    print(f"\nTop 10 reversal types: {dict(list(summary['reversal_type_counts'].items())[:4])}")
    print(f"\nCatalog hits (known oxymorons): {len(summary['catalog_hits'])}")
    for hit in summary["catalog_hits"][:10]:
        print(f"  '{hit['bigram']}' S2={hit['s2_second']:.2f}  — {hit['title']} ({hit['author']})")

    print(f"\nTop 5 poems by reversal rate:")
    for p in summary["top_reversal_poems"][:5]:
        print(f"  {p['reversal_rate']:.2%} — {p['title']} ({p['author']}) [{p['era']}]")

    print(f"\nTop 5 S2 reversal tokens:")
    for t in summary["top_s2_reversals"][:5]:
        print(f"  '{t['token']}' S2={t['s2']:.2f} ({t['reversal_type']}) in '{t['title']}'")
