"""
Famous Lines and S2: Does Memorability Correlate with Information-Theoretic Surprise?

Hypothesis: The most widely-quoted, anthologized lines of poems are moments of
high S2 — what makes them memorable to readers is the same thing that makes them
informationally surprising to GPT-2: they defy statistical expectation.

Method:
1. Hardcode canonical famous lines from poems in the corpus
2. Find those line segments in the tokenized corpus results
3. Compare avg S2 of "famous line" tokens vs. poem average
4. Look at the specific high-S2 tokens within famous lines
"""

import json
import re
from statistics import mean, stdev

FAMOUS_LINES = [
    {
        "poem_title": "I Wandered Lonely as a Cloud",
        "author": "William Wordsworth",
        "famous_phrase": "I wandered lonely as a cloud",
        "source": "title line / opening",
    },
    {
        "poem_title": "Because I could not stop for Death",
        "author": "Emily Dickinson",
        "famous_phrase": "Because I could not stop for Death",
        "source": "opening line",
    },
    {
        "poem_title": "Because I could not stop for Death",
        "author": "Emily Dickinson",
        "famous_phrase": "He kindly stopped for me",
        "source": "line 2",
    },
    {
        "poem_title": "Ozymandias",
        "author": "Percy Bysshe Shelley",
        "famous_phrase": "Look on my Works, ye Mighty, and despair",
        "source": "central inscription",
    },
    {
        "poem_title": "Ozymandias",
        "author": "Percy Bysshe Shelley",
        "famous_phrase": "My name is Ozymandias, King of Kings",
        "source": "inscription",
    },
    {
        "poem_title": "The Love Song of J. Alfred Prufrock (opening)",
        "author": "T.S. Eliot",
        "famous_phrase": "Let us go then, you and I",
        "source": "opening line",
    },
    {
        "poem_title": "The Love Song of J. Alfred Prufrock (opening)",
        "author": "T.S. Eliot",
        "famous_phrase": "I have measured out my life with coffee spoons",
        "source": "central line",
    },
    {
        "poem_title": "The Love Song of J. Alfred Prufrock (opening)",
        "author": "T.S. Eliot",
        "famous_phrase": "Do I dare disturb the universe",
        "source": "famous question",
    },
    {
        "poem_title": "In a Station of the Metro",
        "author": "Ezra Pound",
        "famous_phrase": "The apparition of these faces in the crowd",
        "source": "first line (entire poem is canonical)",
    },
    {
        "poem_title": "The Red Wheelbarrow",
        "author": "William Carlos Williams",
        "famous_phrase": "so much depends",
        "source": "opening (entire poem is canonical)",
    },
    {
        "poem_title": "The Red Wheelbarrow",
        "author": "William Carlos Williams",
        "famous_phrase": "a red wheel",
        "source": "core image",
    },
    {
        "poem_title": "Howl (opening)",
        "author": "Allen Ginsberg",
        "famous_phrase": "I saw the best minds of my generation destroyed by madness",
        "source": "opening line (one of most famous in American poetry)",
    },
    {
        "poem_title": "Harlem",
        "author": "Langston Hughes",
        "famous_phrase": "What happens to a dream deferred",
        "source": "opening question",
    },
    {
        "poem_title": "We Real Cool",
        "author": "Gwendolyn Brooks",
        "famous_phrase": "We real cool",
        "source": "opening / title",
    },
    {
        "poem_title": "The Tyger",
        "author": "William Blake",
        "famous_phrase": "Tyger Tyger, burning bright",
        "source": "opening line",
    },
    {
        "poem_title": "One Art",
        "author": "Elizabeth Bishop",
        "famous_phrase": "The art of losing isn't hard to master",
        "source": "opening / refrain",
    },
    {
        "poem_title": "Daddy (opening)",
        "author": "Sylvia Plath",
        "famous_phrase": "You do not do, you do not do",
        "source": "anaphoric opening",
    },
    {
        "poem_title": "Dover Beach",
        "author": "Matthew Arnold",
        "famous_phrase": "Ah, love, let us be true",
        "source": "the turn / central appeal",
    },
    {
        "poem_title": "The Raven (opening stanzas)",
        "author": "Edgar Allan Poe",
        "famous_phrase": "Nevermore",
        "source": "refrain",
    },
    {
        "poem_title": "Song of Myself (section 1)",
        "author": "Walt Whitman",
        "famous_phrase": "I celebrate myself, and sing myself",
        "source": "opening declaration",
    },
    {
        "poem_title": "The Negro Speaks of Rivers",
        "author": "Langston Hughes",
        "famous_phrase": "I've known rivers",
        "source": "opening / refrain",
    },
    {
        "poem_title": "If We Must Die",
        "author": "Claude McKay",
        "famous_phrase": "If we must die",
        "source": "opening / refrain",
    },
    {
        "poem_title": "We Wear the Mask",
        "author": "Paul Laurence Dunbar",
        "famous_phrase": "We wear the mask that grins and lies",
        "source": "opening line",
    },
]


def normalize(text):
    """Normalize text for matching."""
    return re.sub(r"\s+", " ", text.strip().lower())


def find_phrase_in_tokens(phrase, tokens):
    """Find a phrase in the token sequence; return matching token indices."""
    norm_phrase = normalize(phrase)

    for start_idx in range(len(tokens)):
        accumulated = ""
        for end_idx in range(start_idx, min(start_idx + 30, len(tokens))):
            tok = tokens[end_idx]["token"]
            accumulated += tok
            if normalize(accumulated) == norm_phrase:
                return list(range(start_idx, end_idx + 1))
            if len(normalize(accumulated)) > len(norm_phrase) + 5:
                break

    for start_idx in range(len(tokens)):
        accumulated = ""
        for end_idx in range(start_idx, min(start_idx + 30, len(tokens))):
            tok = tokens[end_idx]["token"]
            accumulated += tok
            acc_norm = normalize(accumulated)
            if norm_phrase in acc_norm or acc_norm in norm_phrase:
                if len(acc_norm) >= len(norm_phrase) * 0.7:
                    return list(range(start_idx, end_idx + 1))
            if len(acc_norm) > len(norm_phrase) + 15:
                break
    return []


def main():
    data = json.load(open("results/corpus_results.json"))
    poem_by_title = {}
    for item in data:
        poem_by_title[item["metadata"]["title"]] = item

    results = []
    not_found = []

    for entry in FAMOUS_LINES:
        title = entry["poem_title"]
        phrase = entry["famous_phrase"]

        poem = poem_by_title.get(title)
        if poem is None:
            not_found.append(f"  POEM NOT FOUND: {title}")
            continue

        tokens = poem["tokens"]
        artifact_free = [t for t in tokens if t.get("p_newline", 0) < 0.9]

        indices = find_phrase_in_tokens(phrase, tokens)
        if not indices:
            not_found.append(f"  PHRASE NOT FOUND: '{phrase}' in '{title}'")
            continue

        phrase_tokens = [tokens[i] for i in indices if i < len(tokens)]
        phrase_s2 = [t["s2"] for t in phrase_tokens]
        poem_s2 = [t["s2"] for t in artifact_free] if artifact_free else [t["s2"] for t in tokens]

        phrase_avg = mean(phrase_s2)
        poem_avg = mean(poem_s2)
        delta = phrase_avg - poem_avg

        reconstructed = "".join(t["token"] for t in phrase_tokens)

        highest_token = max(phrase_tokens, key=lambda t: t["s2"])
        top_alt = highest_token["alternatives"][0]["token"] if highest_token.get("alternatives") else "?"

        results.append({
            "poem": title,
            "author": entry["author"],
            "phrase": phrase,
            "source": entry["source"],
            "reconstructed": reconstructed.strip(),
            "phrase_avg_s2": round(phrase_avg, 3),
            "poem_avg_s2": round(poem_avg, 3),
            "delta": round(delta, 3),
            "n_tokens": len(phrase_tokens),
            "max_s2_token": highest_token["token"].strip(),
            "max_s2": round(highest_token["s2"], 2),
            "model_expected": top_alt.strip(),
            "phrase_tokens": [
                {
                    "token": t["token"],
                    "s2": round(t["s2"], 2),
                    "top_alt": t["alternatives"][0]["token"] if t.get("alternatives") else "?"
                }
                for t in phrase_tokens
            ],
        })

    results.sort(key=lambda r: r["delta"], reverse=True)

    above_avg = [r for r in results if r["delta"] > 0]
    below_avg = [r for r in results if r["delta"] <= 0]
    all_deltas = [r["delta"] for r in results]
    mean_delta = mean(all_deltas)

    print("=" * 70)
    print("FAMOUS LINES AND S2: MEMORABILITY AS SURPRISE")
    print("=" * 70)
    print(f"\nTotal famous lines analyzed: {len(results)}")
    print(f"Lines ABOVE their poem's avg S2: {len(above_avg)} / {len(results)} ({100*len(above_avg)/len(results):.0f}%)")
    print(f"Mean delta (famous - poem avg): {mean_delta:+.3f} bits")
    if len(all_deltas) > 1:
        print(f"SD of deltas: {stdev(all_deltas):.3f}")

    print("\n" + "=" * 70)
    print("RANKED BY DELTA (phrase avg S2 - poem avg S2)")
    print("=" * 70)
    print(f"{'Phrase':<45} {'Auth':<12} {'Phrase':>8} {'Poem':>8} {'Delta':>8}")
    print("-" * 83)
    for r in results:
        marker = "+" if r["delta"] > 0 else " "
        phrase_short = r["phrase"][:42] + "..." if len(r["phrase"]) > 45 else r["phrase"]
        author_short = r["author"].split()[-1][:11]
        print(
            f"{marker}{phrase_short:<44} {author_short:<12} "
            f"{r['phrase_avg_s2']:>8.2f} {r['poem_avg_s2']:>8.2f} {r['delta']:>+8.2f}"
        )

    print("\n" + "=" * 70)
    print("HIGHEST-SURPRISE FAMOUS LINES (top 10 by phrase avg S2)")
    print("=" * 70)
    top_by_phrase = sorted(results, key=lambda r: r["phrase_avg_s2"], reverse=True)[:10]
    for r in top_by_phrase:
        print(f"\n'{r['phrase']}'  ({r['author']})")
        print(f"  Source: {r['source']}")
        print(f"  Phrase avg S2: {r['phrase_avg_s2']:+.2f}  |  Poem avg: {r['poem_avg_s2']:+.2f}  |  Delta: {r['delta']:+.2f}")
        print(f"  Peak moment: '{r['max_s2_token']}' (S2={r['max_s2']:.2f}, GPT-2 expected '{r['model_expected']}')")
        print(f"  Token-level: " + "  ".join(f"{t['token']}({t['s2']:+.1f})" for t in r["phrase_tokens"]))

    print("\n" + "=" * 70)
    print("NOTABLE LOW-SURPRISE FAMOUS LINES")
    print("=" * 70)
    bottom = sorted(results, key=lambda r: r["phrase_avg_s2"])[:5]
    for r in bottom:
        print(f"\n'{r['phrase']}'  ({r['author']})")
        print(f"  Source: {r['source']}")
        print(f"  Phrase avg S2: {r['phrase_avg_s2']:+.2f}  |  Poem avg: {r['poem_avg_s2']:+.2f}  |  Delta: {r['delta']:+.2f}")
        print(f"  Token-level: " + "  ".join(f"{t['token']}({t['s2']:+.1f})" for t in r["phrase_tokens"]))

    if not_found:
        print("\n" + "=" * 70)
        print("NOT FOUND:")
        for nf in not_found:
            print(nf)

    output = {
        "summary": {
            "n_lines": len(results),
            "above_poem_avg": len(above_avg),
            "pct_above": round(100 * len(above_avg) / len(results), 1),
            "mean_delta": round(mean_delta, 4),
            "hypothesis_supported": mean_delta > 0,
        },
        "results": results,
    }
    with open("results/famous_lines_s2.json", "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nResults saved to results/famous_lines_s2.json")


if __name__ == "__main__":
    main()
