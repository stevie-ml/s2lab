# Deixis and S₂: The Poetics of Pointing

**Date:** 2026-09-13
**Experiment:** `experiments/deixis_s2.py`
**Corpus:** 106 English-language texts from `results/corpus_results.json`
**Research question:** Do deictic "pointing words" — here, now, this, that — carry distinctive information-theoretic signatures? And do they open high-entropy windows that poets fill with surprising choices?

---

## Background

Deixis names the class of expressions that anchor meaning to the context of utterance:
- **Temporal**: now, then, today, tonight, yesterday, tomorrow, once, again, still, yet, never, ever
- **Spatial**: here, there, yonder, hence, hither
- **Demonstrative**: this, that, these, those

Poetry famously exploits deictic language to create **lyric immediacy** — the sense that the poem is happening NOW, HERE, to THIS speaker. "Now more than ever seems it rich to die" (Keats), "Here is the place; right here" (Williams). Literary scholars call this the "lyric present" — the paradox that a poem written centuries ago can still speak in the present tense.

GPT-2 is trained on prose that also uses deixis, but in anchored contexts (news articles, web writing). Does poetry's *rhetorical* deixis — pointing at moments of existential weight — produce different S₂ signatures than prose deixis?

---

## Method

1. Classify all tokens by deictic category (temporal / spatial / demonstrative)
2. Measure S₂ at deictic tokens and at the following token (post-deictic)
3. Compute poem-level deictic density and correlate with mean S₂
4. Identify the highest-S₂ individual deictic moments

---

## Key Results

### 1. Deictic Tokens vs. Control

| Category | n | mean S₂ | median S₂ | pos% | max S₂ |
|---|---|---|---|---|---|
| **Temporal** (now, tonight, never…) | 96 | **+0.997** | +0.710 | **57.3%** | 19.72 |
| **Spatial** (here, there, yonder…) | 33 | **+1.313** | −0.124 | 48.5% | 16.52 |
| **Demonstrative** (this, that, these…) | 132 | **+1.014** | −0.520 | 43.2% | 25.44 |
| Control (all non-deictic alpha tokens) | 5,591 | +1.012 | −0.211 | 47.2% | 38.55 |

**Overall deictic S₂ matches the control baseline** (≈+1.0), but with striking internal heterogeneity. The mean hides a wide spread: some deictic tokens are highly surprising, others are deeply predictable.

**The surprise is in the positive-percentage:** Temporal deictics are positive-S₂ 57% of the time — the highest of any group, including the control baseline. When the model expected something else and the poet wrote "now" or "tonight," that choice registered as genuinely surprising.

### 2. Per-Token Breakdown (n ≥ 3)

| Token | Category | n | mean S₂ | pos% |
|---|---|---|---|---|
| **tonight** | temporal | 3 | **+4.988** | **100%** |
| **after** | temporal | 4 | **+2.814** | 75% |
| **those** | demonstrative | 8 | **+2.653** | 88% |
| **again** | temporal | 11 | **+2.107** | 82% |
| **still** | temporal | 8 | **+1.968** | 63% |
| **yet** | temporal | 12 | **+1.890** | 67% |
| **these** | demonstrative | 11 | **+1.506** | 73% |
| **this** | demonstrative | 28 | +1.293 | 43% |
| **soon** | temporal | 5 | +1.207 | 40% |
| **there** | spatial | 24 | +0.948 | 46% |
| **now** | temporal | 5 | +0.899 | 60% |
| **here** | spatial | 6 | +0.844 | 50% |
| **that** | demonstrative | 85 | +0.705 | 35% |
| **then** | temporal | 20 | +0.615 | 60% |
| — | — | — | — | — |
| **never** | temporal | 10 | **−1.035** | 30% |
| **ever** | temporal | 4 | **−2.226** | 25% |
| **once** | temporal | 3 | **−3.210** | **0%** |

**The gradient of temporal deixis reveals a taxonomy of poetic time:**

- **"Tonight"** (mean S₂ = +4.99): 100% positive, the most surprising deictic. Every deployment of "tonight" in the corpus was more unexpected than the context predicted. Poets use "tonight" for charged, singular moments — it marks **the night of consequence**, and GPT-2 finds it surprising at nearly every turn.
- **"Once"** (mean S₂ = −3.21): 0% positive. "Once" announces the fairy-tale or historical anecdote — it is a *narrative formula* that GPT-2 has seen thousands of times. It is the most predictable word in the deictic lexicon. The poet who writes "once" is invoking distance, not immediacy.
- **"Never"** (mean S₂ = −1.04): Also below baseline. "Never" is a strongly marked word in idiomatic English — frequent in emphatic negative constructions — which GPT-2 predicts readily in many contexts.

**The insight:** Poetic deixis has two registers, *proximity* vs. *distance*. Proximity markers ("tonight," "again," "still," "yet") are high-S₂; distance markers ("once," "never," "ever") are low-S₂. The poem's "lyric now" is genuinely surprising to the model; the "storied then" is expected.

### 3. Post-Deictic S₂: What Follows a Pointer?

| Category | n | post mean S₂ | post median | mean entropy after deictic |
|---|---|---|---|---|
| **Demonstrative** | 132 | **+0.010** | −0.357 | **8.371 nats** |
| Spatial | 33 | −0.188 | −0.759 | 4.884 nats |
| Temporal | 96 | −0.659 | −1.378 | 6.203 nats |

**After demonstratives, GPT-2 opens its widest window** (entropy = 8.37 nats — one of the highest values in the corpus). "This" and "that" point at something: the referent could be any noun, and the model knows it. The context is maximally open.

Yet post-demonstrative S₂ is near zero (+0.010). Despite the wide-open window, poets fill it with expected words. The demonstrative creates **the appearance of specificity** — "this rose," "that moment" — but the noun following it is precisely what the model predicted in an open context.

**Contrast**: after temporal deictics, post-token S₂ drops to −0.659. "Now I lay me down," "then she wept," "still waters run" — the verb or continuation after a temporal deictic is strongly constrained. Time-words set up highly predictable completions.

**Spatial deictics** ("here," "there") sit in between: medium entropy, near-zero post-S₂.

### 4. Top Deictic S₂ Moments

| S₂ | Token | Author | Poem | Category |
|---|---|---|---|---|
| **+25.44** | "that" | E.E. Cummings | "anyone lived in a pretty how town" | demonstrative |
| **+24.51** | "that" | Traditional | "The Wife of Usher's Well" | demonstrative |
| **+20.98** | "that" | Traditional | "The Wife of Usher's Well" | demonstrative |
| **+20.80** | "this" | Traditional | "Sir Patrick Spens" | demonstrative |
| **+20.77** | "this" | Layli Long Soldier | "Whereas (excerpt)" | demonstrative |
| **+19.72** | "yet" | Robert Frost | "The Road Not Taken" | temporal |
| **+19.00** | "that" | John Ashbery | "Paradoxes and Oxymorons" | demonstrative |
| **+16.74** | "that" | Wordsworth | "I Wandered Lonely as a Cloud" | demonstrative |
| **+16.52** | "there" | Traditional | "Barbara Allen" | spatial |
| **+13.72** | "that" | Robert Burns | "A Red, Red Rose" | demonstrative |

**Demonstratives dominate the top-S₂ deictic list.** The reason: "this" and "that" frequently appear in **line-initial position** — the highest-S₂ structural position in the corpus (avg initial S₂ = +5.57, see `line_position_analysis.md`). When a poet begins a line with "That" or "This," the model (which strongly predicted a newline or whitespace continuation) is caught off-guard.

The Cummings peak (+25.44) reflects his grammatical inversions — "anyone" used as a name, "that" appearing in syntactically anomalous positions.

Long Soldier's "Whereas" uses "this" as a legal-document cataphoric pointer ("Whereas this resolution") — the demonstrative here is institutional deixis repurposed for lyric witness.

### 5. Poem-Level: Deictic Density vs. Mean S₂

| Deictic Density | n poems | avg density | avg poem S₂ |
|---|---|---|---|
| Low tercile | 35 | 0.004 | **+0.243** |
| **Mid tercile** | 35 | 0.019 | **+0.477** |
| High tercile | 36 | 0.047 | **+0.097** |

**A non-linear relationship**: moderate deictic use (mid-tercile) correlates with the highest mean S₂ (+0.477). Both low-deictic and high-deictic poems have lower mean S₂.

Interpretation:
- **Low deictic** poems (Ginsberg's "Howl," Whitman's "Song of Myself," Williams's "The Red Wheelbarrow"): these are often maximally "present" without pointing — they don't need to say "now" because the entire poem IS now. This is the "enacted" lyric present, not the "declared" one. These poems often have high S₂ for other reasons (vocabulary, lineation).
- **High deictic** poems (Marianne Moore's "Poetry," Ashbery's "The Painter," Tennyson's "Ulysses"): heavy deictic density correlates with lower mean S₂. When a poet points *too much*, each pointing word is expected — the deictic becomes a verbal tic rather than an existential gesture.
- **Mid-range** poems (Frost's "The Road Not Taken," Burns's ballads, Millay's sonnets): balanced deixis that serves genuine contrast ("two roads diverged... yet knowing how way leads on to way").

### 6. Era-Level Deictic Density

| Era | n | avg density | avg poem S₂ |
|---|---|---|---|
| Victorian | 13 | **0.035** | +0.337 |
| Mid-century | 3 | 0.033 | +0.871 |
| New York School | 18 | 0.025 | −0.179 |
| Romantic | 9 | 0.023 | +0.171 |
| Modernist | 18 | 0.021 | +0.370 |
| 19th century | 9 | 0.018 | +0.393 |
| Ballad | 6 | 0.019 | +0.814 |
| Confessional | 3 | 0.010 | +0.534 |
| **Beat** | 2 | **0.005** | +1.031 |
| **Surrealist** | 1 | **0.000** | −0.328 |

**Victorian poetry has the highest deictic density** (0.035): dramatic monologue ("My Last Duchess," "Ulysses") and narrative poetry use "there," "that," "this" as narrative scaffolding. Browning's and Tennyson's speakers are *placed* in scenes.

**Beat poetry (Ginsberg/Kerouac) has near-zero deictic density** despite high S₂. The Beat poem unfolds in a continuous present-tense accumulation — it doesn't need to say "here" because each line enacts presence. The deixis is embodied in the catalogue structure itself.

**Confessional poetry** (Plath, Sexton, Lowell) also has low deictic density despite having among the highest mean S₂. Confessional poems are about interiority, not pointing — the "I" is already situated without needing spatial or temporal flags.

---

## Summary of Findings

1. **"Tonight" is the most surprising deictic** (S₂ = +4.99, 100% positive). It marks the charged singular night — GPT-2 is always surprised when a poet reaches for it.

2. **"Once" is the most predictable deictic** (S₂ = −3.21, 0% positive). The fairy-tale opener is so formulaic that the model expects it fully.

3. **Demonstratives open wider windows than any other deictic** (entropy = 8.37 nats after "this/that") — but what follows is predictable. The demonstrative creates *apparent* specificity; the noun it points to is what the model expected.

4. **Temporal deictics drive the positive-S₂ surplus** in deictic language: 57.3% positive, above the baseline. Poets deploy temporal deictics at moments of genuine significance, making them locally surprising.

5. **Moderate deictic density maximizes poem-level S₂**. Too little pointing = the poet enacts presence without declaring it (Ginsberg, Williams). Too much pointing = the deictic becomes expected and cheap.

6. **Victorian poems use deixis most; Beat poems use it least** — despite Beat having higher average S₂. The Beat lyric is enacted presence; the Victorian dramatic monologue is narrated presence.

---

## Hypothesis for Next Steps

1. **Cross-category: deictic + high-S₂ tokens**: Are poems that use "tonight" (high-S₂ deictic) also the ones with the highest surrounding S₂? Or is the high-S₂ deictic token an *isolated* spike in an otherwise predictable poem?

2. **Deictic + punctuation**: Do deictic words followed by exclamation marks or colons ("Here!"; "Now:") have higher S₂ than bare deictic tokens? The punctuation reinforces the pointing gesture.

3. **"Now" in the final line**: Is there a structural preference for temporal deictics in final positions (closural "now")? This connects to `closure_tokens_analysis.md`.

4. **Expand corpus**: Add poems specifically chosen for extreme deictic use — Celan's spatial deictics, O'Hara's urban "here/now," or Oppen's objectivist pointing — to stress-test the high-density hypothesis.
