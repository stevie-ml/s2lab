# Spike Symmetry Profile: Genuine Surprise and the Context-Specification Effect

**Date:** 2026-10-08
**Corpus:** 225 texts | Genuine (non-artifact) spikes: 3932
**Spike threshold:** S2 ≥ 3.0 | Artifact filter: p_newline < 0.9
**Window:** ±8 tokens (artifact tokens excluded from window too)

## Research Question

Two prior experiments mapped the temporal neighborhood of S2 spikes:

- **`pre_peak_setup.md`**: Found entropy DROPS at k=−1 (model more confident just before spike).
  This was the 'confidence-trap' narrative: the poet exploits the model's certainty.
- **`surprise_decay_curves.md`**: Found S2 collapses to ~0 at k=+1 (universal half-life = 1).

**Critical limitation of both:** neither experiment filtered stanza-break artifact tokens
from the *spike identification* step. The corpus contains many tokens with p_newline ≈ 1.0
(the line-break token), which score as false high-S2 tokens. These dominate the top-spike
list and distort the surrounding entropy profile — because before a line break, the model
expects ONLY the newline token (very low entropy), producing the artificial confidence-trap.

This experiment applies the artifact filter to **both** spike identification and the
surrounding window, yielding the first clean symmetric view of genuine poetic surprise.

---

## Global Symmetric Spike Profile

Mean S2 and entropy at each lag around a genuine spike (S2 ≥ 3.0, p_newline < 0.9).

| Lag | Mean S2 | Mean Entropy | n | Side |
|-----|---------|-------------|---|------|
| k=−8 | -0.368 | 6.273 | 3343 | PRE |
| k=−7 | -0.342 | 6.284 | 3380 | PRE |
| k=−6 | -0.226 | 6.343 | 3434 | PRE |
| k=−5 | -0.271 | 6.317 | 3479 | PRE |
| k=−4 | -0.196 | 6.377 | 3545 | PRE |
| k=−3 | -0.198 | 6.288 | 3562 | PRE |
| k=−2 | -0.326 | 6.406 | 3620 | PRE |
| k=−1 | -0.281 | 6.455 | 3692 | PRE |
| **k=0** | **SPIKE (≥3.0)** | — | 3932 | PEAK |
| k=+1 | -0.351 | 5.845 | 3846 | POST |
| k=+2 | -0.357 | 6.377 | 3718 | POST |
| k=+3 | -0.258 | 6.375 | 3606 | POST |
| k=+4 | -0.327 | 6.391 | 3591 | POST |
| k=+5 | -0.370 | 6.242 | 3562 | POST |
| k=+6 | -0.326 | 6.316 | 3544 | POST |
| k=+7 | -0.406 | 6.327 | 3526 | POST |
| k=+8 | -0.488 | 6.332 | 3546 | POST |

**S2 summary:** mean at k=−1..−3: -0.269 | mean at k=+1..+3: -0.323
**Asymmetry ratio (post/pre S2):** 1.202
**Entropy:** mean at k=−1..−3: 6.384 bits | mean at k=+1..+3: 6.193 bits

---

## Key Findings

### Finding 1: Entropy Rises BEFORE the Spike, Falls AFTER

- Entropy at k=−1: **6.455 bits** (more uncertain)
- Entropy at k=+1: **5.845 bits** (more certain)
- Difference: +0.610 bits (k=−1 is higher entropy)

**This directly contradicts the confidence-trap narrative from `pre_peak_setup.md`.**

That earlier analysis found entropy *dropping* at k=−1, suggesting the model
became MORE certain just before the spike. But that finding was driven by
stanza-break artifact tokens, where the 'spike' was a word at the start of a new
line and the 'k=−1' token was the last word of the previous line — a position where
GPT-2 expects almost nothing but a newline, giving near-zero entropy (near-certainty).

Once those artifact spikes are removed, the clean pattern emerges:
**the model is MORE uncertain before genuine poetic surprises than after them.**

### Finding 2: Genuine Spikes Specify Context (The Context-Specification Effect)

After a genuine high-S2 token, entropy drops by 0.610 bits at k=+1.
This means the unexpected word *narrows* the model's prediction space for what follows.

**Interpretation:** When a poet chooses an unexpected word — especially a specific
proper noun, a rare content word, or a domain-marking term — the model receives
a signal that is initially unpredicted but then *highly constraining*. A poem that
suddenly says 'leviathan' or 'obsidian' or a personal name has specified a domain,
and what follows in that domain is more predictable than the general background.

This is the **context-specification effect**: genuine poetic surprise is not a
random deviation but a *naming event* that opens a new but coherent channel.

### Finding 3: Post-Spike S2 Is Lower Than Pre-Spike S2

- Mean S2 at k=−1..−3: **-0.269**
- Mean S2 at k=+1..+3: **-0.323**
- Asymmetry ratio: **1.202** (post > pre)

Both pre- and post-spike tokens have *negative* S2 — they are more predictable than
average. This makes sense: genuine spikes are isolated events in otherwise conformist
language. But the post-spike tokens are systematically *more* predictable (more negative
S2) than pre-spike tokens at every lag except k=±1's entropy reversal.

This is the **post-spike conformity effect**: after the deviation, the poem snaps
back hard to statistical expectation, even harder than the pre-peak baseline.

### Finding 4: The Revised Spike Architecture

The genuine spike profile (artifact-cleaned) looks like this:

```
S2:      low     neutral   [SPIKE]   very low   neutral
Entropy: rising  rising    [SPIKE]   falling    stable
         ←————————————————→          ←—————————————→
              Setup zone             Recovery zone
         (uncertainty building)    (certainty restored)
```

The spike sits at the apex of both the S2 curve AND the entropy curve —
it is simultaneously the most surprising token AND the point of maximum
model uncertainty. After it, both metrics fall: the poem is predictable,
and the model is confident about that predictability.

---

## Per-Era Results

| Era | Poems | Spikes | S2 k=−1 | S2 k=+1 | Ent k=−1 | Ent k=+1 | S2 ratio |
|-----|-------|--------|---------|---------|----------|----------|----------|
| nursery_rhyme | 1 | 31 | +0.405 | +0.032 | 5.49 | 4.80 | -8.54 |
| black_arts | 1 | 21 | +0.390 | +1.314 | 6.09 | 5.67 | -6.12 |
| ballad | 6 | 140 | -0.047 | -0.343 | 6.69 | 6.72 | -5.77 |
| concrete | 3 | 15 | -1.296 | -1.651 | 4.87 | 5.28 | -3.39 |
| contemporary | 9 | 132 | -0.081 | -0.059 | 6.04 | 5.36 | -1.96 |
|  | 11 | 270 | +0.152 | -0.095 | 5.94 | 5.83 | -1.79 |
| korean_modernist | 1 | 16 | +0.708 | +0.817 | 6.71 | 6.30 | 0.24 |
| deep_image | 1 | 15 | -0.524 | -0.591 | 6.34 | 6.10 | 0.25 |
| fixed_form | 8 | 142 | -0.820 | -0.536 | 6.76 | 5.88 | 0.31 |
| beat | 2 | 39 | +0.535 | +0.219 | 6.73 | 5.38 | 0.51 |
| confessional | 6 | 77 | -0.614 | -0.450 | 6.46 | 6.24 | 0.52 |
| german_symbolist | 3 | 73 | +0.269 | +0.367 | 6.79 | 6.59 | 0.74 |
| harlem_renaissance | 5 | 82 | -0.431 | -0.398 | 7.09 | 5.77 | 0.76 |
| victorian | 21 | 563 | -0.381 | -0.355 | 6.90 | 6.14 | 0.79 |
| german_modernist | 2 | 53 | +0.444 | -0.016 | 6.62 | 5.36 | 0.82 |
| new_york_school | 18 | 214 | -0.761 | -0.534 | 6.61 | 5.68 | 0.85 |
| metaphysical | 4 | 78 | -1.455 | -1.043 | 6.78 | 6.16 | 0.86 |
| biblical | 7 | 128 | -1.001 | -0.910 | 4.99 | 4.58 | 0.88 |
| imagist | 2 | 40 | -0.889 | -1.019 | 6.56 | 5.32 | 0.95 |
| prose_poetry | 9 | 120 | -0.245 | +0.013 | 5.59 | 4.89 | 1.03 |
| song_lyrics | 3 | 67 | -1.070 | -1.019 | 5.42 | 5.36 | 1.07 |
| haiku | 14 | 61 | -0.355 | -0.432 | 7.19 | 6.39 | 1.21 |
| latin_american | 3 | 49 | -0.360 | -0.992 | 4.99 | 5.35 | 1.25 |
| found_poetry | 7 | 102 | -0.670 | -0.768 | 4.77 | 4.70 | 1.27 |
| early_modern | 5 | 93 | -0.205 | -0.407 | 6.74 | 6.21 | 1.28 |
| spoken_word | 2 | 31 | -1.651 | -1.445 | 6.71 | 6.13 | 1.30 |
| 19th_century | 11 | 276 | -0.138 | -0.287 | 6.66 | 5.91 | 1.39 |
| cliche_control | 3 | 37 | -0.835 | -0.920 | 5.34 | 4.48 | 1.43 |
| german_expressionist | 2 | 66 | +0.146 | +0.172 | 6.67 | 5.62 | 1.57 |
| language | 3 | 31 | -0.299 | -0.401 | 6.97 | 6.17 | 1.65 |
| romantic | 15 | 331 | -0.057 | -0.120 | 6.87 | 5.99 | 1.70 |
| ancient | 3 | 57 | -0.411 | -0.622 | 7.23 | 6.30 | 1.70 |
| modernist | 22 | 378 | +0.104 | -0.207 | 6.63 | 6.32 | 2.50 |
| mid_century | 3 | 26 | +0.694 | -1.201 | 6.98 | 5.13 | 3.19 |
| 18th_century | 2 | 54 | +0.333 | -0.344 | 5.74 | 5.77 | 4.10 |

---

## Relation to Prior Findings

| Prior finding | Revision |
|---------------|---------|
| `pre_peak_setup.md`: entropy drops at k=−1 (confidence trap) | **Artifact-driven**. Clean analysis shows entropy rises into the spike. |
| `surprise_decay_curves.md`: half-life = 1 token (S2 collapses at k=+1) | **Partially confirmed**: post-spike S2 is low, but POST-spike entropy also falls (not just S2). |
| `straussian_gap_taxonomy.md`: proper nouns are highest-S2 | **Consistent**: proper nouns (naming events) would trigger context-specification. |
| `confidence_trap.md`: spike exploits model certainty | **Contradicted at aggregate level**. Model is LESS certain at k=−1 for genuine spikes. |

## Suggested Next Steps

1. **Re-run `pre_peak_setup.md` with artifact filter** to confirm the entropy reversal
   holds across all eras, not just the global average.
2. **Context-specification by token class**: do proper nouns specifically show a larger
   post-spike entropy drop than other high-S2 token classes?
3. **Semantic field narrowing**: after a high-S2 domain-marking word, do subsequent
   tokens come from the same semantic field? (Measure with embedding similarity)
4. **Cascade test**: when multiple spikes occur in a window (cascade doublets from
   `s2_cascade_doublets.md`), does the entropy after the first spike predict
   the timing of the second?