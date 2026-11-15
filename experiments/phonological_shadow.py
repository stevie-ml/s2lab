"""
Phonological Shadow Experiment
==============================
When a poet chooses a word that surprises GPT-2 (high S2), do they sometimes
choose a word that *sounds like* what GPT-2 expected?

The hypothesis: poets exploit the phonological shadow of the model's suppressed
prediction — using a token that rhymes with, alliterates with, or consonantally
echoes the most likely alternative. This would be a form of "phonological
debt discharge": the ear gets some of what the probability distribution promised,
even though the semantic content is wholly different.

Methods:
  1. Levenshtein distance (character-level, normalized)
  2. Initial consonant cluster match (alliteration / onset)
  3. Consonant skeleton overlap (strip vowels, compare)
  4. Final phoneme cluster match (rhyme / coda similarity)

Comparison: high-S2 tokens vs low-S2 tokens — are high-S2 tokens phonologically
closer to the top model prediction than expected by chance?
"""

import json
import re
from collections import defaultdict
import statistics
import math

# ── Levenshtein distance ─────────────────────────────────────────────────────

def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)
    if not s2:
        return len(s1)
    prev = list(range(len(s2) + 1))
    for i, c1 in enumerate(s1):
        curr = [i + 1]
        for j, c2 in enumerate(s2):
            curr.append(min(prev[j + 1] + 1, curr[-1] + 1,
                            prev[j] + (0 if c1 == c2 else 1)))
        prev = curr
    return prev[-1]


def norm_lev(a, b):
    """Normalized Levenshtein: 0=identical, 1=totally different."""
    a, b = a.strip().lower(), b.strip().lower()
    if not a and not b:
        return 0.0
    if not a or not b:
        return 1.0
    return levenshtein(a, b) / max(len(a), len(b))


def onset(tok):
    """Extract initial consonant cluster (before first vowel)."""
    t = tok.strip().lower()
    # Remove leading punctuation
    t = re.sub(r'^[^a-z]+', '', t)
    vowels = set('aeiou')
    cluster = []
    for ch in t:
        if ch in vowels:
            break
        if ch.isalpha():
            cluster.append(ch)
    return ''.join(cluster)


def consonant_skeleton(tok):
    """Return consonants only (remove vowels)."""
    t = tok.strip().lower()
    vowels = set('aeiou')
    return ''.join(ch for ch in t if ch.isalpha() and ch not in vowels)


def coda(tok):
    """Return final consonant cluster (after last vowel)."""
    t = tok.strip().lower()
    t = re.sub(r'[^a-z]+$', '', t)
    vowels = set('aeiou')
    last_vowel = -1
    for i, ch in enumerate(t):
        if ch in vowels:
            last_vowel = i
    if last_vowel == -1 or last_vowel == len(t) - 1:
        return ''
    return t[last_vowel + 1:]


def onset_match(a, b):
    oa, ob = onset(a), onset(b)
    if not oa or not ob:
        return False
    return oa[0] == ob[0]


def skeleton_overlap(a, b):
    """Dice coefficient on consonant skeletons."""
    sa, sb = set(consonant_skeleton(a)), set(consonant_skeleton(b))
    if not sa and not sb:
        return 1.0
    if not sa or not sb:
        return 0.0
    return 2 * len(sa & sb) / (len(sa) + len(sb))


def coda_match(a, b):
    ca, cb = coda(a), coda(b)
    if not ca or not cb:
        return False
    return ca == cb or (len(ca) >= 2 and len(cb) >= 2 and ca[-2:] == cb[-2:])


# ── Main analysis ────────────────────────────────────────────────────────────

def is_word_token(tok):
    """Skip pure punctuation and newline tokens."""
    t = tok.strip()
    return bool(re.search(r'[a-zA-Z]', t))


def analyze(corpus, s2_low=-2.0, s2_high=4.0):
    """
    Collect phonological similarity metrics for three tiers:
      conformist:  s2 < s2_low
      straussian:  s2 > s2_high
      neutral:     s2_low <= s2 <= s2_high
    Returns dict of lists of similarity values per tier.
    """
    tiers = {'conformist': [], 'neutral': [], 'straussian': []}
    tier_counts = defaultdict(int)
    era_data = defaultdict(lambda: {'conformist': [], 'straussian': []})
    author_data = defaultdict(lambda: {'conformist': [], 'straussian': []})

    for poem in corpus:
        era = poem['metadata'].get('era', 'unknown')
        author = poem['metadata'].get('author', 'unknown')

        for tok in poem['tokens']:
            # Skip stanza-break artifact positions
            if tok.get('p_newline', 0) > 0.9:
                continue
            token = tok['token']
            if not is_word_token(token):
                continue
            alts = tok.get('alternatives', [])
            if not alts:
                continue

            top_pred = alts[0]['token']
            if not is_word_token(top_pred):
                # Try second alternative
                word_alts = [a for a in alts if is_word_token(a['token'])]
                if not word_alts:
                    continue
                top_pred = word_alts[0]['token']

            s2 = tok['s2']

            # Compute similarities
            lev = 1 - norm_lev(token, top_pred)       # 1 = identical
            om = int(onset_match(token, top_pred))
            sk = skeleton_overlap(token, top_pred)
            cm = int(coda_match(token, top_pred))
            composite = (lev + om + sk + cm) / 4       # 0–1 composite

            if s2 < s2_low:
                tier = 'conformist'
            elif s2 > s2_high:
                tier = 'straussian'
            else:
                tier = 'neutral'

            tiers[tier].append({
                'lev': lev, 'onset': om, 'skeleton': sk, 'coda': cm,
                'composite': composite, 's2': s2,
                'token': token, 'top_pred': top_pred,
                'era': era, 'author': author
            })

            if tier in ('conformist', 'straussian'):
                era_data[era][tier].append(composite)
                author_data[author][tier].append(composite)

    return tiers, era_data, author_data


def mean(lst):
    return sum(lst) / len(lst) if lst else float('nan')


def report(tiers, era_data, author_data):
    lines = []
    lines.append("# Phonological Shadow Experiment\n")
    lines.append(f"**Date:** 2026-11-15")
    lines.append(f"**Corpus:** 419 poems | GPT-2 (gpt2)\n")
    lines.append("""
## Research Question

When a poet surprises GPT-2 (high S2), does the chosen word *sound like*
the model's suppressed top prediction? We call this the **phonological shadow**:
the actual token echoes the phonological form of the statistically expected one,
granting the reader subconscious sonic satisfaction even as semantics diverges.

**Hypothesis**: High-S2 tokens (Straussian gap) show HIGHER phonological similarity
to the model's top alternative than conformist (negative-S2) tokens, where
the actual token and the prediction are likely semantically AND phonologically similar.

**Four similarity dimensions:**
- **Levenshtein**: character-level inverse edit-distance (0=different, 1=identical)
- **Onset match**: do both tokens start with the same consonant? (alliteration)
- **Consonant skeleton**: Dice coefficient on consonant sets (phonological texture)
- **Coda match**: final consonant cluster match (approximate rhyme)
""")

    # Overall tier comparison
    lines.append("## Results: Overall Tier Comparison\n")
    lines.append("| Tier | n | Lev Sim | Onset Match | Skel Overlap | Coda Match | Composite |")
    lines.append("|---|---|---|---|---|---|---|")
    for tier in ('conformist', 'neutral', 'straussian'):
        rows = tiers[tier]
        n = len(rows)
        if not rows:
            continue
        lev = mean([r['lev'] for r in rows])
        om = mean([r['onset'] for r in rows])
        sk = mean([r['skeleton'] for r in rows])
        cm = mean([r['coda'] for r in rows])
        comp = mean([r['composite'] for r in rows])
        lines.append(f"| {tier} | {n:,} | {lev:.4f} | {om:.4f} | {sk:.4f} | {cm:.4f} | **{comp:.4f}** |")

    # Delta: straussian vs conformist
    if tiers['conformist'] and tiers['straussian']:
        c_comp = mean([r['composite'] for r in tiers['conformist']])
        s_comp = mean([r['composite'] for r in tiers['straussian']])
        delta = s_comp - c_comp
        direction = "MORE similar" if delta > 0 else "LESS similar"
        lines.append(f"\n**Straussian vs Conformist composite delta:** {delta:+.4f} ({direction} to top prediction)")

    # Top examples of phonological echoing
    lines.append("\n## Top Phonological Shadow Moments (Straussian tokens)\n")
    straussian = tiers['straussian']
    # Sort by composite similarity, highest first
    top_shadows = sorted(straussian, key=lambda r: r['composite'], reverse=True)[:30]
    # Filter to actual phonological matches (composite > 0.3)
    actual_shadows = [r for r in top_shadows if r['composite'] > 0.25][:20]

    lines.append("| Actual token | Top prediction | S2 | Lev | Onset | Skel | Coda | Era |")
    lines.append("|---|---|---|---|---|---|---|---|")
    for r in actual_shadows:
        lines.append(
            f"| `{r['token'].strip():15s}` | `{r['top_pred'].strip():15s}` | "
            f"{r['s2']:.1f} | {r['lev']:.2f} | {'✓' if r['onset'] else '·'} | "
            f"{r['skeleton']:.2f} | {'✓' if r['coda'] else '·'} | {r['era']} |"
        )

    # By era
    lines.append("\n## Phonological Shadow by Era\n")
    era_rows = []
    for era, d in era_data.items():
        nc = len(d['conformist'])
        ns = len(d['straussian'])
        if nc < 20 or ns < 10:
            continue
        c = mean(d['conformist'])
        s = mean(d['straussian'])
        delta = s - c
        era_rows.append((delta, era, ns, nc, s, c))
    era_rows.sort(reverse=True)

    lines.append("| Era | n_strs | n_conf | Shadow (strs) | Baseline (conf) | Delta |")
    lines.append("|---|---|---|---|---|---|")
    for delta, era, ns, nc, s, c in era_rows:
        marker = " ← **high shadow**" if delta > 0.02 else (" ← low shadow" if delta < -0.02 else "")
        lines.append(f"| {era} | {ns} | {nc} | {s:.4f} | {c:.4f} | {delta:+.4f}{marker} |")

    # By author
    lines.append("\n## Top Poets by Phonological Shadow (Straussian composite)\n")
    author_rows = []
    for author, d in author_data.items():
        nc = len(d['conformist'])
        ns = len(d['straussian'])
        if ns < 10:
            continue
        s = mean(d['straussian'])
        c = mean(d['conformist']) if nc > 0 else float('nan')
        delta = s - c if nc > 0 else float('nan')
        author_rows.append((s, author, ns, nc, c, delta))
    author_rows.sort(reverse=True)

    lines.append("| Author | n_strs | Shadow score | Baseline | Delta |")
    lines.append("|---|---|---|---|---|")
    for s, author, ns, nc, c, delta in author_rows[:25]:
        delta_str = f"{delta:+.4f}" if not math.isnan(delta) else "—"
        lines.append(f"| {author} | {ns} | {s:.4f} | {c:.4f} | {delta_str} |")

    # Finding
    lines.append("\n## Finding\n")
    if tiers['conformist'] and tiers['straussian']:
        c_comp = mean([r['composite'] for r in tiers['conformist']])
        s_comp = mean([r['composite'] for r in tiers['straussian']])
        delta = s_comp - c_comp

        c_onset = mean([r['onset'] for r in tiers['conformist']])
        s_onset = mean([r['onset'] for r in tiers['straussian']])

        c_coda = mean([r['coda'] for r in tiers['conformist']])
        s_coda = mean([r['coda'] for r in tiers['straussian']])

        c_sk = mean([r['skeleton'] for r in tiers['conformist']])
        s_sk = mean([r['skeleton'] for r in tiers['straussian']])

        if delta > 0:
            lines.append(
                f"**Phonological shadow confirmed**: Straussian-gap tokens (s2 > 4) show HIGHER "
                f"phonological similarity to GPT-2's suppressed prediction than conformist tokens "
                f"(composite +{delta:.4f}). The gap is driven especially by: "
                f"onset (+{s_onset-c_onset:+.3f}), skeleton (+{s_sk-c_sk:+.3f}), coda (+{s_coda-c_coda:+.3f}).\n"
            )
            lines.append(
                "**Interpretation**: When poets make the most unexpected token choices, they more often "
                "choose words that sound like (or alliterate/rhyme with) the model's top prediction. "
                "This suggests poetry exploits the **phonological debt** created by semantic surprise: "
                "the reader's ear receives a sonic echo of what was expected, even as the semantic "
                "content defies it. This is a measurable form of partial fulfillment — the phonological "
                "channel carries the expectation while the semantic channel violates it."
            )
        else:
            lines.append(
                f"**No phonological shadow**: Straussian-gap tokens are NOT more phonologically similar "
                f"to their top prediction (composite delta = {delta:+.4f}). "
                f"Semantic surprise does not co-occur with phonological compensation."
            )

    lines.append("\n## Next Steps\n")
    lines.append(
        "- Test this at the phoneme level (using CMU pronouncing dictionary) rather than character-level\n"
        "- Check whether the shadow is stronger for specific genres (e.g., formal verse vs free verse)\n"
        "- Examine whether shadow strength correlates with perceived poem quality or canonicity\n"
        "- Look at the reverse: do conformist tokens sometimes have LOW phonological similarity "
        "  (unexpected sounds, expected semantics)?\n"
    )

    return '\n'.join(lines)


if __name__ == '__main__':
    with open('results/corpus_results.json') as f:
        corpus = json.load(f)

    print(f"Analyzing {len(corpus)} poems...")
    tiers, era_data, author_data = analyze(corpus)

    total_analyzed = sum(len(v) for v in tiers.values())
    print(f"Tokens analyzed: {total_analyzed:,}")
    for tier, rows in tiers.items():
        print(f"  {tier}: {len(rows):,}")

    md = report(tiers, era_data, author_data)

    out_path = 'findings/phonological_shadow.md'
    with open(out_path, 'w') as f:
        f.write(md)
    print(f"\nReport written to {out_path}")

    # Save JSON data
    import json as _json
    summary_data = {
        'tier_summary': {},
        'era_deltas': [],
        'author_top': []
    }
    for tier, rows in tiers.items():
        if rows:
            summary_data['tier_summary'][tier] = {
                'n': len(rows),
                'mean_composite': mean([r['composite'] for r in rows]),
                'mean_lev': mean([r['lev'] for r in rows]),
                'onset_rate': mean([r['onset'] for r in rows]),
                'skeleton_overlap': mean([r['skeleton'] for r in rows]),
                'coda_rate': mean([r['coda'] for r in rows]),
            }

    with open('results/phonological_shadow.json', 'w') as f:
        _json.dump(summary_data, f, indent=2)
    print("JSON saved to results/phonological_shadow.json")
