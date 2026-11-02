"""
Second-Person Direct Address and S₂

Research Question:
  When poets directly address an entity — "O thou", "Death be not proud",
  "How do I love thee?" — does the S₂ profile change in the apostrophic
  passage vs. the rest of the poem?

Hypothesis:
  Direct address collapses the expected syntactic range: GPT-2 may become
  more uncertain about what follows "thou" (high entropy) or more
  predictable (low entropy), but the poet's actual choice may veer in
  unusual directions (high S₂). Alternatively, apostrophe may function as
  a normative framing device (establishing "thou art" grammar) that
  REDUCES subsequent surprisal.

Method:
  1. Load corpus_results.json.
  2. For each poem, walk the token list and flag tokens that are in a
     "direct address window" — starting from an address marker and
     running for N tokens. Address markers include:
       - Standalone "O" (vocative O) before a noun phrase
       - "thou", "thee", "thy", "thine", "ye"  (archaic 2nd person)
       - "you", "your", "yours" at sentence / line start (modern apostrophe)
       - Apostrophe openers: "Death", "Love", "Time", "God", "Nature",
         "Life", "Soul", "Wind", "Sea", "Night", "Day" in isolation
  3. Separate tokens: address-window vs. non-address.
  4. Compare avg_s2, avg_entropy, avg_surprisal in each zone.
  5. Compute per-poem "apostrophe lift" = mean_s2_address - mean_s2_non_address.
  6. Identify poems with strongest positive / negative lift.
  7. Inspect the specific high-S₂ tokens in address windows — what did
     GPT-2 expect vs. what the poet wrote?
"""

import json
import re
import os
from collections import defaultdict
import statistics

RESULTS_FILE = os.path.join(os.path.dirname(__file__), "..", "results", "corpus_results.json")
OUTPUT_FILE  = os.path.join(os.path.dirname(__file__), "..", "results", "second_person_address_s2.json")

# Address window in tokens
WINDOW = 12

# Vocative O pattern: token text is exactly ' O' or 'O' (possibly leading space)
def is_vocative_O(text: str) -> bool:
    return text.strip() in {"O", "Oh"}

# Archaic 2nd person pronouns
ARCHAIC_2P = {"thou", "thee", "thy", "thine", "ye"}

# Common direct address nouns used in apostrophe
APOSTROPHE_NOUNS = {
    "Death", "Love", "Time", "God", "Nature", "Life", "Soul", "Wind",
    "Sea", "Night", "Day", "Spring", "Autumn", "Earth", "Sky",
    "Fortune", "Truth", "Beauty", "Muse", "Fame", "Memory", "Youth",
    "Heaven", "Hell", "Sleep", "Dream", "Silence", "Liberty", "Hope",
}

def is_address_opener(text: str) -> bool:
    stripped = text.strip()
    return (
        stripped in ARCHAIC_2P
        or stripped in APOSTROPHE_NOUNS
        or is_vocative_O(stripped)
    )

def is_modern_2p_at_line_start(tokens: list, i: int) -> bool:
    """'you' or 'your' that appears at the start of a line / after newline."""
    tok = tokens[i]["token"].strip().lower()
    if tok not in {"you", "your", "yours"}:
        return False
    # Check if preceded by a newline token
    if i == 0:
        return True
    prev_text = tokens[i - 1]["token"]
    return "\n" in prev_text or prev_text.strip() in {".", "!", "?", "—", ",", ";", ":"}

def label_tokens(tokens: list) -> list[bool]:
    """Return a bool list: True = inside an address window."""
    n = len(tokens)
    in_window = [False] * n
    i = 0
    while i < n:
        tok_text = tokens[i]["token"]
        if is_address_opener(tok_text) or is_modern_2p_at_line_start(tokens, i):
            for j in range(i, min(i + WINDOW, n)):
                in_window[j] = True
            i += WINDOW
        else:
            i += 1
    return in_window

def analyze():
    with open(RESULTS_FILE) as f:
        data = json.load(f)

    raw = data if isinstance(data, list) else data.get("poems", [])
    # Normalize: support both flat and metadata-wrapped formats
    poems = []
    for p in raw:
        if "metadata" in p:
            flat = dict(p["metadata"])
            flat["tokens"] = p.get("tokens", [])
            flat["summary"] = p.get("summary", {})
        else:
            flat = p
        poems.append(flat)
    # filter English poems with token data
    poems = [p for p in poems if p.get("language", "en") == "en"
             and p.get("tokens") and len(p["tokens"]) > 15]

    results = []
    all_address_s2 = []
    all_non_address_s2 = []

    for poem in poems:
        tokens = poem["tokens"]
        flags = label_tokens(tokens)

        addr_s2  = [t["s2"] for t, f in zip(tokens, flags) if f     and t.get("s2") is not None]
        non_s2   = [t["s2"] for t, f in zip(tokens, flags) if not f and t.get("s2") is not None]

        if not addr_s2 or not non_s2:
            # poem has no address windows — record as non-address only
            results.append({
                "title": poem.get("title"),
                "author": poem.get("author"),
                "year": poem.get("year"),
                "era": poem.get("era"),
                "has_address": False,
                "n_address_tokens": 0,
                "n_non_address_tokens": len(non_s2),
                "mean_s2_address": None,
                "mean_s2_non_address": statistics.mean(non_s2) if non_s2 else None,
                "apostrophe_lift": None,
            })
            all_non_address_s2.extend(non_s2)
            continue

        mean_addr = statistics.mean(addr_s2)
        mean_non  = statistics.mean(non_s2)
        lift = mean_addr - mean_non

        # Gather high-S2 address tokens for inspection
        top_addr = sorted(
            [t for t, f in zip(tokens, flags) if f and t.get("s2") is not None],
            key=lambda t: t["s2"],
            reverse=True
        )[:5]

        results.append({
            "title":  poem.get("title"),
            "author": poem.get("author"),
            "year":   poem.get("year"),
            "era":    poem.get("era"),
            "has_address": True,
            "n_address_tokens":     len(addr_s2),
            "n_non_address_tokens": len(non_s2),
            "mean_s2_address":     round(mean_addr, 4),
            "mean_s2_non_address": round(mean_non,  4),
            "apostrophe_lift":     round(lift, 4),
            "top_address_tokens": [
                {
                    "token": t["token"],
                    "s2": round(t["s2"], 3),
                    "surprisal": round(t.get("surprisal", 0), 3),
                    "entropy": round(t.get("entropy", 0), 3),
                    "top1_alternative": (t.get("alternatives") or [{}])[0].get("token", ""),
                }
                for t in top_addr
            ],
        })

        all_address_s2.extend(addr_s2)
        all_non_address_s2.extend(non_s2)

    # Poems with address windows
    with_addr = [r for r in results if r["has_address"]]
    without_addr = [r for r in results if not r["has_address"]]

    # Aggregate stats
    aggregate = {
        "n_poems_with_address":    len(with_addr),
        "n_poems_without_address": len(without_addr),
        "global_mean_s2_address":     round(statistics.mean(all_address_s2),     4) if all_address_s2     else None,
        "global_mean_s2_non_address": round(statistics.mean(all_non_address_s2), 4) if all_non_address_s2 else None,
        "global_apostrophe_lift":     round(
            statistics.mean(all_address_s2) - statistics.mean(all_non_address_s2), 4
        ) if all_address_s2 and all_non_address_s2 else None,
    }

    # Rank by lift
    ranked_positive = sorted(with_addr, key=lambda r: r["apostrophe_lift"], reverse=True)[:10]
    ranked_negative = sorted(with_addr, key=lambda r: r["apostrophe_lift"])[:10]

    # Era breakdown
    era_data = defaultdict(lambda: {"addr": [], "non": []})
    for r in with_addr:
        era_data[r["era"]]["addr"].append(r["mean_s2_address"])
        era_data[r["era"]]["non"].append(r["mean_s2_non_address"])

    era_summary = {}
    for era, d in era_data.items():
        if d["addr"] and d["non"]:
            era_summary[era] = {
                "n_poems": len(d["addr"]),
                "mean_s2_address":     round(statistics.mean(d["addr"]), 4),
                "mean_s2_non_address": round(statistics.mean(d["non"]),  4),
                "lift": round(statistics.mean(d["addr"]) - statistics.mean(d["non"]), 4),
            }

    output = {
        "aggregate": aggregate,
        "era_summary": era_summary,
        "top_positive_lift": ranked_positive,
        "top_negative_lift": ranked_negative,
        "all_poems": results,
    }

    with open(OUTPUT_FILE, "w") as f:
        json.dump(output, f, indent=2)

    # ── Print summary ────────────────────────────────────────────────────────
    print("=" * 60)
    print("SECOND-PERSON DIRECT ADDRESS vs. S₂")
    print("=" * 60)
    print(f"\nPoems with address windows:    {aggregate['n_poems_with_address']}")
    print(f"Poems without address windows: {aggregate['n_poems_without_address']}")
    print(f"\nGlobal mean S₂ in address windows:     {aggregate['global_mean_s2_address']}")
    print(f"Global mean S₂ in non-address text:    {aggregate['global_mean_s2_non_address']}")
    print(f"Global apostrophe lift:                {aggregate['global_apostrophe_lift']}")

    print("\n── Era breakdown (lift = address_mean − non_address_mean) ──")
    for era, s in sorted(era_summary.items(), key=lambda x: -(x[1]["lift"] or 0)):
        addr = s['mean_s2_address']
        non  = s['mean_s2_non_address']
        lift = s['lift']
        if addr is None or non is None or era is None:
            continue
        era_str = str(era)
        print(f"  {era_str:25s}  n={s['n_poems']:3d}  addr={addr:+.3f}  non={non:+.3f}  lift={lift:+.3f}")

    print("\n── Top 8 poems by POSITIVE apostrophe lift ──")
    for r in ranked_positive[:8]:
        author = str(r.get('author') or 'Unknown')
        title  = str(r.get('title')  or 'Untitled')
        print(f"  [{r['year']}] {author:30s} '{title[:35]}'  lift={r['apostrophe_lift']:+.3f}  n_addr={r['n_address_tokens']}")
        for t in r.get("top_address_tokens", [])[:2]:
            print(f"        '{t['token']}' (S₂={t['s2']:+.2f}) ← GPT-2 wanted '{t['top1_alternative']}'")

    print("\n── Top 8 poems by NEGATIVE apostrophe lift ──")
    for r in ranked_negative[:8]:
        author = str(r.get('author') or 'Unknown')
        title  = str(r.get('title')  or 'Untitled')
        print(f"  [{r['year']}] {author:30s} '{title[:35]}'  lift={r['apostrophe_lift']:+.3f}  n_addr={r['n_address_tokens']}")

    print(f"\nResults saved → {OUTPUT_FILE}")

if __name__ == "__main__":
    analyze()
