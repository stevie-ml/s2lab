"""
Focus Particles and S2 in Poetry

Focus particles (only, even, still, yet, just, merely, also, too, almost, quite)
are small words that carry disproportionate semantic weight. In poetry, "only"
or "even" often pivot an entire line's meaning. This experiment asks:

1. Do focus particles themselves show high or low S2?
2. Do tokens immediately AFTER focus particles show elevated S2?
3. Which poets use focus particles most effectively?
4. Compare poetry vs. prose control texts.
"""

import json
import re
from collections import defaultdict

RESULTS_PATH = "results/corpus_results.json"

# Focus particles — function words with intensifying/limiting/focusing semantics
FOCUS_PARTICLES = {
    "only", "even", "still", "yet", "just", "merely", "also", "too",
    "almost", "quite", "hardly", "scarcely", "barely", "never",
    "always", "ever", "already", "again", "once", "alone", "very",
    "so", "such", "both", "neither", "either",
}

# For GPT-2, tokens for these words:
FOCUS_PARTICLE_STRINGS = FOCUS_PARTICLES | {
    " only", " even", " still", " yet", " just", " merely", " also", " too",
    " almost", " quite", " hardly", " scarcely", " barely", " never",
    " always", " ever", " already", " again", " once", " alone", " very",
    " so", " such", " both", " neither", " either",
    "Only", " Only", "Even", " Even", "Still", " Still", "Yet", " Yet",
    "Just", " Just", "Never", " Never", "Always", " Always",
}


def load_results():
    with open(RESULTS_PATH) as f:
        return json.load(f)


def is_focus_particle(token_str):
    t = token_str.strip()
    return t.lower() in FOCUS_PARTICLES


def analyze_focus_particles(data):
    corpus_s2_all = []
    focus_particle_s2 = []
    post_focus_s2 = []  # S2 of token immediately after a focus particle

    by_poem = defaultdict(lambda: {
        "title": "",
        "author": "",
        "era": "",
        "is_control": False,
        "focus_count": 0,
        "focus_s2_sum": 0.0,
        "post_focus_s2_sum": 0.0,
        "total_tokens": 0,
    })

    particle_details = []  # (particle, post_token, s2_particle, s2_post, author, title)

    for poem in data:
        meta = poem.get("metadata", {})
        title = meta.get("title", "")
        author = meta.get("author", "")
        era = meta.get("era", "")
        tokens = poem.get("tokens", [])
        is_control = era in ("control", "prose_control") or "control" in era.lower()
        key = f"{author}|||{title}"
        by_poem[key]["title"] = title
        by_poem[key]["author"] = author
        by_poem[key]["era"] = era
        by_poem[key]["is_control"] = is_control
        by_poem[key]["total_tokens"] += len(tokens)

        for i, tok in enumerate(tokens):
            s2 = tok.get("s2", None)
            if s2 is None:
                continue
            token_str = tok.get("token", "")
            corpus_s2_all.append(s2)

            if is_focus_particle(token_str):
                focus_particle_s2.append(s2)
                by_poem[key]["focus_count"] += 1
                by_poem[key]["focus_s2_sum"] += s2

                # Look at the next token
                if i + 1 < len(tokens):
                    next_tok = tokens[i + 1]
                    next_s2 = next_tok.get("s2", None)
                    next_str = next_tok.get("token", "")
                    if next_s2 is not None:
                        post_focus_s2.append(next_s2)
                        by_poem[key]["post_focus_s2_sum"] += next_s2
                        particle_details.append({
                            "particle": token_str.strip(),
                            "post_token": next_str.strip(),
                            "s2_particle": s2,
                            "s2_post": next_s2,
                            "author": author,
                            "title": title,
                            "era": era,
                        })

    return corpus_s2_all, focus_particle_s2, post_focus_s2, by_poem, particle_details


def mean(lst):
    return sum(lst) / len(lst) if lst else 0.0


def report():
    data = load_results()
    corpus_s2_all, focus_s2, post_focus_s2, by_poem, details = analyze_focus_particles(data)

    corpus_mean = mean(corpus_s2_all)
    focus_mean = mean(focus_s2)
    post_focus_mean = mean(post_focus_s2)

    print("=" * 60)
    print("FOCUS PARTICLES AND S2")
    print("=" * 60)
    print(f"Corpus mean S2:              {corpus_mean:+.4f}")
    print(f"Focus particle mean S2:      {focus_mean:+.4f}  (n={len(focus_s2)})")
    print(f"Post-focus-particle mean S2: {post_focus_mean:+.4f}  (n={len(post_focus_s2)})")
    print()

    # Separate poetry vs. control
    poetry_focus = []
    control_focus = []
    poetry_post = []
    control_post = []
    for d in details:
        if d["era"] in ("control", "prose_control") or "control" in d["era"].lower():
            control_focus.append(d["s2_particle"])
            control_post.append(d["s2_post"])
        else:
            poetry_focus.append(d["s2_particle"])
            poetry_post.append(d["s2_post"])

    print(f"Poetry focus particle S2:   {mean(poetry_focus):+.4f}  (n={len(poetry_focus)})")
    print(f"Control focus particle S2:  {mean(control_focus):+.4f}  (n={len(control_focus)})")
    print(f"Poetry post-focus S2:       {mean(poetry_post):+.4f}  (n={len(poetry_post)})")
    print(f"Control post-focus S2:      {mean(control_post):+.4f}  (n={len(control_post)})")
    print()

    # Which particles show highest S2 contrast (post-focus vs. corpus)?
    by_particle = defaultdict(list)
    for d in details:
        by_particle[d["particle"]].append(d["s2_post"])

    print("Per-particle post-focus S2 (n >= 5, sorted by avg S2):")
    rows = []
    for p, vals in by_particle.items():
        if len(vals) >= 5:
            rows.append((p, mean(vals), len(vals)))
    rows.sort(key=lambda x: -x[1])
    for p, avg, n in rows:
        print(f"  '{p}': post-S2={avg:+.3f}  (n={n})")
    print()

    # Poems with highest focus particle density and post-focus S2
    ranked = []
    for key, d in by_poem.items():
        if d["focus_count"] >= 3 and d["total_tokens"] > 20:
            density = d["focus_count"] / d["total_tokens"]
            avg_post = d["post_focus_s2_sum"] / d["focus_count"] if d["focus_count"] else 0
            ranked.append((d["author"], d["title"], d["era"], d["focus_count"],
                           density, avg_post, d["is_control"]))
    ranked.sort(key=lambda x: -x[5])

    print("Top poems by avg post-focus-particle S2 (focus_count >= 3):")
    print(f"{'Author':<25} {'Title':<35} {'Era':<18} {'n':<4} {'density':<8} {'avg_post_S2'}")
    print("-" * 105)
    for row in ranked[:20]:
        author, title, era, fc, dens, avg_post, is_ctrl = row
        ctrl_marker = " [ctrl]" if is_ctrl else ""
        print(f"{author[:24]:<25} {title[:34]:<35} {era[:17]:<18} {fc:<4} {dens:.3f}    {avg_post:+.3f}{ctrl_marker}")
    print()

    # Most striking examples: high post-focus S2
    print("Most striking focus-particle → next-token S2 spikes (post-S2 > 5):")
    high = [d for d in details if d["s2_post"] > 5.0]
    high.sort(key=lambda x: -x["s2_post"])
    for d in high[:25]:
        print(f"  S2_post={d['s2_post']:+.2f}  '{d['particle']}' → '{d['post_token']}'  "
              f"| {d['author']}, \"{d['title'][:40]}\"")
    print()

    # By era
    by_era = defaultdict(list)
    for d in details:
        by_era[d["era"]].append(d["s2_post"])

    print("Post-focus S2 by era (n >= 5):")
    era_rows = [(era, mean(vals), len(vals)) for era, vals in by_era.items() if len(vals) >= 5]
    era_rows.sort(key=lambda x: -x[1])
    for era, avg, n in era_rows:
        print(f"  {era:<25} post-S2={avg:+.4f}  n={n}")

    return {
        "corpus_mean": corpus_mean,
        "focus_mean": focus_mean,
        "post_focus_mean": post_focus_mean,
        "poetry_focus_mean": mean(poetry_focus),
        "control_focus_mean": mean(control_focus),
        "poetry_post_focus_mean": mean(poetry_post),
        "control_post_focus_mean": mean(control_post),
        "by_particle": {p: {"mean_post_s2": mean(v), "n": len(v)}
                        for p, v in by_particle.items() if len(v) >= 3},
        "top_examples": [d for d in sorted(details, key=lambda x: -x["s2_post"])[:30]],
        "era_breakdown": {era: {"mean": mean(v), "n": len(v)}
                          for era, v in by_era.items() if len(v) >= 5},
    }


if __name__ == "__main__":
    results = report()
    out_path = "results/focus_particles_s2.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {out_path}")
