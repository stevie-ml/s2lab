# Information Arcs and Poetic Closure: How S₂ Evolves Across a Poem
**Date:** 2026-09-07  
**Experiment:** inline analysis of `results/corpus_results.json`  
**Corpus:** 90 English poems (control prose excluded)

---

## Research Question

Previous work (line_position_analysis.md) showed that *within a line*, S₂ peaks at line-initial position and falls at line-final. But what about the whole poem? Does S₂ rise or fall across the arc from first token to last? Do poems resolve informatively (ending near expectation) or remain open (ending with a spike)?

**Three competing hypotheses:**
- **H-Frontload**: Poems front-load surprise to seize attention, then settle into a world they've established.
- **H-Crescendo**: Poems build toward a revelation, so S₂ rises toward the close.
- **H-Flat**: Poets distribute surprise evenly across the text.

---

## Method

For each poem, tokens were binned into 10 equal deciles (by position as a fraction of total length). Mean S₂ was computed per decile and per poem. Poems were classified by their *delta* (last-20% S₂ minus first-20% S₂):
- **Crescendo**: delta > +1.5
- **Decrescendo**: delta < −1.5
- **Plateau**: −1.5 ≤ delta ≤ +1.5

---

## Results

### 1. Global Arc Across All Poetry

| Decile | Range | Avg S₂ |
|--------|-------|--------|
| D1 | 0–10% | **+1.201** |
| D2 | 10–20% | **+1.059** |
| D3 | 20–30% | +0.145 |
| D4 | 30–40% | +0.158 |
| D5 | 40–50% | +0.115 |
| D6 | 50–60% | +0.276 |
| D7 | 60–70% | −0.018 |
| D8 | 70–80% | +0.241 |
| D9 | 80–90% | +0.113 |
| D10 | 90–100% | **−0.077** |

**H-Frontload confirmed.** S₂ is highest in the first two deciles and lowest at the end. The opening 20% averages +1.13 S₂; the final 20% averages +0.02 S₂. The mean delta across all poems is **−1.287** — poems lose over 1 bit of S₂ from opening to close.

### 2. Arc Type Distribution

| Arc Type | Count | % |
|----------|-------|---|
| Decrescendo | 43 | 48% |
| Plateau | 38 | 42% |
| Crescendo | 9 | 10% |

Nearly half of all poems are informational decrescendos. Only 1 in 10 crescendos toward a close.

### 3. Arc Type by Era

| Era | n | Crescendo % | Mean Δ |
|-----|---|-------------|--------|
| confessional | 3 | **67%** | **+1.39** |
| haiku | 1 | 100% | +2.58 |
| beat | 2 | 50% | −0.10 |
| romantic | 6 | 17% | −0.89 |
| victorian | 8 | 12% | −0.39 |
| contemporary | 7 | 14% | −1.33 |
| modernist | 15 | 7% | −1.22 |
| new_york_school | 18 | 6% | **−2.39** |
| language | 3 | 0% | **−2.97** |
| harlem_renaissance | 4 | 0% | −1.93 |
| 19th_century | 9 | 0% | −1.24 |

**The major exception is confessional poetry.** While every other substantial era decrescendos on average, confessional poetry (Plath, Sexton) crescendos — ending at higher S₂ than it begins.

**Language poetry** has the steepest decrescendo (−2.97). Bruce Andrews and other Language poets begin in maximum fragmentation (high S₂ openings from syntactic disruption) but end more predictably.

---

## Case Studies

### "We Real Cool" (Gwendolyn Brooks, 1959) — The Terminal Detonation
**Delta: −1.47 (plateau), but final token S₂ = +36.38**

Brooks's poem is a perfect anaphoric machine: "We / Jazz June. / We / Die soon." The repeating "We" creates a groove that GPT-2 learns quickly. By token 43, the model overwhelmingly expects a newline after "We" (as it has appeared every time). Instead Brooks writes:

> **"Die"**  → S₂ = **+36.38** (model expected: `\n`)

This is the highest S₂ value for any final-position token in the corpus. The anaphoric structure doesn't raise average S₂ (hence plateau) but concentrates the entire poem's information into the single terminal syllable. The poem *performs* death through information theory: the "We" creates false security, then "Die" detonates it.

### "Lady Lazarus" (Sylvia Plath, 1962) — Confessional Crescendo
**Delta: +3.82**

Lady Lazarus grows more surprising as it progresses. The final 10% contains:

| Token | Position | S₂ | Model Expected |
|-------|----------|----|----------------|
| `fine` | 53/57 (93%) | +5.01 | `\n` |
| `Jew` | 55/57 (96%) | **+25.56** | `\n` |
| `linen` | 56/57 (96%) | +9.05 | `el` (completing "Jewel") |

Plath fractures the expected word "Jewel" into "Jew" + "linen" — the break carries enormous S₂ because the model predicted the completion `el`. The racial naming performs the same function as Brooks's "Die": the proper noun arrives at a moment when formulaic continuation was expected, and it cannot be predicted. This is Straussian naming at its most extreme.

### "I Wandered Lonely as a Cloud" (Wordsworth, 1807) — Romantic Resolution
**Delta: −6.31**

Wordsworth begins with his most surprising word ("wandered" at S₂ = +6.10 in a context where the model expected ".", ",", or "\n") and ends with almost entirely expected language. The informational resolution mirrors the poem's thematic structure: the opening establishes strangeness, the closing brings philosophical comfort.

### Language Poetry: The Exhaustion Arc (Bruce Andrews, 1983)
**Delta: −7.16** (steepest decrescendo in corpus)

Andrews's "Islets/Irritations" opens with maximum grammatical disruption (S₂ = +5.34 in first 20%) but by the end falls to −1.81. This is the inverse of what we might expect from a poet committed to defamiliarization throughout. The pattern suggests that Language poetry's disruptions *normalize* over the course of a text — GPT-2 adapts to the disrupted grammar and begins predicting it more accurately.

---

## Core Finding: The Information Cliff

**Poetry is not uniformly surprising — it front-loads surprise.** The model faces maximum uncertainty in the opening lines (novel syntax, unexpected images, proper nouns) and calibrates over the course of the poem. By the final decile, average S₂ is near zero.

This has a cognitive parallel: readers update their expectations as they build a model of the poem's "world." The poem itself teaches the reader how to read it — and by the end, there is less left to surprise.

**The crescendo exception** (confessional poetry) reverses this logic. Plath, Sexton, and their successors *use* the normalized-expectation state that builds over a poem, then violate it at the last moment with a proper noun, a racial or historical reference, or a grammatical break. The crescendo is a trap: the poem lulls the reader, then detonates.

---

## Taxonomy: Information Arc as Genre Signature

| Arc Type | Exemplary Era | Mechanism |
|----------|--------------|-----------|
| Decrescendo (resolution) | romantic, 19th_century | Opens with novel images, closes with wisdom/comfort |
| Steep decrescendo | new_york_school, language | High opening disruption, normalizes over text |
| Crescendo (detonation) | confessional | Banal opening → shocking final naming |
| Terminal spike (plateau + detonation) | harlem_renaissance | Low average S₂ until single terminal word |

---

## Next Steps

1. **Longer poems**: Re-run on full Plath poems (not just "opening" excerpts) to confirm crescendo arc holds at scale.
2. **Closure tokens specifically**: Build a dataset of just the final 5 tokens per poem — what are the structural categories of "good" high-S₂ endings?
3. **Reader experience modeling**: The information arc could model *when* a reader "gets" a poem — when S₂ drops to near-zero, have they "solved" it?
4. **Corpus expansion**: Add more confessional poems (Sexton, Lowell) to strengthen the era-level claim with n > 3.
