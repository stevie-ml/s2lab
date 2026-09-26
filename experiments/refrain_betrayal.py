"""
Refrain betrayal: what happens when a poet breaks an established in-context copy?

For every token t_i we find the longest suffix of the preceding context
(t_{i-L}..t_{i-1}) that already occurred earlier in the same poem, ending at j-1.
That earlier occurrence implies a "copy prediction" t_j. If t_i == t_j the poet
HONORED the copy; otherwise the poet BETRAYED it.

Measures:
  1. Lock-in curve: entropy / S2 / copy-hit rate as a function of matched length L
  2. Betrayal vs honored vs baseline S2 (artifact-free, L >= MIN_L)
  3. Share of the corpus's top-S2 tokens that are betrayals vs their base rate
  4. Every betrayal listed with the copy target the model was steered toward
"""
import json
import os
import statistics as st
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MIN_L = 3
ARTIFACT_P = 0.9
EXCLUDE_ERAS = {"control", "cliche_control"}


def longest_prior_match(toks, i):
    """Return (L, j) for the longest suffix ending at i-1 that also ends at some j-1 < i-1."""
    best_L, best_j = 0, None
    for j in range(1, i):
        L = 0
        while L < j and toks[j - 1 - L] == toks[i - 1 - L]:
            L += 1
        if L >= best_L and L > 0:  # ties -> most recent occurrence
            best_L, best_j = L, j
    return best_L, best_j


def fmt(tok):
    return tok.replace("\n", "⏎")


def main():
    with open(os.path.join(ROOT, "results", "corpus_results.json")) as f:
        data = json.load(f)

    rows = []
    baseline = []
    for poem in data:
        md = poem["metadata"]
        if md["era"] in EXCLUDE_ERAS:
            continue
        toks_d = poem["tokens"]
        toks = [t["token"] for t in toks_d]
        for i, t in enumerate(toks_d):
            if t.get("p_newline", 0) >= ARTIFACT_P:
                continue
            baseline.append(t["s2"])
            L, j = longest_prior_match(toks, i)
            if j is None:
                continue
            target = toks[j]
            alts = t.get("alternatives") or []
            top1 = alts[0]["token"] if alts else None
            p_target = next((a["prob"] for a in alts if a["token"] == target), 0.0)
            reentry = None
            if t["token"] != target and L >= MIN_L and i + 1 < len(toks) and j + 1 < i:
                nxt = toks_d[i + 1]
                nalts = nxt.get("alternatives") or []
                reentry = {
                    "resumes": toks[i + 1] == toks[j + 1],
                    "s2": nxt["s2"],
                    "model_expects_resume": bool(nalts) and nalts[0]["token"] == toks[j + 1],
                    "artifact": nxt.get("p_newline", 0) >= ARTIFACT_P,
                }
            rows.append({
                "reentry": reentry,
                "poem": md["title"], "author": md["author"], "era": md["era"],
                "lang": md.get("language", "en"), "i": i, "L": L,
                "token": t["token"], "target": target,
                "honored": t["token"] == target,
                "model_copies": top1 == target,
                "p_target": p_target,
                "s2": t["s2"], "entropy": t["entropy"], "surprisal": t["surprisal"],
                "rank": t["rank"],
                "context": "".join(toks[max(0, i - 8):i]),
            })

    out = {"n_tokens_clean": len(baseline), "baseline_mean_s2": st.mean(baseline)}
    print(f"Artifact-free tokens: {len(baseline)}  baseline mean S2 = {st.mean(baseline):+.2f}")

    # 1. Lock-in curve
    print("\n## Lock-in curve (by matched prefix length L)")
    print("| L | n | honored % | model top-1 = copy % | mean entropy | mean S2 (honored) | mean S2 (betrayed) |")
    print("|---|---|---|---|---|---|---|")
    curve = []
    buckets = [(1, 1), (2, 2), (3, 3), (4, 5), (6, 9), (10, 10**6)]
    for lo, hi in buckets:
        b = [r for r in rows if lo <= r["L"] <= hi]
        if not b:
            continue
        hon = [r for r in b if r["honored"]]
        bet = [r for r in b if not r["honored"]]
        rec = {
            "L": f"{lo}" if lo == hi else (f"{lo}-{hi}" if hi < 10**6 else f"{lo}+"),
            "n": len(b),
            "honored_pct": 100 * len(hon) / len(b),
            "model_copies_pct": 100 * sum(r["model_copies"] for r in b) / len(b),
            "entropy": st.mean(r["entropy"] for r in b),
            "s2_honored": st.mean(r["s2"] for r in hon) if hon else None,
            "s2_betrayed": st.mean(r["s2"] for r in bet) if bet else None,
        }
        curve.append(rec)
        f = lambda x: "—" if x is None else f"{x:+.2f}"
        print(f"| {rec['L']} | {rec['n']} | {rec['honored_pct']:.1f}% | {rec['model_copies_pct']:.1f}% | "
              f"{rec['entropy']:.2f} | {f(rec['s2_honored'])} | {f(rec['s2_betrayed'])} |")
    out["lock_in_curve"] = curve

    # 2. Betrayal vs honored at L >= MIN_L
    strong = [r for r in rows if r["L"] >= MIN_L]
    hon = [r for r in strong if r["honored"]]
    bet = [r for r in strong if not r["honored"]]
    bet_confident = [r for r in bet if r["model_copies"]]
    print(f"\n## Established copies (L >= {MIN_L})")
    print("| Group | n | mean S2 | median S2 | mean entropy | mean surprisal |")
    print("|---|---|---|---|---|---|")
    lexical = lambda r: any(c.isalnum() for c in r["token"]) and any(c.isalnum() for c in r["target"])
    groups = {
        "honored": hon, "betrayed (all)": bet,
        "betrayed, model was copying": bet_confident,
        "betrayed, model copying, word→word": [r for r in bet_confident if lexical(r)],
        "betrayed, model copying, involves punct/space": [r for r in bet_confident if not lexical(r)],
    }
    out["groups"] = {}
    for name, g in groups.items():
        if not g:
            continue
        rec = {"n": len(g), "mean_s2": st.mean(r["s2"] for r in g),
               "median_s2": st.median(r["s2"] for r in g),
               "entropy": st.mean(r["entropy"] for r in g),
               "surprisal": st.mean(r["surprisal"] for r in g)}
        out["groups"][name] = rec
        print(f"| {name} | {rec['n']} | {rec['mean_s2']:+.2f} | {rec['median_s2']:+.2f} | "
              f"{rec['entropy']:.2f} | {rec['surprisal']:.2f} |")
    print(f"| baseline (all clean tokens) | {len(baseline)} | {st.mean(baseline):+.2f} | "
          f"{st.median(baseline):+.2f} | — | — |")

    # 3. Over-representation among top-S2 tokens
    all_s2 = sorted(baseline, reverse=True)
    bet_s2 = sorted((r["s2"] for r in bet), reverse=True)
    base_rate = len(bet) / len(baseline)
    print(f"\n## Betrayals among the corpus's highest-S2 tokens (base rate {100*base_rate:.2f}%)")
    print("| Top-k | threshold S2 | betrayals | share | lift |")
    print("|---|---|---|---|---|")
    out["top_k"] = []
    for k in (25, 50, 100, 250, 500):
        thr = all_s2[k - 1]
        n_b = sum(1 for s in bet_s2 if s >= thr)
        share = n_b / k
        out["top_k"].append({"k": k, "threshold": thr, "betrayals": n_b, "share": share,
                             "lift": share / base_rate})
        print(f"| {k} | {thr:.2f} | {n_b} | {100*share:.1f}% | {share/base_rate:.1f}× |")

    # Betrayal typology by what was expected vs what was written
    kind = lambda s: "space" if s.strip() == "" else ("word" if any(c.isalnum() for c in s) else "punct")
    types = {("punct", "word"): "extension", ("word", "word"): "substitution",
             ("word", "punct"): "truncation", ("punct", "punct"): "repunctuation"}
    print(f"\n## Betrayal typology (L >= {MIN_L}; whitespace-involved cases excluded)")
    print("| Type | n | mean S2 | mean S2 (model copying) | in top-100 | in top-500 | top-100 lift |")
    print("|---|---|---|---|---|---|---|")
    out["typology"] = {}
    n_space = sum(1 for r in bet if "space" in (kind(r["target"]), kind(r["token"])))
    for key, name in types.items():
        g = [r for r in bet if (kind(r["target"]), kind(r["token"])) == key]
        if not g:
            continue
        gc = [r["s2"] for r in g if r["model_copies"]]
        t100 = sum(r["s2"] >= all_s2[99] for r in g)
        t500 = sum(r["s2"] >= all_s2[499] for r in g)
        lift = (t100 / 100) / (len(g) / len(baseline))
        out["typology"][name] = {"n": len(g), "mean_s2": st.mean(r["s2"] for r in g),
                                 "mean_s2_model_copying": st.mean(gc) if gc else None,
                                 "n_model_copying": len(gc), "top100": t100, "top500": t500,
                                 "top100_lift": lift}
        mc = f"{st.mean(gc):+.2f} (n={len(gc)})" if gc else "—"
        print(f"| {name} | {len(g)} | {st.mean(r['s2'] for r in g):+.2f} | {mc} | {t100} | {t500} | {lift:.0f}× |")
    print(f"(whitespace-involved betrayals excluded: {n_space})")

    # Re-entry: the token after a betrayal, when the poet resumes the earlier line
    re_rows = [r["reentry"] for r in bet if r["reentry"] and not r["reentry"]["artifact"]]
    resumed = [x for x in re_rows if x["resumes"]]
    diverged = [x for x in re_rows if not x["resumes"]]
    print("\n## Re-entry: token after a betrayal")
    print("| Next token | n | mean S2 | median S2 | model expected the resume |")
    print("|---|---|---|---|---|")
    out["reentry"] = {}
    for name, g in (("poet resumes the earlier line", resumed), ("poet keeps diverging", diverged)):
        if not g:
            continue
        rec = {"n": len(g), "mean_s2": st.mean(x["s2"] for x in g),
               "median_s2": st.median(x["s2"] for x in g),
               "model_expects_resume_pct": 100 * sum(x["model_expects_resume"] for x in g) / len(g)}
        out["reentry"][name] = rec
        print(f"| {name} | {rec['n']} | {rec['mean_s2']:+.2f} | {rec['median_s2']:+.2f} | "
              f"{rec['model_expects_resume_pct']:.0f}% |")

    # Positive-S2 rate
    pos = lambda g: 100 * sum(r["s2"] > 0 for r in g) / len(g)
    print(f"\n+S2 rate: honored {pos(hon):.1f}%, betrayed {pos(bet):.1f}%, "
          f"betrayed&model-copying {pos(bet_confident):.1f}%, "
          f"baseline {100*sum(s>0 for s in baseline)/len(baseline):.1f}%")
    out["pos_rate"] = {"honored": pos(hon), "betrayed": pos(bet),
                       "betrayed_model_copying": pos(bet_confident),
                       "baseline": 100 * sum(s > 0 for s in baseline) / len(baseline)}

    # 4. Content vs function betrayals / list
    print(f"\n## Strongest betrayals (L >= {MIN_L}, model top-1 = copy target)")
    print("| S2 | L | p(copy) | context | copy target | poet wrote | poet |")
    print("|---|---|---|---|---|---|---|")
    top = sorted(bet_confident, key=lambda r: -r["s2"])
    for r in top[:25]:
        print(f"| {r['s2']:.2f} | {r['L']} | {r['p_target']:.2f} | `{fmt(r['context'][-40:])}` | "
              f"`{fmt(r['target'])}` | `{fmt(r['token'])}` | {r['author']} — {r['poem']} |")
    out["top_betrayals"] = top[:40]

    # Designed refrain-variation test set: every departure from an established copy
    test_set = {"The Tyger", "The Raven (opening stanzas)", "Tears, Idle Tears",
                "Break, Break, Break", "The Lady of Shalott (Part I)", "Recessional (stanzas 1-3)"}
    print(f"\n## Refrain-variation test set: departures with L >= {MIN_L}")
    print("| Poem | L | model top-1 = copy | copy target | poet wrote | S2 | entropy |")
    print("|---|---|---|---|---|---|---|")
    out["test_set"] = []
    for r in sorted((r for r in bet if r["poem"] in test_set), key=lambda r: (r["poem"], r["i"])):
        out["test_set"].append(r)
        print(f"| {r['poem']} | {r['L']} | {'yes' if r['model_copies'] else 'no'} | `{fmt(r['target'])}` | "
              f"`{fmt(r['token'])}` | {r['s2']:+.2f} | {r['entropy']:.2f} |")

    # Per-poem betrayal profile
    per = defaultdict(lambda: {"hon": 0, "bet": 0, "bet_s2": []})
    for r in strong:
        p = per[(r["author"], r["poem"])]
        if r["honored"]:
            p["hon"] += 1
        else:
            p["bet"] += 1
            p["bet_s2"].append(r["s2"])
    print(f"\n## Poems with most established-copy events (L >= {MIN_L})")
    print("| Poem | honored | betrayed | betrayal rate | mean betrayal S2 |")
    print("|---|---|---|---|---|")
    ranked = sorted(per.items(), key=lambda kv: -(kv[1]["hon"] + kv[1]["bet"]))
    out["per_poem"] = []
    for (a, t), p in ranked[:20]:
        tot = p["hon"] + p["bet"]
        mb = st.mean(p["bet_s2"]) if p["bet_s2"] else None
        out["per_poem"].append({"author": a, "poem": t, "honored": p["hon"], "betrayed": p["bet"],
                                "mean_betrayal_s2": mb})
        print(f"| {a} — {t} | {p['hon']} | {p['bet']} | {100*p['bet']/tot:.0f}% | "
              f"{'—' if mb is None else f'{mb:+.2f}'} |")

    with open(os.path.join(ROOT, "results", "refrain_betrayal.json"), "w") as f:
        json.dump(out, f, indent=2)


if __name__ == "__main__":
    main()
