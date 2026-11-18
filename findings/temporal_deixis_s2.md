# Temporal Deixis and S₂: Time Words as Poetic Surprise Vehicles
**Date:** 2026-11-18
**Experiment:** `experiments/temporal_deixis_s2.py`
**Corpus:** 707 temporal tokens across 30 distinct temporal adverbs

---

## Research Question

Temporal adverbs — *now, then, always, never, once, still* — are among poetry's most charged words. They compress infinite time into single tokens. Do they carry a distinctive information-theoretic signature? When a poet writes "always" or "never," was GPT-2 expecting something else?

## 1. Temporal Adverbs vs. Rest of Poetry

| Metric | Temporal adverbs (n=704) | Non-temporal tokens (n=55960) |
|---|---|---|
| Avg S₂ | **0.694** | -0.427 |
| % positive S₂ | **54.4%** | 33.5% |
| Std S₂ | 3.284 | 3.637 |

## 2. Temporal Adverbs in Poetry vs. Prose Control

| | Poetry (n=704) | Prose Control (n=3) |
|---|---|---|
| Avg S₂ at temporal adverbs | **0.694** | -1.643 |
| Avg S₂ overall | -0.413 | -1.721 |
| Temporal lift above baseline | **+1.107** | +0.078 |

## 3. Per-Word S₂ Rankings (Poetry, ≥5 occurrences)

| Temporal Word | n | Avg S₂ | % Positive | Avg Entropy | Top-1 Alt (most common) |
|---|---|---|---|---|---|
| `already` | 5 | **4.656** | 100.0% | 6.18 | `'t` |
| `today` | 12 | **3.131** | 83.3% | 6.02 | ` I` |
| `eternal` | 5 | **2.480** | 80.0% | 8.44 | ` beauty` |
| `immortal` | 8 | **2.376** | 75.0% | 7.35 | ` the` |
| `after` | 19 | **2.338** | 73.7% | 6.39 | `,` |
| `ancient` | 14 | **2.222** | 64.3% | 9.42 | ` the` |
| `often` | 5 | **2.209** | 40.0% | 5.02 | ` the` |
| `again` | 41 | **1.744** | 80.5% | 5.62 | `,` |
| `now` | 43 | **1.399** | 62.8% | 6.09 | `,` |
| `once` | 29 | **1.288** | 58.6% | 6.47 | ` the` |
| `still` | 57 | **0.978** | 56.1% | 7.71 | ` the` |
| `soon` | 21 | **0.919** | 57.1% | 6.13 | ` soon` |
| `before` | 26 | **0.872** | 69.2% | 6.13 | ` in` |
| `always` | 16 | **0.680** | 50.0% | 7.30 | ` a` |
| `sometimes` | 8 | **0.614** | 62.5% | 6.95 | ` the` |
| `never` | 45 | **0.410** | 48.9% | 7.10 | ` not` |
| `then` | 50 | **0.241** | 48.0% | 6.79 | ` I` |
| `at` | 144 | **0.077** | 49.3% | 6.01 | ` at` |
| `yet` | 39 | **-0.025** | 43.6% | 7.52 | `,` |
| `long` | 46 | **-0.601** | 32.6% | 6.85 | ` long` |
| `old` | 46 | **-0.822** | 37.0% | 8.51 | ` the` |
| `ago` | 9 | **-0.929** | 22.2% | 4.92 | ` ago` |

## 4. Temporal Category Analysis

| Category | n | Avg S₂ |
|---|---|---|
| frequency | 59 | 1.833 |
| indefinite_present | 156 | 1.127 |
| indefinite_future | 93 | 0.926 |
| absolute_eternal | 76 | 0.913 |
| indefinite_past | 174 | 0.173 |
| sudden_change | 146 | 0.130 |

## 5. Pure Straussian Temporal Moments (S₂ ≥ 3.0, H < 5.0)

Found **65** moments where a temporal adverb shocked a confident model.

| Token | S₂ | Entropy | GPT-2 Expected | Author | Title | Era |
|---|---|---|---|---|---|---|
| `ancient` | 14.31 | 3.90 | `:` | Langston Hughes | The Negro Speaks of Rivers | harlem_renaissance |
| `still` | 12.54 | 3.04 | `shalt` | John Keats | Ode on a Grecian Urn | ekphrastic |
| `then` | 11.61 | 1.15 | `and` | Christian Bök | Eunoia: Chapter E (excerpt) | oulipo |
| `today` | 11.49 | 4.68 | `the` | Synthetic (procedural test case) | Field Notes for Living (Synthe | procedural |
| `now` | 10.62 | 1.98 | `Would` | Gertrude Stein | If I Told Him: A Completed Por | oulipo |
| `again` | 9.79 | 0.42 | `different` | Charles Bernstein | The Sheds of Our Webs | language |
| `old` | 9.78 | 4.54 | `,` | John Keats | The Eve of St. Agnes (stanzas  | romantic |
| `now` | 9.38 | 2.09 | `me` | Robert Browning | Andrea del Sarto (opening) | ekphrastic |
| `yet` | 9.29 | 4.35 | `,` | Gerard Manley Hopkins | Inversnaid | victorian |
| `once` | 9.24 | 4.79 | `cried` | Felicia Hemans | Casabianca | victorian |
| `never` | 9.18 | 3.69 | `—` | Edgar Allan Poe | The Raven (opening stanzas) | 19th_century |
| `yet` | 9.09 | 4.74 | `you` | Felicia Hemans | Casabianca | victorian |
| `after` | 8.48 | 4.30 | `to` | Anonymous (found text) | Weather Observations (Found Po | found_poetry |
| `eternal` | 8.48 | 4.43 | `,` | Caedmon (trans. anon.) | Caedmon's Hymn (modern prose t | old_english |
| `often` | 8.16 | 4.48 | `'ll` | Robert Browning | Andrea del Sarto (opening) | ekphrastic |
| `still` | 8.11 | 3.41 | `to` | Horace (trans. Howes, 1849) | Ars Poetica (opening, trans. H | procedural |
| `now` | 8.06 | 3.81 | `,` | Hart Crane | The Harbor Dawn (from The Brid | modernist |
| `still` | 8.04 | 4.01 | `in` | Isaac Watts | How Doth the Little Busy Bee | parody_original |
| `ago` | 7.75 | 3.64 | `'s` | Walt Whitman | Song of Myself (section 15, ca | 19th_century |
| `at` | 7.74 | 1.38 | `for` | Joy Harjo | She Had Some Horses | postcolonial |

## 6. Era Comparison: Temporal S₂ vs. Baseline

| Era | Temporal n | Temporal Avg S₂ | Baseline Avg S₂ | Lift |
|---|---|---|---|---|
| song_lyrics | 6 | 3.773 | -0.678 | **+4.451** |
| postcolonial | 6 | 2.442 | -0.484 | **+2.927** |
| procedural | 8 | 2.410 | -0.455 | **+2.865** |
| concrete | 5 | 2.260 | -0.584 | **+2.844** |
| surrealist | 12 | 2.014 | -0.505 | **+2.519** |
| latin_american | 12 | 1.996 | -0.481 | **+2.476** |
| oulipo | 19 | 1.775 | -0.182 | **+1.958** |
| early_modern | 28 | 1.466 | -0.371 | **+1.837** |
| ekphrastic | 24 | 1.273 | -0.508 | **+1.781** |
| old_english | 7 | 1.430 | -0.309 | **+1.739** |
| confessional | 5 | 1.483 | -0.234 | **+1.717** |
| parody_original | 13 | 1.213 | -0.454 | **+1.667** |
| ancient | 6 | 1.414 | -0.203 | **+1.617** |
| 18th_century | 13 | 1.186 | -0.285 | **+1.472** |
| limerick | 9 | 0.641 | -0.661 | **+1.302** |
| modernist | 34 | 0.881 | -0.396 | **+1.277** |
| elegy | 21 | 0.784 | -0.455 | **+1.239** |
| prose_poetry | 19 | 0.732 | -0.471 | **+1.203** |
| war_poetry | 10 | 0.820 | -0.340 | **+1.160** |
| victorian | 66 | 0.801 | -0.289 | **+1.090** |

## 7. Eternal vs. Contingent Temporality

Hypothesis: *Eternal* words (always, never, forever) carry different S₂ than
*contingent* words (now, then, once, soon) because they collapse the time axis
in a way GPT-2 doesn't expect.

| Type | n | Avg S₂ | % Positive |
|---|---|---|---|
| Eternal (always/never/forever...) | 67 | **0.727** | 52.2% |
| Contingent (now/then/once/still...) | 346 | 1.144 | 61.3% |

## Findings

1. **Temporal adverbs have HIGHER S₂ than the average poetry token** (Δ = +1.121 bits). Temporal words are charged moments of Straussian deviation — they signal the poet's departure from the statistically expected.

2. **Most surprising temporal word:** `already` (avg S₂ = 4.656). **Least surprising:** `ago` (avg S₂ = -0.929).

3. **Contingent temporality is more Straussian** (eternal avg = 0.727, contingent avg = 1.144). Specific time words (now, then, once) are more surprising than absolutes — the particular disrupts the general.

4. Found **65** 'pure Straussian' temporal moments (S₂ ≥ 3, H < 5) — where the model was highly confident but the poet wrote a time word anyway. Most common suppressed alternatives: `,`×13, `.`×8, `and`×4. These are the grammatically 'expected' words displaced by temporal ones.

## Suggested Next Steps

- **Temporal polarity**: Compare how poets use `never` vs `always` and their local S₂ context.
- **Tense-time consistency**: Do verbs immediately adjacent to temporal adverbs violate tense expectations?
- **Temporal clustering**: Are temporal adverbs clustered in certain parts of poems?
- **Cross-era vocabulary**: Which eras favor eternal vs contingent temporality?
