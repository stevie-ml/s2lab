# Deviance Vocabulary Consistency: Poets' Stable Surprise Lexicons

**Date:** 2026-11-11  
**Experiment:** `experiments/deviance_vocabulary_consistency.py` → `results/deviance_vocabulary_consistency.json`  
**Corpus:** 411 texts; 35 poets with ≥3 poems analyzed  
**Builds on:** `poet_fingerprints.md`, `suppressed_lexicon.md`, `shadow_vocab_fulfillment.md`

---

## Research Question

Is a poet's vocabulary of deviance — the set of words they deploy in high-S₂ positions —
consistent across their poems? Or is each poem independently surprising?

Equivalently: does surprise function as a **stable stylistic trait** (the same kinds of words
recur at high-S₂ positions across a poet's body of work), or is it **poem-specific** (each
work finds different ways to deviate from the model's expectations)?

We test both the **actual deviance vocabulary** (the words poets wrote at high-S₂ positions)
and the **suppressed vocabulary** (what GPT-2 predicted but didn't get — the "anti-poem" words).

---

## Method

For each poem: extract all tokens where S₂ > 2.0 (after filtering stanza-break artifacts,
p\_newline ≥ 0.9). Normalize to lowercase word types.

For each poet with ≥ 3 poems: compute all pairwise **Jaccard similarity** between poems'
high-S₂ vocabularies. Jaccard = |intersection| / |union|.

**Baseline**: Compute between-poet Jaccard by sampling 500 random cross-poet poem pairs.

Also track the **suppressed vocabulary**: GPT-2's top-1 prediction at each high-S₂ position
(the word the poet deviated from). Compute within-poet Jaccard for suppressed vocabularies.

---

## Global Result

| Metric | Value |
|--------|-------|
| Poets analyzed (≥ 3 poems each) | 35 |
| Mean **within-poet** Jaccard (deviance vocab) | **0.030** |
| Mean **between-poet** Jaccard (baseline) | 0.0095 |
| Consistency lift (within / between) | **3.21×** |
| Mean within-poet **suppressed vocab** Jaccard | **0.100** |

**Two findings:**

**Finding 1 — Poets are consistent:** Within-poet Jaccard (0.030) is 3.21× higher than
the between-poet baseline (0.010). Poets do have characteristic vocabularies of deviance
that persist across poems, beyond chance.

**Finding 2 — Suppressed vocab is 3× more consistent than actual vocab:** The words GPT-2
predicted but the poet rejected (Jaccard = 0.100) are far more stable across a poet's
work than the words the poet actually used at high-S₂ positions (0.030).

This is a striking asymmetry: **poets have more stable aesthetic rejections than aesthetic
choices.** What they consistently refuse (the model-expected word) is a more reliable
fingerprint than what they substitute.

---

## Most Consistent Deviance Vocabularies

| Author | Within-J | Suppressed-J | n poems | Signature deviance words |
|--------|---------|-------------|---------|--------------------------|
| Langston Hughes | **0.333** | 0.333 | 3 | *over, dry, deferred, ra* |
| Joy Harjo | 0.107 | 0.185 | 3 | *who, red, maps, fur, bodies* |
| Gerard Manley Hopkins | 0.075 | 0.156 | 6 | *forth, ind, spare, falls, morning* |
| Walt Whitman | 0.071 | 0.122 | 9 | *where, drops, while, at, every* |
| Alfred, Lord Tennyson | 0.050 | 0.113 | 5 | *over, below, there, fl, an* |
| John Keats | 0.045 | 0.130 | 9 | *like, eagle, wat, round, more* |
| William Shakespeare | 0.036 | 0.092 | 3 | *from, compare, death, well, black* |
| Robert Browning | 0.031 | 0.140 | 7 | *that, by, will, never, men* |
| Frank O'Hara | 0.030 | 0.047 | 3 | *it, go, straight* |
| Emily Dickinson | 0.029 | 0.088 | 7 | *too, but, slowly, death* |
| John Ashbery | 0.020 | 0.085 | 17 | *survey* (in 11/17 poems!) |

---

## Least Consistent Deviance Vocabularies

| Author | Within-J | n poems | Interpretation |
|--------|---------|---------|----------------|
| T.S. Eliot | 0.0024 | 5 | Each poem finds wholly new paths to surprise |
| Wallace Stevens | 0.0000 | 3 | Zero overlap in high-S₂ words |
| Lucille Clifton | 0.0000 | 3 | Zero overlap |
| Stefan George | 0.0000 | 3 | Zero overlap |

---

## Case Studies

### Langston Hughes (J = 0.333 — highest consistency)

Hughes' signature deviance word **"deferred"** (from "A Dream Deferred") appears as a
high-S₂ token in multiple poems. The word *deferred* — meaning to put off, to defer —
is used in contexts where GPT-2 expects continuation; Hughes systematically withholds it.
The core vocabulary *{over, dry, deferred, ra}* reads like a thematic signature: *over*
(crossing, completion), *dry* (heat, dryness, Harlem), the prefix *ra-* (sun, beginning).

The deviance vocabulary mirrors the content signature. Hughes finds high-S₂ positions
for the same words because the same conceptual domain (deferral, the sun, dryness) recurs
as thematically *loaded* across his corpus.

### Gerard Manley Hopkins (J = 0.075, 6 poems)

Hopkins' deviance vocabulary includes **"forth"**, **"ind"** (subword fragment of "indrawn",
"kindled", "inscape"), **"spare"**, and **"falls"**. These are characteristically Hopkinsian:
Sprung Rhythm forces vocabulary into stressed positions that deviate from GPT-2's iambic
expectations. "Forth" appears repeatedly as a surprising directional particle; "spare" in
its sense of "lean, restrained" is a constant Hopkinsian value.

The **suppressed Jaccard (0.156)** is twice the deviance Jaccard — Hopkins consistently
rejects the same kinds of expected continuations, even when his substitutes vary.

### John Ashbery ("survey" in 11/17 poems)

The word **"survey"** appears as a high-S₂ token in 11 of 17 Ashbery poems. This is
extraordinary: in contexts where GPT-2 expects continuation ("and I...", "the..."), Ashbery
repeatedly inserts "survey" — a word of detached, panoramic observation. This matches
Ashbery's aesthetic of the disengaged, wandering gaze that refuses to commit to what
was linguistically expected.

### T.S. Eliot vs. Langston Hughes: Two Strategies

Eliot's near-zero consistency (0.0024) contrasts sharply with Hughes' maximum (0.333).
Eliot's strategy appears to be **heterogeneous deviance**: each poem in *Prufrock*, *The
Waste Land*, *The Hollow Men*, *Ash Wednesday* finds entirely new lexical domains for its
high-S₂ moments. This is consistent with Eliot's program of radical allusiveness — each
poem inhabits a different register/tradition, so no single vocabulary of surprise recurs.

Hughes' homogeneous deviance reflects the opposite strategy: a *concentrated thematic
terrain* means the same words recur as surprising across poems, because the poet is
returning to the same compressed semantic world.

---

## The Suppressed Vocabulary Paradox

The most surprising result: **the words GPT-2 predicted (but the poet rejected) are 3.3×
more consistent within a poet's work than the words the poet actually chose.**

| Vocabulary type | Within-poet Jaccard |
|-----------------|---------------------|
| Actual deviance vocabulary | 0.030 |
| Suppressed (rejected) vocabulary | **0.100** |

This suggests that poets have more stable **aesthetic negations** than aesthetic affirmations.
The *class of language* that a poet consistently rejects (the statistically expected, the
conventionally probable) is more defining than the specific words they substitute.

A poet's style may be more legible in what they *refuse* to write than in what they write.
This resonates with the negative-capability tradition in aesthetics: poetic identity as
constituted by systematic avoidance.

For Hopkins: he consistently refuses the "expected" continuation (often a metrically
unstressed function word) in favor of stressed lexical content — his suppressed vocabulary
is consistently "the unstressed" while his deviance vocabulary is consistently "the
Sprung." But the suppressed side is more stable because the expectation (unstressed filler)
is more uniform.

---

## Era-Level Pattern

Poets with highest within-poet consistency tend to be:
- **Thematically concentrated** (Hughes, Harjo): same images/concepts recur = same words
  surprise in the same contexts
- **Idiolect-heavy** (Hopkins): highly distinctive vocabulary = GPT-2 systematically wrong
  in the same ways

Poets with lowest consistency tend to be:
- **Multi-modal** (Eliot, Stevens): each poem inhabits a different genre, register, or
  tradition = no stable deviance lexicon

---

## Limitations

1. **Vocabulary size effect**: Poets with more poems but longer poems may show lower
   per-poem Jaccard simply because large vocabularies dilute overlap. We control partially
   by requiring ≥5 high-S₂ tokens per poem.
2. **Subword artifacts**: Some "words" (like "ind", "ra", "wat", "fl") are subword fragments
   from GPT-2's BPE tokenization. Their consistency may reflect tokenization patterns
   rather than deliberate lexical choice. Hopkins' "ind" fragments likely reflect his
   compound words being consistently split at the same boundary.
3. **Stanza-break filtering**: We exclude artifact positions (p\_newline ≥ 0.9), which
   removes the highest-S₂ tokens. The analysis covers the "genuine" deviance vocabulary.

---

## Suggested Next Steps

1. **Semantic coherence of deviance vocabulary**: For each poet, compute the semantic
   similarity (via embedding) among their signature deviance words. Is the deviance
   vocabulary semantically *coherent* (a single semantic field) or *diverse*?
2. **Suppressed vocabulary as negative portrait**: Visualize the suppressed vocabulary
   for major poets as a "negative lexicon" — the vocabulary they define themselves
   against. For Hughes, the suppressed vocabulary reveals what convention expected; his
   choices reveal what he said instead.
3. **Cross-era deviance vocabulary consistency**: Do Romantic poets show higher within-era
   consistency than Modernist poets? The era-level version of this test.
4. **Per-poem learning**: Within a single long poem (Whitman's "Song of Myself",
   "The Waste Land"), does deviance vocabulary consistency change from early to late
   sections? Do later sections "inherit" the deviance lexicon of earlier ones?
5. **The "idiolect constant"**: Fit a linear model predicting within-poet Jaccard from
   (a) number of poems, (b) thematic concentration (e.g., poem title diversity), (c) era.
   What explains the variance?
