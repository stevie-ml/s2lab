# The Frequency Confound Audit: How Much of S₂ Is Just Word Rarity?

**Date:** 2026-11-13
**Experiment:** `experiments/frequency_confound_audit.py` → `results/frequency_confound_audit.json`
**Corpus:** 403 English texts, 29,608 complete-word tokens (52.9% of 55,998)
**Frequency source:** `wordfreq` Zipf scale — external, corpus-independent
**Builds on / re-tests:** `polysemy_s2.md`, `content_vs_function_word_s2.md`, `word_length_vs_s2.md`, `stanza_break_artifact.md`

---

## Why This Experiment

Earlier today, `polysemy_s2.md` found that polysemy correlates *inversely* with S₂ — and
traced the cause to a confound. Polysemous words ("heart", "hand", "place") are
overwhelmingly high-frequency words that GPT-2 always expects. The apparent polysemy
effect was largely a frequency effect wearing a costume.

That is a warning shot for the whole lab. S₂ = surprisal − entropy, and surprisal is
driven hard by how rare a word is. If a large share of the S₂ signal is unigram word
rarity, then any finding of the form *"linguistic feature X has elevated S₂"* may be
reporting nothing more than *"feature X co-occurs with rarer words."*

With 563 findings now resting on raw S₂, this audit asks the question directly: build a
frequency baseline from an external reference, measure how much of S₂ it explains, then
re-test the lab's headline claims against frequency-residualised S₂.

---

## Method

**Complete words only.** GPT-2 uses BPE, so many tokens are subword fragments ("ain"
inside "mountain"). Scoring a fragment against a word-frequency table is meaningless. A
token qualifies only if it is word-initial (leading space) and is not continued by an
alphabetic token. This yields 29,608 of 55,998 tokens (52.9%).

Two confounds are eliminated as a side effect:

* The filter drops newline tokens, so the **stanza-break artifact** cannot contaminate
  these numbers.
* Only **English-language** texts are analysed. The corpus holds 8 German poems; scoring
  German words against an English frequency table would misread them as ultra-rare
  English, manufacturing exactly the confound being measured. (In a first pass that
  skipped this filter, `german_symbolist` showed a mean Zipf of 3.37 and a spurious
  rank-2 placement.)

**Residualisation is non-parametric.** S₂_resid = S₂ − mean(S₂ | Zipf bin), using
0.25-wide bins fit on the pooled analysed set. This removes the average frequency effect
without assuming linearity.

---

## Finding 1: Frequency Explains ~21% of S₂ — and the Curve Spans 7 Bits

| Relationship | Pearson r | R² |
|---|---|---|
| Zipf vs **surprisal** | −0.604 | **0.365** |
| Zipf vs **S₂** | −0.457 | **0.209** |
| Zipf vs **entropy** | −0.360 | 0.130 |

Word frequency alone accounts for **20.9% of all variance in S₂**. The bin-mean curve is
cleanly monotonic across almost the entire range:

| Zipf bin | n | Mean S₂ | | Zipf bin | n | Mean S₂ |
|---|---|---|---|---|---|---|
| 3.25 | 268 | **+3.91** | | 6.00 | 1,869 | −0.38 |
| 3.75 | 849 | +3.10 | | 6.50 | 2,157 | −1.03 |
| 4.25 | 1,285 | +2.11 | | 7.00 | 2,114 | −1.70 |
| 4.75 | 1,875 | +1.07 | | 7.50 | 2,303 | −2.06 |
| 5.25 | 1,908 | +0.47 | | 7.75 | 2,020 | **−3.42** |

From the rarest to the commonest bin is a **7.3-bit swing in mean S₂, driven by nothing
but word frequency.** Any S₂ comparison between groups whose vocabularies differ in
rarity is reading this curve unless it controls for it.

**A mechanistic note worth keeping.** Frequency predicts entropy too (r = −0.360): rare
words tend to arrive in high-entropy contexts. Because S₂ subtracts entropy, the entropy
term *partially self-corrects* for frequency — which is why S₂'s frequency dependence
(R² = 0.21) is materially weaker than raw surprisal's (R² = 0.36). **S₂ is already a
partial frequency control. It is not a sufficient one.**

---

## Finding 2: The Core Claim Survives Intact — Poetry vs Prose Was Never a Vocabulary Effect

This is the project's foundational claim, and it is the one most worth stress-testing.

| | n words | Mean Zipf | Raw S₂ | Residual S₂ |
|---|---|---|---|---|
| Poetry | 29,493 | **5.848** | −0.246 | **+0.014** |
| Prose control | 115 | **5.846** | −1.939 | **−1.621** |
| **Gap** | | **0.002** | **+1.694** | **+1.635** |

Poetry and prose in this corpus use words of **virtually identical average frequency**
(5.848 vs 5.846, a difference of 0.002 Zipf). The 1.69-bit S₂ gap therefore cannot be a
vocabulary-rarity effect, and residualising removes almost none of it — 96.5% of the gap
survives.

Bootstrap (2,000 resamples) on the residual gap: **+1.635, 95% CI [1.218, 2.067]**, with
100% of resamples above zero.

**The honest unit of analysis is the text, not the token**, and the separation holds
there too:

| | n texts | Mean residual S₂ | SD |
|---|---|---|---|
| Poems (≥20 words) | 348 | **+0.017** | 0.688 |
| Prose controls | 4 | **−1.631** | — |

| Prose control text | Residual S₂ |
|---|---|
| Academic prose | −2.17 |
| Technical prose | −1.52 |
| Simple narrative prose | −1.46 |
| News article prose | −1.38 |

The four prose texts sit roughly **2.4 standard deviations below the poetry mean**, and
only **3 of 348 poems (0.9%)** score below even the *least* conformist prose text.

**Caveat, stated plainly:** the prose side is 4 usable texts and 115 analysable words.
The effect is large and consistent, but it rests on a thin control sample. Expanding the
prose control set is the single highest-value corpus investment this project can make.

---

## Finding 3: The Content/Function Word Effect Is ~99% Frequency Artifact

| Word class | n | Mean Zipf | Raw S₂ | Residual S₂ |
|---|---|---|---|---|
| Content | 14,889 | 4.849 | **+1.113** | +0.027 |
| Function | 14,719 | 6.859 | **−1.633** | −0.012 |
| **Gap** | | 2.010 | **2.746** | **0.039** |

A 2.746-bit raw gap collapses to **0.039 bits** — **98.6% of it was frequency.**

Content words are not informationally special in poetry. They are simply rarer. Once
words of equal frequency are compared, content and function words are
**indistinguishable** in their deviation from expectation. Any interpretation built on
content words "carrying the poetic load" needs revisiting.

---

## Finding 4: The Word-Length Effect Is ~76% Frequency — but Long Words Keep a Real Residual

`word_length_vs_s2.md` reported a "near-linear relationship" between word length and S₂.
Most of it is frequency, but not all:

| Length | n | Mean Zipf | Raw S₂ | Residual S₂ |
|---|---|---|---|---|
| 1–2 | 6,074 | 6.95 | −1.678 | −0.078 |
| 3–4 | 13,885 | 6.13 | −0.861 | −0.147 |
| 5–6 | 6,706 | 4.89 | +1.013 | −0.003 |
| 7–9 | 2,683 | 4.45 | +2.632 | **+0.926** |
| 10+ | 260 | 4.22 | +3.147 | **+1.027** |

The raw range of 4.83 bits shrinks to 1.17 bits — a **76% reduction**. Words of 1–6
characters flatten to approximately zero: their apparent S₂ differences were entirely
rarity.

But the long-word buckets retain roughly **+1 bit of genuine excess surprise beyond what
their rarity predicts**. Long words in poetry are more surprising than equally rare short
words. The monotonic story is wrong; the correct one is a **threshold effect at ~7
characters.** Plausibly, polysyllabic words are register-marked — a long Latinate word
signals a shift in diction that the model cannot anticipate from frequency alone.

---

## Finding 5: Era and Author Rankings Reshuffle Substantially

Frequency control does not merely rescale the rankings; it reorders them.

**Eras — biggest rank movements (of 48 with n ≥ 100):**

| Era | Raw rank | Resid rank | Raw S₂ | Resid S₂ | Mean Zipf |
|---|---|---|---|---|---|
| language | 37 | **11** | −0.529 | +0.171 | 6.145 |
| persian | 41 | **22** | −0.668 | +0.032 | 6.143 |
| black_arts | 39 | **21** | −0.546 | +0.041 | 6.081 |
| postcolonial | 19 | **6** | −0.221 | +0.233 | 5.956 |
| ancient | 15 | **34** | −0.158 | −0.171 | 5.691 |
| concrete | 25 | **41** | −0.318 | −0.337 | 5.547 |
| classical_chinese | 26 | **39** | −0.319 | −0.319 | 5.625 |

The pattern is systematic: **movements up belong to eras with common vocabularies
(Zipf ≈ 6.0–6.2), movements down to eras with rarer ones (Zipf ≈ 5.5–5.7).** Language
poetry, Black Arts, and postcolonial verse were being *penalised* by the raw metric for
writing in plain words. Their surprise is contextual, and it was invisible until
frequency was controlled.

**Beat poetry ranks #1 on both measures and strengthens** (+1.284 → +1.619) while using
distinctly common words (Zipf 5.917) — genuine contextual defiance, not a thesaurus.

**Authors (of 51 with n ≥ 150):**

| Poet | Raw rank | Resid rank | Raw S₂ | Resid S₂ | Mean Zipf |
|---|---|---|---|---|---|
| Marianne Moore | 1 | **1** | +1.707 | **+2.109** | 5.954 |
| Gerard Manley Hopkins | 2 | 2 | +0.592 | +0.776 | 5.807 |
| Emily Dickinson | 4 | 4 | +0.394 | +0.661 | 5.845 |
| Frank O'Hara | 45 | **25** | −0.705 | +0.045 | 6.216 |
| Charles Bernstein | 40 | **24** | −0.622 | +0.081 | 6.173 |
| Percy Bysshe Shelley | 16 | **38** | −0.087 | −0.276 | 5.544 |
| Algernon Swinburne | 22 | **39** | −0.177 | −0.288 | 5.595 |

Marianne Moore is the corpus's most genuinely deviant poet by a wide margin, and her lead
*grows* under frequency control despite an unremarkable vocabulary.

O'Hara and Bernstein — the two most colloquial poets in the set — climb ~20 places each.
Shelley and Swinburne, high-Romantic diction poets, fall ~20. The raw metric was
substantially measuring **how ornate a poet's vocabulary is**, not how much they defy
expectation.

---

## What This Means

Frequency control acts as a **discriminator between two distinct poetic strategies** that
raw S₂ conflates:

1. **Lexical surprise** — reach for a rare word. Cheap to measure, and the raw metric
   rewards it heavily. Shelley, Swinburne, the Romantics.
2. **Contextual surprise** — place an ordinary word where it was not expected. Invisible
   to raw S₂, revealed by residual S₂. Moore, O'Hara, Bernstein, the Beats, Language
   poetry.

The Straussian gap thesis is really a claim about **(2)**: the space between what
language expects and what the poet writes. Residual S₂ measures that far more cleanly
than raw S₂ does, because it holds the lexicon constant and isolates placement.

**Scorecard for the re-tested findings:**

| Finding | Verdict |
|---|---|
| Poetry less conformist than prose | **Survives** (96.5% of gap retained; identical mean Zipf) |
| Content > function words in S₂ | **Collapses** (98.6% artifact) |
| Word length → S₂, near-linear | **Partly survives** — not linear; threshold at ~7 chars |
| Era rankings | **Reshuffles** — systematically by vocabulary commonness |
| Author rankings | **Reshuffles** — ±20 places, by diction ornateness |

---

## Suggested Next Steps

1. **Adopt residual S₂ as a standard reported measure.** Headline claims should cite raw
   and residual side by side. The helper in this experiment is reusable as-is.

2. **Expand the prose control set.** Four texts and 115 analysable words is too thin a
   foundation for the project's central claim, however large the effect. Target 30–50
   prose texts spanning registers (academic, journalistic, technical, fiction, spoken
   transcript, instruction manual).

3. **Re-audit the high-traffic findings.** The content/function collapse suggests others
   are vulnerable — any experiment contrasting groups with differing vocabulary rarity.
   Priority candidates: `latinate_germanic_results`, `technical_vocabulary_s2`,
   `proper_names_as_s2_anchors`, `archaic_english_s2`, `abstract_concrete_s2`.

4. **Re-run the polysemy retest with local WordNet data.** NLTK's download is blocked in
   this environment by SSRF protection on the proxy, so the polysemy arm of this audit
   did not execute. Vendoring the WordNet corpus into the repo would close the loop on
   the finding that motivated this work.

5. **Test the ~7-character threshold directly.** Is it length, syllable count, or
   Latinate etymology that produces the residual +1 bit? These are separable with a
   syllable counter and an etymology list.

---

## Environment Note

The documented setup (`pip install torch transformers` then `python3 engine.py`) is
broken in the current container: `pip` installs into Python 3.13's site-packages while
`python3` resolves to 3.11, so imports fail silently after an apparently successful
install. **Use `python3.13` explicitly** to run engine and experiment scripts here.
