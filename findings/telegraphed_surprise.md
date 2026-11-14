# The Anti-Telegraphed Surprise: Poetic Shock Has No Local Foreshadowing

**Date:** 2026-11-14  
**Experiment:** `experiments/telegraphed_surprise.py` → `results/telegraphed_surprise.json`  
**Corpus:** 419 texts, 9,795 clean high-S₂ positions (s₂ > 2.0, non-artifact, non-punctuation, non-whitespace)  
**Research Question:** When a poet writes something surprising, was that word "hovering" in GPT-2's alternative space one token earlier?

---

## Motivation

The `pre_peak_setup.md` study showed that in the **8 tokens preceding** a surprise spike, S₂ systematically drops — the poet conforms before striking. But that study measured S₂ of the preceding tokens, not whether the surprising word itself was anticipated.

This experiment asks a more direct question: at position i-1 (one step before a spike), does GPT-2's top-10 alternative list contain the actual word that will appear at position i?

If yes → the surprise is **telegraphed**: GPT-2 had the word "in mind" one step early but let it slip  
If no → the surprise is a **true ambush**: the word materializes from completely outside GPT-2's local anticipation space

---

## Central Finding: Poetic Surprise Is Anti-Telegraphed

| Population | n | Telegraphed | Rate |
|---|---|---|---|
| **High-S₂ spikes** (s₂ > 2.0) | 9,795 | 261 | **2.7%** |
| **Baseline** (s₂ < 2.0, clean) | 28,197 | 4,498 | **16.0%** |

**High-S₂ tokens are 6× LESS likely** to have been in the previous position's alternatives than ordinary tokens. Poetic surprise is not just locally unexpected at position i — it was absent from the prediction space even one token earlier.

The inverse relationship with surprise magnitude is monotone:

| S₂ band | Spikes | Telegraphed | Rate |
|---|---|---|---|
| 2–3 | 2,267 | 87 | 3.8% |
| 3–5 | 3,244 | 95 | 2.9% |
| 5–10 | 3,480 | 71 | 2.0% |
| **10+** | 804 | 8 | **1.0%** |

**The more extreme the surprise, the less it was locally anticipated.** The rarest poetic shocks — those with s₂ > 10 — appear in the previous alternative space only 1% of the time, 16× below the baseline rate.

---

## The Uniform Alt-Rank Distribution

When telegraphing does occur, at what rank among GPT-2's alternatives was the surprising word at t-1?

| Alt rank | Count |
|---|---|
| 1 | 30 |
| 2 | 32 |
| 3 | 26 |
| 4 | 27 |
| 5 | 30 |
| 6 | 32 |
| 7 | 22 |
| 8 | 23 |
| 9 | 19 |
| 10 | 20 |

The distribution is essentially **flat across ranks 1–10**. If telegraphing were a systematic "setup" mechanism (the poet deliberately primes the word by placing it in the previous alternatives), we'd expect the word to be alt-rank-1 or -2 at t-1. Instead, the uniform distribution suggests these are **coincidences**, not setups — when telegraphing happens, it's because the word happened to be somewhere in the top-10 alternatives for unrelated reasons.

---

## Era Patterns: Constraint Enables Telegraphing

| Era | Rate | (n/N) | Interpretation |
|---|---|---|---|
| **concrete** | 11.1% | 4/36 | Extreme repetition (Gomringer's "silencio") |
| **latin_american** | 7.8% | 7/90 | Surrealist vocabulary recycling |
| **language** | 7.5% | 6/80 | Procedural/constrained vocabulary |
| **oulipo** | 6.4% | 14/218 | Formal constraints force lexical return |
| **found_poetry** | 5.7% | 8/140 | Fixed source text vocabulary |
| **biblical** | 5.0% | 10/199 | Parallelism/anaphora recycles words |
| **villanelle** | 4.5% | 3/66 | Refrain structure |

**Eras with zero telegraphing:**

| Era | Spikes | Rate |
|---|---|---|
| control (prose) | 12 | 0.0% |
| haiku | 52 | 0.0% |
| old_english | 134 | 0.0% |
| beat | 174 | 0.6% |
| deep_image | 15 | 0.0% |
| parody | 112 | 0.0% |

**Hypothesis:** Forms with structural repetition (villanelle, biblical parallelism, oulipo constraint, concrete) produce telegraphing because they intentionally recycle vocabulary. When a constrained poem returns to a word it used earlier, GPT-2's local alternatives may have "learned" to anticipate that word — not from poetic intent, but from the statistical shadow of repetition.

The eras with zero telegraphing are either: (a) purely expressive forms with no structural repetition (beat, haiku, deep_image), (b) archaic forms whose vocabulary GPT-2 simply never anticipates (old_english), or (c) the prose control.

---

## The Newline Confound

Approximately 55% of telegraphed examples in our sample involve `'\n'` as the previous token. After a line break, GPT-2's alternatives include common line-starting words ("The", "I", "A", "My"). When these words are also surprising at the specific post-newline position (high s₂ due to context), they appear as "telegraphed." This is a structural phenomenon of line-based poetry rather than intentional setup.

The 45% of telegraphed cases NOT involving a previous newline represent a more genuine "hovering word" phenomenon — where a word appears in the previous position's alternatives for semantic/syntactic reasons and then materializes as a surprise.

**Example of genuine telegraphing:**  
- Percy Bysshe Shelley, *Ozymandias*: `'sunk'` → `' a'` (s₂=3.88, was alt rank 2)  
  After "sunk", "a" (indefinite article) was alt-rank-2 — a natural continuation — but became surprising in context.

---

## Theoretical Implications

**1. Surprise requires long-range preparation.** The fact that high-S₂ tokens are essentially absent from the immediately prior alternative space means poets cannot rely on local anticipation to set up their surprises. The "trap" documented in `pre_peak_setup.md` (S₂ drops in the 8 tokens before a spike) works by CONFORMING to general expectations, not by specifically priming the surprising word.

**2. True poetic shock is globally unexpected.** The inverse scaling — 10+s₂ spikes at only 1.0% telegraphing rate — suggests that the most extreme Straussian moments are words that could not have been predicted from even the most generous local alternative space. They arrive fully formed, without local precedent.

**3. Constrained forms are locally predictable but globally surprising.** Oulipo and villanelle have higher telegraphing rates, but this isn't because those poets "set up" their surprises — it's because constraint forces vocabulary recycling, making the prediction space a closed loop. The surprise comes not from the word being unexpected but from its being contextually misaligned when it returns.

---

## Suggested Next Steps

1. **Extend the horizon**: Test whether high-S₂ tokens appear in alternatives at t-2, t-3, t-5, t-10. Is there a "preparation distance" at which telegraphing approaches baseline?
2. **Filter newline-previous cases**: Rerun with `prev_token != '\n'` to isolate genuine semantic telegraphing from line-start effects.
3. **Poet-level analysis**: Which poets most consistently produce anti-telegraphed surprises? This could be a new dimension of poet fingerprinting.
4. **Reverse direction**: At positions where the actual token WAS in the previous alternatives (telegraphed), does the poem's overall coherence/theme density predict this? Constrained poems should cluster there.
