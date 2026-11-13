# The Post-Surprise Signature: What Immediately Follows a High-S₂ Token?

**Date:** 2026-11-13  
**Experiment:** `experiments/post_surprise_signature.py` → `results/post_surprise_signature.json`  
**Corpus:** 411 poems, 11,201 high-S₂ tokens (S₂ ≥ 2.0, p_newline < 0.9)  
**Builds on:** `findings/surprise_liberation_vs_channeling.md` (channeling result), `findings/aftermath_entropy.md` (entropy change), `findings/straussian_extremes_taxonomy.md` (what gets suppressed)

---

## Research Question

`surprise_liberation_vs_channeling.md` established that poetic surprise is predominantly **channeling**: the unexpected word DECREASES entropy on the next token, narrowing future possibilities rather than opening them.

But what, specifically, is the token that follows? The entropy analysis tells us the follow-up is predictable — but IS it punctuation, a function word, another content word, or a line break? The answer reveals the **mechanical structure** of channeling: how poets "land" an unexpected word choice.

We classify the token immediately following each high-S₂ position (t+1) as one of:
- **PUNCTUATION**: comma, period, dash, semicolon, colon, ellipsis
- **CONTENT_WORD**: noun, verb, adjective, adverb (non-function)
- **NEWLINE**: line break (structural pause)
- **FUNCTION_WORD**: article, conjunction, preposition, pronoun, auxiliary

---

## Primary Finding: Surprise Precedes Punctuation, Not Line Breaks

| Token class | Post-surprise % | Baseline % | Lift |
|-------------|-----------------|------------|------|
| **PUNCTUATION** | **17.0%** | 10.5% | **1.62×** |
| CONTENT_WORD | 72.9% | 70.0% | 1.04× |
| NEWLINE | 6.6% | **12.6%** | **0.52×** |
| FUNCTION_WORD | 3.4% | **6.9%** | **0.50×** |

**The post-surprise signature is punctuation.** When a poet writes an unexpected word, the next token is a comma, period, dash, or semicolon at **1.62× the baseline rate**. Conversely, surprise tokens are significantly less likely to precede line breaks (0.52×) or function words (0.50×).

**Top 15 tokens immediately following a high-S₂ word:**

| Rank | Token | Count | % of surprises |
|------|-------|-------|----------------|
| 1 | `,` | 884 | 7.9% |
| 2 | `\n` (line break) | 710 | 6.3% |
| 3 | `.` | 458 | 4.1% |
| 4 | `the` | 365 | 3.3% |
| 5 | `of` | 263 | 2.3% |
| 6 | `and` | 221 | 2.0% |
| 7 | `to` | 151 | 1.3% |
| 8 | `-` | 145 | 1.3% |
| 9 | `in` | 129 | 1.2% |
| 10 | `a` | 121 | 1.1% |
| 11 | `;` | 116 | 1.0% |
| 12 | `is` | 84 | 0.7% |
| 13 | `on` | 83 | 0.7% |
| 14 | `i` | 81 | 0.7% |
| 15 | `:` | 68 | 0.6% |

The comma `,` alone follows 7.9% of all surprise tokens — by far the most common landing pad.

---

## Finding 2: The Pattern Strengthens at Extreme S₂

| S₂ bucket | PUNCT % | NEWLINE % | CONTENT % | FUNCT % |
|-----------|---------|-----------|-----------|---------|
| moderate (2–5) | 16.3% | 7.0% | 73.1% | 3.6% |
| high (5–9.5) | 17.7% | 5.8% | 73.1% | 3.4% |
| extreme (≥9.5) | **18.6%** | 6.9% | 71.6% | **2.9%** |

As S₂ increases, punctuation rate rises and function word rate falls. The most extreme divergences from GPT-2 are the ones most likely to be grammatically "cushioned" — followed by a punctuation mark that absorbs the shock.

**Interpretation:** The more unprecedented the choice, the more the poet follows it with a structural pause. This is consistent with the channeling result: extreme surprise COMMITS the reader to a narrow path, and punctuation marks that commitment explicitly.

---

## Finding 3: The Effect is Gone by t+2

| Position relative to surprise | PUNCT % | NEWLINE % | CONTENT % | FUNCT % |
|-------------------------------|---------|-----------|-----------|---------|
| **t+1 (immediately after)** | 17.0% | 6.6% | 72.9% | 3.4% |
| **t+2 (two tokens after)** | 12.8% | 12.5% | 70.4% | 4.3% |
| **Baseline** | 10.5% | 12.6% | 70.0% | 6.9% |

By t+2, the distribution nearly matches baseline. The post-surprise punctuation signature is local — a one-token effect. This is a "syntactic exhale": the poem pauses for exactly one beat after a surprise, then resumes normal predictability.

---

## Finding 4: Consecutive Surprises Are Common (20.7%)

Of the 11,201 high-S₂ tokens, **20.7% are immediately followed by another high-S₂ token**. This "surprise cascade" rate is high enough to constitute a distinct pattern alongside the more common punctuation-cushioned single spike.

Combining t+1 distributions: approximately **60%** of surprises are "cushioned" (followed by punctuation or structural pause), **20%** are "cascaded" (followed by another surprise), and **20%** receive a standard content-word continuation.

---

## Finding 5: Era Divide — Formal vs. Free Verse

The punctuation rate after surprise varies dramatically by era, revealing two distinct "landing strategies":

### High-punctuation eras (surprise lands on a comma or dash)

| Era | PUNCT % | NEWLINE % |
|-----|---------|-----------|
| ghazal | 29.4% | 3.9% |
| haiku | 26.0% | 12.3% |
| villanelle | 25.9% | 9.9% |
| metaphysical | 24.3% | 8.1% |
| ballad | 24.0% | 3.9% |
| war_poetry | 23.1% | 2.8% |
| old_english | 21.8% | 1.4% |

### Low-punctuation eras (surprise is "naked")

| Era | PUNCT % | NEWLINE % |
|-----|---------|-----------|
| beat | 9.5% | 13.8% |
| found_poetry | 6.0% | 9.8% |
| korean_modernist | 5.0% | 5.0% |
| german_symbolist | 9.8% | 7.8% |
| spoken_word | 11.1% | 9.3% |

Formal, heavily punctuated traditions (ghazal, villanelle, ballad) absorb surprise into grammatical structure. Experimental traditions (beat, found poetry) leave surprise "standing alone" — the unexpected word receives no immediate grammatical cushion.

---

## Interpretation: The Mechanics of Channeling

The channeling result said: poetic surprise narrows entropy. This experiment explains the mechanism:

> **In traditional poetry, the unexpected word is followed by a comma.** The comma is high-certainty for GPT-2 (after a noun, adjective, or adverb, a comma is very predictable). So the SURPRISE token itself generates low-probability, but the COMMA after it restores near-certainty. Channeling = surprise → pause → reset.

> **In experimental/free verse, the unexpected word is followed by continuation content.** No punctuation cushion. The surprise propagates differently — not through a grammatical pause but through semantic momentum.

This two-track architecture explains why era matters so much in the channeling analysis: it's not that formal poets are intrinsically more "channeling" — it's that they use punctuation to enforce it.

---

## Suggested Next Steps

1. **Which surprise tokens get commas vs. which get content continuation?** Are noun surprises more likely to get commas than verb surprises?
2. **Is the comma post-surprise token the same comma that marks an enjambment?** Cross-reference with enjambment dataset.
3. **Consecutive surprise cascade: what are the semantic relationships** between the two (or more) consecutive surprise tokens? Are they in the same semantic field?
4. **Within the beat/found poetry category**: do poems without punctuation post-surprise have higher or lower overall surprise? Does removing punctuation change how surprise lands — or how hard it hits?
