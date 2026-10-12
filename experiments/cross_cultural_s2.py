"""
Cross-Cultural Poetic Signatures: S2 in Classical Chinese, Persian, and Japanese Tanka.

Tests whether poems from non-Western traditions, translated into English, show
distinctive information-theoretic profiles compared to Western poetry of comparable
historical periods. Specifically tests:

H1 (Terse Syntax): Classical Chinese poems, famous for ellipsis and parataxis,
    should have higher S2 in their English translations because the terse English
    renderings violate GPT-2's expectation of full-clause syntax.

H2 (Sufi Paradox): Persian Sufi poetry (Rumi, Khayyam) uses mystical paradox and
    unusual imagery; these should produce higher S2 than Western court poetry.

H3 (Tanka Coda): Japanese tanka's 7-7 coda (compared to haiku's final 5) should
    distribute S2 differently — the coda resolves or deepens the opening image.

H4 (Translation Flattening): All translated poems from non-Western traditions may
    show LOWER S2 than original-language Western poems, because the translator
    normalizes syntax toward English expectations (flattening the exotic).
"""

import json
import os
import statistics
from collections import defaultdict

RESULTS_FILE = os.path.join(os.path.dirname(__file__), "..", "results", "corpus_results.json")
FINDINGS_DIR = os.path.join(os.path.dirname(__file__), "..", "findings")
ARTIFACT_P = 0.90


def newline_prob(tok):
    return sum(a["prob"] for a in tok["alternatives"] if a["token"].strip("\r\n") == "")


def clean_tokens(tokens):
    return [t for t in tokens if newline_prob(t) < ARTIFACT_P]


def poem_stats(poem):
    tokens = poem["tokens"]
    clean = clean_tokens(tokens)
    if len(clean) < 5:
        return None
    s2s = [t["s2"] for t in clean]
    h_vals = [t["entropy"] for t in clean]
    return {
        "title": poem["metadata"]["title"],
        "author": poem["metadata"]["author"],
        "era": poem["metadata"]["era"],
        "year": poem["metadata"].get("year"),
        "n": len(clean),
        "avg_s2": statistics.mean(s2s),
        "std_s2": statistics.stdev(s2s) if len(s2s) > 1 else 0,
        "pos_ratio": sum(1 for x in s2s if x > 0) / len(s2s),
        "avg_h": statistics.mean(h_vals),
        "max_s2": max(s2s),
        "p90_s2": sorted(s2s)[int(len(s2s) * 0.9)],
    }


def main():
    with open(RESULTS_FILE) as f:
        results = json.load(f)

    # Group by era
    era_groups = defaultdict(list)
    for r in results:
        era = r["metadata"]["era"]
        st = poem_stats(r)
        if st:
            era_groups[era].append(st)

    # Eras we're comparing
    focus_eras = ["classical_chinese", "persian", "japanese_classical"]
    comparison_eras = [
        "haiku", "ancient", "medieval" , "metaphysical", "romantic",
        "victorian", "modernist", "imagist", "control",
    ]

    lines = []
    lines.append("# Cross-Cultural Poetic Signatures: S2 in Non-Western Traditions")
    lines.append("")
    lines.append("**Date:** 2026-10-12")
    lines.append("**Experiment:** `experiments/cross_cultural_s2.py`")
    lines.append(f"**New eras added:** classical_chinese ({len(era_groups.get('classical_chinese', []))} poems), "
                 f"persian ({len(era_groups.get('persian', []))} poems), "
                 f"japanese_classical ({len(era_groups.get('japanese_classical', []))} poems)")
    lines.append("")

    lines.append("## Research Question")
    lines.append("")
    lines.append("Do poems from Classical Chinese (Tang Dynasty, ~700-760 CE), Persian (Khayyam/Rumi, ~12th-13th c.), "
                 "and Japanese classical (tanka, ~880-905 CE) traditions show distinctive information-theoretic "
                 "profiles when analyzed in English translation, compared to Western poetry of similar periods?")
    lines.append("")
    lines.append("Four hypotheses tested:")
    lines.append("")
    lines.append("- **H1 (Terse Syntax):** Classical Chinese translations, characterized by ellipsis and parataxis, "
                 "should produce higher artifact-free S2 because they violate English clause-structure expectations.")
    lines.append("- **H2 (Sufi Paradox):** Persian Sufi poetry's mystical imagery should produce higher S2 than "
                 "comparable Western court/lyric verse.")
    lines.append("- **H3 (Tanka Arc):** Japanese tanka should have a different S2 distribution shape than haiku — "
                 "the coda (7-7) resolves the opening image, potentially dropping S2 there.")
    lines.append("- **H4 (Translation Flattening):** Alternatively, translators may normalize exotic syntax into "
                 "conventional English, producing LOWER S2 than native English poems of comparable age.")
    lines.append("")

    # Individual poem results for focus eras
    lines.append("## Individual Poem Results: New Eras")
    lines.append("")
    for era in focus_eras:
        poems = era_groups.get(era, [])
        if not poems:
            lines.append(f"### {era}: NO DATA (poems not yet analyzed)")
            lines.append("")
            continue
        lines.append(f"### {era} (n={len(poems)})")
        lines.append("")
        lines.append("| Poem | Author | Year | Avg S2 (clean) | +S2% | Max S2 | Avg H |")
        lines.append("|---|---|---|---|---|---|---|")
        for p in sorted(poems, key=lambda x: x["avg_s2"], reverse=True):
            lines.append(f"| {p['title'][:50]} | {p['author'][:30]} | {p['year']} | "
                         f"**{p['avg_s2']:.3f}** | {p['pos_ratio']*100:.0f}% | {p['max_s2']:.2f} | {p['avg_h']:.2f} |")
        lines.append("")

    # Era comparison table
    lines.append("## Era Comparison: Focus Eras vs. Western Baselines")
    lines.append("")
    lines.append("> Artifact-free S2 (p_newline < 0.9 tokens excluded)")
    lines.append("")
    lines.append("| Era | n poems | Avg S2 | +S2% | Avg H | Max S2 |")
    lines.append("|---|---|---|---|---|---|")

    # Collect all relevant eras
    all_eras_to_show = focus_eras + [e for e in comparison_eras if e in era_groups]
    era_summaries = {}
    for era in all_eras_to_show:
        poems = era_groups.get(era, [])
        if not poems:
            continue
        avg_s2 = statistics.mean(p["avg_s2"] for p in poems)
        pos_r = statistics.mean(p["pos_ratio"] for p in poems)
        avg_h = statistics.mean(p["avg_h"] for p in poems)
        max_s2 = max(p["max_s2"] for p in poems)
        era_summaries[era] = (len(poems), avg_s2, pos_r, avg_h, max_s2)

    for era in sorted(era_summaries, key=lambda e: era_summaries[e][1], reverse=True):
        n, avg_s2, pos_r, avg_h, max_s2 = era_summaries[era]
        marker = " ← **new**" if era in focus_eras else ""
        lines.append(f"| {era}{marker} | {n} | **{avg_s2:.3f}** | {pos_r*100:.0f}% | {avg_h:.2f} | {max_s2:.2f} |")
    lines.append("")

    # H1: Chinese terse syntax
    lines.append("## H1: Terse Syntax (Classical Chinese)")
    lines.append("")
    chinese = era_groups.get("classical_chinese", [])
    if chinese:
        ch_avg = statistics.mean(p["avg_s2"] for p in chinese)
        ancient = era_groups.get("ancient", [])
        romantic = era_groups.get("romantic", [])
        compare_avg = statistics.mean(p["avg_s2"] for p in (ancient + romantic)) if (ancient + romantic) else None

        lines.append(f"Classical Chinese avg S2: **{ch_avg:.3f}**")
        if compare_avg is not None:
            direction = "HIGHER" if ch_avg > compare_avg else "LOWER"
            lines.append(f"vs. ancient+romantic avg: {compare_avg:.3f} → **{direction}**")
            if ch_avg > compare_avg:
                lines.append("")
                lines.append("**H1 SUPPORTED**: Classical Chinese translations produce higher S2 than Western poetry "
                              "of comparable historical periods. Terse, paratactic English renderings do appear to "
                              "violate GPT-2's clause-structure expectations.")
            else:
                lines.append("")
                lines.append("**H1 NOT SUPPORTED**: Classical Chinese translations do not show elevated S2 "
                              "compared to comparable Western poetry — translation flattening (H4) may dominate.")
        lines.append("")
        lines.append("**Terse-syntax indicators:**")
        for p in chinese:
            lines.append(f"- {p['title']}: avg_s2={p['avg_s2']:.3f}, avg_H={p['avg_h']:.2f}")
        lines.append("")
    else:
        lines.append("*No data yet — poems not yet analyzed*")
        lines.append("")

    # H2: Persian Sufi paradox
    lines.append("## H2: Sufi Paradox (Persian Poetry)")
    lines.append("")
    persian = era_groups.get("persian", [])
    if persian:
        p_avg = statistics.mean(p["avg_s2"] for p in persian)
        metaphysical = era_groups.get("metaphysical", [])
        victorian = era_groups.get("victorian", [])
        comp = metaphysical + victorian
        comp_avg = statistics.mean(p["avg_s2"] for p in comp) if comp else None

        lines.append(f"Persian avg S2: **{p_avg:.3f}**")
        if comp_avg is not None:
            direction = "HIGHER" if p_avg > comp_avg else "LOWER"
            lines.append(f"vs. metaphysical+victorian avg: {comp_avg:.3f} → **{direction}**")
        lines.append("")
        lines.append("| Poem | Avg S2 | Max S2 | +S2% |")
        lines.append("|---|---|---|---|")
        for p in sorted(persian, key=lambda x: x["avg_s2"], reverse=True):
            lines.append(f"| {p['title'][:55]} | {p['avg_s2']:.3f} | {p['max_s2']:.2f} | {p['pos_ratio']*100:.0f}% |")
        lines.append("")
    else:
        lines.append("*No data yet — poems not yet analyzed*")
        lines.append("")

    # H3: Tanka vs. haiku
    lines.append("## H3: Tanka Coda vs. Haiku (Japanese Classical)")
    lines.append("")
    tanka = era_groups.get("japanese_classical", [])
    haiku_list = era_groups.get("haiku", [])
    if tanka and haiku_list:
        t_avg = statistics.mean(p["avg_s2"] for p in tanka)
        h_avg = statistics.mean(p["avg_s2"] for p in haiku_list)
        t_pos = statistics.mean(p["pos_ratio"] for p in tanka)
        h_pos = statistics.mean(p["pos_ratio"] for p in haiku_list)
        lines.append("| Form | n | Avg S2 | +S2% | Avg H |")
        lines.append("|---|---|---|---|---|")
        lines.append(f"| Tanka (5-7-5-7-7) | {len(tanka)} | **{t_avg:.3f}** | {t_pos*100:.0f}% | "
                     f"{statistics.mean(p['avg_h'] for p in tanka):.2f} |")
        lines.append(f"| Haiku (5-7-5) | {len(haiku_list)} | **{h_avg:.3f}** | {h_pos*100:.0f}% | "
                     f"{statistics.mean(p['avg_h'] for p in haiku_list):.2f} |")
        lines.append("")
        diff = t_avg - h_avg
        lines.append(f"Tanka - Haiku avg S2 gap: **{diff:+.3f}**")
        lines.append("")
        if diff < -0.1:
            lines.append("**H3 SUPPORTED**: Tanka shows lower avg S2 than haiku, consistent with the idea that "
                         "the 7-7 coda provides conventional resolution after the 5-7-5 opening image.")
        elif diff > 0.1:
            lines.append("**H3 INVERTED**: Tanka shows higher avg S2 than haiku — the coda introduces *additional* "
                         "complexity rather than resolving it.")
        else:
            lines.append("**H3 NULL**: Tanka and haiku show similar S2 profiles (within 0.1 bits).")
        lines.append("")
    elif tanka:
        lines.append("*Haiku data present but no tanka data yet*")
        lines.append("")
    else:
        lines.append("*No tanka data yet — poems not analyzed*")
        lines.append("")

    # H4: Translation flattening hypothesis
    lines.append("## H4: Translation Flattening?")
    lines.append("")
    lines.append("If translators normalize exotic syntax, all translated non-Western poems should cluster toward "
                 "LOWER S2 than native English poems of comparable periods.")
    lines.append("")
    native_english_eras = ["romantic", "victorian", "modernist", "metaphysical"]
    native_avgs = [statistics.mean(p["avg_s2"] for p in era_groups[e])
                   for e in native_english_eras if e in era_groups]
    native_grand = statistics.mean(native_avgs) if native_avgs else None

    translated_eras = focus_eras
    trans_avgs = [statistics.mean(p["avg_s2"] for p in era_groups[e])
                  for e in translated_eras if e in era_groups and era_groups[e]]
    trans_grand = statistics.mean(trans_avgs) if trans_avgs else None

    lines.append("| Group | n eras | Grand avg S2 |")
    lines.append("|---|---|---|")
    if native_grand is not None:
        lines.append(f"| Native English poetry | {len(native_avgs)} | {native_grand:.3f} |")
    if trans_grand is not None:
        lines.append(f"| Translated non-Western poetry | {len(trans_avgs)} | {trans_grand:.3f} |")
        if native_grand is not None:
            direction = "LOWER" if trans_grand < native_grand else "HIGHER"
            lines.append("")
            lines.append(f"Translated poetry avg S2 is **{direction}** than native English. "
                         f"{'H4 (flattening) is consistent with this result.' if direction == 'LOWER' else 'H4 is NOT supported — translated poetry is more, not less, surprising.'}")
    else:
        lines.append("*Insufficient translated era data*")
    lines.append("")

    # Notable tokens
    lines.append("## Notable High-S2 Tokens in New Traditions")
    lines.append("")
    all_focus = []
    for era in focus_eras:
        for r in results:
            if r["metadata"]["era"] == era:
                for t in clean_tokens(r["tokens"]):
                    all_focus.append({
                        "token": t["token"],
                        "s2": t["s2"],
                        "entropy": t["entropy"],
                        "title": r["metadata"]["title"],
                        "author": r["metadata"]["author"],
                        "era": era,
                        "top_pred": t["alternatives"][0]["token"] if t["alternatives"] else "",
                        "top_prob": t["alternatives"][0]["prob"] if t["alternatives"] else 0,
                    })

    if all_focus:
        top_tokens = sorted(all_focus, key=lambda x: x["s2"], reverse=True)[:15]
        lines.append("| S2 | Token | GPT-2 expected | Prob | Poem |")
        lines.append("|---|---|---|---|---|")
        for t in top_tokens:
            pred = repr(t["top_pred"])
            lines.append(f"| {t['s2']:.2f} | `{repr(t['token'])}` | {pred} | {t['top_prob']:.1%} | "
                         f"{t['author']}, \"{t['title'][:40]}\" |")
        lines.append("")
    else:
        lines.append("*No focus era data yet*")
        lines.append("")

    # Summary findings
    lines.append("## Summary and Interpretation")
    lines.append("")
    if trans_grand is not None and native_grand is not None:
        if trans_grand < native_grand - 0.1:
            finding = (
                "The data tentatively supports **H4 (Translation Flattening)**: translated non-Western poetry "
                "averages lower artifact-free S2 than native English poetry. This suggests translators do normalize "
                "syntax toward English expectations, reducing the information-theoretic distinctiveness of these "
                "traditions. The cross-cultural 'surprise' of Chinese parataxis or Persian Sufi paradox is attenuated "
                "in English renderings."
            )
        elif trans_grand > native_grand + 0.1:
            finding = (
                "The data does **not** support H4: translated non-Western poetry shows **higher** S2 than native "
                "English poetry. This suggests the exotic syntax, imagery, and register of these traditions produces "
                "genuine information-theoretic distinctiveness even in English translation — the translational gap "
                "itself may be a source of surprise."
            )
        else:
            finding = (
                "Results are mixed: translated non-Western poetry sits near the center of the native English S2 "
                "distribution. Neither strong flattening nor strong elevation is observed. This may mean the "
                "information-theoretic signature of these traditions is primarily determined by content (sparse "
                "imagery, mystical vocabulary) rather than syntactic structure."
            )
        lines.append(finding)
        lines.append("")
    lines.append("**Next steps:**")
    lines.append("1. Add more classical Chinese poems (especially Du Fu's longer regulated verse) to increase n")
    lines.append("2. Compare Arabic poetry (pre-Islamic qasida) in translation")
    lines.append("3. Test whether *different translators* of the same Chinese poem produce different S2 profiles "
                 "(cf. `translation_s2.md` methodology applied to Chinese sources)")
    lines.append("4. Add Sanskrit poetry (Kalidasa, Bhartrihari) as a test of highly inflected language in translation")

    output = "\n".join(lines) + "\n"
    out_path = os.path.join(FINDINGS_DIR, "cross_cultural_s2.md")
    with open(out_path, "w") as f:
        f.write(output)
    print(f"Written: {out_path}")

    # Save JSON for downstream analysis
    summary = {
        "date": "2026-10-12",
        "focus_eras": {era: [p for p in era_groups.get(era, [])] for era in focus_eras},
        "era_summaries": {era: list(v) for era, v in era_summaries.items()},
    }
    json_path = os.path.join(FINDINGS_DIR, "..", "results", "cross_cultural_s2.json")
    with open(json_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"JSON saved: {json_path}")
    return output


if __name__ == "__main__":
    main()
