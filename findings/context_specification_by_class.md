# Context-Specification by Token Class: What Kind of Surprise Narrows the Future?

**Date:** 2026-10-10  
**Experiment:** `experiments/context_specification_by_class.py`  
**Corpus:** 227 texts, 3,916 genuine high-S2 spikes (artifact-filtered)  
**Builds on:** `findings/spike_symmetry_profile.md` (suggestion #2)

---

## Research Question

`spike_symmetry_profile.md` showed that after a genuine high-S2 spike, entropy drops at k=+1
(post-spike uncertainty falls). But is all surprise equal in how much it *specifies* the
subsequent context?

**The hypothesis (from spike_symmetry_profile.md suggestion #2):** Proper nouns should
cause the *largest* entropy drop — by naming a specific entity, the poet narrows subsequent
prediction space (the model now knows which entity to track).

**The test:** For each genuine spike (S2 ≥ 3.0, p_newline < 0.9), classify the spike token
by class and measure entropy delta = H(k+1) − H(k−1).

- Negative delta: entropy DROPS after the spike (context is specified by the choice)
- Positive delta: entropy RISES after the spike (the choice opens new uncertainty)

---

## Main Finding: The Hypothesis Is Reversed — and There Are Two Types of Surprise

| Class | n | Avg delta | Avg H before | Avg H after |
|---|---|---|---|---|
| SHORT_ALPHA (subword fragments) | 630 | **−1.704** | 6.80 | 5.10 |
| CONTENT_LOWER (whole content words) | 2,158 | **−0.832** | 6.59 | 5.76 |
| PROPER_NOUN (mid-sentence capitalized) | 222 | **−0.457** | 6.44 | 5.99 |
| PUNCTUATION | 116 | **−0.146** | 6.09 | 5.94 |
| FUNCTION words | 351 | **+1.345** | 5.64 | 6.98 |
| SENTENCE_START (capitalized, after stop) | 206 | **+1.123** | 4.86 | 5.98 |
| WHITESPACE (surprising whitespace) | 160 | **+1.637** | 5.36 | 7.00 |

**The key split:** content-class tokens (content words, proper nouns, subword fragments)
cause entropy to DROP; structural tokens (function words, sentence boundaries, whitespace)
cause entropy to RISE.

---

## Finding 1: The Subword Fragment Effect

The largest entropy drop (−1.704) comes from SHORT_ALPHA tokens — but investigation reveals
these are mostly **GPT-2 subword fragments** like "gro-" (from "groaning"), "neb-" (from
"nebulous"), "bos-" (from "bosom"), "rhy-" (from "rhyme").

When a poet uses an unexpected rare word, GPT-2 tokenizes it as a surprising first subword
followed by highly *predictable* continuation subwords. The massive entropy drop at k+1 is
largely **within-word predictability**: once you've started "groaning" with "gro-", the
continuation "-aning" has near-zero uncertainty.

This is an important subword artifact: **the highest "context-specification" in the corpus
is the internal predictability of rare words, not semantic context-narrowing**.

---

## Finding 2: Proper Nouns Do NOT Narrow Context More Than Content Words

The initial hypothesis is **disconfirmed**. Proper nouns (avg delta = −0.457) cause *less*
entropy narrowing than common content words (avg delta = −0.832). Both are in the
"specifying" direction (negative), but regular content words are more context-constraining.

**Why?** Likely because:
- A surprising proper noun (e.g., "Agamemnon", "Euphrates", "Thursday") labels an entity
  but doesn't syntactically constrain what comes next (many things can follow a name)
- A surprising content word (e.g., "throbs", "vaults", "depends") often carries strong
  syntactic transitivity: verbs demand objects, specific nouns demand specific determiners
- Proper nouns appear in many grammatical roles; content verbs constrain their objects more

The poets who most often use proper nouns as their high-S2 device: **19th_century** (11.8%
of spikes are proper nouns) and **romantic** (7.4%). The most context-constraining per-era
use of proper nouns: Victorian proper noun spikes average −1.013, compared to −0.457 global.

---

## Finding 3: Function Words Cause Entropy to RISE — Two Mechanisms of Deviation

The sharpest finding: **unexpected function words don't narrow context — they open it**.

Average entropy delta for FUNCTION word spikes: **+1.345** (entropy rises by more than 1 bit
after a surprising function word). WHITESPACE is even more extreme: +1.637.

This reveals **two fundamentally different types of poetic deviation**:

| Type | Example class | Avg delta | Effect |
|---|---|---|---|
| **Context-specifying surprise** | Unexpected content word, rare proper noun | −0.8 to −0.5 | Narrows prediction space |
| **Context-opening surprise** | Unexpected function word, unexpected structural break | +1.3 to +1.6 | Widens prediction space |

**Why do function words open entropy?**

A surprising conjunction or preposition signals *syntactic pivot*. When "but" or "of" or
"with" appears in a position where the model expected a noun phrase, it resets the syntactic
context entirely: the upcoming phrase is now uncertain in a way it wasn't before. The model's
"plan" for the sentence is disrupted. This is the linguistic version of a pivot-turn: the
poem goes somewhere structurally unexpected.

---

## Finding 4: What GPT-2 Expected Also Matters

The top alternative (what GPT-2 *would* have chosen) predicts post-spike entropy:

| What model expected | n | Actual spike's entropy delta |
|---|---|---|
| Content word | 835 | **−1.030** |
| Proper noun | 64 | **−1.050** |
| Punctuation | 576 | **−0.955** |
| Short alpha | 446 | **−0.730** |
| Function word | 1,566 | **−0.342** |
| Sentence start | 48 | **+1.857** |
| Whitespace | 322 | **+0.990** |

When GPT-2 expected a content word but got something else: entropy drops the most (−1.030).  
When GPT-2 expected a new sentence but something else happened: entropy rises sharply (+1.857).

This suggests **the model's frustrated expectation type matters**: missing on a content word
creates more contextual certainty; missing on a sentence boundary creates more uncertainty.
The "most costly" deviation (to the model's predictions) is also the most context-narrowing.

---

## Summary

| Statistic | Value |
|---|---|
| Total genuine spikes analyzed | 3,916 |
| Global avg entropy delta | −0.515 bits |
| Content word spikes (largest group, 55%) | avg delta = −0.832 |
| Proper noun avg delta | −0.457 |
| Function word avg delta | +1.345 |
| Subword fragment SHORT_ALPHA | −1.704 (within-word artifact) |

---

## Interpretation: The Two-Mode Model of Poetic Deviation

Poetic deviation operates in two modes with opposite downstream effects:

1. **Lexical deviation** (unexpected content word or proper noun): specifies context,
   narrows the model's subsequent prediction space. The "surprising thing chosen" locks in
   what comes next. This is the dominant mode (55% + 6% = 61% of spikes).

2. **Structural deviation** (unexpected function word, conjunction, spacing): disrupts
   syntactic framing, opens subsequent context. The "surprising structure" frees what
   comes next. This is the minority mode (9% of spikes) but has the *largest absolute effect*.

These map onto two poetic strategies: **naming-as-surprise** (specifying) vs.
**framing-as-surprise** (opening). A poet who uses structural deviation
(unexpected function words, surprising sentence boundaries) creates a different kind
of tension than one who uses lexical deviation.

---

## Suggested Next Steps

1. **Filter out subword fragments from SHORT_ALPHA** to get a clean picture of whether
   "short whole words" (archaic particles like "thy", "ere", "oft") behave differently
   from their modern equivalents.
2. **Test whether high-entropy-opening spikes cluster near line boundaries** — if structural
   deviation (function words) tends to appear at syntactically "reset" positions, the
   stanza/line structure may drive this signal.
3. **Are function-word spikes associated with enjambment?** An unexpected "of" at line-end
   before enjambment would fit the "context-opening" profile.
4. **The "most costly" spike**: for each poem, identify whether its single highest-S2 spike
   is context-specifying or context-opening, and test whether this correlates with the
   poem's subsequent S2 trajectory.
