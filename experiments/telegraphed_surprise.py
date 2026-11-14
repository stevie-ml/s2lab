"""
Telegraphed Surprise: Did GPT-2 Almost Predict It One Step Early?

For every high-S2 token (s2 > 2.0, non-artifact), check whether that
token text appeared anywhere in the PREVIOUS position's top-10 alternatives.

If yes → the surprise was "telegraphed": GPT-2 had it in mind one position early.
If no  → the surprise was "ambush": GPT-2 had no foreshadowing.

This asks: do poets set up surprising words by putting them in the
nearby alternative space before deploying them?
"""

import json
from collections import defaultdict, Counter

RESULTS_PATH = "results/corpus_results.json"
S2_THRESHOLD = 2.0
P_NEWLINE_ARTIFACT = 0.9
MIN_TOKENS = 5


def is_artifact(tok):
    return tok.get("p_newline", 0) >= P_NEWLINE_ARTIFACT


def is_whitespace_or_newline(tok):
    text = tok.get("token", "").strip()
    return len(text) == 0 or text == "\n"


def is_pure_punctuation(tok):
    text = tok.get("token", "").strip()
    return len(text) > 0 and all(c in '.,;:!?\'"-—()[]{}' for c in text)


def normalize_token(t):
    return t.strip().lower()


def run():
    with open(RESULTS_PATH) as f:
        data = json.load(f)

    # Overall counts
    total_spikes = 0
    telegraphed = 0
    ambush = 0

    # Baseline: non-spike positions
    total_baseline = 0
    baseline_telegraphed = 0

    # By era
    era_stats = defaultdict(lambda: {"spikes": 0, "telegraphed": 0})

    # Detailed examples: telegraphed and ambush
    telegraphed_examples = []  # (s2, prev_token, actual_token, prev_alt_rank, era, title, author)
    ambush_examples = []

    # Distribution: at what rank in alternatives was the telegraphed token?
    alt_rank_distribution = Counter()

    # Rate by spike magnitude bucket
    s2_buckets = {
        "2-3": {"spikes": 0, "telegraphed": 0},
        "3-5": {"spikes": 0, "telegraphed": 0},
        "5-10": {"spikes": 0, "telegraphed": 0},
        "10+": {"spikes": 0, "telegraphed": 0},
    }

    for poem in data:
        meta = poem["metadata"]
        era = meta.get("era", "unknown")
        title = meta.get("title", "")
        author = meta.get("author", "")
        tokens = poem["tokens"]

        if len(tokens) < MIN_TOKENS:
            continue

        for i, tok in enumerate(tokens):
            # Skip artifact positions, whitespace, and punctuation
            if is_artifact(tok):
                continue
            if is_whitespace_or_newline(tok):
                continue
            if is_pure_punctuation(tok):
                continue

            s2 = tok.get("s2", 0)
            if s2 < S2_THRESHOLD:
                continue

            # Skip position 0 — no previous token
            if i == 0:
                continue

            prev_tok = tokens[i - 1]
            # Skip if previous position is an artifact
            if is_artifact(prev_tok):
                continue

            actual_text = normalize_token(tok["token"])
            prev_alts = prev_tok.get("alternatives", [])

            # Check if actual token appears in previous alternatives
            found_rank = None
            for rank_in_alts, alt in enumerate(prev_alts):
                if normalize_token(alt["token"]) == actual_text:
                    found_rank = rank_in_alts + 1  # 1-indexed
                    break

            total_spikes += 1
            era_stats[era]["spikes"] += 1

            # S2 bucket
            if s2 < 3:
                bucket = "2-3"
            elif s2 < 5:
                bucket = "3-5"
            elif s2 < 10:
                bucket = "5-10"
            else:
                bucket = "10+"
            s2_buckets[bucket]["spikes"] += 1

            if found_rank is not None:
                telegraphed += 1
                era_stats[era]["telegraphed"] += 1
                s2_buckets[bucket]["telegraphed"] += 1
                alt_rank_distribution[found_rank] += 1
                if len(telegraphed_examples) < 20:
                    telegraphed_examples.append({
                        "s2": round(s2, 2),
                        "prev_token": prev_tok["token"],
                        "actual_token": tok["token"],
                        "alt_rank": found_rank,
                        "era": era,
                        "title": title,
                        "author": author,
                        "entropy": round(tok.get("entropy", 0), 2),
                        "rank_in_poem": tok.get("rank", "?"),
                    })
            else:
                ambush += 1
                if len(ambush_examples) < 10:
                    ambush_examples.append({
                        "s2": round(s2, 2),
                        "prev_token": prev_tok["token"],
                        "actual_token": tok["token"],
                        "era": era,
                        "title": title,
                        "author": author,
                        "prev_top3": [a["token"] for a in prev_alts[:3]],
                    })

        # Baseline: non-spike positions (s2 < 0, clean, non-punct)
        for i, tok in enumerate(tokens):
            if is_artifact(tok) or is_whitespace_or_newline(tok) or is_pure_punctuation(tok):
                continue
            s2 = tok.get("s2", 0)
            if s2 >= S2_THRESHOLD or s2 < -5:  # only mild baseline
                continue
            if i == 0:
                continue
            prev_tok = tokens[i - 1]
            if is_artifact(prev_tok):
                continue
            actual_text = normalize_token(tok["token"])
            prev_alts = prev_tok.get("alternatives", [])
            found = any(normalize_token(a["token"]) == actual_text for a in prev_alts)
            total_baseline += 1
            if found:
                baseline_telegraphed += 1

    # Era rates
    era_rates = []
    for era, stats in era_stats.items():
        if stats["spikes"] >= 5:
            rate = stats["telegraphed"] / stats["spikes"]
            era_rates.append((era, stats["spikes"], stats["telegraphed"], round(rate, 3)))
    era_rates.sort(key=lambda x: -x[3])

    # Sort examples by S2
    telegraphed_examples.sort(key=lambda x: -x["s2"])
    ambush_examples.sort(key=lambda x: -x["s2"])

    baseline_rate = round(baseline_telegraphed / total_baseline, 4) if total_baseline > 0 else 0

    result = {
        "summary": {
            "total_spikes": total_spikes,
            "telegraphed": telegraphed,
            "ambush": ambush,
            "telegraphed_rate": round(telegraphed / total_spikes, 4) if total_spikes > 0 else 0,
            "s2_threshold": S2_THRESHOLD,
            "baseline_total": total_baseline,
            "baseline_telegraphed": baseline_telegraphed,
            "baseline_rate": baseline_rate,
        },
        "s2_bucket_rates": {
            bucket: {
                "spikes": v["spikes"],
                "telegraphed": v["telegraphed"],
                "rate": round(v["telegraphed"] / v["spikes"], 4) if v["spikes"] > 0 else 0,
            }
            for bucket, v in s2_buckets.items()
        },
        "alt_rank_distribution": dict(sorted(alt_rank_distribution.items())),
        "era_rates": [
            {"era": e, "spikes": n, "telegraphed": t, "rate": r}
            for e, n, t, r in era_rates
        ],
        "telegraphed_examples": telegraphed_examples[:20],
        "ambush_examples": ambush_examples[:10],
    }

    out_path = "results/telegraphed_surprise.json"
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)

    print(f"Results saved to {out_path}")
    return result


if __name__ == "__main__":
    result = run()
    s = result["summary"]
    print(f"\nTotal spikes (s2>{s['s2_threshold']}, clean): {s['total_spikes']}")
    print(f"Telegraphed (token in prev alternatives): {s['telegraphed']} ({s['telegraphed_rate']*100:.1f}%)")
    print(f"True ambush: {s['ambush']} ({100-s['telegraphed_rate']*100:.1f}%)")
    print(f"Baseline (non-spike) telegraphed rate: {s['baseline_rate']*100:.1f}% ({s['baseline_telegraphed']}/{s['baseline_total']})")
    print(f"Surprise-to-baseline ratio: {s['telegraphed_rate']/s['baseline_rate']:.2f}x")

    print("\nBy S2 magnitude:")
    for bucket, v in result["s2_bucket_rates"].items():
        print(f"  {bucket}: {v['telegraphed']}/{v['spikes']} = {v['rate']*100:.1f}%")

    print("\nAlt rank distribution for telegraphed:")
    for rank, count in sorted(result["alt_rank_distribution"].items()):
        print(f"  Rank {rank}: {count}")

    print("\nTop eras by telegraphing rate:")
    for row in result["era_rates"][:10]:
        print(f"  {row['era']:25s}: {row['rate']*100:.1f}% ({row['telegraphed']}/{row['spikes']})")

    print("\nSample telegraphed surprises:")
    for ex in result["telegraphed_examples"][:5]:
        print(f"  [{ex['era']}] {ex['author']!r}: ...{ex['prev_token']!r}→{ex['actual_token']!r} (s2={ex['s2']}, was alt rank {ex['alt_rank']})")

    print("\nSample ambush surprises:")
    for ex in result["ambush_examples"][:5]:
        print(f"  [{ex['era']}] {ex['author']!r}: ...{ex['prev_token']!r}→{ex['actual_token']!r} (s2={ex['s2']}, prev top3={ex['prev_top3']})")
