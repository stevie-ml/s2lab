"""
Proper Names as S2 Anchors in Poetry

Research question: Do proper nouns (personal names, place names, mythological
figures) carry systematically higher S2 than common nouns in poetry?

Hypothesis: Proper names are maximally specific referents that GPT-2 cannot
predict well from linguistic context alone. When a poet writes "Mississippi"
instead of "river", or "Keats" instead of "poet", they are deploying a kind of
precision that short-circuits statistical prediction. This should produce high
S2 — high surprisal relative to low local entropy (the model is confident, but
wrong).

The 'nominal anchor' effect: proper names act as reality anchors, tethering
the poem to a specific world. This anchoring should be visible as a distinctive
S2 signature.

Method:
1. Identify candidate proper names: capitalized tokens not at sentence start
2. Split into sub-categories:
   a. Personal names (from a name lexicon)
   b. Place names (geography + political entities)
   c. Classical/mythological names
   d. Generic capitalized nouns (not names)
3. Compare S2 distributions: proper names vs. common nouns vs. function words
4. Examine the 'suppressed' alternatives: what does GPT-2 expect when a proper
   name appears? (Do proper names suppress common nouns, other proper nouns,
   or pronouns?)
5. Measure 'anchor density': poems high in proper names vs. poems with few —
   do they have different S2 architectures?
"""

import json
import re
import os
import statistics
from collections import defaultdict, Counter
from pathlib import Path

RESULTS_DIR = Path(__file__).parent.parent / "results"
FINDINGS_DIR = Path(__file__).parent.parent / "findings"

# ── Name lexicons ──────────────────────────────────────────────────────────────
# Personal names (a broad set of common English first/last names appearing in
# the poetry corpus)
PERSONAL_NAMES = {
    # Poets themselves / addressed poets
    'Shakespeare', 'Milton', 'Keats', 'Shelley', 'Byron', 'Wordsworth',
    'Coleridge', 'Blake', 'Whitman', 'Dickinson', 'Yeats', 'Eliot',
    'Pound', 'Stevens', 'Williams', 'Moore', 'Bishop', 'Lowell', 'Plath',
    'Hughes', 'Ginsberg', 'Neruda', 'Rilke', 'Baudelaire', 'Rimbaud',
    'Verlaine', 'Donne', 'Herbert', 'Hopkins', 'Hardy', 'Auden', 'Larkin',
    'Sexton', 'Oliver', 'Heaney', 'Walcott', 'Brooks', 'Clifton',
    # Historical / mythological persons
    'Achilles', 'Odysseus', 'Orpheus', 'Narcissus', 'Icarus', 'Daedalus',
    'Prometheus', 'Hercules', 'Hector', 'Helen', 'Penelope', 'Circe',
    'Perseus', 'Medusa', 'Persephone', 'Demeter', 'Aphrodite', 'Ares',
    'Athena', 'Apollo', 'Artemis', 'Dionysus', 'Hermes', 'Zeus', 'Hera',
    'Poseidon', 'Pluto', 'Hades', 'Jupiter', 'Venus', 'Mars', 'Mercury',
    'Diana', 'Juno', 'Minerva', 'Bacchus', 'Cupid', 'Psyche',
    # Biblical / religious figures
    'Jesus', 'Christ', 'Mary', 'Moses', 'David', 'Solomon', 'Abraham',
    'Isaac', 'Jacob', 'Joseph', 'Adam', 'Eve', 'Noah', 'Daniel', 'Lazarus',
    'Magdalene', 'Peter', 'Paul', 'John', 'Matthew', 'Luke', 'Mark',
    'Gabriel', 'Michael', 'Lucifer', 'Satan', 'God', 'Lord',
    # Historical figures
    'Caesar', 'Cleopatra', 'Napoleon', 'Lincoln', 'Washington', 'Columbus',
    'Alexander', 'Socrates', 'Plato', 'Aristotle', 'Virgil', 'Homer',
    'Dante', 'Chaucer', 'Spenser', 'Dryden', 'Pope', 'Johnson',
    # Common first names appearing in addressed poems
    'Mary', 'Anne', 'Jane', 'Elizabeth', 'Margaret', 'Rose', 'Alice',
    'William', 'John', 'James', 'Thomas', 'Robert', 'Henry', 'Edward',
    'Charles', 'George', 'Richard', 'Arthur',
}

PLACE_NAMES = {
    # US geography
    'America', 'American', 'Mississippi', 'Missouri', 'Ohio', 'Hudson',
    'Harlem', 'Brooklyn', 'Manhattan', 'Boston', 'Chicago', 'Detroit',
    'California', 'Texas', 'Alabama', 'Georgia', 'Carolina', 'Virginia',
    'Appalachian', 'Niagara', 'Chesapeake',
    # European / classical geography
    'England', 'Britain', 'London', 'Paris', 'Rome', 'Athens', 'Troy',
    'Carthage', 'Sparta', 'Corinth', 'Ithaca', 'Aegean', 'Mediterranean',
    'Thames', 'Seine', 'Rhine', 'Tiber', 'Nile', 'Jordan', 'Euphrates',
    'Jerusalem', 'Bethlehem', 'Canaan', 'Eden', 'Galilee',
    'Scotland', 'Ireland', 'Wales', 'France', 'Germany', 'Italy', 'Greece',
    'Spain', 'Portugal', 'Russia', 'China', 'Japan', 'India', 'Africa',
    'Egypt', 'Persia', 'Arabia', 'Babylon',
    # Mythological / imaginative places
    'Olympus', 'Elysium', 'Hades', 'Tartarus', 'Arcadia', 'Avalon',
    'Camelot', 'Albion', 'Elsinore', 'Lethe', 'Styx', 'Phlegethon',
    'Parnassus', 'Helicon', 'Ida', 'Delphi',
    # Nature / landscape proper names
    'Alps', 'Apennines', 'Pyrenees', 'Himalayas', 'Andes', 'Sahara',
    'Atlantic', 'Pacific', 'Arctic',
}

MYTHOLOGICAL = {
    'Muse', 'Muses', 'Fate', 'Fates', 'Fortune', 'Nature', 'Time', 'Death',
    'Love', 'Truth', 'Beauty', 'Justice', 'Virtue', 'Reason', 'Fancy',
    'Imagination', 'Memory', 'Hope', 'Faith', 'Charity', 'Grace',
    'Elysian', 'Olympian', 'Stygian', 'Lethean',
}

ALL_PROPER = PERSONAL_NAMES | PLACE_NAMES | MYTHOLOGICAL


def is_sentence_start(tokens: list[dict], idx: int) -> bool:
    """Return True if token at idx begins a sentence (after period, newline, or start)."""
    if idx == 0:
        return True
    prev_token = tokens[idx - 1]['token']
    # Newline token = line start
    if prev_token.strip('\n\r') == '':
        return True
    # After sentence-ending punctuation
    if prev_token.strip() in {'.', '!', '?', '...', '…'}:
        return True
    # After colon (new clause, common in poetry)
    if prev_token.strip() == ':':
        return True
    return False


def classify_token(token: str, tokens: list[dict], idx: int) -> str:
    """
    Classify a GPT-2 token into one of:
      PROPER_PERSON, PROPER_PLACE, PROPER_MYTHOLOGICAL,
      PROPER_OTHER, COMMON_NOUN, FUNCTION, PUNCT, OTHER
    """
    # Strip leading space (GPT-2 uses 'Ġ' encoded as space prefix)
    clean = token.strip()

    if not clean:
        return 'OTHER'

    # Punctuation
    if re.fullmatch(r'[^\w]+', clean):
        return 'PUNCT'

    # Is it capitalized?
    if clean[0].isupper() and not is_sentence_start(tokens, idx):
        # Try to match against lexicons
        if clean in PERSONAL_NAMES or clean.rstrip('s') in PERSONAL_NAMES:
            return 'PROPER_PERSON'
        if clean in PLACE_NAMES or clean.rstrip('s') in PLACE_NAMES:
            return 'PROPER_PLACE'
        if clean in MYTHOLOGICAL:
            return 'PROPER_MYTHOLOGICAL'
        # Heuristic: short capitalized words mid-sentence are likely proper names
        if len(clean) >= 3 and clean.isalpha():
            return 'PROPER_OTHER'

    # Function word check (high-frequency closed-class words)
    function_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to',
        'of', 'for', 'with', 'by', 'from', 'is', 'are', 'was', 'were',
        'be', 'been', 'being', 'have', 'has', 'had', 'will', 'would',
        'shall', 'should', 'may', 'might', 'can', 'could', 'do', 'does',
        'did', 'that', 'this', 'these', 'those', 'it', 'its', 'their',
        'they', 'we', 'you', 'he', 'she', 'I', 'me', 'my', 'your',
        'our', 'his', 'her', 'not', 'no', 'nor', 'yet', 'so', 'as',
        'if', 'when', 'while', 'though', 'although', 'because', 'since',
        'than', 'like', 'into', 'out', 'up', 'down', 'off', 'over',
        'through', 'about', 'after', 'before', 'between', 'among',
    }
    lower = clean.lower()
    if lower in function_words:
        return 'FUNCTION'

    # Default to common noun/word
    if clean[0].islower() or is_sentence_start(tokens, idx):
        return 'COMMON_NOUN'

    return 'OTHER'


def analyze_corpus(corpus_path: str) -> dict:
    with open(corpus_path) as f:
        poems = json.load(f)

    # Per-category accumulation
    cat_s2 = defaultdict(list)
    cat_surprisal = defaultdict(list)
    cat_entropy = defaultdict(list)

    # Per-poem proper name count → S2 architecture
    poem_stats = []

    # Suppressed alternatives for proper names
    suppressed = Counter()      # what GPT-2 expected instead of a proper name
    suppressed_cats = Counter() # category of suppressed token

    # Proper name frequency
    name_frequency = Counter()

    for poem in poems:
        tokens = poem['tokens']
        metadata = poem['metadata']

        proper_count = 0
        poem_proper_s2 = []
        poem_common_s2 = []

        for i, tok in enumerate(tokens):
            cat = classify_token(tok['token'], tokens, i)
            s2 = tok['s2']
            cat_s2[cat].append(s2)
            cat_surprisal[cat].append(tok['surprisal'])
            cat_entropy[cat].append(tok['entropy'])

            is_proper = cat.startswith('PROPER')

            if is_proper:
                proper_count += 1
                poem_proper_s2.append(s2)
                name_frequency[tok['token'].strip()] += 1

                # Examine suppressed alternatives
                for alt in (tok.get('alternatives') or [])[:3]:
                    alt_tok = alt.get('token', '')
                    alt_clean = alt_tok.strip()
                    suppressed[alt_clean] += 1
                    # Classify the alternative
                    alt_cat = classify_token(alt_tok, [], 0)
                    suppressed_cats[alt_cat] += 1

            else:
                poem_common_s2.append(s2)

        poem_stats.append({
            'title': metadata.get('title', '?'),
            'author': metadata.get('author', '?'),
            'era': metadata.get('era', '?'),
            'proper_count': proper_count,
            'total_tokens': len(tokens),
            'proper_density': proper_count / max(len(tokens), 1),
            'proper_avg_s2': statistics.mean(poem_proper_s2) if poem_proper_s2 else None,
            'common_avg_s2': statistics.mean(poem_common_s2) if poem_common_s2 else None,
        })

    return {
        'cat_s2': dict(cat_s2),
        'cat_surprisal': dict(cat_surprisal),
        'cat_entropy': dict(cat_entropy),
        'poem_stats': poem_stats,
        'suppressed': suppressed.most_common(30),
        'suppressed_cats': dict(suppressed_cats),
        'name_frequency': name_frequency.most_common(50),
    }


def summarize(values: list) -> dict:
    if not values:
        return {'n': 0, 'mean': None, 'median': None, 'stdev': None}
    return {
        'n': len(values),
        'mean': round(statistics.mean(values), 4),
        'median': round(statistics.median(values), 4),
        'stdev': round(statistics.stdev(values), 4) if len(values) > 1 else 0.0,
    }


def main():
    corpus_path = RESULTS_DIR / 'corpus_results.json'
    results = analyze_corpus(str(corpus_path))

    # Build summary table
    categories = [
        'PROPER_PERSON', 'PROPER_PLACE', 'PROPER_MYTHOLOGICAL', 'PROPER_OTHER',
        'COMMON_NOUN', 'FUNCTION', 'PUNCT',
    ]
    summary = {}
    for cat in categories:
        vals = results['cat_s2'].get(cat, [])
        sup = results['cat_surprisal'].get(cat, [])
        ent = results['cat_entropy'].get(cat, [])
        summary[cat] = {
            's2': summarize(vals),
            'surprisal': summarize(sup),
            'entropy': summarize(ent),
        }

    # Poems ranked by proper-name density
    high_density = sorted(
        [p for p in results['poem_stats'] if p['proper_count'] > 0],
        key=lambda x: x['proper_density'], reverse=True
    )[:15]

    low_density = sorted(
        [p for p in results['poem_stats'] if p['proper_count'] == 0],
        key=lambda x: x['proper_density']
    )[:10]

    # Poems where proper names have highest S2 lift over common nouns
    s2_lift = [
        {
            **p,
            'lift': p['proper_avg_s2'] - p['common_avg_s2']
        }
        for p in results['poem_stats']
        if p['proper_avg_s2'] is not None and p['common_avg_s2'] is not None
    ]
    s2_lift.sort(key=lambda x: x['lift'], reverse=True)

    output = {
        'category_summary': summary,
        'high_proper_density_poems': high_density,
        's2_lift_poems': s2_lift[:20],
        'suppressed_alternatives': results['suppressed'],
        'suppressed_categories': results['suppressed_cats'],
        'most_frequent_proper_names': results['name_frequency'],
    }

    out_path = RESULTS_DIR / 'proper_names_s2.json'
    with open(out_path, 'w') as f:
        json.dump(output, f, indent=2)
    print(f"Results saved to {out_path}")

    # Print summary
    print("\n── Category S2 Summary ──────────────────────────────")
    print(f"{'Category':<25} {'N':>7} {'Mean S2':>9} {'Median S2':>10}")
    print("-" * 55)
    for cat in categories:
        s = summary[cat]['s2']
        if s['n'] > 0:
            print(f"{cat:<25} {s['n']:>7,} {s['mean']:>9.3f} {s['median']:>10.3f}")

    print("\n── Top suppressed alternatives when proper names appear ──")
    for tok, cnt in results['suppressed'][:15]:
        print(f"  {tok!r:20s}: {cnt}")

    print("\n── Suppressed alternative categories ──")
    total = sum(results['suppressed_cats'].values())
    for cat, cnt in sorted(results['suppressed_cats'].items(), key=lambda x: -x[1]):
        pct = cnt / total * 100 if total else 0
        print(f"  {cat:<20}: {cnt:>6,} ({pct:.1f}%)")

    print("\n── Poems with highest proper-name S2 lift ──")
    for p in s2_lift[:10]:
        print(f"  {p['lift']:>+6.2f}  {p['title'][:40]} ({p['author']})")

    return output


if __name__ == '__main__':
    main()
