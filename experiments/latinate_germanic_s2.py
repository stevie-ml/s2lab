"""
Experiment: Latinate vs. Germanic Diction and S2

Question: Do words of Latin/French origin (Latinate) show systematically different
S2 values compared to words of Germanic/Anglo-Saxon origin in poetry?

This is a classic tension in English poetics: Milton's grandiloquent Latinate
vocabulary vs. Wordsworth's "language really used by men" (Anglo-Saxon).
Information theory can test whether GPT-2's training reflects this,
and whether poets exploit the difference for surprise.

Method: Use curated word lists for Latinate and Germanic vocabulary,
look up their S2 values in the corpus, and compare distributions.
"""

import json
import re
from collections import defaultdict
import statistics

# Curated word lists based on etymology
# Germanic/Anglo-Saxon: short, concrete, everyday English words of OE/Proto-Germanic origin
GERMANIC_WORDS = {
    # body
    "blood", "bone", "flesh", "hand", "head", "heart", "eye", "ear", "mouth",
    "tooth", "foot", "knee", "lip", "skin", "breath", "arm", "leg",
    # nature
    "sun", "moon", "star", "stone", "wind", "rain", "snow", "fire", "earth",
    "water", "wood", "leaf", "tree", "flower", "hill", "sea", "sky", "cloud",
    "grass", "field", "light", "dark", "night", "day",
    # death and life
    "death", "birth", "life", "live", "die", "dead", "born", "grow",
    # emotions/states
    "love", "hate", "fear", "grief", "hope", "joy", "anger", "glad", "sad",
    "holy", "true", "good", "kind", "sweet", "dear", "free",
    # actions
    "stand", "walk", "run", "fall", "sleep", "wake", "speak", "sing",
    "fly", "swim", "swim", "hold", "give", "take", "go", "come",
    # connectives/determiners
    "and", "but", "for", "the", "that", "this", "with", "from", "into",
    # pronouns
    "we", "they", "our", "thee", "thou", "thine",
    # misc concrete
    "old", "new", "long", "deep", "cold", "warm", "bright", "white", "black",
    "red", "green", "gold", "hard", "soft", "wild", "bare", "still", "full",
    "small", "great", "wide", "far", "high", "low", "here", "there",
    "bird", "wolf", "fish", "horse", "hound", "worm", "bear", "bee",
    "bread", "milk", "salt", "ale", "sword", "shield", "road", "gate",
    "friend", "king", "folk", "lot", "land", "house", "home",
    "weight", "weight", "shape", "shape", "clean", "lean",
}

# Latinate/Romance words: typically from Latin, French, or Italian — often abstract,
# polysyllabic, learned; entered English after the Norman Conquest (1066)
LATINATE_WORDS = {
    # abstract concepts
    "beauty", "nature", "fortune", "virtue", "justice", "reason", "passion",
    "desire", "pleasure", "liberty", "glory", "honor", "grace", "mercy",
    "silence", "absence", "presence", "desire", "patience",
    "sorrow", "desolate", "solitude", "eternity", "infinity",
    # intellectual/spiritual
    "contemplation", "imagination", "inspiration", "revelation", "creation",
    "tranquil", "serene", "divine", "celestial", "immortal", "eternal",
    "infinite", "sublime", "gentle", "noble", "tender", "pure",
    # verbs
    "perceive", "conceive", "achieve", "receive", "believe", "receive",
    "remain", "contain", "maintain", "attain", "obtain", "retain",
    "illuminate", "celebrate", "contemplate", "meditate", "consecrate",
    "adorn", "ascend", "descend", "emerge", "immerse", "transform",
    "restore", "compose", "dispose", "impose", "suppose", "expose",
    # adjectives
    "ardent", "fervent", "ancient", "distant", "brilliant", "radiant",
    "obscure", "profound", "transparent", "magnificent", "exquisite",
    "elaborate", "eloquent", "luminous", "tremulous", "solitary",
    "mortal", "mortal", "final", "vital", "central", "spiritual",
    "tender", "gentle", "noble", "humble", "simple",
    # from French
    "journey", "palace", "mountain", "river", "forest", "garden",
    "shadow", "mirror", "color", "flower", "power", "tower", "hour",
    "voice", "choice", "noise", "rejoice",
    # more abstract
    "memory", "history", "story", "glory", "victory", "mystery",
    "beauty", "duty", "pity", "city", "liberty", "vanity",
    "melancholy", "elegy", "sonnet", "lyric", "rhyme",
}

def normalize_token(token):
    """Strip leading space and lowercase."""
    return token.strip().lower().strip(".,!?;:\"'()-–—")

def classify_word(word):
    """Classify a word as 'germanic', 'latinate', or 'unknown'."""
    word_lower = word.lower()
    if word_lower in GERMANIC_WORDS:
        return "germanic"
    if word_lower in LATINATE_WORDS:
        return "latinate"
    return "unknown"

def syllable_count(word):
    """Rough syllable count using vowel groups."""
    word = word.lower()
    word = re.sub(r'[^a-z]', '', word)
    count = len(re.findall(r'[aeiou]+', word))
    # Final 'e' usually silent
    if word.endswith('e') and len(word) > 1:
        count = max(1, count - 1)
    return max(1, count)

def main():
    with open('results/corpus_results.json') as f:
        corpus = json.load(f)

    # Per-category stats
    germanic_s2 = []
    latinate_s2 = []
    germanic_surprisal = []
    latinate_surprisal = []
    germanic_entropy = []
    latinate_entropy = []

    # Track by poet
    poet_germanic = defaultdict(list)
    poet_latinate = defaultdict(list)

    # Track specific high-contrast examples
    top_germanic = []  # (s2, token, context, poem_title)
    top_latinate = []

    # Track era-level differences
    era_germanic = defaultdict(list)
    era_latinate = defaultdict(list)

    # Syllable length vs S2 (proxy for Latinate)
    syllable_s2 = defaultdict(list)  # syllable_count -> [s2]

    for poem_data in corpus:
        meta = poem_data['metadata']
        title = meta.get('title', 'Unknown')
        author = meta.get('author', 'Unknown')
        era = meta.get('era', 'unknown')
        lang = meta.get('language', 'en')

        if lang != 'en':
            continue

        for tok in poem_data.get('tokens', []):
            raw_token = tok['token']
            norm = normalize_token(raw_token)
            s2 = tok['s2']
            surprisal = tok['surprisal']
            entropy = tok['entropy']

            # Skip stanza break artifact tokens
            # (high prob newline = stanza break)
            if raw_token.strip() == '' or norm == '':
                continue

            classification = classify_word(norm)

            if classification == 'germanic':
                germanic_s2.append(s2)
                germanic_surprisal.append(surprisal)
                germanic_entropy.append(entropy)
                poet_germanic[author].append(s2)
                era_germanic[era].append(s2)
                top_germanic.append((s2, raw_token, tok.get('context_before', ''), title, author))
            elif classification == 'latinate':
                latinate_s2.append(s2)
                latinate_surprisal.append(surprisal)
                latinate_entropy.append(entropy)
                poet_latinate[author].append(s2)
                era_latinate[era].append(s2)
                top_latinate.append((s2, raw_token, tok.get('context_before', ''), title, author))

            # Syllable-based analysis (regardless of classification)
            syl = syllable_count(norm)
            if syl <= 4:  # reasonable range
                syllable_s2[syl].append(s2)

    # Summary stats
    def stats(vals):
        if not vals:
            return {}
        return {
            'n': len(vals),
            'mean': round(statistics.mean(vals), 4),
            'median': round(statistics.median(vals), 4),
            'stdev': round(statistics.stdev(vals) if len(vals) > 1 else 0, 4),
            'pos_ratio': round(sum(1 for v in vals if v > 0) / len(vals), 4),
        }

    results = {
        'germanic': {
            's2': stats(germanic_s2),
            'surprisal': stats(germanic_surprisal),
            'entropy': stats(germanic_entropy),
        },
        'latinate': {
            's2': stats(latinate_s2),
            'surprisal': stats(latinate_surprisal),
            'entropy': stats(latinate_entropy),
        },
        'syllable_s2': {
            str(syl): stats(vals)
            for syl, vals in sorted(syllable_s2.items())
        },
        'era_comparison': {},
        'poet_comparison': {},
        'top_germanic_moments': [],
        'top_latinate_moments': [],
    }

    # Era comparison
    all_eras = set(list(era_germanic.keys()) + list(era_latinate.keys()))
    for era in all_eras:
        g = era_germanic.get(era, [])
        l = era_latinate.get(era, [])
        if g or l:
            results['era_comparison'][era] = {
                'germanic_mean_s2': round(statistics.mean(g), 4) if g else None,
                'latinate_mean_s2': round(statistics.mean(l), 4) if l else None,
                'germanic_n': len(g),
                'latinate_n': len(l),
                'gap': round(statistics.mean(g) - statistics.mean(l), 4) if (g and l) else None,
            }

    # Poet comparison (poets with sufficient data)
    all_poets = set(list(poet_germanic.keys()) + list(poet_latinate.keys()))
    for poet in all_poets:
        g = poet_germanic.get(poet, [])
        l = poet_latinate.get(poet, [])
        if len(g) >= 5 and len(l) >= 5:
            results['poet_comparison'][poet] = {
                'germanic_mean_s2': round(statistics.mean(g), 4),
                'latinate_mean_s2': round(statistics.mean(l), 4),
                'germanic_n': len(g),
                'latinate_n': len(l),
                'gap_g_minus_l': round(statistics.mean(g) - statistics.mean(l), 4),
            }

    # Top moments
    top_germanic_sorted = sorted(top_germanic, key=lambda x: x[0], reverse=True)[:10]
    top_latinate_sorted = sorted(top_latinate, key=lambda x: x[0], reverse=True)[:10]

    results['top_germanic_moments'] = [
        {'s2': round(s2, 2), 'token': tok, 'context': ctx[:40], 'poem': poem, 'author': auth}
        for s2, tok, ctx, poem, auth in top_germanic_sorted
    ]
    results['top_latinate_moments'] = [
        {'s2': round(s2, 2), 'token': tok, 'context': ctx[:40], 'poem': poem, 'author': auth}
        for s2, tok, ctx, poem, auth in top_latinate_sorted
    ]

    # Print summary
    print("=== LATINATE vs. GERMANIC DICTION: S2 ANALYSIS ===\n")
    print(f"Germanic words found: {results['germanic']['s2']['n']} tokens")
    print(f"Latinate words found: {results['latinate']['s2']['n']} tokens")
    print()
    print("Mean S2:")
    print(f"  Germanic: {results['germanic']['s2']['mean']}")
    print(f"  Latinate: {results['latinate']['s2']['mean']}")
    print(f"  Gap (G-L): {round(results['germanic']['s2']['mean'] - results['latinate']['s2']['mean'], 4)}")
    print()
    print("Mean Surprisal:")
    print(f"  Germanic: {results['germanic']['surprisal']['mean']}")
    print(f"  Latinate: {results['latinate']['surprisal']['mean']}")
    print()
    print("Mean Entropy:")
    print(f"  Germanic: {results['germanic']['entropy']['mean']}")
    print(f"  Latinate: {results['latinate']['entropy']['mean']}")
    print()
    print("+S2 Ratio (fraction with positive S2):")
    print(f"  Germanic: {results['germanic']['s2']['pos_ratio']}")
    print(f"  Latinate: {results['latinate']['s2']['pos_ratio']}")
    print()
    print("=== SYLLABLE COUNT vs. S2 ===")
    for syl, st in results['syllable_s2'].items():
        print(f"  {syl} syllables: mean S2 = {st['mean']}, n = {st['n']}")
    print()
    print("=== ERA COMPARISON ===")
    for era, d in sorted(results['era_comparison'].items(), key=lambda x: (x[1]['gap'] or 0), reverse=True):
        if d['gap'] is not None:
            print(f"  {era}: G={d['germanic_mean_s2']} (n={d['germanic_n']}), "
                  f"L={d['latinate_mean_s2']} (n={d['latinate_n']}), gap={d['gap']}")
    print()
    print("=== POET COMPARISON (Germanic S2 - Latinate S2) ===")
    poet_data = sorted(results['poet_comparison'].items(),
                       key=lambda x: x[1]['gap_g_minus_l'], reverse=True)
    for poet, d in poet_data[:15]:
        print(f"  {poet}: G={d['germanic_mean_s2']}, L={d['latinate_mean_s2']}, gap={d['gap_g_minus_l']}")
    print()
    print("=== TOP GERMANIC HIGH-S2 MOMENTS ===")
    for m in results['top_germanic_moments'][:5]:
        print(f"  S2={m['s2']}: '{m['token']}' in '{m['poem']}' by {m['author']}")
        print(f"    Context: ...{m['context']}...")
    print()
    print("=== TOP LATINATE HIGH-S2 MOMENTS ===")
    for m in results['top_latinate_moments'][:5]:
        print(f"  S2={m['s2']}: '{m['token']}' in '{m['poem']}' by {m['author']}")
        print(f"    Context: ...{m['context']}...")

    with open('results/latinate_germanic_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    print("\n\nResults saved to results/latinate_germanic_results.json")
    return results

if __name__ == '__main__':
    main()
