# Line Length vs S₂: The Compression Hypothesis

**Date:** 2026-09-15  
**Experiment:** `experiments/line_length_s2.py`  
**Data:** 128 texts, 1,248 poetry lines analyzed

---

## Question

Does line length predict S₂ per token? If poets compress meaning into shorter lines, each token should carry more semantic weight — appearing more surprising relative to GPT-2's distributional expectations. We call this the **compression hypothesis**.

---

## Key Results

### Global Correlation

| Scope | n lines | r(line_len, S₂) |
|---|---|---|
| All texts | 1,248 | **-0.28** |
| Poetry only | 1,248 | **-0.28** |

A negative correlation: **shorter lines → higher S₂**. Modest but consistent.

### S₂ by Line-Length Bucket (poetry)

| Bucket | n | Avg S₂ | Median S₂ |
|---|---|---|---|
| 1–3 tokens (very short) | 50 | **+5.31** | +3.45 |
| 4–6 tokens (short) | 182 | **+1.00** | +0.34 |
| 7–10 tokens (medium) | 635 | **+0.66** | +0.50 |
| 11–15 tokens (long) | 320 | **+0.08** | -0.01 |
| 16+ tokens (very long) | 61 | **-0.29** | -0.38 |

**The gradient is stark and monotone.** From very short to very long lines, avg S₂ drops from +5.31 to -0.29 — a range of 5.6 units. Very long lines actually dip into negative S₂ territory, indistinguishable from prose.

### Within-Poem Direction

Across 118 analyzable poems:
- **70% show negative within-poem r** (shorter lines → higher S₂)  
- 29% show positive within-poem r (longer lines → higher S₂)
- Mean within-poem r = **-0.163**

The compression hypothesis holds within poems as well as across them.

---

## Era Analysis

| Era | Avg line length | Avg S₂ |
|---|---|---|
| haiku | 5.1 tokens | **+3.60** |
| confessional | 7.7 | +1.33 |
| mid_century | 7.9 | +1.56 |
| modernist | 8.5 | +0.80 |
| romantic | 9.5 | +0.52 |
| victorian | 10.4 | +0.58 |
| song_lyrics | 11.3 | +0.34 |
| beat | 24.3 | +1.21 |

Cross-era r(avg_line_len, avg_S₂) = **-0.16**

The haiku result is decisive: the shortest-line tradition produces the highest S₂ by far. The **beat poetry anomaly** (long lines, but still high S₂) is the key exception — see below.

---

## The Beat Anomaly

Ginsberg's "A Supermarket in California" has a within-poem r = **-0.998** (near-perfect negative correlation), yet it has the longest average line length in the corpus (31.3 tokens). How? 

The poem's structure oscillates: some lines sprawl (catalogs, questions), some concentrate. When Ginsberg shortens a line, he concentrates maximum surprise. The long lines are padding; the short lines are bombs. This suggests Ginsberg deploys line-length *variation* as a rhetorical weapon — the contrast between long and short is itself an information-theoretic device.

---

## Same-Poet Comparisons

| Poet | Shorter poem | S₂ | Longer poem | S₂ |
|---|---|---|---|---|
| Langston Hughes | "Harlem" (5.8 tok/line) | **+1.83** | "The Negro Speaks of Rivers" (11.7) | +0.79 |
| T.S. Eliot | "The Hollow Men" (5.6) | **+0.19** | "Prufrock" (9.1) | -0.14 |
| E.E. Cummings | "anyone lived…" (7.5) | **+2.09** | "Buffalo Bill's" (16.0) | +1.60 |
| Traditional ballad | "Bonnie George Campbell" (6.3) | **+2.14** | "Lord Randal" (15.3) | +0.11 |
| John Ashbery | "Some Trees" (6.5) | -0.38 | "The Instruction Manual" (14.4) | -0.99 |

When the same poet writes shorter vs longer lines, the shorter poem consistently shows higher S₂ — even Ashbery, whose S₂ is generally negative, gets *less negative* in his shorter-line work.

---

## Interpretation

The compression hypothesis is **confirmed** with moderate strength:

1. **Short lines = high S₂** — the monotone gradient across length buckets (5.31 → -0.29) is the clearest quantitative finding yet about poetic form and information theory.

2. **Form constrains content** — poets working in compressed forms (haiku, epigram, short lyric) are *forced* to choose more surprising tokens per unit because they have less syntactic runway to build conventional context.

3. **The long-line exception is instructive** — poets like Ginsberg and Whitman who maintain high S₂ in long lines do so not despite their form but *against* it: they use line-length variation (not brevity per se) to manipulate S₂ locally.

4. **Prose-like collapse** — lines of 16+ tokens have avg S₂ = -0.29, nearly identical to control prose. The information-theoretic boundary between "poetry" and "prose" may be approximately 15 tokens per line.

---

## Suggested Next Steps

- **Stanza coherence**: Does S₂ tend to cluster within stanzas, or is the line the true unit of information-theoretic analysis?
- **Line-break as commitment device**: Each newline resets GPT-2's expectation to "newline = end." Shorter lines do this more often per word count — is the line-break itself the compression mechanism?
- **Test with syllable count**: Replace token count with syllable count for meter-sensitive analysis (iambic pentameter has fixed syllables but varying token counts).
- **Minimal pairs**: Find poems with two versions at different line lengths (prose poems vs lineated originals) and directly test the compression effect.
