"""
The Poetry Anti-Lexicon: What Words Do Poets Consistently Reject?

When a poet's S2 > 0, GPT-2 expected something different. This experiment
builds a corpus-wide frequency table of the words most commonly suppressed
by poets — the model's top prediction when the poet chose something else.

This inverts the usual Straussian gap analysis: instead of asking "what did
the poet choose that was surprising?", we ask "what did language expect that
the poet kept refusing?"

Metrics:
  - Global rejection frequency: which words appear most as top-1 alternative
    when the poet diverged (S2 > 0.5)
  - Rejection weight: total "probability mass" rejected (sum of prob of #1
    prediction across all high-S2 positions)
  - Persistence: positions where GPT-2 wanted a word, didn't get it, wanted
    it AGAIN next token, didn't get it, etc. (n-token dodges)
  - Per-era anti-lexicons: do different eras reject different words?
  - Co-rejection mapping: what do poets choose INSTEAD of the most rejected?

Works purely from precomputed corpus_results.json — no GPU needed.
"""

import json
from collections import defaultdict, Counter
import math

RESULT_PATH = "results/corpus_results.json"
S2_THRESHOLD = 0.5  # minimum S2 to count as a "rejection" event


def clean_token(t: str) -> str:
    return t.strip().lower().replace("Ġ", "").replace("Ċ", "\n").strip()


def load_corpus():
    with open(RESULT_PATH) as f:
        return json.load(f)


def run_anti_lexicon(data):
    # ── Global rejection counts ───────────────────────────────────────────────
    global_reject_count = Counter()
    global_reject_prob = defaultdict(float)   # total probability mass rejected
    global_choices = defaultdict(list)         # rejected_word -> [what poet chose instead]
    era_rejects = defaultdict(Counter)         # era -> Counter of rejected words
    author_rejects = defaultdict(Counter)

    total_s2_positive = 0
    total_tokens = 0

    for poem in data:
        meta = poem.get("metadata", {})
        era = meta.get("era", "unknown")
        author = meta.get("author", "unknown")
        tokens = poem.get("tokens", [])

        for tok in tokens:
            total_tokens += 1
            s2 = tok.get("s2", 0)
            alts = tok.get("alternatives", [])
            chosen = clean_token(tok.get("token", ""))

            if s2 > S2_THRESHOLD and alts:
                total_s2_positive += 1
                top_pred = clean_token(alts[0]["token"])
                top_prob = alts[0]["prob"]

                if top_pred and top_pred != "\n" and top_pred != chosen:
                    global_reject_count[top_pred] += 1
                    global_reject_prob[top_pred] += top_prob
                    global_choices[top_pred].append(chosen)
                    era_rejects[era][top_pred] += 1
                    author_rejects[author][top_pred] += 1

    # ── Persistence analysis: token dodges ────────────────────────────────────
    # A "dodge sequence" = GPT-2 keeps wanting the same word but poet keeps refusing.
    dodge_sequences = []
    for poem in data:
        tokens = poem.get("tokens", [])
        meta = poem.get("metadata", {})
        title = meta.get("title", "?")
        author = meta.get("author", "?")

        i = 0
        while i < len(tokens):
            if not tokens[i].get("alternatives"):
                i += 1
                continue
            top_pred = clean_token(tokens[i]["alternatives"][0]["token"])
            if tokens[i].get("s2", 0) > S2_THRESHOLD and top_pred and top_pred != "\n":
                # Check how long this word persists as top-1 prediction
                run_len = 1
                j = i + 1
                while j < len(tokens):
                    alts_j = tokens[j].get("alternatives", [])
                    if not alts_j:
                        break
                    next_pred = clean_token(alts_j[0]["token"])
                    if next_pred == top_pred and tokens[j].get("s2", 0) > 0:
                        run_len += 1
                        j += 1
                    else:
                        break
                if run_len >= 3:
                    dodge_sequences.append({
                        "word": top_pred,
                        "run_len": run_len,
                        "start_pos": i,
                        "title": title,
                        "author": author,
                        "tokens_chosen": [clean_token(tokens[i+k]["token"]) for k in range(run_len)],
                    })
                i = j
            else:
                i += 1

    return {
        "global_reject_count": global_reject_count,
        "global_reject_prob": global_reject_prob,
        "global_choices": global_choices,
        "era_rejects": era_rejects,
        "author_rejects": author_rejects,
        "dodge_sequences": sorted(dodge_sequences, key=lambda x: -x["run_len"]),
        "total_tokens": total_tokens,
        "total_s2_positive": total_s2_positive,
    }


def analyze_co_rejections(global_choices):
    """What do poets choose INSTEAD of each commonly rejected word?"""
    results = {}
    for rejected, choices in global_choices.items():
        if len(choices) < 5:
            continue
        counter = Counter(choices)
        results[rejected] = counter.most_common(10)
    return results


def print_report(res):
    print("=" * 68)
    print("THE POETRY ANTI-LEXICON")
    print("=" * 68)
    print(f"\nCorpus: {res['total_tokens']} tokens, {res['total_s2_positive']} S2>0.5 events\n")

    # Top 25 rejected words by count
    print("── TOP 30 MOST REJECTED WORDS (by frequency) ──────────────────")
    print(f"{'Rank':<5} {'Word':<20} {'Rejections':<12} {'Avg Prob':<12}")
    print("-" * 52)
    for rank, (word, cnt) in enumerate(res["global_reject_count"].most_common(30), 1):
        avg_prob = res["global_reject_prob"][word] / cnt
        print(f"{rank:<5} {repr(word):<20} {cnt:<12} {avg_prob:.4f}")

    # Top 15 by probability mass (what the model was MOST confident about)
    print("\n── TOP 15 BY PROBABILITY MASS REJECTED ─────────────────────────")
    print("(These are the words the model was most sure about — and poets ignored)")
    top_by_prob = sorted(res["global_reject_prob"].items(), key=lambda x: -x[1])[:15]
    print(f"{'Rank':<5} {'Word':<20} {'Total Prob Mass':<18} {'Count':<10}")
    print("-" * 56)
    for rank, (word, prob_mass) in enumerate(top_by_prob, 1):
        cnt = res["global_reject_count"][word]
        print(f"{rank:<5} {repr(word):<20} {prob_mass:<18.3f} {cnt:<10}")

    # Era-level anti-lexicons
    print("\n── ERA-LEVEL ANTI-LEXICONS (top 5 per era) ─────────────────────")
    for era, counter in sorted(res["era_rejects"].items()):
        top5 = counter.most_common(5)
        words_str = ", ".join(f"{repr(w)} ({c})" for w, c in top5)
        print(f"\n{era.upper()}")
        print(f"  {words_str}")

    # Dodge sequences
    print("\n── LONGEST DODGE SEQUENCES (GPT-2 wants the same word N times) ─")
    print("(Consecutive positions where the model kept predicting a word but poet refused)")
    for seq in res["dodge_sequences"][:15]:
        chosen_str = " → ".join(repr(t) for t in seq["tokens_chosen"])
        print(f"\n  '{seq['word']}' avoided {seq['run_len']}x  |  {seq['title']} ({seq['author']})")
        print(f"  Poet chose instead: {chosen_str}")


if __name__ == "__main__":
    print("Loading corpus...")
    data = load_corpus()
    print(f"Loaded {len(data)} texts.")

    print("Running anti-lexicon analysis...")
    res = run_anti_lexicon(data)

    co = analyze_co_rejections(res["global_choices"])

    print_report(res)

    # Co-rejection analysis
    print("\n── CO-REJECTION: What do poets choose INSTEAD? ─────────────────")
    top_rejected = [w for w, _ in res["global_reject_count"].most_common(10)]
    for word in top_rejected:
        if word in co:
            alts_str = ", ".join(f"{repr(t)} ({c})" for t, c in co[word][:5])
            print(f"\n  Rejected '{word}' → poet chose: {alts_str}")

    print("\nDone.")
