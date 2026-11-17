"""
Experiment: S2 and Metapoetic Vocabulary
When poetry talks about itself — words about language, writing, silence, voice —
does that reflexive vocabulary carry MORE or LESS surprise than non-metapoetic content?

Hypothesis A (formulaic reflexivity): metapoetic words are LOW S2 — they're conventional
moves in the game of poetry-writing, expected by any reader of poems.

Hypothesis B (defamiliarizing language-about-language): metapoetic words are HIGH S2 —
the poet turns language on itself in an unexpected direction, exploiting the gap.

A finding either way is interpretable. If A: poetry's self-reference is a cliché.
If B: metapoetry is a heightened act of linguistic alienation.
"""

import json
import re
import sys
from collections import defaultdict

DATA_PATH = "results/corpus_results.json"
OUT_PATH  = "results/metapoetic_vocabulary_s2.json"

# --- Metapoetic lexicon ---
# Words that refer to the act/medium of language itself:
# speaking, writing, silence, naming, the poem-object, voice, text
METAPOETIC_STEMS = {
    # Language acts
    "say": "speech_act", "said": "speech_act", "says": "speech_act",
    "speak": "speech_act", "spoke": "speech_act", "spoken": "speech_act", "speaking": "speech_act",
    "tell": "speech_act", "told": "speech_act", "tells": "speech_act",
    "utter": "speech_act", "uttered": "speech_act",
    "whisper": "speech_act", "whispered": "speech_act",
    "cry": "speech_act", "cried": "speech_act",
    "shout": "speech_act",
    "call": "speech_act", "called": "speech_act",
    # Writing acts
    "write": "writing", "wrote": "writing", "written": "writing", "writes": "writing", "writing": "writing",
    "inscribe": "writing", "inscribed": "writing",
    "read": "writing", "reads": "writing", "reading": "writing",
    "text": "writing",
    "page": "writing",
    "book": "writing",
    "letter": "writing",
    # Poetry/poem as object
    "poem": "poem_object", "poems": "poem_object", "poetry": "poem_object",
    "verse": "poem_object", "verses": "poem_object",
    "lyric": "poem_object", "lyrics": "poem_object",
    "song": "poem_object", "songs": "poem_object",
    "line": "poem_object", "lines": "poem_object",
    "stanza": "poem_object",
    # Language/words
    "word": "language", "words": "language",
    "language": "language",
    "tongue": "language",
    "name": "language", "names": "language", "named": "language", "naming": "language",
    "meaning": "language",
    "metaphor": "language",
    "image": "language", "images": "language",
    # Voice / silence
    "voice": "voice_silence", "voices": "voice_silence",
    "silence": "voice_silence", "silent": "voice_silence",
    "mute": "voice_silence", "muted": "voice_silence",
    "soundless": "voice_silence",
    "dumb": "voice_silence",
    "sound": "voice_silence", "sounds": "voice_silence",
    # Naming / address
    "address": "address", "addressed": "address",
}

def normalize(tok):
    return re.sub(r"[^a-z]", "", tok.lower())

def is_metapoetic(token_str):
    t = normalize(token_str)
    return METAPOETIC_STEMS.get(t)

def run():
    with open(DATA_PATH) as f:
        data = json.load(f)

    # Only English poetry (no prose controls, no non-English)
    poetry_eras = {"control"}  # will EXCLUDE these
    poems = [d for d in data
             if d["metadata"].get("language", "en") == "en"
             and d["metadata"]["era"] not in poetry_eras]

    # Collect per-token data
    meta_tokens   = []  # (s2, category, era, title)
    other_tokens  = []  # (s2, era)
    era_meta      = defaultdict(list)
    era_other     = defaultdict(list)
    word_records  = defaultdict(list)

    for poem in poems:
        era = poem["metadata"]["era"]
        title = poem["metadata"]["title"]
        for tok in poem["tokens"]:
            if tok.get("p_newline", 0) >= 0.9:
                continue  # skip stanza-break artifact
            s2 = tok["s2"]
            cat = is_metapoetic(tok["token"])
            norm = normalize(tok["token"])
            if cat:
                meta_tokens.append(s2)
                era_meta[era].append(s2)
                word_records[norm].append((s2, era, title))
            else:
                other_tokens.append(s2)
                era_other[era].append(s2)

    def stats(vals):
        if not vals:
            return {}
        import statistics
        m = sum(vals) / len(vals)
        pos_ratio = sum(1 for v in vals if v > 0) / len(vals)
        sd = statistics.stdev(vals) if len(vals) > 1 else 0
        return {"n": len(vals), "mean": round(m, 4), "std": round(sd, 4),
                "pos_ratio": round(pos_ratio, 4)}

    # Overall comparison
    overall = {
        "metapoetic": stats(meta_tokens),
        "other_content": stats(other_tokens),
        "delta_mean": round((sum(meta_tokens)/len(meta_tokens) if meta_tokens else 0)
                            - (sum(other_tokens)/len(other_tokens) if other_tokens else 0), 4)
    }

    # Era breakdown: delta = metapoetic mean - other mean
    era_results = {}
    all_eras = sorted(set(list(era_meta.keys()) + list(era_other.keys())))
    for era in all_eras:
        mm = era_meta[era]
        om = era_other[era]
        if len(mm) < 5:
            continue
        m_mean = sum(mm) / len(mm)
        o_mean = sum(om) / len(om) if om else 0
        era_results[era] = {
            "n_meta": len(mm),
            "meta_mean": round(m_mean, 4),
            "other_mean": round(o_mean, 4),
            "delta": round(m_mean - o_mean, 4),
            "meta_pos_ratio": round(sum(1 for v in mm if v > 0) / len(mm), 4)
        }

    # Top/bottom metapoetic words by mean S2
    word_stats = {}
    for w, records in word_records.items():
        if len(records) < 5:
            continue
        vals = [r[0] for r in records]
        word_stats[w] = {
            "n": len(vals),
            "mean_s2": round(sum(vals) / len(vals), 4),
            "pos_ratio": round(sum(1 for v in vals if v > 0) / len(vals), 4),
            "sample_titles": list({r[2] for r in records})[:3]
        }

    # Category breakdown
    cat_records = defaultdict(list)
    for tok in poems:
        for t in tok["tokens"]:
            if t.get("p_newline", 0) >= 0.9:
                continue
            cat = is_metapoetic(t["token"])
            if cat:
                cat_records[cat].append(t["s2"])
    cat_stats = {c: stats(v) for c, v in cat_records.items()}

    output = {
        "overall": overall,
        "era_breakdown": era_results,
        "word_stats": word_stats,
        "category_stats": cat_stats,
        "corpus_size": len(poems),
        "total_meta_tokens": len(meta_tokens),
        "total_other_tokens": len(other_tokens),
    }

    with open(OUT_PATH, "w") as f:
        json.dump(output, f, indent=2)

    # Print summary
    print("=== Metapoetic Vocabulary S2 Analysis ===")
    print(f"Corpus: {len(poems)} poems")
    print(f"Metapoetic tokens: {len(meta_tokens):,}  Other tokens: {len(other_tokens):,}")
    print()
    print(f"Metapoetic mean S2:    {overall['metapoetic']['mean']:+.4f}  "
          f"(pos_ratio={overall['metapoetic']['pos_ratio']:.2%})")
    print(f"Other content mean S2: {overall['other_content']['mean']:+.4f}  "
          f"(pos_ratio={overall['other_content']['pos_ratio']:.2%})")
    print(f"Delta (meta - other):  {overall['delta_mean']:+.4f}")
    print()

    print("Era-level delta (meta S2 - other S2), top/bottom 10:")
    sorted_eras = sorted(era_results.items(), key=lambda x: -x[1]["delta"])
    for era, v in sorted_eras[:5]:
        print(f"  {era:<30} delta={v['delta']:+.4f}  n_meta={v['n_meta']}")
    print("  ...")
    for era, v in sorted_eras[-5:]:
        print(f"  {era:<30} delta={v['delta']:+.4f}  n_meta={v['n_meta']}")
    print()

    print("Top 10 highest-S2 metapoetic words:")
    top_words = sorted(word_stats.items(), key=lambda x: -x[1]["mean_s2"])[:10]
    for w, v in top_words:
        print(f"  '{w}' mean={v['mean_s2']:+.4f} n={v['n']} pos_ratio={v['pos_ratio']:.0%}")
    print()
    print("Top 10 lowest-S2 metapoetic words:")
    bot_words = sorted(word_stats.items(), key=lambda x: x[1]["mean_s2"])[:10]
    for w, v in bot_words:
        print(f"  '{w}' mean={v['mean_s2']:+.4f} n={v['n']} pos_ratio={v['pos_ratio']:.0%}")
    print()

    print("Category breakdown:")
    for cat, v in sorted(cat_stats.items(), key=lambda x: -x[1]["mean"]):
        print(f"  {cat:<20} mean={v['mean']:+.4f}  pos_ratio={v['pos_ratio']:.0%}  n={v['n']}")

    print(f"\nResults saved to {OUT_PATH}")

if __name__ == "__main__":
    run()
