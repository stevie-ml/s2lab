# S₂ Scaling with Poem Length: A Power-Law Analysis

**Date:** 2026-11-01  
**Corpus:** 387 English-language poems (artifact-filtered), 10–674 tokens  
**Question:** Does poetic surprise accumulate linearly with poem length, or are there diminishing returns?

---

## Background

If S₂ represents the poet's "surprise budget" — the total deviation from expectation — we can ask whether that budget scales with poem length. Three possible regimes:

- **α ≈ 1 (linear)**: Longer poems simply accumulate surprise at a constant rate per token  
- **α < 1 (sub-linear)**: Diminishing returns — longer poems become more conventional per token  
- **α > 1 (super-linear)**: Longer poems concentrate more surprise per token (accumulating momentum)

We fit a power law: `total_pos_S₂ ~ length^α` across 387 poems.

---

## Main Findings

### 1. Near-Linear Scaling at the Corpus Level

| Metric | Value |
|--------|-------|
| Scaling exponent α | **0.979** |
| Fit quality R² | **0.81** |
| Interpretation | Sub-linear, but marginally (α nearly 1) |

**Finding:** Total positive S₂ scales almost linearly with poem length. The R² = 0.81 is high, indicating poem length alone explains ~81% of variance in total surprise. The slight sub-linearity (α < 1) suggests a mild diminishing returns effect.

### 2. S₂ Per Token Is Length-Independent

| Metric | Value |
|--------|-------|
| Per-token scaling α | **0.002** |
| Per-token R² | **0.0001** |

**Finding:** Average S₂ per token has essentially zero correlation with poem length. The information density of a poem is not a function of its length — poets maintain roughly constant surprise density whether writing haiku or epic excerpts.

### 3. Short Poems Have Higher S₂ Density

Despite the per-token correlation being flat overall, the extremes tell a different story:

| Group | Avg Length | Avg S₂/token | Pos-S₂ Ratio | Gini |
|-------|-----------|-------------|-------------|------|
| Shortest 20 poems | 18 tokens | **+0.18** | 39.4% | 0.42 |
| Longest 20 poems | 424 tokens | **-0.43** | 32.4% | 0.44 |

The shortest poems in the corpus achieve **positive** average S₂ — they surprise GPT-2 more often than not, on a per-token basis. The longest poems are uniformly sub-baseline. This gap (+0.18 vs -0.43 = 0.61 bits) is substantial.

**Interpretation:** Short poems can sustain high surprise density throughout because they consist almost entirely of carefully chosen words. Long poems necessarily contain more conventional connective tissue. The constraint of brevity concentrates surprise.

### 4. Length-Bin Analysis: Maximum S₂ Grows, Average Stays Flat

| Length Range | n | Avg S₂/token | +S₂ Ratio | Max S₂ | Gini |
|---|---|---|---|---|---|
| 13–53 tokens | 79 | -0.38 | 35.4% | 9.7 | 0.387 |
| 53–97 tokens | 82 | -0.33 | 36.4% | 12.3 | 0.399 |
| 97–133 tokens | 77 | -0.48 | 32.6% | 12.0 | 0.395 |
| 133–178 tokens | 77 | -0.41 | 34.5% | 13.0 | 0.404 |
| 178–674 tokens | 78 | -0.43 | 32.3% | 16.0 | 0.423 |

Two trends as poems lengthen:
- **Max S₂ increases** (9.7 → 16.0): Longer poems achieve higher peak surprises — more extreme "Straussian gap" moments
- **Gini increases** (0.387 → 0.423): Surprise becomes more *unequally distributed* — longer poems concentrate their surprise in fewer extreme events

This implies a structural shift: short poems distribute surprise broadly; long poems concentrate it in rare spikes.

### 5. Form-Dependent Scaling: Super-Linear vs Sub-Linear Eras

| Era | n | α | R² | Avg S₂ | Interpretation |
|---|---|---|---|---|---|
| **Double dactyl** | 5 | -1.37 | 0.05 | -0.95 | Longer ones LESS surprising |
| **Spoken word** | 3 | -1.14 | 0.84 | -0.58 | Strong negative scaling |
| **Ballad** | 6 | 0.20 | 0.04 | -0.39 | Weak linear |
| **Song lyrics** | 3 | 0.32 | 0.98 | -0.64 | Verse-chorus repetition dampens |
| **Beat** | 6 | 0.34 | 0.80 | +0.28 | Sub-linear but high overall |
| **Victorian** | 29 | 0.89 | 0.67 | -0.29 | Near-linear |
| **Modernist** | 27 | 1.09 | 0.87 | -0.43 | Near-linear |
| **Romantic** | 21 | 1.13 | 0.91 | -0.50 | Slightly super-linear |
| **Confessional** | 6 | 1.40 | 0.83 | -0.30 | Super-linear |
| **Postcolonial** | 6 | 1.56 | 0.94 | -0.50 | **Super-linear** |
| **Harlem Renaissance** | 7 | 1.61 | 0.98 | -0.46 | **Super-linear** |
| **Ancient** | 3 | 1.47 | 1.00 | -0.19 | **Super-linear** |
| **Villanelle** | 3 | 2.13 | 0.71 | -0.57 | **Super-linear** |

**Most striking:** Harlem Renaissance (α=1.61, R²=0.98) and Postcolonial (α=1.56, R²=0.94) show *strong super-linear scaling* — these traditions accumulate disproportionately more surprise in longer poems, with excellent fit. This may reflect these traditions' rhetorical architecture: longer poems build cumulative rhetorical force.

**Villanelle** (α=2.13): The repeating-line structure of the villanelle creates super-linear surprise — each return of the refrain gains S₂ relative to the initial occurrence, because the context has shifted.

**Spoken word** (α=-1.14): The one tradition with strongly *negative* scaling — a performance-oriented form that depends on rhythmic predictability, and longer works become more, not less, conventional.

---

## Synthesis: Three Structural Types

From the scaling exponent, we can classify poetic traditions:

| Type | α range | Surprise structure | Examples |
|------|---------|-------------------|---------|
| **Density-focused** | α < 0 | Longer = less surprising | Double dactyl, Spoken word |
| **Constant-density** | 0.8 < α < 1.2 | Consistent S₂ per token | Victorian, Modernist, 19th century |
| **Accumulative** | α > 1.2 | Longer = more surprising per token | Harlem Renaissance, Postcolonial, Villanelle, Ancient |

The "accumulative" cluster is the most interesting: these traditions build *rhetorical momentum* through length, rather than spreading surprise evenly.

---

## Key Finding

**Poetic surprise scales near-linearly with poem length (α=0.98, R²=0.81), but with a critical asymmetry: short poems achieve higher per-token surprise through concentration, while long poems achieve higher maximum single-token surprises through scope. The scaling exponent varies systematically by tradition, with Harlem Renaissance and postcolonial poetry showing super-linear accumulation, and spoken word showing inverse scaling.**

---

## Suggested Next Steps

1. **Rhetorical momentum analysis**: For super-linear eras (Harlem Renaissance, postcolonial), identify the structural mechanism — is it anaphora, escalating catalog, turn-and-return, or something else?
2. **Optimal poem length**: Is there an L* (optimal length) that maximizes total surprise per token? The data hints at 50–100 tokens as a sweet spot.
3. **Per-stanza scaling**: Within long poems, does each stanza restart the scaling clock, or does surprise accumulate continuously?
4. **Controlled comparison**: Take long poems and compare excerpts (first N tokens) to short poems of length N — does the short-poem advantage persist when length is held constant?
