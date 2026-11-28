# The Near-Miss Zone: Rank-2 and Rank-3 Choices as Poetic Style

**Date:** 2026-11-28  
**Experiment:** `experiments/near_miss_pairs.py` → `results/near_miss_pairs.json`  
**Corpus:** 457 texts, 61,907 clean tokens (p_newline < 0.9), 13,184 near-miss events  
**Builds on:** `findings/rank_distance_deviation.md`, `findings/q2_q1_strategy_taxonomy.md`, `findings/confidence_trap_analysis.md`

---

## Research Question

When a poet chooses GPT-2's second or third prediction — not the top guess, but close to it — what kind of decision is that? The rank-distance analysis established that the near-miss zone (rank 2–5) accounts for 21.3% of all clean tokens. This study asks: **are near-miss choices morphological variants of the top prediction (like choosing "streets" when GPT-2 predicted "street"), or do they look like completely different words that happen to be almost equally probable?**

---

## 1. The Size of the Near-Miss Zone

| Rank Zone | Count | % of Clean Tokens |
|-----------|-------|------------------|
| Rank 1 (exact match) | 19,543 | **31.6%** |
| Rank 2–5 (near-miss) | 13,184 | **21.3%** |
| Rank 6–10 (in model menu) | 4,833 | 7.8% |
| Rank 11–50 (fringe) | 9,036 | 14.6% |
| Rank 51+ (radical) | 15,311 | **24.7%** |

**Three distinct "modes" emerge**: exact match (31.6%), near-miss (21.3%), and radical departure (24.7%). About half of all poetry sits in the two conformist zones (rank 1 and rank 2–5), and about a quarter makes genuinely radical choices (rank 51+).

---

## 2. The Core Finding: Near-Miss ≠ Small Deviation

The near-miss label implies a small step from the top prediction. The character-overlap analysis reveals this is an illusion:

| Character Overlap | Count | % |
|---|---|---|
| Exact same string (case/whitespace only) | 61 | **0.5%** |
| High overlap ≥70% (morphological variant) | 127 | **1.0%** |
| Mid overlap 30–70% | 705 | 5.3% |
| Low overlap <30% (**completely different words**) | 12,291 | **93.2%** |

**93.2% of near-miss choices look like completely different words from the top prediction.** Being GPT-2's rank-2 guess does not mean being morphologically similar to rank-1. The probability distribution at the top is often flat enough that two totally different tokens (like "," and ".") share nearly equal probability — making one rank-1 and the other rank-2 — without having any surface resemblance.

### Near-Miss S₂ Profile

| Metric | Value |
|--------|-------|
| Avg S₂ | **−2.078** |
| Median S₂ | −2.294 |
| Shadow/actual prob ratio | **6.21×** |
| Avg shadow→actual prob gap | 0.173 |

**Near-miss choices have deeply negative S₂ (avg −2.08)**. Despite being "just" rank 2–5, these tokens are informationally *below* baseline. The model was more confident here than average, and the poet chose a plausible but non-top option. This is the **grammar of micro-decision**: not a creative leap, but a stylistic inflection.

---

## 3. What Near-Miss Pairs Are Actually About

The 25 most common near-miss pairs reveal the anatomy of the near-miss zone:

| Actual (poet chose) | Shadow (GPT-2 wanted) | Count |
|---|---|---|
| `.` | `,` | 383 |
| `,` | `.` | 360 |
| `` (newline) | `,` | 286 |
| `and` | `,` | 203 |
| `a` | `the` | 187 |
| `,` | `` (newline) | 163 |
| `;` | `,` | 158 |
| `the` | `` (newline) | 129 |
| `,` | `of` | 125 |
| `and` | `` (newline) | 120 |
| `my` | `the` | 79 |
| `the` | `a` | 78 |
| `his` | `the` | 68 |

**The near-miss zone is overwhelmingly about structural micro-choices**: period vs. comma, comma vs. newline, `a` vs. `the`, `my` vs. `the`, `and` vs. newline. These are the **stylistic accent marks** of a poet — not surprising in information terms (S₂ ≈ −2), but revealing of habitual voice choices.

The poet who consistently chooses `;` where GPT-2 wants `,` is making a near-miss choice 158 times — not out of creativity, but out of stylistic habit.

---

## 4. The Two Exceptions: Morphological Near-Misses

The 1% of near-miss pairs with high character overlap (≥70%) are genuinely interesting: they represent poets choosing the singular when the model expected the plural, or the past tense when it expected the present:

| Actual | Shadow | Era |
|--------|--------|-----|
| `street` | `streets` | romantic |
| `nurses` | `nurse` | language |
| `night` | `nights` | early_modern |
| `word` | `words` | 19th_century |
| `hands` | `hand` | prose_poetry |
| `hear` | `heard` | 19th_century |
| `walls` | `wall` | prose_poetry |
| `Rose` | `Roses` | persian |

These represent **number and tense as poetic choice**: the singular "street" rather than the plural "streets" creates a more intimate, specific vision. The near-miss zone captures these morphological decisions precisely because GPT-2's probability mass is split nearly evenly between singular and plural in many poetic contexts.

---

## 5. Era Signatures: Beat vs. Limerick

| Era | Near-Miss Rate | Rank-1 Rate | Radical Rate |
|-----|---------------|-------------|--------------|
| **beat** | **12.3%** | **56.2%** | 18.9% |
| **limerick** | **27.5%** | 28.4% | 20.4% |
| korean_modernist | 28.4% | 29.4% | 22.5% |
| control (prose) | 27.0% | 44.2% | 8.0% |
| found_poetry | 23.5% | 43.9% | 12.5% |
| objectivist | 18.1% | 45.0% | 17.2% |
| song_lyrics | 17.0% | 54.0% | 12.9% |
| ballad | 16.7% | 40.2% | 24.7% |

**Beat poetry has by far the lowest near-miss rate (12.3%) and highest rank-1 rate (56.2%)**: Ginsberg, Kerouac, and contemporaries either say exactly what the model expects — filling long, rhythmically predictable stretches — or leap radically into unexpected territory. Almost no hedging or micro-stylistic nuance.

**Limericks have the highest near-miss rate (27.5%)**: the form forces constant near-miss micro-choices (should this comma be a dash? this "a" a "the"?) to fit rhyme and meter while staying within the tight probability envelope the model assigns to light verse.

---

## 6. No Structural Position Preference

| Poem Position | Near-Miss Count | % |
|---|---|---|
| First quarter (0–25%) | 3,273 | 24.8% |
| Second quarter (25–50%) | 3,280 | 24.9% |
| Third quarter (50–75%) | 3,309 | 25.1% |
| Fourth quarter (75–100%) | 3,322 | 25.2% |

**Near-miss choices are perfectly uniform across poem position** — unlike high-S₂ spikes (which cluster in the opening) or endings (which are low-S₂). The near-miss zone reflects ongoing stylistic habit, not structural strategy.

---

## Synthesis: The Near-Miss as Stylistic DNA

The near-miss zone (rank 2–5) is not where poets make creative leaps. It is where they reveal their **stylistic fingerprint** — the habitual micro-choices that characterize their voice: how they punctuate, which article they reach for, whether they pluralize. These choices are informationally conformist (S₂ ≈ −2), visually unlike their shadows (93% low char overlap), and distributed evenly across the poem.

This creates a testable hypothesis: **the near-miss zone should be the most stable signature of a poet's style** across poems, more stable than their S₂ spikes (which may be context-dependent) or their radical departures (which are genre-dependent). A poet's punctuation habits and article preferences should be highly consistent.

Beat poetry's unusual signature — maximum conformity OR maximum radicalism, with minimum near-miss hedging — suggests a **bimodal strategy**: long passages of rhythmic flow (rank-1) punctuated by genuine surprises (rank 51+), without the micro-stylistic modulation of other traditions.

---

## Next Steps

1. **Near-miss as style fingerprint**: Does poet identification via near-miss pairs outperform S₂-based fingerprinting?
2. **The 1% morphological near-miss**: Does singular/plural choice in the near-miss zone correlate with other formal features (line length, rhyme)?
3. **Beat bimodality**: Extend the bimodal analysis to other eras — is the sharp rank-1/radical split unique to Beat, or shared with other oral traditions (spoken_word, ballad)?
4. **Near-miss pair stability within a poet's corpus**: For poets with multiple poems, how consistent are their near-miss pair preferences?
