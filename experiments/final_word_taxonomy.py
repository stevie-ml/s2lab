"""
The Last Stand: Vocabulary of Poetic Endings
============================================
Extension of the trilogy: opening_salvo → closing_salvo → penultimate_anomaly.

We know: the "penultimate" position (clean[-2]) is the true final semantic
choice in most poems (92.7% end with punctuation as the last token). This
experiment asks: WHAT does the poet choose at that slot, and WHAT does GPT-2
expect? We compare the "expected closing vocabulary" (GPT-2's alternatives)
against the "actual closing vocabulary" (what poets wrote) to reveal the
systematic divergence between model expectation and poetic choice at the
single most semantically charged moment of a poem.

Research questions:
1. What words appear most often as the final semantic word (penultimate position)?
2. What does GPT-2 predict at the penultimate position? Is it a different vocabulary?
3. Is the actual final word in GPT-2's top-10 alternatives? What rank?
4. Do certain eras more often choose unexpected final words (higher rank divergence)?
5. Are there semantic categories that dominate closings?
   (e.g., do poets close with nature words? abstractions? body parts?)
6. Is there a "default closing word" GPT-2 almost always wants?
"""

import json
import re
import math
from collections import Counter, defaultdict

CORPUS_PATH = "results/corpus_results.json"
OUTPUT_PATH = "results/final_word_taxonomy.json"

P_NEWLINE_MAX = 0.9
MIN_CLEAN = 30

FUNCTION = {
    "the", "a", "an", "of", "in", "on", "at", "to", "by", "with",
    "from", "for", "and", "or", "but", "nor", "yet", "so",
    "i", "you", "he", "she", "it", "we", "they", "my", "your",
    "his", "her", "its", "our", "their", "me", "him", "us", "them",
    "is", "are", "was", "were", "be", "been", "being", "am",
    "have", "has", "had", "do", "does", "did",
    "not", "no", "never", "nor",
    "that", "this", "these", "those",
    "as", "if", "when", "while", "though", "although",
    "after", "before", "since", "until", "than",
    "all", "any", "each", "every", "both", "more", "most", "own",
    "such", "what", "which", "who", "whom", "whose",
    "can", "could", "may", "might", "shall", "should", "will", "would",
    "must", "ought",
}

PUNCT_ONLY = re.compile(r'^[\s.,;:!?\'\"–—\-()[\]{}/\\]+$')


def is_punct(text):
    t = text.strip()
    if not t:
        return True
    return bool(PUNCT_ONLY.match(t))


def is_subword_suffix(text):
    """GPT-2 subword tokens that continue a word don't start with a space."""
    return len(text) > 0 and not text.startswith(' ') and not text[0].isdigit()


def classify_token_type(text):
    t = text.strip().lower()
    if not t:
        return "empty"
    if is_punct(text):
        return "punct"
    if t.isdigit():
        return "numeral"
    if "'" in t:
        return "contraction"
    if text[0].isupper() and len(text.strip()) > 1:
        return "capitalized"
    if t in FUNCTION:
        return "function"
    return "content"


def clean_tokens(poem):
    return [t for t in poem["tokens"] if t.get("p_newline", 0) < P_NEWLINE_MAX]


def find_final_content_slot(clean):
    """
    Find the 'final semantic slot' — the last clean token that is a
    content word or capitalized word (not pure punctuation, not function word,
    not a subword fragment mid-word). This extends the penultimate_anomaly
    methodology by walking backward until we find a semantically meaningful token.
    """
    for i in range(len(clean) - 1, -1, -1):
        tok = clean[i]
        text = tok['token']
        cat = classify_token_type(text)
        # Skip punctuation and empty
        if cat in ('punct', 'empty'):
            continue
        # Skip function words
        if cat == 'function':
            continue
        # Skip bare subword suffixes (e.g. 'ility', 'ing', 'ness' < 4 chars with no space)
        if is_subword_suffix(text) and len(text.strip()) <= 3:
            continue
        # Accept content, capitalized, numeral, contraction
        return i, tok, cat
    return None, None, None


def rank_of_actual(tok):
    """Rank of the actual token in GPT-2's top-10 alternatives. None if not listed."""
    actual = tok['token']
    for i, a in enumerate(tok.get('alternatives', [])):
        if a['token'] == actual:
            return i + 1
    return None  # beyond top-10


def gpt2_top_content_preds(tok, n=5):
    """GPT-2's top predicted tokens excluding punctuation."""
    results = []
    for a in tok.get('alternatives', []):
        if not is_punct(a['token']):
            results.append((a['token'].strip().lower(), a['prob']))
        if len(results) >= n:
            break
    return results


def semantic_group(word):
    w = word.strip(" ,.'\"").lower()

    NATURE = {
        'sea', 'sky', 'sun', 'moon', 'star', 'stars', 'wind', 'rain', 'water',
        'earth', 'night', 'day', 'light', 'dark', 'darkness', 'dawn', 'fire',
        'tree', 'flower', 'stone', 'grass', 'cloud', 'snow', 'air', 'shore',
        'wave', 'waves', 'hill', 'river', 'field', 'bird', 'birds', 'leaf',
        'leaves', 'spring', 'winter', 'summer', 'autumn', 'ground', 'sky',
        'breeze', 'ocean', 'mountain', 'valley', 'forest', 'wood', 'woods',
        'rain', 'shadow', 'shadows', 'silence', 'quiet', 'still', 'deep',
        'heaven', 'heavens', 'god', 'gods',
    }
    DEATH_ABSENCE = {
        'death', 'dead', 'die', 'died', 'end', 'nothing', 'void',
        'gone', 'lost', 'grave', 'tomb', 'bones', 'dust', 'ash', 'ashes',
        'fall', 'falls', 'fade', 'fades', 'forgotten', 'empty', 'absence',
        'away', 'far', 'vanish', 'vanished', 'pass', 'passed', 'perish',
        'ruin', 'ruins', 'bare', 'bleak', 'alone', 'apart',
    }
    TIME = {
        'time', 'hour', 'hours', 'day', 'days', 'years', 'year', 'night',
        'long', 'old', 'age', 'past', 'ever', 'never', 'always', 'again',
        'moment', 'once', 'last', 'first', 'then', 'now', 'soon', 'brief',
        'eternal', 'endless', 'forever', 'before', 'after',
    }
    EMOTION = {
        'love', 'heart', 'tears', 'joy', 'grief', 'pain', 'fear', 'hope',
        'dream', 'dreams', 'desire', 'longing', 'sorrow', 'peace', 'happiness',
        'sweet', 'dear', 'beautiful', 'beauty', 'grace', 'wonder', 'awe',
        'pride', 'shame', 'regret', 'bliss', 'despair', 'anguish', 'delight',
        'weep', 'weeping', 'laugh', 'laughter', 'smile',
    }
    BODY_SOUL = {
        'eye', 'eyes', 'hand', 'hands', 'face', 'mouth', 'voice', 'blood',
        'skin', 'bone', 'breath', 'lips', 'tongue', 'head', 'soul', 'spirit',
        'mind', 'body', 'flesh', 'heart', 'arms', 'feet', 'brow', 'breast',
    }
    LIGHT_DARK = {
        'light', 'dark', 'darkness', 'bright', 'brightness', 'shine', 'shines',
        'glow', 'gleam', 'shadow', 'shadows', 'black', 'white', 'gold', 'golden',
        'pale', 'dim', 'radiant', 'luminous', 'gloom', 'dusk', 'twilight',
    }

    if w in NATURE:
        return 'nature/cosmos'
    if w in DEATH_ABSENCE:
        return 'death/absence'
    if w in TIME:
        return 'time'
    if w in EMOTION:
        return 'emotion'
    if w in BODY_SOUL:
        return 'body/soul'
    if w in LIGHT_DARK:
        return 'light/dark'
    return 'other'


def pearson(xs, ys):
    n = len(xs)
    if n < 2:
        return float('nan')
    mx = sum(xs) / n
    my = sum(ys) / n
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    dx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    dy = math.sqrt(sum((y - my) ** 2 for y in ys))
    if dx == 0 or dy == 0:
        return 0.0
    return num / (dx * dy)


def main():
    with open(CORPUS_PATH) as f:
        corpus = json.load(f)

    # ── per-poem records
    records = []
    # ── aggregate counters
    actual_words = Counter()
    gpt2_top1_words = Counter()
    gpt2_top5_words = Counter()
    actual_groups = Counter()
    gpt2_groups = Counter()

    era_records = defaultdict(list)
    author_records = defaultdict(list)

    # ── poems where actual is in GPT-2's top-10
    in_top10 = 0
    in_top5 = 0
    in_top1 = 0
    total = 0

    rank_list = []  # rank when in top-10

    # ── rank histogram
    rank_hist = Counter()

    for poem in corpus:
        lang = poem['metadata'].get('language', 'en')
        if lang != 'en':
            continue
        clean = clean_tokens(poem)
        if len(clean) < MIN_CLEAN:
            continue

        era = poem['metadata'].get('era', 'unknown')
        author = poem['metadata'].get('author', 'unknown')
        title = poem['metadata'].get('title', '')

        # Overall poem S2
        all_s2 = [t['s2'] for t in clean]
        poem_s2 = sum(all_s2) / len(all_s2)

        # Find final semantic slot
        idx, tok, cat = find_final_content_slot(clean)
        if tok is None:
            continue

        total += 1

        actual_text = tok['token']
        actual_word = actual_text.strip().lower()
        actual_s2 = tok['s2']
        actual_entropy = tok['entropy']
        top_pred = tok.get('alternatives', [{}])[0].get('token', '') if tok.get('alternatives') else ''
        rank = rank_of_actual(tok)
        gpt2_content_preds = gpt2_top_content_preds(tok, 5)

        # Counters
        if actual_word:
            actual_words[actual_word] += 1
        if top_pred:
            gpt2_top1_words[top_pred.strip().lower()] += 1
        for w, _ in gpt2_content_preds:
            gpt2_top5_words[w] += 1

        # Semantic groups
        sg_actual = semantic_group(actual_word)
        actual_groups[sg_actual] += 1
        for w, _ in gpt2_content_preds:
            sg_gpt2 = semantic_group(w)
            gpt2_groups[sg_gpt2] += 1

        # Rank stats
        if rank is not None:
            in_top10 += 1
            rank_list.append(rank)
            rank_hist[rank] += 1
            if rank <= 5:
                in_top5 += 1
            if rank == 1:
                in_top1 += 1

        # Whether actual matches GPT-2's top-content prediction
        top_content = gpt2_content_preds[0][0] if gpt2_content_preds else ''
        matches_top_content = (actual_word == top_content)

        # How far down the full alternatives list is the actual word?
        # (rank=None means beyond top-10, treat as rank=11 for stats)
        rank_for_stats = rank if rank is not None else 11

        rec = {
            'title': title,
            'author': author,
            'era': era,
            'actual_word': actual_word,
            'actual_s2': actual_s2,
            'actual_entropy': actual_entropy,
            'actual_surprisal': actual_s2 + actual_entropy,
            'token_cat': cat,
            'rank': rank,
            'rank_for_stats': rank_for_stats,
            'in_top10': rank is not None,
            'in_top1': rank == 1,
            'top_pred': top_pred.strip().lower(),
            'gpt2_content_preds': [w for w, _ in gpt2_content_preds],
            'matches_top_content': matches_top_content,
            'actual_group': sg_actual,
            'poem_s2': poem_s2,
            'poem_length': len(clean),
            'position_from_end': len(clean) - 1 - idx,  # how many tokens from end
        }
        records.append(rec)
        era_records[era].append(rec)
        author_records[author].append(rec)

    # ── Era-level divergence stats
    era_stats = {}
    for era, recs in era_records.items():
        if len(recs) < 3:
            continue
        ranks = [r['rank_for_stats'] for r in recs]
        in10 = [r for r in recs if r['in_top10']]
        actual_s2s = [r['actual_s2'] for r in recs]
        era_stats[era] = {
            'n': len(recs),
            'mean_rank': sum(ranks) / len(ranks),
            'pct_in_top10': 100 * len(in10) / len(recs),
            'pct_in_top1': 100 * sum(1 for r in recs if r['in_top1']) / len(recs),
            'mean_actual_s2': sum(actual_s2s) / len(actual_s2s),
            'top_actual_words': [w for w, _ in Counter(
                r['actual_word'] for r in recs).most_common(5)],
            'top_gpt2_preds': [w for w, _ in Counter(
                r['top_pred'] for r in recs).most_common(5)],
        }

    # ── Author-level divergence (authors with >= 3 poems)
    author_stats = {}
    for author, recs in author_records.items():
        if len(recs) < 3:
            continue
        ranks = [r['rank_for_stats'] for r in recs]
        actual_s2s = [r['actual_s2'] for r in recs]
        author_stats[author] = {
            'n': len(recs),
            'mean_rank': sum(ranks) / len(ranks),
            'pct_in_top10': 100 * sum(1 for r in recs if r['in_top10']) / len(recs),
            'mean_actual_s2': sum(actual_s2s) / len(actual_s2s),
            'top_actual_words': [w for w, _ in Counter(
                r['actual_word'] for r in recs).most_common(5)],
        }

    # ── Rank correlation: does final-word rank predict poem-level S2?
    pairs = [(r['rank_for_stats'], r['poem_s2']) for r in records]
    r_rank_poems2 = pearson([p[0] for p in pairs], [p[1] for p in pairs])

    # ── GPT-2's "default closing vocabulary" — what it always wants
    # (top-1 prediction at final semantic position across all poems)
    gpt2_default_closing = gpt2_top1_words.most_common(20)

    output = {
        'corpus_stats': {
            'total_poems': total,
            'pct_in_top10': 100 * in_top10 / total,
            'pct_in_top5': 100 * in_top5 / total,
            'pct_in_top1': 100 * in_top1 / total,
            'mean_rank_when_in_top10': sum(rank_list) / len(rank_list) if rank_list else None,
            'r_rank_vs_poem_s2': r_rank_poems2,
        },
        'rank_histogram': {str(k): v for k, v in sorted(rank_hist.items())},
        'actual_closing_words': actual_words.most_common(30),
        'gpt2_top1_closing_words': gpt2_default_closing,
        'gpt2_top5_closing_words': gpt2_top5_words.most_common(20),
        'actual_semantic_groups': dict(actual_groups),
        'gpt2_semantic_groups': dict(gpt2_groups),
        'era_stats': dict(sorted(era_stats.items(), key=lambda x: x[1]['mean_rank'], reverse=True)),
        'author_stats': dict(sorted(author_stats.items(), key=lambda x: x[1]['mean_rank'], reverse=True)),
        'per_poem_records': records,
    }

    with open(OUTPUT_PATH, 'w') as f:
        json.dump(output, f, indent=2)

    # Print summary to stdout
    cs = output['corpus_stats']
    print(f"FINAL WORD TAXONOMY — {total} poems analyzed")
    print(f"\n=== Divergence from GPT-2 ===")
    print(f"  Final word in GPT-2's top-1:  {cs['pct_in_top1']:.1f}%")
    print(f"  Final word in GPT-2's top-5:  {cs['pct_in_top5']:.1f}%")
    print(f"  Final word in GPT-2's top-10: {cs['pct_in_top10']:.1f}%")
    print(f"  Mean rank (when in top-10): {cs['mean_rank_when_in_top10']:.2f}")
    print(f"  r(rank, poem S2): {cs['r_rank_vs_poem_s2']:.3f}")

    print(f"\n=== Actual Closing Vocabulary (top 15) ===")
    for w, n in output['actual_closing_words'][:15]:
        print(f"  {w!r:20s}  n={n}")

    print(f"\n=== GPT-2's Default Closing Predictions (top 15) ===")
    for w, n in output['gpt2_top1_closing_words'][:15]:
        print(f"  {w!r:20s}  n={n}")

    print(f"\n=== Semantic Groups — Actual vs GPT-2 ===")
    total_actual = sum(actual_groups.values())
    total_gpt2 = sum(gpt2_groups.values())
    groups = sorted(set(actual_groups) | set(gpt2_groups))
    for g in groups:
        a = actual_groups.get(g, 0)
        b = gpt2_groups.get(g, 0)
        print(f"  {g:20s}  actual={100*a/total_actual:.1f}%  gpt2={100*b/total_gpt2:.1f}%")

    print(f"\n=== Era Divergence (sorted by mean rank — higher = more surprising) ===")
    for era, st in list(output['era_stats'].items()):
        print(f"  {era:25s}  n={st['n']:3d}  mean_rank={st['mean_rank']:.2f}  "
              f"in_top10={st['pct_in_top10']:.0f}%  "
              f"avg_s2={st['mean_actual_s2']:+.3f}")

    print(f"\n=== Author Divergence (top 10 most surprising enders) ===")
    for author, st in list(output['author_stats'].items())[:10]:
        print(f"  {author:25s}  n={st['n']:3d}  mean_rank={st['mean_rank']:.2f}  "
              f"words={st['top_actual_words']}")

    print(f"\nSaved: {OUTPUT_PATH}")


if __name__ == '__main__':
    main()
