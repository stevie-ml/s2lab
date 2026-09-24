"""
Archaic English in Poetry: Is GPT-2's Confusion Genuine Straussian Deviation?

When poets use archaic forms (thee, thou, thy, hath, doth, 'tis, etc.),
does GPT-2 assign genuine Straussian deviation, or is it a statistical artifact
of rare tokens—surprisal without low entropy (so S2 is not truly 'earned')?

S2 = surprisal - entropy
- High S2 = token is more surprising than context warrants (low entropy, high surprisal)
- High surprisal alone is not enough — entropy must also be low
"""

import json
import re
from collections import defaultdict

CORPUS_FILE = "results/corpus_results.json"

# Archaic English forms — normalized to lowercase for matching
ARCHAIC_TOKENS = {
    # Second-person singular pronouns
    "thee", "thou", "thy", "thine",
    # Third-person singular archaic verb conjugations
    "hath", "doth", "hast", "dost",
    # Second-person singular verb conjugations
    "wilt", "wouldst", "shouldst", "couldst", "canst", "shalt",
    "darest", "needst", "hadst", "wast", "wert",
    # First-person plural archaic
    # Contractions
    "'tis", "'twas", "'twere", "'twill", "'tis",
    # Adverbs
    "oft", "ere", "nigh", "hereafter", "heretofore", "wherefore",
    "whence", "thence", "hence", "henceforth", "withal", "perchance",
    "methinks", "mayhaps", "forsooth", "verily", "behold",
    # Verbs
    "sayeth", "knoweth", "giveth", "taketh", "cometh", "goeth",
    "maketh", "speaketh", "standeth", "seeth", "heareth",
    # Articles / determiners in archaic usage (just track these as context)
    "mine",  # when used as possessive determiner rather than noun
    # Prepositions used archaically
    "o'er", "ne'er", "e'er", "'neath", "betwixt", "neath",
    # Other archaic
    "yonder", "yon", "anon", "aught", "naught", "nought",
    "quoth", "prithee", "fain", "loth", "loath",
}

# These require context to classify as archaic (e.g., "art" as verb vs noun)
CONTEXT_SENSITIVE = {"art"}  # "art" as 2nd-person singular of "to be"

def is_archaic_token(token_text, context_before=""):
    """Check if a token is archaic."""
    # Strip leading space and normalize
    clean = token_text.strip().lower()
    # Handle subword tokens that form archaic words
    # Match if clean matches exactly or is part of an archaic word
    if clean in ARCHAIC_TOKENS:
        return True
    # Handle subword pieces: "thou" might be " thou" or "thou"
    # Check for contractions stored as 'tis etc.
    for archaic in ARCHAIC_TOKENS:
        if clean == archaic.replace("'", ""):
            return True
    return False

def classify_archaic(token_text):
    """Return the category of archaic token."""
    clean = token_text.strip().lower()
    pronouns = {"thee", "thou", "thy", "thine"}
    verb_conj = {"hath", "doth", "hast", "dost", "wilt", "wouldst",
                 "shouldst", "couldst", "canst", "shalt", "darest",
                 "needst", "hadst", "wast", "wert", "sayeth", "knoweth",
                 "giveth", "taketh", "cometh", "goeth", "maketh",
                 "speaketh", "standeth", "seeth", "heareth"}
    contractions = {"'tis", "'twas", "'twere", "'twill", "tis", "twas"}
    adverbs = {"oft", "ere", "nigh", "whence", "thence", "hence",
               "henceforth", "withal", "perchance", "methinks", "forsooth",
               "verily", "behold", "yonder", "yon", "anon", "aught",
               "naught", "nought", "quoth", "prithee", "fain", "loth",
               "hereafter", "heretofore", "wherefore"}
    elisions = {"o'er", "ne'er", "e'er", "'neath", "neath", "betwixt"}

    if clean in pronouns:
        return "pronoun"
    elif clean in verb_conj:
        return "verb_conjugation"
    elif clean in contractions:
        return "contraction"
    elif clean in adverbs:
        return "adverb_other"
    elif clean in elisions:
        return "elision"
    else:
        return "other"

def load_corpus():
    with open(CORPUS_FILE) as f:
        return json.load(f)

def main():
    data = load_corpus()

    # Collect all archaic tokens with their metrics
    archaic_hits = []
    modern_baseline = []  # non-archaic, non-punctuation content word tokens

    era_archaic = defaultdict(list)  # era -> list of s2 values for archaic tokens
    era_modern = defaultdict(list)   # era -> list of s2 values for modern tokens

    poet_archaic = defaultdict(list)

    archaic_by_category = defaultdict(list)

    # For "false positive" detection: high surprisal but also high entropy
    # S2 < 0 but surprisal > 5 = high surprisal but model was uncertain anyway
    false_positive_count = 0
    genuine_straussian_count = 0

    for poem in data:
        meta = poem["metadata"]
        era = meta.get("era", "unknown")
        author = meta.get("author", "unknown")
        tokens = poem["tokens"]

        if meta.get("language", "en") != "en":
            continue

        for t in tokens:
            tok = t["token"]
            clean = tok.strip().lower()
            s2 = t["s2"]
            surprisal = t["surprisal"]
            entropy = t["entropy"]

            if is_archaic_token(tok):
                category = classify_archaic(tok)
                hit = {
                    "token": tok,
                    "clean": clean,
                    "s2": s2,
                    "surprisal": surprisal,
                    "entropy": entropy,
                    "era": era,
                    "author": author,
                    "title": meta.get("title", ""),
                    "category": category,
                    "context_before": t.get("context_before", "")[-40:],
                    "alternatives": t.get("alternatives", []),
                }
                archaic_hits.append(hit)
                era_archaic[era].append(s2)
                poet_archaic[author].append(s2)
                archaic_by_category[category].append(s2)

                # Classify as genuine Straussian or false positive
                # Genuine: S2 > 0 because entropy is LOW (model was confident → poet deviated)
                # False positive: surprisal is high but entropy is also high (model uncertain)
                if s2 > 0:
                    if entropy < 3.0:  # model was confident, yet was surprised
                        genuine_straussian_count += 1
                    else:
                        false_positive_count += 1

            else:
                # Track modern token baseline (content words only)
                if (len(clean) >= 3 and
                    not re.match(r'^[^a-zA-Z]+$', clean) and
                    clean not in {'the', 'and', 'for', 'that', 'this', 'with',
                                  'but', 'are', 'was', 'not', 'his', 'her',
                                  'has', 'had', 'him', 'they', 'from', 'its'}):
                    era_modern[era].append(s2)
                    modern_baseline.append({
                        "s2": s2, "surprisal": surprisal, "entropy": entropy, "era": era
                    })

    # Summary stats
    print(f"\n{'='*60}")
    print("ARCHAIC ENGLISH IN POETRY: S2 ANALYSIS")
    print(f"{'='*60}\n")

    print(f"Total archaic token hits: {len(archaic_hits)}")
    print(f"Unique archaic token types: {len(set(h['clean'] for h in archaic_hits))}")
    print(f"Poems containing archaisms: {len(set(h['title'] for h in archaic_hits))}\n")

    if not archaic_hits:
        print("No archaic tokens found!")
        return

    avg_s2 = sum(h['s2'] for h in archaic_hits) / len(archaic_hits)
    avg_surp = sum(h['surprisal'] for h in archaic_hits) / len(archaic_hits)
    avg_ent = sum(h['entropy'] for h in archaic_hits) / len(archaic_hits)

    mb_s2 = sum(h['s2'] for h in modern_baseline) / len(modern_baseline)
    mb_surp = sum(h['surprisal'] for h in modern_baseline) / len(modern_baseline)
    mb_ent = sum(h['entropy'] for h in modern_baseline) / len(modern_baseline)

    print(f"{'Metric':<25} {'Archaic':>10} {'Modern Baseline':>15}")
    print(f"{'-'*55}")
    print(f"{'Avg S2':<25} {avg_s2:>10.3f} {mb_s2:>15.3f}")
    print(f"{'Avg Surprisal':<25} {avg_surp:>10.3f} {mb_surp:>15.3f}")
    print(f"{'Avg Entropy':<25} {avg_ent:>10.3f} {mb_ent:>15.3f}")
    print(f"{'n':<25} {len(archaic_hits):>10} {len(modern_baseline):>15}")

    pos_s2_archaic = sum(1 for h in archaic_hits if h['s2'] > 0) / len(archaic_hits)
    pos_s2_modern = sum(1 for h in modern_baseline if h['s2'] > 0) / len(modern_baseline)
    print(f"{'%+S2':<25} {pos_s2_archaic:>10.1%} {pos_s2_modern:>15.1%}")

    # Genuine Straussian vs false positive
    pos_archaic = [h for h in archaic_hits if h['s2'] > 0]
    if pos_archaic:
        genuine = sum(1 for h in pos_archaic if h['entropy'] < 3.0)
        false_pos = sum(1 for h in pos_archaic if h['entropy'] >= 3.0)
        print(f"\nAmong {len(pos_archaic)} positive-S2 archaic tokens:")
        print(f"  Genuine Straussian (low-entropy context): {genuine} ({genuine/len(pos_archaic):.1%})")
        print(f"  False positive (high-entropy context):    {false_pos} ({false_pos/len(pos_archaic):.1%})")

    # By category
    print(f"\n{'--- S2 by Archaic Category ---':}")
    print(f"{'Category':<25} {'n':>5} {'Avg S2':>10} {'Avg Surprisal':>15} {'Avg Entropy':>12}")
    print(f"{'-'*70}")
    for cat, vals in sorted(archaic_by_category.items(), key=lambda x: -sum(x[1])/len(x[1])):
        cat_hits = [h for h in archaic_hits if h['category'] == cat]
        a_s = sum(h['s2'] for h in cat_hits) / len(cat_hits)
        a_surp = sum(h['surprisal'] for h in cat_hits) / len(cat_hits)
        a_ent = sum(h['entropy'] for h in cat_hits) / len(cat_hits)
        print(f"{cat:<25} {len(cat_hits):>5} {a_s:>10.3f} {a_surp:>15.3f} {a_ent:>12.3f}")

    # By era
    print(f"\n{'--- S2 by Era (archaic vs baseline) ---':}")
    all_eras = set(list(era_archaic.keys()) + list(era_modern.keys()))
    era_data = []
    for era in all_eras:
        a_vals = era_archaic.get(era, [])
        m_vals = era_modern.get(era, [])
        if a_vals:
            era_data.append((era, len(a_vals),
                             sum(a_vals)/len(a_vals),
                             sum(m_vals)/len(m_vals) if m_vals else float('nan')))

    era_data.sort(key=lambda x: -x[1])  # sort by count
    print(f"{'Era':<25} {'n_archaic':>10} {'Avg S2 (archaic)':>18} {'Avg S2 (modern)':>16}")
    print(f"{'-'*72}")
    for era, n, as2, ms2 in era_data[:15]:
        print(f"{era:<25} {n:>10} {as2:>18.3f} {ms2:>16.3f}")

    # By poet
    print(f"\n{'--- Top Poets by Archaic Token Count ---':}")
    poet_data = [(p, len(v), sum(v)/len(v)) for p, v in poet_archaic.items() if len(v) >= 2]
    poet_data.sort(key=lambda x: -x[1])
    print(f"{'Poet':<35} {'n':>5} {'Avg S2':>10}")
    print(f"{'-'*55}")
    for poet, n, as2 in poet_data[:12]:
        print(f"{poet:<35} {n:>5} {as2:>10.3f}")

    # Most striking archaic tokens
    print(f"\n{'--- Top Archaic S2 Moments (S2 > 1, entropy < 3) ---':}")
    striking = [h for h in archaic_hits if h['s2'] > 1 and h['entropy'] < 3.0]
    striking.sort(key=lambda x: -x['s2'])
    print(f"{'Token':<12} {'S2':>8} {'Surp':>8} {'Ent':>8} {'Poet':<25} {'Context'}")
    print(f"{'-'*90}")
    for h in striking[:15]:
        ctx = h['context_before'].replace('\n', '↵').strip()[-30:]
        alt = h['alternatives'][0]['token'] if h['alternatives'] else '?'
        print(f"{h['token']:<12} {h['s2']:>8.2f} {h['surprisal']:>8.2f} {h['entropy']:>8.2f} {h['author']:<25} ...{ctx} → POET: {h['token'].strip()} / GPT2: {alt}")

    # Tokens where GPT-2 predicted a modern equivalent
    print(f"\n{'--- What GPT-2 Expected Instead of the Archaic Form ---':}")
    substitutions = defaultdict(list)
    for h in archaic_hits:
        if h['alternatives']:
            top_pred = h['alternatives'][0]['token'].strip().lower()
            clean = h['clean']
            substitutions[(clean, top_pred)].append(h['s2'])

    sub_summary = [(k, len(v), sum(v)/len(v)) for k, v in substitutions.items()]
    sub_summary.sort(key=lambda x: -x[1])
    print(f"{'Archaic':<12} {'GPT-2 Expected':<20} {'n':>5} {'Avg S2':>10}")
    print(f"{'-'*55}")
    for (archaic, expected), n, as2 in sub_summary[:20]:
        print(f"{archaic:<12} {expected:<20} {n:>5} {as2:>10.3f}")

    # Save results
    results = {
        "total_archaic": len(archaic_hits),
        "avg_s2_archaic": avg_s2,
        "avg_s2_modern_baseline": mb_s2,
        "avg_surprisal_archaic": avg_surp,
        "avg_entropy_archaic": avg_ent,
        "pos_s2_rate_archaic": pos_s2_archaic,
        "pos_s2_rate_modern": pos_s2_modern,
        "by_category": {
            cat: {
                "n": len(vals),
                "avg_s2": sum(vals)/len(vals)
            }
            for cat, vals in archaic_by_category.items()
        },
        "by_era": {
            era: {
                "n": n,
                "avg_s2_archaic": as2,
                "avg_s2_modern": ms2
            }
            for era, n, as2, ms2 in era_data
        },
        "top_substitutions": [
            {"archaic": k[0], "gpt2_expected": k[1], "n": n, "avg_s2": s}
            for k, n, s in sub_summary[:30]
        ]
    }
    with open("results/archaic_english_s2.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to results/archaic_english_s2.json")


if __name__ == "__main__":
    main()
