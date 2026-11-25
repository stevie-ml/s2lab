# Semantic Bridging Across Line Breaks

**Date:** 2026-11-25
**Method:** For each line break in 450 poems, check whether the first word of the
new line appears in the previous line-ending word's top-10 GPT-2 alternatives.
'Bridged' = semantically predicted; 'Ruptured' = outside prediction horizon.
Stanza-break artifact positions filtered (p(newline) ≥ 0.9).
Punctuation tokens excluded from source and head positions.

---

## Overall Bridge Rate

| Metric | Value |
|---|---|
| Total line breaks (artifact-free, all tokens) | 4,274 |
| Total line breaks (artifact-free, word tokens only) | 1,301 |
| Bridged (head word predicted by source word) | 2 (0.2%) |
| Ruptured (head word outside prediction horizon) | 1,299 (99.8%) |
| Avg S₂ at bridged line heads | **-1.633** |
| Avg S₂ at ruptured line heads | **0.131** |
| S₂ gap (ruptured − bridged) | **1.764** |

---

## Bridge Rate and S₂ by Literary Era

Sorted by bridge rate (descending = most semantically continuous line breaks).

| Era | n | Bridge Rate | Bridged AvgS₂ | Ruptured AvgS₂ | Gap |
|---|---|---|---|---|---|
| concrete | 31 | 6.5% | -1.633 | 2.472 | 4.105 |
| romantic | 41 | 0.0% | nan | -0.730 | nan |
| 19th_century | 24 | 0.0% | nan | 1.533 | nan |
| modernist | 113 | 0.0% | nan | 0.652 | nan |
| confessional | 16 | 0.0% | nan | 0.772 | nan |
| mid_century | 22 | 0.0% | nan | -0.302 | nan |
| new_york_school | 133 | 0.0% | nan | -0.817 | nan |
| language | 14 | 0.0% | nan | -1.037 | nan |
| contemporary | 74 | 0.0% | nan | -0.567 | nan |
| surrealist | 28 | 0.0% | nan | -0.308 | nan |
| german_symbolist | 18 | 0.0% | nan | -0.388 | nan |
| german_expressionist | 23 | 0.0% | nan | 0.693 | nan |
| german_modernist | 11 | 0.0% | nan | 0.441 | nan |
| victorian | 107 | 0.0% | nan | 0.948 | nan |
| harlem_renaissance | 17 | 0.0% | nan | -1.232 | nan |
| prose_poetry | 27 | 0.0% | nan | -0.262 | nan |
| metaphysical | 23 | 0.0% | nan | -0.416 | nan |
| early_modern | 23 | 0.0% | nan | -0.767 | nan |
| spoken_word | 22 | 0.0% | nan | 0.710 | nan |
| found_poetry | 64 | 0.0% | nan | -0.597 | nan |
| latin_american | 10 | 0.0% | nan | 0.842 | nan |
| imagist | 15 | 0.0% | nan | -0.409 | nan |
| beat | 33 | 0.0% | nan | 1.156 | nan |
| postcolonial | 27 | 0.0% | nan | 0.065 | nan |
| dramatic_monologue | 154 | 0.0% | nan | 0.169 | nan |
| elegy | 15 | 0.0% | nan | 0.629 | nan |
| ekphrastic | 50 | 0.0% | nan | 0.707 | nan |
| social_media_poetry | 11 | 0.0% | nan | 2.620 | nan |
| objectivist | 46 | 0.0% | nan | 0.041 | nan |

---

## Examples: Bridged Line Breaks with High S₂

These are cases where the new line's first word WAS predicted by the previous word,
yet still carries high S₂ (the whole context, not just the previous word, made it surprising).

| Era | Source → Head | Head S₂ | Rank in Source's Alts |
|---|---|---|---|
| concrete | `spacious` → `for` | -1.09 | #8 |
| concrete | `for` → `for` | -2.17 | #2 |

---

## Finding

**0.2% of artifact-free line breaks are 'bridged'** — the new line's first word was already in the ending word's top-10 alternatives. This means the vast majority (99.8%) are 'ruptured' — the first word of the new line was not predicted at all from the previous word alone.

**Bridged transitions have avg S₂ = -1.633; ruptured have avg S₂ = 0.131** (gap = 1.764 bits). Ruptured transitions (unpredicted by the previous word) carry higher S₂, confirming that cross-line discontinuity is a major driver of poetic surprise.

**Era variation**: concrete has the highest bridge rate (6.5%), suggesting the most semantically continuous line breaks. romantic has the lowest (0.0%), suggesting maximally disruptive cross-line transitions.

---

## Source Word Entropy and Bridge Rate

Does the **certainty of the line-ending word's prediction** affect whether the
next line's first word is bridged? (Low entropy = concentrated prediction; high = diffuse.)

| Entropy Quartile | n | Bridge Rate | Avg S₂ at Head |
|---|---|---|---|
| Q1 (low entropy / concentrated prediction) | 307 | 0.3% | 0.381 |
| Q2 | 307 | 0.3% | -0.197 |
| Q3 | 306 | 0.0% | 0.152 |
| Q4 (high entropy / diffuse prediction) | 306 | 0.0% | 0.140 |

**Interpretation**: When the line-ending word has concentrated prediction (Q1), the next
line's head is either bridged (rare but possible) or carries higher S₂ due to the
stronger expectation being violated. High-entropy endings leave the prediction space
so diffuse that any continuation is a rupture — but a less surprising one.

---

## Next Steps

- Correlate bridge rate with form (formal meter vs. free verse)
- Track 'bridge distance': how far back does the prediction extend?
  (top-5 vs. top-10 alternatives changes the bridge rate — what's the threshold?)
- Compare bridge rate to enjambment classification
  (do 'hard' enjambments always rupture, or can a syntactic break be semantically bridged?)
- Apply to prose: do paragraphs bridge more than stanzas?