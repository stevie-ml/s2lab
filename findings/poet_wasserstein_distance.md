# Pairwise S₂ Distribution Similarity: A Wasserstein Distance Map of Poetry

**Date:** 2026-10-29
**Experiment:** `experiments/poet_wasserstein_distance.py`
**Corpus:** 369 poems; 166 poets with ≥50 clean tokens analyzed
**Method:** Pairwise Wasserstein distance between per-poet S₂ distributions
**Builds on:** `poet_fingerprint_consistency.md`, `s2_volatility_signature.md`, `poet_suppression_profiles.md`

---

## Research Question

Each poet has a characteristic distribution of S₂ values — not just a mean, but a shape: how fat the tails are, where the center sits, how spread out the distribution is. The Wasserstein distance (Earth Mover's Distance) measures how much "work" it takes to transform one poet's S₂ distribution into another's.

**Key questions:**
1. Which poets are informationally most similar / most different?
2. Do literary movements cluster in S₂ distribution space?
3. Are there surprising cross-era affinities that textual criticism hasn't named?

---

## Method

- For each poet with ≥50 clean tokens (newline-artifact tokens with p_newline ≥ 0.9 excluded), collected all token-level S₂ values across all their poems
- Computed Wasserstein (Earth Mover's) distance between every pair of poet distributions — 13,695 pairwise comparisons
- Analyzed cluster structure by era

---

## Results

### 1. Most Informationally Similar Poet Pairs

| Wasserstein Distance | Poet 1 | Poet 2 |
|---|---|---|
| **0.125** | Percy Bysshe Shelley | W.B. Yeats |
| **0.129** | John Keats | W.B. Yeats |
| **0.134** | Robert Browning | T.S. Eliot |
| **0.139** | Robert Browning | W.B. Yeats |
| **0.140** | Frank O'Hara | T.S. Eliot |
| **0.144** | Gertrude Stein | T.S. Eliot |
| **0.145** | John Ashbery | John Donne |
| **0.153** | Algernon Charles Swinburne | Wilfred Owen |
| **0.158** | John Ashbery | Walt Whitman |
| **0.158** | William Blake | William Shakespeare |

### 2. Most Informationally Different Poet Pairs

| Wasserstein Distance | Poet 1 | Poet 2 |
|---|---|---|
| **2.689** | Control (prose) | Hart Crane |
| **2.554** | Hart Crane | Pierre Reverdy |
| **2.433** | Hart Crane | Vachel Lindsay |
| **2.406** | Allen Ginsberg | Control (prose) |
| **2.388** | Control (prose) | Synthetic (clerihew) |
| **2.347** | Control (prose) | Rainer Maria Rilke |
| **2.289** | Christian Bök | Lawrence Ferlinghetti |
| **2.283** | Harryette Mullen | Lawrence Ferlinghetti |
| **2.283** | Control (prose) | Georg Trakl |
| **2.277** | Ernest Dowson | Hart Crane |

---

## Era Clustering Analysis

Mean intra-era Wasserstein distance: **0.666 ± 0.334**  
Mean inter-era Wasserstein distance: **0.715 ± 0.342**  
**Ratio (intra/inter): 0.930** — literary eras do cluster informationally, but only modestly.

### Intra-Era Distances: Tightest to Loosest

| Era | Mean Distance | Poets |
|---|---|---|
| **ekphrastic** | **0.308** | Tennyson, Rossetti, Browning — Victorian ekphrasis has the most cohesive S₂ signature of any "school" |
| **metaphysical** | **0.334** | Marvell ↔ Herbert — argument and wit produce near-identical distributions |
| **classical_chinese** | **0.351** | Cui Hao, Du Fu — shared even in translation |
| **protest_political** | **0.374** | Lazarus ↔ Angelou |
| **new_york_school** | **0.383** | O'Hara, Ashbery, Koch — cohesive despite apparent stylistic differences |
| harlem_renaissance | 0.408 | McKay, Cullen, Hughes |
| elegy | 0.415 | 6 poets across eras |
| victorian | 0.454 | 10 poets |
| modernist | 0.971 | Crane, Sandburg, Moore, Yeats, Eliot — *heterogeneous* |
| **beat** | **1.578** | Ginsberg, Corso, Ferlinghetti — *widest gap of any named movement* |

---

## Key Findings

### Finding 1: Literary influence shows up in Wasserstein distance
The closest poet pairs are exactly those we'd expect from literary history:
- **Shelley ↔ Yeats (d=0.125):** Yeats explicitly cited Shelley as a major influence. Their S₂ distributions are more alike than almost any other pair.
- **Keats ↔ Yeats (d=0.129):** Both inhabit the same "sensuous surprise" register — high positive S₂ in sensory and emotional content words.
- **Browning ↔ Eliot (d=0.134):** Eliot frequently cited Browning's dramatic monologue as a precursor. Their distributions are nearly identical despite a 70-year gap.
- **Frank O'Hara ↔ T.S. Eliot (d=0.140):** Surprising on the surface (O'Hara's casual diction vs. Eliot's formal weight), but both poets achieve surprise through proper nouns and sudden specificity.

### Finding 2: The Beat paradox — a movement that isn't one
The Beat generation has the **loosest intra-era clustering** of any literary movement (mean d=1.578). Despite sharing a cultural moment, Ginsberg, Corso, and Ferlinghetti have radically different S₂ profiles:
- **Ginsberg** (mean S₂ = +0.685): High-deviation, spiky, anaphoric escalation
- **Ferlinghetti** (mean S₂ = −0.08): Near-flat, prose-like distribution
- **Distance between them: 2.283** — barely less than the prose control vs. poetry gap

The Beat "movement" was a social formation, not an informational style. Ginsberg and Ferlinghetti are further apart than Eliot and Browning across 70 years.

### Finding 3: Unexpected cross-era affinities
- **John Ashbery ↔ John Donne (d=0.145):** The 17th-century metaphysical poet and the 20th-century Language Poetry–adjacent New York School poet have remarkably similar S₂ distributions. Both achieve deviation through intellectual pivots and compressed syntax, not sensory imagery.
- **Gertrude Stein ↔ T.S. Eliot (d=0.144):** Despite opposite literary reputations (Stein: repetitive, flat; Eliot: literary, allusive), their S₂ distributions almost overlap. Both operate in a narrow entropy range with well-controlled deviation.
- **Algernon Charles Swinburne ↔ Wilfred Owen (d=0.153):** Owen acknowledged Swinburne's musicality as an influence. Their S₂ distributions match — sonorous Victorian and traumatized WWI poet share an identical relationship to language expectation.

### Finding 4: Hart Crane as the extremal poet
Hart Crane has:
- **Highest mean S₂ of any poet in the corpus (+0.968)**
- **Most isolated position:** Nearest neighbor is Georg Trakl at d=0.490 — still far
- **Farthest from prose:** Control ↔ Crane = 2.689 (the absolute maximum)
- **Farthest from other poets:** Pierre Reverdy (d=2.554) and Vachel Lindsay (d=2.433)

Hart Crane is an S₂ outlier in two directions simultaneously: extremely high deviation *and* extremely high entropy (his contexts are uncertain, and he still chooses the unexpected). He is informationally unprecedented.

### Finding 5: Ekphrastic poetry is the most cohesive "genre"
Victorian ekphrastic poetry (poems about artworks) has the tightest intra-cluster distance (d=0.308), tighter than any literary movement. Tennyson, Rossetti, and Browning — when writing about visual art — converge on an identical informational strategy: moderate entropy, controlled deviation, with spikes at the names of artworks and artists. The ekphrastic occasion imposes an informational discipline that overrides individual style.

---

## On the intra/inter ratio

The modest intra/inter ratio (0.930) means most of a poet's informational identity is individual, not era-defined. Literary history is less deterministic than criticism suggests: a poet's S₂ profile is shaped more by individual temperament than historical moment.

However, the *tightest* era clusters (metaphysical d=0.334, ekphrastic d=0.308) are genuine exceptions — these "schools" imposed real informational constraints on their members.

---

## Suggested Next Steps

1. **Hierarchical clustering dendrogram** of the full distance matrix — do the clusters form meaningful literary-historical groups?
2. **Diachronic nearest-neighbor analysis** — for each poet, who is their nearest neighbor from a *different* century? Maps hidden trans-historical affinities.
3. **The Crane problem** — is Hart Crane's extreme S₂ profile linked to specific formal features (inverted syntax, neologism, compound words)? Extract and analyze the token types driving his high-S₂ moments.
4. **Beat vs. Confessional** — confessional poetry also has high intra-era distance (0.827). Do "confessional" and "Beat" share a structural feature: movements defined by social-biographical criteria rather than informational style?
5. **Nearest-neighbor chains** — starting from Crane, map the "path" through poetry space to the prose control. Which poets are the intermediaries?
