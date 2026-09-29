# The Counter-Lexicon: What Words Does Poetry Most Systematically Suppress?

**Date:** 2026-09-29  
**Experiment:** `experiments/suppressed_lexicon.py` → `results/suppressed_lexicon.json`  
**Corpus:** 179 poetry texts (control/cliché excluded), 18,869 artifact-free tokens  
**Builds on:** `straussian_gap_taxonomy.md`, `confidence_trap_analysis.md`, `cliche_vs_originality.md`

---

## Research Question

Every token in the corpus has a `top-1 alternative` — the single word GPT-2 most expected at that position. For the 2,246 distinct words the model nominated as top-1 predictions, this experiment asks:

1. Which words does GPT-2 most frequently predict in poetry contexts?
2. When GPT-2 confidently expects a specific word, how often does the poet actually write it?
3. Which commonly-predicted words are most systematically suppressed — never or rarely written despite the model's confidence?
4. What does poetry write *instead* of these suppressed words?

---

## Finding 1: The Grammar of Prediction — What GPT-2 "Wants" to Write

The top-30 most-frequently-predicted words are almost entirely function words and punctuation:

| Word | Predicted | Accepted | Acceptance% | Avg S₂ when rejected |
|------|-----------|----------|------------|---------------------|
| `,` | 2,064 | 639 | 31.0% | +0.639 |
| `` (start) | 1,849 | 1,062 | 57.4% | +1.280 |
| `the` | 1,528 | 399 | 26.1% | +0.746 |
| `.` | 775 | 291 | 37.5% | +0.597 |
| `of` | 528 | 160 | 30.3% | +0.946 |
| `I` | 484 | 115 | 23.8% | +0.428 |
| `and` | 481 | 95 | 19.8% | +0.015 |
| `a` | 368 | 96 | 26.1% | +0.119 |
| `to` | 366 | 113 | 30.9% | +1.410 |
| `And` | 314 | 40 | 12.7% | +0.553 |
| `is` | 289 | 86 | 29.8% | +0.723 |
| `man` | 86 | 13 | 15.1% | +0.513 |

GPT-2 lives in a world of grammar. Its most confident predictions are the connective tissue of language: commas, articles, prepositions, conjunctions, the copula. Every position in a poem is first evaluated through this grammatical lens before semantic content matters.

**Function word acceptance rate: 26.0%**  
**Punctuation acceptance rate: 32.3%**

Poets override GPT-2's function word predictions roughly **three times out of four**. The grammatical skeleton of the poem is the primary arena of Straussian deviation.

---

## Finding 2: The Counter-Lexicon — Words Poetry Never Writes

Among words predicted ≥20 times, these have the lowest acceptance rates:

| Word | Predicted | Accepted | Acceptance% | Avg S₂ when rejected |
|------|-----------|----------|------------|---------------------|
| `great` | 23 | **0** | **0.0%** | −0.446 |
| `world` | 42 | 1 | 2.4% | +0.346 |
| `little` | 34 | 1 | 2.9% | +1.268 |
| `In` | 26 | 1 | 3.8% | +0.380 |
| `can` | 25 | 1 | 4.0% | +0.201 |
| `O` | 25 | 1 | 4.0% | +0.622 |
| `light` | 23 | 1 | 4.3% | −0.867 |
| `house` | 20 | 1 | 5.0% | −0.358 |
| `face` | 22 | 2 | 9.1% | +1.755 |
| `have` | 59 | 6 | 10.2% | +0.116 |
| `sun` | 42 | 5 | 11.9% | +0.616 |
| `sea` | 41 | 6 | 14.6% | −0.344 |
| `man` | 86 | 13 | 15.1% | +0.513 |

Also predicted ≥15 times but accepted **zero** times: `great`, `first`, `earth`, `air`.

### The Central Finding: Poetry's Counter-Lexicon Is "Expected Poetic Diction"

The most-suppressed words fall into a recognizable category: **the aestheticized general vocabulary of conventional poetry**. These are the "poetic" words that non-poets reach for and that literary critics call clichés:

- **Grand abstractions**: `world`, `earth`, `air`, `light`, `sun`, `sea`, `sky`
- **Generic emotional anchors**: `great`, `little`, `face`
- **Generic human referent**: `man`

GPT-2 has learned from its vast training corpus (which includes discussion of poetry, quotations of poetry, and three centuries of poetic tradition) that these words are statistically common in poetic contexts. But the actual poets in our corpus — spanning contemporary, modernist, confessional, and Romantic traditions — **systematically avoid the words the model expects them to write**.

This creates a paradox: **the most "poetic" vocabulary in the statistical sense is the vocabulary that actual poets most reliably suppress**.

---

## Finding 3: What Poetry Writes Instead — Two Suppression Strategies

For each top-suppressed word, the most common replacements reveal distinct strategies:

| Suppressed word | Top replacements | Strategy |
|----------------|-----------------|---------|
| `great` | crowd, lake, plain, rolling, green | **Specificity substitution** — abstract scale replaced by concrete particulars |
| `world` | whole, prayer, survey, role, clearing | **Conceptual deflection** — a global noun replaced by partial or abstract variants |
| `light` | hills, fire, air, wheel, train, space | **Image cluster** — a diffuse aesthetic noun replaced by specific images |
| `little` | heavy, bag, paper, feature, headache | **Tonal inversion** — diminutive adjective replaced by weighty or mundane terms |
| `house` | moon, building, wood, hut, wild | **Domain shift** — interior space replaced by exterior or elemental alternatives |
| `face` | frown, lip, sculpt, hand, gesture | **Synecdoche** — the whole replaced by a part; or action replaced by abstract |

Two suppression strategies emerge:

**1. Mundane avoidance** (avg_rej_S2 ≈ −0.5 to 0): `great`, `light`, `air`, `earth`, `sea` — when the poet refuses these, the replacement is itself relatively ordinary or specific. The avoidance is less about surprise than about precision. The poet doesn't want to be *shocking* — they want to be *exact*. "Great" is replaced by "rolling," not "quantum."

**2. Radical avoidance** (avg_rej_S2 > 1.5): `sky` (+2.514), `face` (+1.755), `He` (+2.324), `little` (+1.268) — when the poet refuses these, the replacement is *genuinely surprising*. Refusing "sky" leads to S2 = +2.514; refusing "face" to S2 = +1.755. These are sites where poetic deviation is both categorical (no "sky" here) and radical (the actual choice is unexpected).

---

## Finding 4: The Near-Absence of High-Acceptance Words

Only **one word** in the corpus achieves ≥80% acceptance when predicted ≥15 times:

| Word | Predicted | Accepted | Acceptance% |
|------|-----------|----------|------------|
| `For` | 22 | 21 | **95.5%** |

`For` appears in highly formal or ritualistic syntactic frames (anaphoric "For" at line openings: "For the world is too much with us," "For I have known them all already"). These frames are so strongly conditioned that both the model and the poet arrive at the same word almost every time.

This near-total absence of high-acceptance content words means: **poetry never "confirms" GPT-2's content-word predictions**. Anywhere GPT-2 expects a specific noun, adjective, or verb, the poet almost always writes something different.

---

## Finding 5: Era-Level Suppression Patterns

Among the most-suppressed words, no era accepts them consistently. Notable exceptions:

- **Fixed form** (sonnets, villanelles): 33.3% acceptance of `world` — formal poems occasionally use the grand noun in expected positions (e.g., "the world" as a standard rhyme partner)
- **Harlem Renaissance**: 50.0% acceptance of `In` — formal syntactic openings ("In the dark," "In Harlem") honor the model's prediction
- **Victorian**: 16.7% acceptance of `can` — Victorian syntax sometimes confirms the auxiliary frame

**Modernist, New York School, Romantic, Contemporary**: all have 0% acceptance for most counter-lexicon words. Contemporary and New York School poetry most completely avoids the expected aesthetic vocabulary.

---

## Theoretical Interpretation: The Average Poem GPT-2 Has Internalized

The counter-lexicon reveals the "average poem" that GPT-2 has internalized from its training: a poem full of `great` and `world` and `light` and `face` and `man` — the vocabulary of sentiment and grandiosity. This is, roughly, the aesthetic of third-rate Victorian verse, greeting-card poetry, and the kind of "poetic" language that surrounds poetry in ordinary discourse (epithets, reviews, descriptions of poems).

Actual poets — trained in the modernist tradition's rejection of "Poetic Diction" — operate explicitly against this average. The S2 framework quantifies exactly how far they depart from it.

**The Straussian Gap, at the lexical level, is the gap between the "average poem GPT-2 was trained on" and the poem actually written.**

---

## Comparison with Straussian Taxonomy

The `straussian_gap_taxonomy.md` classified high-S2 deviations by grammatical category (function→content, content substitution, proper noun break). This experiment provides the **lexical** level: not just "the poet chose a content word when GPT-2 expected a function word," but specifically WHICH content words are most universally avoided.

The two levels are consistent: the taxonomy showed that CONTENT_SUBSTITUTION is the most common deviation type (33%). This experiment shows that what's being substituted is systematically the aestheticized general vocabulary: `great`, `world`, `light`, `face`, `man`, `earth`, `air`.

---

## Suggested Next Steps

1. **Temporal tracking**: Does the counter-lexicon change by era? Do Romantic poets suppress fewer "romantic" aesthetic words than modernists? (Hypothesis: the counter-lexicon shifts with each generation's reaction against its predecessors' diction.)

2. **The "positive counter-lexicon"**: What words appear in poetry *more* than GPT-2 predicts? These are the words that mark a distinctively poetic register — the specific, concrete, unexpected vocabulary that replaces the grand abstractions.

3. **The cliché control test**: The corpus includes three cliché-control texts. Does the cliché control *accept* the counter-lexicon words at higher rates than real poems? If so, the counter-lexicon serves as an empirical test for poetic quality.

---
