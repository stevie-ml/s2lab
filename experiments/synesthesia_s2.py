"""
Synesthetic Language and S2: Cross-Domain Sensory Surprise

When poets use synesthesia (describing one sense in terms of another —
"loud color," "sweet darkness," "cold silence"), does this produce
measurable S2 spikes? And does GPT-2 predict cross-domain or same-domain
sensory words?

Hypothesis: Cross-sensory substitutions are high-S2 moments because
GPT-2, having learned co-occurrence patterns, expects sensory continuation
within the same domain. A visual word in an auditory context (or vice versa)
should produce a distinct Straussian gap.
"""

import json
import sys
import os
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

RESULTS_PATH = "results/corpus_results.json"

# ── Sensory Domain Lexicons ──────────────────────────────────────────────────
# Each word is lowercased; we'll check stripped tokens against these sets

VISUAL = {
    "bright", "dark", "light", "glow", "gleam", "glare", "shine", "shadow",
    "flash", "radiant", "dim", "vivid", "pale", "golden", "silver", "crimson",
    "scarlet", "azure", "amber", "ivory", "ebony", "glitter", "shimmer", "blaze",
    "luminous", "dazzle", "sparkling", "obscure", "hazy", "clear", "opaque",
    "translucent", "iridescent", "ochre", "violet", "indigo", "emerald",
    "sapphire", "ruby", "pearl", "dull", "brilliant", "faded", "vivid",
    "invisible", "visible", "glowing", "flickering", "blazing", "gleaming",
    "shining", "darkened", "lit", "unlit", "moonlit", "sunlit", "shadow",
    "shade", "silhouette", "mirror", "reflection", "transparent", "blind"
}

AUDITORY = {
    "silent", "silence", "loud", "quiet", "whisper", "roar", "hiss", "crash",
    "murmur", "echo", "ring", "buzz", "hum", "drone", "crack", "thunder",
    "rumble", "rustle", "clatter", "bang", "snap", "creak", "screech", "shriek",
    "moan", "groan", "sigh", "sing", "song", "music", "melody", "harmony",
    "discord", "noise", "sound", "voice", "cry", "shout", "scream", "whistle",
    "toll", "chime", "peal", "knell", "din", "clamor", "cacophony", "symphony",
    "note", "chord", "resonance", "vibration", "reverberation", "mute",
    "deaf", "deafening", "hushed", "inaudible", "audible", "tuneful", "musical",
    "melodious", "discordant", "sonorous", "strident", "shrill", "mellow"
}

TACTILE = {
    "smooth", "rough", "sharp", "soft", "hard", "warm", "cold", "hot",
    "cool", "tender", "bristle", "prickle", "sting", "burn", "freeze",
    "numb", "tingle", "caress", "stroke", "touch", "feel", "grasp",
    "grip", "clasp", "press", "squeeze", "clench", "pinch", "bite",
    "itch", "scratch", "scrape", "rub", "polish", "coarse", "fine",
    "velvety", "silky", "satin", "rough", "jagged", "serrated", "blunt",
    "pointed", "firm", "brittle", "fragile", "solid", "liquid", "fluid",
    "viscous", "slippery", "sticky", "wet", "dry", "damp", "moist",
    "dense", "porous", "hollow", "thick", "thin", "heavy", "light",
    "supple", "rigid", "elastic", "taut", "slack", "tensile", "limp"
}

OLFACTORY = {
    "fragrant", "foul", "sweet", "acrid", "musty", "perfume", "scent",
    "odor", "aroma", "smell", "stench", "reek", "incense", "floral",
    "pungent", "rank", "putrid", "fetid", "rancid", "fresh", "stale",
    "moldy", "smoky", "spicy", "musky", "earthy", "redolent", "heady",
    "aromatic", "fragrance", "bouquet", "nosegay", "vapor", "whiff",
    "breath", "exhale", "inhale", "breathe"
}

GUSTATORY = {
    "bitter", "salty", "sour", "savory", "flavor", "taste", "savor",
    "spice", "bland", "insipid", "sharp", "pungent", "mild", "strong",
    "rich", "thin", "thick", "watery", "sugary", "honeyed", "tart",
    "tangy", "zesty", "acidic", "alkaline", "sweet", "sugary",
    "delicious", "palatable", "unpalatable", "ripe", "unripe", "stale",
    "fresh", "luscious", "succulent", "juicy", "dry", "bite"
}

ALL_SENSORY = {
    "visual": VISUAL,
    "auditory": AUDITORY,
    "tactile": TACTILE,
    "olfactory": OLFACTORY,
    "gustatory": GUSTATORY,
}


def get_domain(word: str) -> str | None:
    """Return the sensory domain of a word, or None if not sensory."""
    w = word.lower().strip().strip("'\",.;:!?-")
    for domain, lexicon in ALL_SENSORY.items():
        if w in lexicon:
            return domain
    return None


def get_alt_domains(alternatives: list[dict]) -> dict[str, float]:
    """Get the probability mass of each sensory domain in the top alternatives."""
    domain_probs: dict[str, float] = defaultdict(float)
    for alt in alternatives:
        d = get_domain(alt["token"])
        if d:
            domain_probs[d] += alt["prob"]
    return dict(domain_probs)


def is_artifact_token(token: dict) -> bool:
    """Filter stanza-break artifacts and pure punctuation."""
    t = token["token"].strip()
    if t == "" or t == "\n" or t == "\r\n":
        return True
    if token.get("p_newline", 0) >= 0.9:
        return True
    if all(c in ".,;:!?-–—()[]{}\"'`" for c in t):
        return True
    return False


def analyze_synesthesia():
    print("Loading corpus...")
    with open(RESULTS_PATH) as f:
        corpus = json.load(f)

    # Track synesthetic vs same-domain sensory tokens
    results = []
    domain_stats: dict[str, dict] = {d: {"n": 0, "total_s2": 0.0, "pos_s2": 0} for d in ALL_SENSORY}
    cross_domain_cases = []
    same_domain_cases = []
    no_alt_sensory = []

    poet_synesthesia: dict[str, list] = defaultdict(list)

    for poem in corpus:
        meta = poem["metadata"]
        tokens = poem["tokens"]

        for tok in tokens:
            if is_artifact_token(tok):
                continue

            token_domain = get_domain(tok["token"])
            if token_domain is None:
                continue

            # This token belongs to a sensory domain — now check alternatives
            alt_domains = get_alt_domains(tok.get("alternatives", []))

            domain_stats[token_domain]["n"] += 1
            domain_stats[token_domain]["total_s2"] += tok["s2"]
            if tok["s2"] > 0:
                domain_stats[token_domain]["pos_s2"] += 1

            if not alt_domains:
                no_alt_sensory.append(tok)
                continue

            # Check if the dominant expected domain matches the token's domain
            dominant_alt_domain = max(alt_domains, key=alt_domains.get)
            is_cross_domain = dominant_alt_domain != token_domain

            entry = {
                "token": tok["token"],
                "s2": tok["s2"],
                "token_domain": token_domain,
                "alt_domain": dominant_alt_domain,
                "alt_domain_prob": alt_domains[dominant_alt_domain],
                "all_alt_domains": alt_domains,
                "poem": meta["title"],
                "author": meta["author"],
                "era": meta["era"],
                "is_cross_domain": is_cross_domain,
            }
            results.append(entry)

            if is_cross_domain:
                cross_domain_cases.append(entry)
            else:
                same_domain_cases.append(entry)

            poet_synesthesia[meta["author"]].append(entry)

    print(f"\n=== SYNESTHESIA S2 ANALYSIS ===")
    print(f"Total sensory tokens analyzed: {len(results)}")
    print(f"Cross-domain (synesthetic): {len(cross_domain_cases)}")
    print(f"Same-domain: {len(same_domain_cases)}")
    print(f"No sensory alternatives: {len(no_alt_sensory)}")

    if not cross_domain_cases and not same_domain_cases:
        print("\nNo sensory tokens found with alternatives. Check the data.")
        return {}

    # Main comparison
    if cross_domain_cases:
        cross_s2 = [e["s2"] for e in cross_domain_cases]
        cross_mean = sum(cross_s2) / len(cross_s2)
        cross_pos = sum(1 for s in cross_s2 if s > 0) / len(cross_s2) * 100
    else:
        cross_mean = float("nan")
        cross_pos = float("nan")

    if same_domain_cases:
        same_s2 = [e["s2"] for e in same_domain_cases]
        same_mean = sum(same_s2) / len(same_s2)
        same_pos = sum(1 for s in same_s2 if s > 0) / len(same_s2) * 100
    else:
        same_mean = float("nan")
        same_pos = float("nan")

    print(f"\n--- Cross-domain (synesthetic) vs. same-domain sensory tokens ---")
    print(f"{'Type':<25} {'N':>6} {'Avg S2':>8} {'% +S2':>8}")
    print(f"{'Cross-domain':<25} {len(cross_domain_cases):>6} {cross_mean:>8.3f} {cross_pos:>7.1f}%")
    print(f"{'Same-domain':<25} {len(same_domain_cases):>6} {same_mean:>8.3f} {same_pos:>7.1f}%")
    print(f"{'Δ (cross − same)':<25} {'':>6} {cross_mean - same_mean:>8.3f} {cross_pos - same_pos:>7.1f}%")

    # Domain-specific stats
    print(f"\n--- S2 by sensory domain ---")
    print(f"{'Domain':<15} {'N':>6} {'Avg S2':>8} {'% +S2':>8}")
    for domain, stats in sorted(domain_stats.items(), key=lambda x: -x[1]["total_s2"] / max(x[1]["n"], 1)):
        n = stats["n"]
        if n == 0:
            continue
        avg = stats["total_s2"] / n
        pos_pct = stats["pos_s2"] / n * 100
        print(f"{domain:<15} {n:>6} {avg:>8.3f} {pos_pct:>7.1f}%")

    # Cross-domain transition matrix
    print(f"\n--- Cross-domain transition matrix (token domain → top-alt domain) ---")
    print(f"{'Poet wrote ↓ / GPT-2 expected →':<15}", end="")
    domains = list(ALL_SENSORY.keys())
    for d in domains:
        print(f"  {d[:5]:>7}", end="")
    print()

    matrix: dict[tuple[str, str], int] = defaultdict(int)
    for entry in results:
        matrix[(entry["token_domain"], entry["alt_domain"])] += 1

    for d_tok in domains:
        total_row = sum(matrix.get((d_tok, d_alt), 0) for d_alt in domains)
        if total_row == 0:
            continue
        print(f"  {d_tok[:13]:<13}", end="")
        for d_alt in domains:
            count = matrix.get((d_tok, d_alt), 0)
            pct = count / total_row * 100 if total_row else 0
            marker = "**" if d_tok != d_alt and pct > 15 else "  "
            print(f"  {pct:>5.1f}%", end="")
        print()

    # Top synesthetic moments
    cross_domain_cases_sorted = sorted(cross_domain_cases, key=lambda x: -x["s2"])
    print(f"\n--- Top 20 highest-S2 cross-domain (synesthetic) moments ---")
    print(f"{'Token':<15} {'S2':>8} {'From':>10} {'→Alt':>10} {'Poem'}")
    for entry in cross_domain_cases_sorted[:20]:
        print(
            f"  {repr(entry['token']):<13} {entry['s2']:>8.3f} "
            f"{entry['token_domain']:>10} → {entry['alt_domain']:<10} "
            f"{entry['poem'][:40]} ({entry['author'].split()[-1]})"
        )

    # Top same-domain sensory moments for comparison
    same_domain_cases_sorted = sorted(same_domain_cases, key=lambda x: -x["s2"])
    print(f"\n--- Top 10 highest-S2 same-domain sensory moments (for comparison) ---")
    print(f"{'Token':<15} {'S2':>8} {'Domain':>10} {'Poem'}")
    for entry in same_domain_cases_sorted[:10]:
        print(
            f"  {repr(entry['token']):<13} {entry['s2']:>8.3f} "
            f"{entry['token_domain']:>10}   "
            f"{entry['poem'][:40]} ({entry['author'].split()[-1]})"
        )

    # Poet synesthesia rates
    print(f"\n--- Poet synesthetic rates (min 5 sensory tokens) ---")
    print(f"{'Poet':<30} {'N':>5} {'Cross%':>8} {'Avg cross S2':>13}")
    poet_stats_list = []
    for author, entries in poet_synesthesia.items():
        if len(entries) < 5:
            continue
        cross = [e for e in entries if e["is_cross_domain"]]
        cross_rate = len(cross) / len(entries) * 100
        cross_avg_s2 = sum(e["s2"] for e in cross) / len(cross) if cross else 0.0
        poet_stats_list.append((author, len(entries), cross_rate, cross_avg_s2))

    for author, n, rate, avg_s2 in sorted(poet_stats_list, key=lambda x: -x[2]):
        print(f"  {author:<28} {n:>5} {rate:>7.1f}% {avg_s2:>12.3f}")

    # Era analysis
    era_cross: dict[str, list] = defaultdict(list)
    era_same: dict[str, list] = defaultdict(list)
    for entry in results:
        if entry["is_cross_domain"]:
            era_cross[entry["era"]].append(entry["s2"])
        else:
            era_same[entry["era"]].append(entry["s2"])

    print(f"\n--- Cross-domain S2 by era (min 3 tokens) ---")
    era_rows = []
    for era in set(list(era_cross.keys()) + list(era_same.keys())):
        cc = era_cross.get(era, [])
        sc = era_same.get(era, [])
        if len(cc) + len(sc) < 3:
            continue
        c_mean = sum(cc) / len(cc) if cc else float("nan")
        s_mean = sum(sc) / len(sc) if sc else float("nan")
        era_rows.append((era, len(cc), len(sc), c_mean, s_mean))

    for row in sorted(era_rows, key=lambda x: -x[3] if x[3] == x[3] else float("-inf")):
        era, nc, ns, cm, sm = row
        print(f"  {era:<25} cross n={nc:>3} S2={cm:>7.3f}  |  same n={ns:>3} S2={sm:>7.3f}")

    output = {
        "n_total_sensory": len(results),
        "n_cross_domain": len(cross_domain_cases),
        "n_same_domain": len(same_domain_cases),
        "cross_domain_mean_s2": cross_mean,
        "same_domain_mean_s2": same_mean,
        "delta_s2": cross_mean - same_mean,
        "cross_domain_pos_s2_pct": cross_pos,
        "same_domain_pos_s2_pct": same_pos,
        "domain_stats": {
            d: {
                "n": v["n"],
                "avg_s2": v["total_s2"] / v["n"] if v["n"] else 0.0,
                "pos_s2_pct": v["pos_s2"] / v["n"] * 100 if v["n"] else 0.0,
            }
            for d, v in domain_stats.items()
        },
        "top_cross_domain": cross_domain_cases_sorted[:30],
        "poet_synesthesia_rates": {
            a: {"n": n, "cross_rate": r, "cross_avg_s2": s}
            for a, n, r, s in poet_stats_list
        },
    }

    with open("results/synesthesia_s2.json", "w") as f:
        json.dump(output, f, indent=2)
    print("\nResults saved to results/synesthesia_s2.json")

    return output


if __name__ == "__main__":
    analyze_synesthesia()
