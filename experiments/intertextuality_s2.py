"""
Intertextuality and Allusion: S2 Signatures at Quotation Moments

Research question: When a poet quotes or directly alludes to another text,
does S2 spike at that moment? The hypothesis is that allusive language
disrupts the model's predictions because it invokes a different register
(the source text's diction), creating a measurable Straussian gap.

We identify poems known to contain direct quotations/allusions and annotate
the token positions where the allusive language occurs, then compare S2 at
those positions vs. the poem's baseline.
"""

import json
import sys
try:
    import numpy as np
except ImportError:
    # Fallback pure-python stats
    class np:
        @staticmethod
        def mean(x):
            return sum(x) / len(x) if x else 0
        @staticmethod
        def std(x):
            if not x: return 0
            m = sum(x) / len(x)
            return (sum((v - m)**2 for v in x) / len(x)) ** 0.5

def load_corpus():
    with open("results/corpus_results.json") as f:
        return json.load(f)

# Manually annotated allusion catalog:
# Each entry: { title, author, allusion_phrase, source, source_author }
# allusion_phrase = substring that appears in poem text (quoted/alluded passage)

ALLUSIONS = [
    # T.S. Eliot's The Waste Land famously weaves in quotes
    {
        "title": "The Waste Land (opening)",
        "allusion_phrase": "April is the cruellest month",
        "source": "Canterbury Tales ('Whan that Aprill')",
        "source_author": "Chaucer",
        "note": "Eliot inverts Chaucer's hopeful April opening"
    },
    # WB Yeats quoting/echoing the Bible
    {
        "title": "The Second Coming",
        "allusion_phrase": "rough beast",
        "source": "Book of Revelation",
        "source_author": "Bible",
        "note": "Beast of Revelation"
    },
    {
        "title": "The Second Coming",
        "allusion_phrase": "slouches towards Bethlehem",
        "source": "Book of Revelation / birth of Christ",
        "source_author": "Bible",
        "note": "Bethlehem as biblical birthplace"
    },
    # Keats echoing Greek epitaphs
    {
        "title": "Ode on a Grecian Urn",
        "allusion_phrase": "Beauty is truth, truth beauty",
        "source": "Philosophical aphorism / Keats's own crystallization",
        "source_author": "Keats (self-allusion to Platonic tradition)",
        "note": "Philosophical maxim embedded in poem"
    },
    # Shakespeare echoes
    {
        "title": "Not marble, nor the gilded monuments",
        "allusion_phrase": "Not marble",
        "source": "Sonnet 55 — durability of verse over monuments",
        "source_author": "Shakespeare",
        "note": "Opening line is itself the famous allusive formula"
    },
    # Whitman's biblical echo
    {
        "title": "Song of Myself (section 1)",
        "allusion_phrase": "every atom belonging to me",
        "source": "Scientific-philosophical discourse / Lucretius",
        "source_author": "Lucretius / Science",
        "note": "Atomic materialism invoked in lyric context"
    },
    # Blake - biblical allusions
    {
        "title": "The Tyger",
        "allusion_phrase": "Did he who made the Lamb make thee",
        "source": "Book of Job; also echoes Blake's own 'The Lamb'",
        "source_author": "Bible / Blake",
        "note": "Explicit cross-poem allusion to 'The Lamb'"
    },
    # Donne - echoes scripture
    {
        "title": "Death, be not proud",
        "allusion_phrase": "Death, be not proud",
        "source": "1 Corinthians 15:55 / Death personification tradition",
        "source_author": "Bible / tradition",
        "note": "Death apostrophe in Pauline tradition"
    },
    # Hopkins - Gerard Manley Hopkins echoes Scripture
    {
        "title": "God's Grandeur",
        "allusion_phrase": "Holy Ghost over the bent",
        "source": "Genesis 1:2 (Spirit moving over the waters)",
        "source_author": "Bible",
        "note": "Direct echo of creation narrative"
    },
    # Frost - echoes ballad tradition
    {
        "title": "The Road Not Taken",
        "allusion_phrase": "I took the one less traveled by",
        "source": "Popular self-help misreading / Frost's own irony",
        "source_author": "cultural cliche",
        "note": "Phrase that became a cultural cliche; Frost's irony is allusion to that future misreading"
    },
]

def find_poem(corpus, title):
    """Find a poem in corpus by title match."""
    for item in corpus:
        if title.lower() in item['metadata']['title'].lower():
            return item
    return None

def find_tokens_for_phrase(tokens, phrase):
    """
    Find the token positions that correspond to a phrase.
    Reconstruct text from tokens and find the phrase's approximate position.
    """
    # Reconstruct text
    text = "".join(t['token'] for t in tokens)
    # Normalize
    phrase_norm = phrase.lower().strip()
    text_norm = text.lower()

    idx = text_norm.find(phrase_norm[:15])  # search by first 15 chars
    if idx == -1:
        return None, None

    # Find which tokens overlap with this span
    pos = 0
    matching_tokens = []
    for i, t in enumerate(tokens):
        tok_len = len(t['token'])
        if pos >= idx and pos < idx + len(phrase_norm) + 10:
            matching_tokens.append(i)
        pos += tok_len

    return matching_tokens, idx

def analyze_allusions(corpus):
    results = []

    for allusion in ALLUSIONS:
        poem = find_poem(corpus, allusion['title'])
        if poem is None:
            print(f"  NOT FOUND: {allusion['title']}", file=sys.stderr)
            continue

        tokens = poem['tokens']
        avg_s2 = poem['summary']['avg_s2']
        std_s2 = poem['summary']['std_s2']

        # Find the allusive phrase in the token stream
        matching_positions, text_idx = find_tokens_for_phrase(tokens, allusion['allusion_phrase'])

        if not matching_positions:
            print(f"  PHRASE NOT FOUND: '{allusion['allusion_phrase']}' in {allusion['title']}", file=sys.stderr)
            continue

        # Get S2 values for the allusive tokens
        allusion_s2_values = [tokens[i]['s2'] for i in matching_positions if i < len(tokens)]

        if not allusion_s2_values:
            continue

        avg_allusion_s2 = np.mean(allusion_s2_values)
        max_allusion_s2 = max(allusion_s2_values)

        # Z-score: how many SDs above mean?
        if std_s2 > 0:
            z_score = (avg_allusion_s2 - avg_s2) / std_s2
        else:
            z_score = 0

        # What did the model predict at the start of the allusion?
        first_tok_idx = matching_positions[0]
        first_tok = tokens[first_tok_idx]
        top_alternatives = [a['token'] for a in first_tok.get('alternatives', [])[:3]]

        results.append({
            'title': allusion['title'],
            'author': poem['metadata']['author'],
            'allusion_phrase': allusion['allusion_phrase'],
            'source': allusion['source'],
            'note': allusion['note'],
            'poem_avg_s2': round(avg_s2, 3),
            'poem_std_s2': round(std_s2, 3),
            'allusion_avg_s2': round(avg_allusion_s2, 3),
            'allusion_max_s2': round(max_allusion_s2, 3),
            'allusion_z_score': round(z_score, 2),
            'n_tokens_in_phrase': len(matching_positions),
            'top_model_alternatives': top_alternatives,
            'token_s2_values': [round(v, 2) for v in allusion_s2_values],
        })

        print(f"  OK: {allusion['title']} | phrase: '{allusion['allusion_phrase'][:30]}' | avg_s2={avg_allusion_s2:.2f} (z={z_score:.2f})")

    return results

def compute_baseline_comparison(corpus):
    """Compare avg S2 for poems with known allusions vs. rest of corpus."""
    allusion_titles = set(a['title'].lower() for a in ALLUSIONS)

    with_allusions = []
    without_allusions = []

    for item in corpus:
        title = item['metadata']['title'].lower()
        avg_s2 = item['summary']['avg_s2']
        # Check if any allusion title matches
        matched = any(al_title in title for al_title in allusion_titles)
        if matched:
            with_allusions.append(avg_s2)
        else:
            without_allusions.append(avg_s2)

    return {
        'allusive_poems_mean_s2': round(np.mean(with_allusions), 3) if with_allusions else None,
        'non_allusive_poems_mean_s2': round(np.mean(without_allusions), 3) if without_allusions else None,
        'n_allusive': len(with_allusions),
        'n_non_allusive': len(without_allusions),
    }

def main():
    print("Loading corpus...")
    corpus = load_corpus()
    print(f"Loaded {len(corpus)} poems")

    print("\nAnalyzing allusive phrases...")
    allusion_results = analyze_allusions(corpus)

    print("\nComputing baseline comparison...")
    baseline = compute_baseline_comparison(corpus)

    # Aggregate stats
    if allusion_results:
        z_scores = [r['allusion_z_score'] for r in allusion_results]
        avg_z = np.mean(z_scores)
        pct_elevated = sum(1 for z in z_scores if z > 0) / len(z_scores) * 100

        print(f"\n=== Summary ===")
        print(f"Allusions analyzed: {len(allusion_results)}")
        print(f"Mean z-score at allusion sites: {avg_z:.2f}")
        print(f"% with elevated S2 (z>0): {pct_elevated:.0f}%")
        print(f"Allusive poems avg S2: {baseline['allusive_poems_mean_s2']}")
        print(f"Non-allusive poems avg S2: {baseline['non_allusive_poems_mean_s2']}")

    output = {
        'allusion_analyses': allusion_results,
        'baseline_comparison': baseline,
        'summary': {
            'n_analyzed': len(allusion_results),
            'mean_z_score_at_allusion': round(float(np.mean([r['allusion_z_score'] for r in allusion_results])), 3) if allusion_results else None,
            'pct_elevated': round(float(sum(1 for r in allusion_results if r['allusion_z_score'] > 0) / len(allusion_results) * 100), 1) if allusion_results else None,
        }
    }

    with open('results/intertextuality_s2.json', 'w') as f:
        json.dump(output, f, indent=2)

    print("\nResults saved to results/intertextuality_s2.json")
    return output

if __name__ == "__main__":
    main()
