# Title Word Recurrence and S₂

**Date:** 2026-10-08  
**Experiment:** `experiments/title_word_recurrence.py`  
**Data:** 122 poems with analyzable title recurrence from the 227-poem corpus

---

## Question

When words from a poem's title reappear in the body text, do they carry different information-theoretic values (S₂) compared to the rest of the poem?

Three hypotheses:
- **Priming**: Title creates semantic frame → body uses of those words feel more predictable → LOWER S₂
- **Strategic recurrence**: Poets echo titles at moments of semantic emphasis → HIGHER S₂
- **Null**: No systematic difference

---

## Method

For each poem:
1. Extract meaningful content words from the title (skip stop words, function words)
2. For each token in the body, check if it matches a title word (4-character stem matching)
3. Filter out stanza-break artifact tokens (`p_newline ≥ 0.9`)
4. Compare avg S₂ at title-word positions vs. all other positions
5. Compute delta = title_avg - non_title_avg per poem, then aggregate

---

## Results

| Metric | Title-word tokens | Non-title tokens | Delta |
|---|---|---|---|
| Count | 386 | 14,800 | — |
| **Mean S₂** | **+0.922** | **-0.434** | **+1.356** |
| Median S₂ | -0.143 | -1.141 | +0.998 |

**66% of poems (80/122) show title words at HIGHER S₂ than poem average.**

---

## Key Cases

### Largest positive deltas (title words most surprising)
| Delta | Author | Title | Era |
|---|---|---|---|
| +11.93 | Gregory Corso | Bomb | — |
| +9.74 | Wordsworth | I Wandered Lonely as a Cloud | romantic |
| +8.75 | Ferlinghetti | Constantly Risking Absurdity | — |
| +8.56 | Plath | Daddy (opening) | confessional |
| +7.96 | Thomas Wyatt | Whoso List to Hunt | early_modern |

In Wordsworth, "wandered," "lonely," and "cloud" reappear in the poem body at unusually deviant moments — the poet chose these exact title words as the text's most semantically unexpected moves.

### Largest negative deltas (title words LEAST surprising)
| Delta | Author | Title | Era |
|---|---|---|---|
| -4.85 | Anne Sexton | The Truth the Dead Know | confessional |
| -3.86 | Gerard Manley Hopkins | The Windhover | victorian |
| -3.69 | Anon (KJV) | Vanity of Vanities (Found Poem, Ecclesiastes) | found_poetry |
| -3.01 | Gregory Corso | Marriage | — |
| -2.53 | Elizabeth Bishop | One Art | mid_century |

Hopkins' "windhover" — a rare, coined word — is LESS surprising in the body than average. Once the title establishes it, its reuse is contextually predicted. Similarly, found poetry shows title words below average because they recur in their natural textual habitat.

---

## Pattern by Era

| Era | Avg delta | n |
|---|---|---|
| spoken_word | +4.79 | 2 |
| 18th_century | +4.73 | 2 |
| prose_poetry | +4.68 | 2 |
| romantic | +4.50 | 9 |
| early_modern | +3.79 | 4 |
| 19th_century | +3.75 | 9 |
| metaphysical | +3.17 | 3 |
| haiku | +3.12 | 9 |
| new_york_school | +2.18 | 8 |
| modernist | +1.31 | 13 |
| victorian | +0.71 | 13 |
| cliche_control | +0.40 | 3 |
| found_poetry | **-1.85** | 5 |

**Found poetry is the only era with systematic negative delta.** All "literary" poetry traditions show positive delta — title recurrence correlates with surprise.

---

## Finding

**Title words, when reused in the poem body, appear at statistically more surprising moments than average (mean delta +1.36 bits, median +1.00 bits). This pattern holds across 66% of poems and across all literary eras — except found poetry.**

This falsifies the "priming" hypothesis. Rather than making the text more predictable, title words mark positions of heightened deviation from GPT-2's expectations. The poet returns to the title's key words precisely where the text most departs from conventional language.

**Interpretation:** This is consistent with a "title as emotional anchor" theory. The poem's title names the central concept, and the poem's body explores it by deploying that word at the most semantically charged moments — where the ordinary language would have chosen something else.

**Found poetry exception:** When the title is metadata (poem source, author, year), title words recur in mundane contexts within the source text, producing below-average S₂.

---

## Caveats

- Title matching uses 4-char stem overlap, which can produce false positives (e.g., "translated" in parenthetical titles)
- Single-occurrence title words give less reliable estimates than frequent reuse
- Mean is inflated by extreme outliers (Corso's "Bomb" = +11.93); median is more robust (+0.998)
- The "title word is unusual" effect may partly drive higher S₂ independently of recurrence (rare words → higher surprisal)

---

## Suggested Next Steps

1. **Frequency control**: Separate analysis of title words that are low-frequency vs. high-frequency in English; test whether the effect survives frequency normalization
2. **Position of recurrence**: Do title words cluster near the poem's end (closure) or beginning (setup)? 
3. **Distance effect**: Does S₂ at title-word recurrence decrease with each subsequent use? (First echo more surprising than second?)
4. **Contrast with first-use position**: Compare S₂ when title word first appears in body vs. subsequent appearances
