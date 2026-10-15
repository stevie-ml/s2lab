#!/usr/bin/env python3.13
"""
Content vs. Function Word S2 by Poetic Tradition

Tests WHERE different poetic traditions locate their "surprise budget":
- Content words (nouns, verbs, adjectives, adverbs) = open class
- Function words (determiners, prepositions, conjunctions, auxiliaries) = closed class

Hypothesis: Language poetry and experimental poetry should show relatively
higher function-word S2 than other traditions, because they specifically
disrupt grammatical (not just lexical) expectations.

The 'Straussian gap' has two flavors:
  - Lexical gap: choosing an unexpected content word
  - Grammatical gap: choosing an unexpected function word / structure word
"""

import json
import sys
from collections import defaultdict
import statistics

# Comprehensive English function word (closed class) list
FUNCTION_WORDS = {
    # Articles
    'the', 'a', 'an',
    # Coordinating conjunctions
    'and', 'or', 'but', 'nor', 'for', 'yet', 'so',
    # Subordinating conjunctions
    'if', 'when', 'while', 'since', 'because', 'although', 'though',
    'unless', 'until', 'after', 'before', 'once', 'whether', 'as',
    'than', 'that', 'where', 'wherever', 'whenever', 'however',
    # Prepositions
    'of', 'in', 'on', 'at', 'by', 'with', 'from', 'to', 'into',
    'through', 'over', 'under', 'above', 'below', 'between', 'among',
    'against', 'along', 'around', 'behind', 'beside', 'beyond', 'during',
    'except', 'inside', 'near', 'off', 'out', 'outside', 'past', 'toward',
    'towards', 'within', 'without', 'upon', 'across', 'about', 'up', 'down',
    # Personal pronouns
    'i', 'you', 'he', 'she', 'it', 'we', 'they',
    'me', 'him', 'her', 'us', 'them',
    'myself', 'yourself', 'himself', 'herself', 'itself', 'ourselves', 'themselves',
    # Possessive pronouns/adjectives
    'my', 'your', 'his', 'its', 'our', 'their',
    # Relative/interrogative pronouns
    'who', 'whom', 'whose', 'which', 'what',
    # Demonstrative pronouns/adjectives
    'this', 'that', 'these', 'those',
    # Auxiliary verbs
    'is', 'are', 'was', 'were', 'be', 'been', 'being', 'am',
    'have', 'has', 'had',
    'will', 'would', 'shall', 'should',
    'may', 'might', 'must', 'can', 'could',
    'do', 'does', 'did',
    # Negation
    'not', 'no', 'never', 'neither', 'nor',
    # Common particles/adverbs
    'very', 'quite', 'rather', 'too', 'so', 'such',
    'already', 'still', 'yet', 'now', 'then', 'here', 'there',
    'also', 'just', 'only', 'even', 'ever', 'more', 'most',
    'less', 'least', 'much', 'many', 'few', 'each', 'every',
    'both', 'either', 'neither', 'all', 'any', 'some', 'none',
    # Common contractions / particles
    "'s", "'t", "n't", "'re", "'ve", "'ll", "'d",
}


def is_function_word(token: str) -> bool:
    """True if token (with or without leading space) is a function word."""
    clean = token.strip().lower()
    return clean in FUNCTION_WORDS


def artifact_free(s2_val: float, p_newline: float) -> bool:
    """True if token passes the stanza-break artifact filter."""
    return p_newline < 0.9


def analyze_corpus(path: str = 'results/corpus_results.json') -> dict:
    with open(path) as f:
        data = json.load(f)

    # Per-poem stats: content word S2 and function word S2
    poem_stats = []

    # Aggregated per-era
    era_content = defaultdict(list)
    era_function = defaultdict(list)
    era_ratio = defaultdict(list)  # function_s2 / content_s2 per poem

    for poem in data:
        meta = poem['metadata']
        era = meta.get('era', 'unknown')
        lang = meta.get('language', 'en')
        if lang != 'en':
            continue

        tokens = poem.get('tokens', [])
        content_s2 = []
        function_s2 = []

        for tok in tokens:
            s2 = tok.get('s2', 0.0)
            p_nl = tok.get('p_newline', 0.0)
            token_str = tok.get('token', '')

            if not artifact_free(s2, p_nl):
                continue

            if is_function_word(token_str):
                function_s2.append(s2)
            else:
                content_s2.append(s2)

        if len(content_s2) < 5 or len(function_s2) < 3:
            continue

        c_mean = statistics.mean(content_s2)
        f_mean = statistics.mean(function_s2)
        gap = f_mean - c_mean  # positive = function words more surprising

        poem_stats.append({
            'title': meta.get('title', ''),
            'author': meta.get('author', ''),
            'era': era,
            'year': meta.get('year', 0),
            'content_mean_s2': c_mean,
            'function_mean_s2': f_mean,
            'gap': gap,  # function - content
            'n_content': len(content_s2),
            'n_function': len(function_s2),
            'content_pos_pct': sum(1 for x in content_s2 if x > 0) / len(content_s2),
            'function_pos_pct': sum(1 for x in function_s2 if x > 0) / len(function_s2),
        })

        era_content[era].append(c_mean)
        era_function[era].append(f_mean)
        era_ratio[era].append(gap)

    return {
        'poem_stats': poem_stats,
        'era_content': dict(era_content),
        'era_function': dict(era_function),
        'era_ratio': dict(era_ratio),
    }


def format_report(results: dict) -> str:
    poem_stats = results['poem_stats']
    era_content = results['era_content']
    era_function = results['era_function']
    era_ratio = results['era_ratio']

    lines = []
    lines.append("# Content vs. Function Word S₂: Where Do Traditions Locate Their Surprise?\n")

    # Era table
    lines.append("## Era Rankings by Content and Function Word S₂\n")
    lines.append("(Artifact-free, English-language poems only)\n")
    lines.append("| Era | n | Content S₂ | Function S₂ | Gap (F−C) | Interpretation |")
    lines.append("|---|---|---|---|---|---|")

    era_rows = []
    for era in era_content:
        if era not in era_function:
            continue
        c_vals = era_content[era]
        f_vals = era_function[era]
        g_vals = era_ratio.get(era, [])
        n = len(c_vals)
        if n < 2:
            continue
        c_mean = statistics.mean(c_vals)
        f_mean = statistics.mean(f_vals)
        gap = statistics.mean(g_vals) if g_vals else f_mean - c_mean
        era_rows.append((era, n, c_mean, f_mean, gap))

    era_rows.sort(key=lambda x: x[4], reverse=True)

    for era, n, c_mean, f_mean, gap in era_rows:
        if gap > 0.3:
            interp = "⬆️ Function-led surprise"
        elif gap > 0.0:
            interp = "≈ Balanced"
        elif gap > -0.3:
            interp = "≈ Content-led"
        else:
            interp = "⬇️ Strongly content-led"
        lines.append(f"| {era} | {n} | {c_mean:+.3f} | {f_mean:+.3f} | {gap:+.3f} | {interp} |")

    lines.append("")

    # Poems with highest function word S2 relative to content
    lines.append("## Poems with Highest Grammar-Disruption (Function S₂ >> Content S₂)\n")
    lines.append("| Title | Author | Era | Content S₂ | Function S₂ | Gap |")
    lines.append("|---|---|---|---|---|---|")

    top_gap = sorted(poem_stats, key=lambda x: x['gap'], reverse=True)[:15]
    for p in top_gap:
        lines.append(f"| {p['title'][:40]} | {p['author'][:25]} | {p['era']} | "
                     f"{p['content_mean_s2']:+.3f} | {p['function_mean_s2']:+.3f} | {p['gap']:+.3f} |")

    lines.append("")

    # Poems with lowest function word S2 (most content-led)
    lines.append("## Poems with Highest Lexical-Only Surprise (Content-Led)\n")
    lines.append("| Title | Author | Era | Content S₂ | Function S₂ | Gap |")
    lines.append("|---|---|---|---|---|---|")

    bot_gap = sorted(poem_stats, key=lambda x: x['gap'])[:15]
    for p in bot_gap:
        lines.append(f"| {p['title'][:40]} | {p['author'][:25]} | {p['era']} | "
                     f"{p['content_mean_s2']:+.3f} | {p['function_mean_s2']:+.3f} | {p['gap']:+.3f} |")

    lines.append("")

    # Corpus-wide aggregate
    all_content = [p['content_mean_s2'] for p in poem_stats]
    all_function = [p['function_mean_s2'] for p in poem_stats]
    all_gap = [p['gap'] for p in poem_stats]

    lines.append("## Corpus-Wide Aggregate\n")
    lines.append(f"- **Poems analyzed**: {len(poem_stats)}")
    lines.append(f"- **Mean content word S₂**: {statistics.mean(all_content):+.4f}")
    lines.append(f"- **Mean function word S₂**: {statistics.mean(all_function):+.4f}")
    lines.append(f"- **Mean gap (F−C)**: {statistics.mean(all_gap):+.4f}")
    lines.append(f"- **Poems with function S₂ > content S₂**: "
                 f"{sum(1 for g in all_gap if g > 0)} ({100*sum(1 for g in all_gap if g > 0)/len(all_gap):.1f}%)")

    return "\n".join(lines)


def main():
    print("Loading corpus results...", file=sys.stderr)
    results = analyze_corpus()

    report = format_report(results)
    print(report)

    # Save JSON
    outpath = 'results/content_vs_function_word_s2.json'
    with open(outpath, 'w') as f:
        # Don't dump poem_stats list (large), just era summaries
        summary = {
            'era_content_mean': {k: statistics.mean(v) for k, v in results['era_content'].items() if v},
            'era_function_mean': {k: statistics.mean(v) for k, v in results['era_function'].items() if v},
            'era_gap_mean': {k: statistics.mean(v) for k, v in results['era_ratio'].items() if v},
            'n_poems': len(results['poem_stats']),
        }
        json.dump(summary, f, indent=2)

    print(f"\nJSON saved to {outpath}", file=sys.stderr)


if __name__ == '__main__':
    main()
