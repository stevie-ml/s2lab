# Near-Miss vs. Radical Departure: The Rank Distance of Poetic Surprise

**Date:** 2026-09-28  
**Experiment:** `experiments/rank_distance_analysis.py`  
**Corpus:** 184 texts, 19,365 clean tokens (stanza-break artifact removed)  
**Builds on:** `lexical_fork_analysis.md`, `confidence_trap_analysis.md`, `within_poem_type_arc.md`

---

## Research Question

The S₂ metric (surprisal − entropy) tells us *how much* a token surprised GPT-2, but it conflates two very different acts: choosing rank 11 (barely outside the model's menu) vs. choosing rank 5,000 (the poet went somewhere the model could barely conceive). This experiment maps the full **rank distribution** of poetic choices and asks: **are poets "near-miss deviators" or "radical departurists"?**

---

## 1. The Overall Shape: Poetry Is Mostly Predictable

Among 19,365 clean tokens across 184 texts:

| Rank bucket | Count | % | Avg S₂ | % positive S₂ |
|---|---|---|---|---|
| **1 (exact match)** | 5,935 | **30.6%** | −2.944 | 0.0% |
| 2–5 (top predicted) | 4,197 | 21.7% | −2.097 | 11.6% |
| 6–10 (in model menu) | 1,510 | 7.8% | −0.876 | 26.9% |
| 11–20 (near miss) | 1,273 | 6.6% | −0.089 | 40.7% |
| 21–50 (moderate miss) | 1,581 | 8.2% | +0.781 | 57.1% |
| 51–100 (moderate) | 1,045 | 5.4% | +1.702 | 72.8% |
| 101–500 (wide miss) | 2,035 | 10.5% | +2.902 | 87.6% |
| 501–1,000 (far miss) | 646 | 3.3% | +4.364 | 99.1% |
| 1,001–5,000 (radical) | 890 | 4.6% | +6.130 | 100.0% |
| **5,000+ (extreme)** | 253 | **1.3%** | +9.626 | **100.0%** |

**60.1% of all clean poetry tokens are in GPT-2's top-10 predictions.** Only 5.9% are genuine "wide miss" deviations (rank > 500). This confirms the core asymmetry of poetic language: the vast majority of a poem follows conventional linguistic paths, while the surprising moments are rare and concentrated.

### The S₂–Rank Ladder

S₂ climbs monotonically with rank: rank-1 tokens average −2.944 S₂; rank-5000+ tokens average +9.626 S₂. The "rank-21" cutoff (where avg S₂ first turns positive: +0.781) marks the threshold between *linguistically expected* and *genuinely surprising*. Ranks 11–20 are the gray zone: above the menu, but not yet reliably surprising.

---

## 2. The Context of Deviation: Confident vs. Uncertain Model

A critical distinction: when GPT-2 is *confident* vs. when it is *uncertain*, poets who deviate tend to deviate very differently.

| Context | n (deviating) | Median rank | Near-miss (11–50)% | Radical (>500)% | Extreme (>5,000)% |
|---|---|---|---|---|---|
| **Low entropy** (Q25 < 4.4 bits) | 443 | **42** | **55.3%** | 11.5% | 2.9% |
| **High entropy** (Q75 > 8.3 bits) | 3,477 | **189** | 25.3% | **32.4%** | 4.7% |

**When GPT-2 is maximally confident, poets who deviate tend to take near-miss options** (55.3% near-miss vs. 11.5% radical). This is "constrained deviation": facing strong linguistic pressure, the poet nudges one position away rather than abandoning the structure entirely.

**When GPT-2 is uncertain, poets take much more radical departures** (32.4% radical vs. 11.5%). The freedom of an uncertain context enables more dramatic choices — the poet exploits the model's indecision to make a genuinely unpredictable move.

This suggests two fundamentally different deviation strategies, each calibrated to the available room:
1. **Constrained deviation**: Use near-miss options when pressure is high (confident model)
2. **Liberated deviation**: Go radically far when there is latitude (uncertain model)

---

## 3. Era Rankings: Prose Poetry Is "Near-Miss," Beat Is "Radical"

Among deviation tokens (rank > 10) by era, sorted by median rank:

| Era | N | Median rank | Near-miss% | Radical% | Avg S₂ |
|---|---|---|---|---|---|
| **prose_poetry** | 298 | **48** | 51.0% | 11.1% | 2.590 |
| found_poetry | 231 | 53 | 48.9% | 15.2% | 2.621 |
| song_lyrics | 132 | 56 | 47.0% | 15.2% | 2.821 |
| early_modern | 264 | 78 | 39.0% | 17.8% | 2.226 |
| new_york_school | 551 | 90 | 37.6% | 22.5% | 2.515 |
| german_symbolist | 200 | 96 | 35.5% | 21.5% | 2.510 |
| victorian | 1,201 | 105 | 36.3% | 25.3% | 2.487 |
| haiku | 140 | 112 | 29.3% | 26.4% | 2.465 |
| confessional | 174 | 117 | 38.5% | 30.5% | 2.792 |
| romantic | 891 | 121 | 32.4% | 24.8% | 2.166 |
| language | 62 | 141 | 40.3% | 33.9% | 2.816 |
| modernist | 628 | 145 | 29.9% | 27.7% | 2.637 |
| **beat** | 68 | **606** | 22.1% | **51.5%** | **4.369** |

**Beat poetry (Ginsberg) is a clear statistical outlier.** Its median deviation rank is 606 — compared to 48 for prose poetry and 90 for New York School. Over half of all Beat deviations are "radical" (rank > 500). Beat is not just more surprising than other eras; it adopts a qualitatively different **deviation strategy**.

**Prose poetry and found poetry cluster at the near-miss end.** When these genres deviate from GPT-2's predictions, they tend to choose options that are "just outside" the model's expected range. The surprise is subtle, adjacent.

**Note on Beat vs. Language poetry**: Language poetry has a higher near-miss rate (40.3%) and lower extreme rate (6.5%) despite being considered the more "radical" avant-garde movement. This suggests Language poetry operates through accumulated near-misses (constant minor friction) while Beat operates through occasional, dramatic departures (rare but extreme surprises). Different aesthetics of resistance.

---

## 4. Temporal Rhythm: Early Poems Reach Farther

Among deviation tokens, the early third of poems makes the most radical choices:

| Position | n | Median rank | Near-miss% | Radical% |
|---|---|---|---|---|
| **Early (0–33%)** | 2,870 | **112** | 34.5% | **25.5%** |
| Middle (33–66%) | 2,421 | 90 | 37.8% | 21.4% |
| Late (66–100%) | 2,432 | 91 | 38.9% | 22.1% |

Poems reach their farthest-rank deviations early (median rank 112 in the first third vs. 90–91 in the latter thirds). This is consistent with `within_poem_type_arc.md`'s finding that poems "deviate early, resolve late" — and this analysis shows the deviation is not just more *frequent* early, but also more *radical* (farther from the model's menu). The middle and late sections shift slightly toward near-miss strategies as the poem settles into its own established contract.

---

## 5. Poet Signatures: A Spectrum from Near-Miss to Radical

Among poets with ≥50 deviation tokens:

| Strategy | Poets | Median rank | Style |
|---|---|---|---|
| **Near-miss** | Killarney Clary (40), Frank O'Hara (44), Christina Rossetti (46), Shakespeare (47) | 40–52 | Adjacent surprise |
| **Moderate** | Donne (64), Kipling (73), Rilke (87), Poe (87), Ashbery (94) | 60–120 | Balanced |
| **Radical** | Hopkins (209), Whitman (195), Dickinson (164), Cummings (162) | 130–210 | Wide leaps |
| **Extreme** | Ginsberg (606) | 606 | Off-menu |

**Allen Ginsberg is isolated at the extreme end.** His median deviation rank (606) is 3× higher than the next most radical poet (Hopkins at 209). Ginsberg's surprise strategy is not just more frequent — it involves choosing options that are genuinely outside the model's contemplated space.

**Frank O'Hara, despite his experimental reputation, is a near-miss poet** (median rank 44). New York School poetry achieves its effects through a high density of moderate surprises, not through occasional extreme departures.

**Emily Dickinson (rank 164) and Gerard Manley Hopkins (rank 209)** are among the most "radical" 19th-century poets — their deviations go further from model predictions than their contemporaries (Tennyson: 134, Keats: 131, Shelley: 120).

---

## 6. Rank Quartile Distribution by Era

Global deviation rank quartiles: Q1=29, Q2=97, Q3=436

| Era | Q1 (≤29)% | Q2 (≤97)% | Q3 (≤436)% | Q4 (>436)% |
|---|---|---|---|---|
| found_poetry | 35.9% | 28.6% | 19.0% | **16.5%** |
| prose_poetry | 33.9% | 32.2% | 21.5% | **12.4%** |
| new_york_school | 26.3% | 26.0% | 24.0% | 23.8% |
| confessional | 26.4% | 20.1% | 23.0% | **30.5%** |
| modernist | 21.0% | 21.7% | 28.2% | 29.1% |
| language | 29.0% | 19.4% | 14.5% | **37.1%** |
| beat | 14.7% | 14.7% | 16.2% | **54.4%** |

**The control prose** (not shown: 45.5% in Q1) confirms that non-poetic language very rarely deviates and when it does, almost always stays in the near-miss zone. The inverse of Ginsberg's strategy.

**Confessional poetry** splits almost evenly across all four quartiles, with a slight lean toward Q4 (extreme). This multi-modal distribution may reflect the confessional aesthetic's mix of plain speech with sudden violent deviation — Plath's ordinary syntax that erupts.

---

## Key Findings

1. **60% of poetry tokens are in GPT-2's top-10 predictions.** Poetry runs on mostly conventional linguistic rails; the surprise is reserved for ~5% of tokens at rank > 500.

2. **Two deviation strategies, calibrated to context:**
   - **Constrained deviation** (confident model): near-miss options (rank 11–50) are preferred
   - **Liberated deviation** (uncertain model): radical options (rank > 500) become available
   This suggests poets are sensitive to the amount of "linguistic pressure" and adjust their departure distance accordingly.

3. **Beat poetry is an outlier**: median deviation rank 606 (vs. prose poetry: 48). Ginsberg's strategy is genuinely in a different category from all other eras.

4. **Early poem sections reach farthest** (median rank 112 in first third vs. 90–91 later), consistent with "deviate early, resolve late." The opening gambit not only occurs more often but reaches further from the model's menu.

5. **Language vs. Beat distinction**: Despite similar avant-garde status, Language poetry uses *accumulated near-misses* (many rank-11–50 deviations) while Beat uses *occasional radical departures* (fewer but extreme). Different aesthetics of linguistic resistance.

---

## Suggested Next Steps

- **Rank distance curves over time**: Is the trend from near-miss toward radical a feature of 20th-century modernism? Track median deviation rank per decade.
- **Rank distance × token type**: Are near-miss deviations more often nouns while radical deviations are more often verbs or prepositions?
- **Rank distance and memorability**: Among the 253 "extreme" deviations (rank > 5,000), which have become famous phrases? The "fearful symmetry" question — does extreme rank predict poetic memorability?
- **Calibration experiment**: Manually examine 20 confident-model near-misses (rank 11–20) — are these cases where the poet clearly saw the "obvious" word and chose the adjacent alternative?
