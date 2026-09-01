# Temporal Evolution of S2 Across Literary History

**Date:** 2026-09-01  
**Research question:** Does the Straussian gap (S2) change systematically across literary history? Are poets becoming more or less surprising relative to GPT-2's contextual confidence?

---

## Method

- English-language poems only (all use GPT-2 base, avoiding cross-model artifacts)
- Control prose excluded
- 67 poems total across 8 literary periods (1686–2017)
- Metrics: avg_s2, pos_s2_ratio (% tokens with positive S2), avg_surprisal, avg_entropy
- Linear regression of avg_s2 ~ year across all individual poems

---

## Key Findings

### 1. No global linear trend — but a clear inverted-U arc

| Period | N | Avg S2 | Pos% | Avg Surprisal | Avg Entropy |
|---|---|---|---|---|---|
| Pre-1700 (Basho, Sappho) | 2 | **+1.163** | 39.2% | 6.899 | 5.736 |
| 1800–1849 (Romantic) | 5 | **−0.042** | 38.8% | 6.594 | 6.635 |
| 1850–1899 (Victorian/Post-Romantic) | 9 | **+0.353** | 40.0% | 6.724 | 6.371 |
| 1900–1929 (Modernist) | 14 | **+0.339** | 36.6% | 6.737 | 6.399 |
| 1930–1959 (Mid-Century) | 9 | **+0.304** | 38.9% | 6.496 | 6.192 |
| 1960–1979 (Postmodern) | 19 | **+0.157** | 37.3% | 6.715 | 6.558 |
| 1980–1999 (Language/Late Postmodern) | 4 | **+0.029** | 33.7% | 6.315 | 6.286 |
| 2000–present (Contemporary) | 5 | **−0.035** | 34.7% | 5.591 | 5.626 |

**Linear trend:** slope = −0.000069 S2/year, r = −0.025 (negligible — history is not directional)

**But the shape is non-linear:** Romantic (low) → Victorian + Modernist (peak) → Postmodern (declining) → Contemporary (near-zero/negative). An inverted-U centered on 1850–1930.

### 2. The Romantic dip: Wordsworth, Keats, Shelley have *negative* avg S2

The canonical Romantic poets (Wordsworth −0.40, Keats −0.36, Shelley −0.03) all score near or below zero. Their vocabulary is elevated but *follows the grammar of confident prediction* — GPT-2 is uncertain about what comes next, and what comes next is usually what the model expected given that uncertainty.

By contrast, the Victorians push against confident contexts. Hopkins's sprung rhythm creates genuinely unpredictable tokens in high-confidence slots. Hardy's archaic diction does the same.

### 3. The Contemporary collapse in surprisal — not just S2

Contemporary poets score not just low S2 (−0.035) but drastically lower **avg_surprisal** (5.59) vs. the historical mean (~6.5). This is the key distinguishing fact: it is not that contemporary poets are choosing expected tokens in confident contexts — rather, the contexts themselves are *less confident* (entropy also drops to 5.63). Contemporary poetry is written in a register GPT-2 understands deeply, because that register — conversational, direct, prose-adjacent — constitutes much of GPT-2's training distribution.

The implication: **the "difficulty" of contemporary experimental poetry (Rankine, Vuong, Long Soldier) operates at a structural and conceptual level that GPT-2 is blind to.** The surprise is in the line break, the white space, the form — not the individual token.

### 4. Hardy's "The Convergence of the Twain" is the Victorian outlier

avg_s2 = **+1.936**, pos_s2_ratio = 52.2%, avg_surprisal = 8.84 — the highest surprisal in the entire English corpus.

Hardy's compressed, archaic, syntactically inverted diction ("In a solitude of the sea / Deep from human vanity") creates exactly the Straussian gap: the model is confident about common words after an unusual construction, and Hardy gives it something else. The poem about the Titanic is itself a collision — of the expected with the utterly chosen.

### 5. The Ashbery paradox: difficulty without S2

John Ashbery (16 poems, avg_s2 = **−0.180**, 10 of 16 poems negative S2) is the most "difficult" poet in the corpus by reputation — but he has among the lowest avg_s2 values. The key: his avg_entropy is consistently *higher* than his avg_surprisal. The model is deeply uncertain about what comes next in Ashbery, and what comes next is also surprising — but not more surprising than the uncertainty predicts.

**Ashbery confuses GPT-2's probability distribution without defeating it.** His "difficulty" is the difficulty of having no confident context — the entropy is high everywhere, so S2 can't spike. This distinguishes him from Hardy, Dickinson, or Gwendolyn Brooks, where the model is momentarily *confident* and is then defeated.

### 6. Highest S2 values: compression, non-standard grammar, archaic diction

| Rank | Poem | Year | avg_s2 |
|---|---|---|---|
| 1 | The Red Wheelbarrow (Williams) | 1923 | **+3.594** |
| 2 | We Real Cool (Brooks) | 1960 | **+2.181** |
| 3 | Three Haiku (Basho, translated) | 1686 | **+2.141** |
| 4 | The Convergence of the Twain (Hardy) | 1912 | **+1.936** |
| 5 | Islets/Irritations (Andrews) | 1983 | **+1.846** |

These are not united by era but by **mechanism**: extreme brevity (haiku, WCW), non-standard grammar ("We real cool" — subject+adj, no verb), archaic diction in confident syntactic slots (Hardy), and disjunctive fragmentation (Andrews). S2 is not a property of "difficulty" in a cultural sense but of **confident context + unexpected choice**.

---

## Hypothesis: The Modernist Commitment to High-Confidence Contexts

The Victorian and Modernist peaks in avg_s2 may reflect a deliberate poetic strategy: build contexts where GPT-2 (a stand-in for "conventional language expectation") is *confident*, then defeat that confidence. Eliot's "[April] is the cruellest month" and Hopkins's "dauphin, dapple-dawn-drawn Falcon" both create moments of high entropy followed by confident slot-filling — which the poet disrupts.

Contemporary poets, working in conversational registers, may be sacrificing S2 at the token level to gain surprise at higher levels (syntactic, formal, conceptual). The S2 framework measures *local lexical surprise*; it may systematically undervalue poetry where the surprise is structural.

---

## Suggested Next Steps

1. **Max S2 by era** — the average obscures whether contemporary poets have occasional high-S2 spikes even if their mean is low. Check per-poem max_s2 distributions.
2. **Isolate the Ashbery corpus** — does Ashbery's S2 change over his career? "Some Trees" (1956) vs "What Is Poetry" (1977) shows different profiles.
3. **Test the "formal constraint → S2" hypothesis** — do poems in strict form (sonnet, villanelle) have higher avg_s2 than free verse? Formal constraints force unexpected lexical choices into confident syntactic slots.
4. **Cross-model comparison** — compare GPT-2 small vs medium on the same poems. If S2 is *higher* with the larger model (which builds more confident contexts), it would confirm that larger models create sharper Straussian gaps.
5. **Add 1890–1910 Decadent/Fin-de-siècle poems** (Housman, Wilde, Dowson) to fill the gap between Victorian and Modernist peaks.
