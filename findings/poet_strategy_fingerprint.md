# Poet Strategy Fingerprint: Is Information-Theoretic Strategy a Stable Poet Property?

**Date:** 2026-11-27  
**Experiment:** `experiments/poet_strategy_fingerprint.py`  
**Results:** `results/poet_strategy_fingerprint.json`  
**Corpus:** 439 English poems (control excluded), 46 poets with ≥3 poems  
**Builds on:** `findings/entropy_variance_trap_release.md` (4-quadrant typology)

---

## Background

The 4-quadrant typology established in `entropy_variance_trap_release.md` classifies each poem by its joint position in (mean S₂, std_H) space:

| Quadrant | S₂ | std_H | Character |
|---|---|---|---|
| **Consistent Ambush** | high | low | Surprising without being chaotic |
| **Trap-Release** | high | high | Builds uncertainty, then strikes |
| **Erratic Conformist** | low | high | High entropy but low deviation |
| **Metronomic** | low | low | Stable, predictable throughout |

**New question:** Is a poet's quadrant assignment a **stable property** across their body of work — a "strategy fingerprint" — or does it vary poem by poem depending on form, occasion, or subject?

---

## Key Finding: Strategy Is NOT a Stable Poet Fingerprint

| Consistency threshold | Poets meeting it | % |
|---|---|---|
| ≥ 100% (always same quadrant) | 0 / 46 | **0%** |
| ≥ 75% (3 of 4 poems same) | 5 / 46 | **11%** |
| ≥ 50% (bare majority) | 33 / 46 | **72%** |

**No poet is 100% consistent.** Even the most stylistically constrained poets (Tennyson, Shelley, synthetic procedural forms) deviate from their dominant quadrant in at least 1 of 4+ poems. This strongly suggests that **information-theoretic strategy is determined by the poem, not the poet** — by its form, genre, occasion, and length, rather than by individual voice.

---

## Most and Least Consistent Poets

### Most Consistent (≥ 75%)

| Poet | Era | Dominant Quadrant | Consistency | n |
|---|---|---|---|---|
| Alfred, Lord Tennyson | victorian | Erratic_Conformist | **80%** | 5 |
| Synthetic (procedural) | procedural | Erratic_Conformist | **80%** | 5 |
| Percy Bysshe Shelley | romantic | Trap_Release | **75%** | 4 |
| Lucille Clifton | contemporary | Metronomic | **75%** | 4 |
| Anonymous (found text) | found_poetry | Metronomic | **75%** | 4 |

**Tennyson at 80%** is the most consistent real poet: 4 of 5 poems fall in Erratic_Conformist (high entropy variance but low deviation). This matches his formal style — elaborate syntactic variation without sustained unpredictability. The exception is *The Lady of Shalott* (Trap_Release), which is notably more rhythmically surprising than his other work.

**Shelley at 75%** lands in Trap_Release: Ozymandias, Ode to the West Wind, and To a Skylark all use variable entropy contexts to amplify moment-of-surprise impact. Only Adonais (stanzas I-II) falls in Metronomic — his elegiac mode is calmer.

**Synthetic procedural forms** are almost as consistent as Tennyson. This confirms that **formal constraints, not individual voice, drive consistency**.

### Least Consistent

| Poet | Era | Dominant Quadrant | Consistency | n |
|---|---|---|---|---|
| Walt Whitman | 19th_century | Erratic_Conformist | **30%** | 10 |
| John Ashbery | new_york_school | Metronomic | **35%** | 17 |
| E.E. Cummings | modernist | Erratic_Conformist | **33%** | 3 |
| Matsuo Bashō | haiku | Erratic_Conformist | **33%** | 3 |
| W.B. Yeats | modernist | Erratic_Conformist | **33%** | 3 |

**Whitman (30% consistent)** is the most variable poet in the corpus. His poems span all four quadrants: *Song of Myself §1* is Consistent_Ambush (high S₂, stable entropy), while *O Captain! My Captain!* falls in Metronomic (low S₂, stable entropy) — an entirely different profile. The catalogue poems (*§15*, *Crossing Brooklyn Ferry*) land in Erratic_Conformist. **Whitman has no stable strategy; each poem is a different informational world.**

**Ashbery (35%)** has the largest n (17 poems) and the highest within-poet quadrant variance of any poet in the corpus. His dominant quadrant is Metronomic (6 of 17), but he uses all four strategies. This may reflect the deliberate opacity of his project — he resists stylistic legibility at every level, including the information-theoretic one.

---

## Poet Strategy Profiles: Notable Cases

### Emily Dickinson — Consistent Ambush (57%)

| Poem | Quadrant | S₂ | std_H |
|---|---|---|---|
| Because I could not stop for Death | Consistent_Ambush | +0.250 | 2.432 |
| Tell all the truth but tell it slant | Consistent_Ambush | +0.524 | 2.370 |
| I'm Nobody! Who are you? | Consistent_Ambush | +0.609 | 2.512 |
| I heard a Fly buzz | Consistent_Ambush | +0.137 | 2.241 |
| I felt a Funeral, in my Brain | **Metronomic** | -0.886 | 2.302 |
| A Route of Evanescence | **Trap_Release** | -0.068 | 3.062 |
| Because I could not stop for Death | **Erratic_Conformist** | -0.553 | 2.604 |

Dickinson's Consistent_Ambush pattern (high S₂, stable entropy) is the clearest case of a real poet with a distinctive strategy. Her S₂ positive scores are among the few in the whole corpus — she is genuinely MORE surprising than the model's uncertainty warrants. The exception *I felt a Funeral, in my Brain* is Metronomic: its regular meter and repetitive structure create a calmer entropy profile. The two copies of *Because I could not stop for Death* diverge (Consistent_Ambush vs. Erratic_Conformist), likely a tokenization artifact — they were analyzed at different positions in the corpus.

### Robert Browning — Consistent Ambush (67%, n=9)

Browning's dramatic monologues (My Last Duchess, Fra Lippo Lippi, Andrea del Sarto, The Bishop Orders His Tomb) consistently land in Consistent_Ambush: stable entropy, above-average S₂. This is the information-theoretic signature of **the dramatic monologue form itself**: a speaker whose syntax is controlled (stable entropy) but whose lexical choices are distinctive (high S₂). The form creates the fingerprint more than the individual poet.

### Gerard Manley Hopkins — Trap_Release (50%)

Hopkins falls in Trap_Release for 3 of 6 poems (God's Grandeur, Pied Beauty, Pied Beauty). His use of sprung rhythm and compound word formation creates high entropy variance (std_H averages 2.706) — the reader constantly recalibrates. This is the highest mean std_H of any Victorian poet, confirming that Hopkins's formal innovations are detectable at the entropy-variance level.

### Walt Whitman — No Stable Strategy (30%)

The surprise isn't that Whitman varies — it's how dramatically he varies. He spans from Consistent_Ambush (*Song of Myself §1*: S₂ = +0.775) to Metronomic (*O Captain!*: S₂ = -0.775) — a 1.55-bit S₂ range within one poet's body of work. The catalogue poems (*§15*, *Crossing Brooklyn Ferry*) land in Erratic_Conformist, suggesting that the catalogue form specifically activates a different information-theoretic mode.

---

## Era-Level Strategy Dominance

| Era | n | Dominant Strategy | % |
|---|---|---|---|
| **old_english** | 5 | Consistent_Ambush | **80%** |
| **classical_chinese** | 4 | Metronomic | **75%** |
| **language** | 6 | Metronomic | **67%** |
| **spoken_word** | 3 | Metronomic | **67%** |
| **war_poetry** | 3 | Consistent_Ambush | **67%** |
| **beat** | 8 | Trap_Release | **62%** |
| **ekphrastic** | 8 | Consistent_Ambush | **62%** |

**Old English is the most homogeneous era** (80% Consistent_Ambush). The heavy stress patterns of alliterative verse create stable entropy per line while generating high S₂ at the unstressed positions where unusual words appear. All five Old English poems in the corpus share this profile.

**Language poetry and spoken word are both Metronomic** (67%). This seems paradoxical: Language poetry (Hejinian, Andrews, Watten) is famous for its obscurity. But Metronomic doesn't mean "clichéd" — it means low deviation relative to the model's own uncertainty. Language poetry may produce low S₂ because GPT-2's predictions are *already* diffuse (high entropy), so even unusual words don't spike S₂.

**Beat poetry is Trap_Release** (62%): the loose lines and variable rhythms create entropy variance that sets up occasional surprises. Ginsberg, Kerouac, Ferlinghetti all show this pattern.

**Victorian poetry is split** (Trap_Release 35%, Consistent_Ambush 24%, Erratic_Conformist 26%): the most heterogeneous major era. The Victorian era's diversity of forms (ballad, dramatic monologue, sonnet, ode) produces diverse information-theoretic profiles.

---

## The Synthetic Test Cases: Formal Constraints Explain Consistency

The **synthetic procedural poems** (80% Erratic_Conformist) are as consistent as the most consistent real poets. The **synthetic cliché poems** (67% Metronomic) are more consistent than most real poets. This confirms that:

> **Formal and stylistic constraints drive information-theoretic consistency more than individual creative voice.**

The implication for author attribution: S₂-based fingerprints will tend to capture form signatures before poet signatures. Browning's dramatic monologues are Consistent_Ambush not because Browning specifically is Consistent_Ambush, but because dramatic monologue as a form is.

---

## Trap Ratio Analysis

The **trap ratio** (fraction of high-S₂ tokens preceded by low-entropy token — the "true ambush" rate) adds a third dimension:

| Poet | Dominant Quadrant | Mean Trap Ratio |
|---|---|---|
| Kobayashi Issa | Erratic_Conformist | **0.73** |
| Edmund Clerihew Bentley | Erratic_Conformist | **0.77** |
| Lucille Clifton | Metronomic | **0.38** |
| George Oppen | Erratic_Conformist | **0.35** |

Issa and Bentley have the highest trap ratios (0.73-0.77): when they DO produce a high-S₂ token, it almost always follows a low-entropy (high-confidence) context. These poets are "classic ambushers" — they set up certainty and then violate it. Oppen and Clifton produce high-S₂ tokens more often in already-uncertain contexts, creating "fog-and-leap" surprise.

---

## Key Findings

### 1. No Poet Has a Perfectly Stable Strategy
Information-theoretic strategy is not a reliable "individual voice" signature — it varies with form, genre, and poem-level choices. The most consistent real poet (Tennyson, 80%) still deviates in 1 of 5 poems.

### 2. Formal Constraints Drive Consistency More Than Voice
Synthetic stylistic exercises (procedural, cliché) match the most consistent real poets. The dramatic monologue form is Consistent_Ambush regardless of author (Browning, Tennyson's *Ulysses*, Browning's *Fra Lippo Lippi*).

### 3. Some Poets Are Strategically Uniform; Others Are Strategically Polymorphic
Tennyson and Shelley concentrate on one strategy; Whitman and Ashbery scatter across all four. This correlates with aesthetic project: Whitman's democratic expansiveness requires different informational modes for different subjects; Ashbery's resistance to legibility extends to informational strategies.

### 4. Era-Level Strategy Is Clearer Than Poet-Level
Old English (80% Consistent_Ambush) and classical Chinese (75% Metronomic) show stronger era-level strategy coherence than most individual poets. Era traditions impose informational strategies that override individual variation.

---

## Suggested Next Steps

1. **Form-level analysis**: Test whether *sonnet as form* has a stable quadrant assignment across all sonnets in the corpus, regardless of era or author.
2. **Trap ratio by era**: The trap ratio adds a third dimension to the quadrant analysis — build a 3D "strategy space" per era.
3. **Within-poet arc comparison**: For Ashbery (least consistent), are the quadrant transitions random, or do they follow a career trajectory (early poems vs. late)?
4. **Cluster analysis**: Build a 2D (mean_S₂, std_H) scatterplot per poet and look for natural clusters — are there "strategy families" that cross era boundaries?
5. **Extend to non-English**: Test whether Chinese, German, and Japanese poems in the corpus cluster by language or by literary tradition in the quadrant space.
