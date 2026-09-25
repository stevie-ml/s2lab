# The 2×2 Surprise Taxonomy: How Poets Create Information-Theoretic Deviation

**Date:** 2026-09-25  
**Experiment:** `experiments/surprise_taxonomy_2x2.py`  
**Corpus:** 180 texts (175 poetry/control), 17,999 artifact-free tokens  
**Artifact filter:** tokens where p(newline) ≥ 0.9 excluded (832 tokens, 4.4%)

---

## Motivation

S₂ = surprisal − entropy lumps together two distinct situations:
1. The model was **confident** about something, but the poet chose something else — genuine surprise
2. The model was **uncertain** anyway, and the poet happened to choose something the model didn't rank first — coincidental surprise

Prior analyses use S₂ as if it were a single thing. This study splits it into a 2×2 taxonomy based on two independent axes:

| | **Model was confident** (entropy < median) | **Model was uncertain** (entropy ≥ median) |
|---|---|---|
| **Poet chose unexpected word** (rank > 10) | **Type I: Definite Straussian Gap** | **Type II: Uncertain Leap** |
| **Poet chose expected word** (rank ≤ 10) | **Type III: Confirmed Prediction** | **Type IV: Lucky Hit** |

**Entropy median (corpus-wide):** 6.34 bits  
**Rank threshold:** top-10 = "expected," rank > 10 = "unexpected"

---

## Corpus-Wide Distribution (artifact-free)

| Type | Name | Count | % | Avg S₂ | Median S₂ |
|---|---|---|---|---|---|
| **I** | Definite Straussian Gap | 1,583 | **8.8%** | +5.36 | +4.65 |
| **II** | Uncertain Leap | 5,634 | **31.3%** | +1.73 | +1.17 |
| **III** | Confirmed Prediction | 7,000 | **38.9%** | −1.58 | −1.77 |
| **IV** | Lucky Hit | 3,782 | **21.0%** | −3.81 | −3.89 |

**Key fact:** Even in poetry, the plurality of tokens are Type III — the poet confirms the model's top prediction. Poetry is not a sustained exercise in surprise. The gap between Type I and Type III is a measure of the net Straussian force.

---

## Poetry vs. Prose

| Corpus | Type I% | Type III% | I−III contrast |
|---|---|---|---|
| **Poetry** | 8.8% | 38.7% | **−0.299** |
| **Prose control** | 5.5% | 59.5% | **−0.540** |
| Gap | +3.3 pp | −20.8 pp | **+0.241** |

Poetry's signature is not just "more Type I" — it is also dramatically "less Type III." The I−III contrast is 60% less negative in poetry (−0.30) than in prose (−0.54). Two independent shifts, in the same direction, reinforce each other.

---

## Top Genuine Straussian Gaps (Type I, artifact-free)

These are positions where GPT-2 was confident and the poet chose something far outside the model's predictions.

| S₂ | Entropy | Rank | Context | Poet's choice | Expected | Poet |
|---|---|---|---|---|---|---|
| 23.40 | 1.25 | 10,720 | `Der schimmer` | ` ferner` | `t` | Stefan George |
| 22.04 | 3.60 | 26,974 | `like shining from` | ` shook` | ` the` | G.M. Hopkins |
| 22.02 | 2.72 | 18,926 | `he rolls upon` | ` prank` | ` the` | Christopher Smart |
| 20.59 | 1.64 | 8,227 | `, the hour` | ` badly` | `glass` | Elizabeth Bishop |
| 20.40 | 2.39 | 5,618 | `at my ease` | ` observing` | `,` | Walt Whitman |
| 18.60 | 0.04 | 61 | `   ` | ` and` | ` ` | E.E. Cummings |
| 18.24 | 0.43 | 457 | `now not reck` | ` his` | `lessly` | G.M. Hopkins |

**Notable:** Hopkins appears **twice** in the top 15, both from "The Windhover." The famous "shining from shook foil" line generates one of the highest artifact-free S₂ scores in the corpus. The model expected "the" after "shining from" (the most probable continuation); "shook" — a past participle used as a noun-modifier — is completely outside expected parse. This is a precisely Straussian choice.

**E.E. Cummings** in the top 15 reflects his visual/typographic intervention: unconventional spacing creates contexts (` ` = 3-space indent token) that the model assigns near-zero entropy to, then Cummings places a normal word where the model expected more space.

---

## Two Strategies for Creating S₂ — The Core Finding

Comparing poets' **avg entropy** against their **Type I rate** reveals two fundamentally different strategies:

### Strategy A: "Straussian Classic" — Confidence Then Deviation
*Low avg entropy, high Type I, high Type III*

These poets write in contexts that the language model finds predictable — prose-like syntax, controlled grammar — creating a low-entropy stage on which they place their surprising word choices.

| Author | Avg H | Type I% | Type II% | Type III% |
|---|---|---|---|---|
| Russell Edson | **5.05** | **19.0%** | 13% | 57% |
| W.S. Merwin | **5.46** | **18.3%** | 12% | 60% |

**Both** Edson and Merwin operate with below-median entropy. Their syntax is predictable; their word choices are not. The high Type III rate is not a failure of ambition — it is the technique itself: you must confirm the model's expectations *most of the time* to create the context in which your deviations land with force. The 19%/57% ratio for Edson says: 1 out of 4 deviating tokens is a genuine Straussian gap, but there are three confirmations for every gap.

### Strategy B: "Ambient Uncertainty" — Maintain Perpetual High Entropy  
*High avg entropy, low Type I, high Type II*

These poets maintain high-entropy contexts throughout, so that even their "surprising" choices appear against a backdrop of ongoing uncertainty. They do not create the quiet before the storm — the poem is always stormy.

| Author | Avg H | Type I% | Type II% | Type III% |
|---|---|---|---|---|
| Gertrude Stein | **6.90** | **2.4%** | 36% | 33% |
| John Donne | **6.91** | **4.6%** | 42% | 25% |

Stein and Donne have the **same average entropy** (6.90–6.91) but very different surface styles. Both keep the model perpetually uncertain. In Stein's case ("Susie Asado"), repetitive incantatory syntax keeps the model in a high-entropy state where it never commits to a prediction. In Donne's case ("Death, Be Not Proud"), his elaborate conceits and inverted syntax create structurally different sources of uncertainty that produce a similar entropy profile.

### Strategy C: "Hybrid"
| Author | Avg H | Type I% | Type II% |
|---|---|---|---|
| Philip Larkin | 6.67 | 14.3% | 34% |
| Thomas Wyatt | 6.14 | 11.4% | 38% |

Larkin and Wyatt operate at moderate entropy with significant presence in both Type I and Type II — drawing on both strategies.

---

## Per-Era Type I Rates (artifact-free, sorted by Type I%)

| Era | N | Type I% | TypeIII% | I−III |
|---|---|---|---|---|
| ancient | 90 | **17.8%** | 44.4% | −0.267 |
| prose_poetry | 935 | 13.5% | 52.4% | −0.389 |
| beat | 148 | 12.2% | 37.2% | −0.250 |
| nursery_rhyme | 222 | 12.2% | 43.2% | −0.311 |
| german_modernist | 234 | 12.0% | 35.5% | −0.235 |
| spoken_word | 193 | 11.9% | 37.8% | −0.259 |
| early_modern | 527 | 10.8% | 27.5% | −0.167 |
| contemporary | 814 | 10.4% | 45.2% | −0.348 |
| modernist | 1,585 | 6.5% | 36.3% | −0.298 |
| metaphysical | 534 | **5.4%** | 30.7% | −0.253 |
| control (prose) | 163 | 5.5% | 59.5% | −0.540 |

**Surprising finding:** "ancient" (Sappho, translated) leads all eras. This likely reflects the distance between classical Greek poetic register and GPT-2's training data: even in translation, ancient poetry creates frequent low-entropy contexts where an unusual word arrives.

**Nursery rhyme** at 12.2% is the most unexpected result. These are short, repetitive, phonetically constrained texts. Their high Type I rate reflects that nursery rhymes use *extremely common words* in *highly unusual sequences* — the classic pattern for Straussian gaps (common word, surprising position).

**Metaphysical poetry** has the lowest Type I rate of any era (5.4%, comparable to prose). This is Strategy B in action at the era level: Donne, Herbert, and Marvell maintain high entropy throughout via elaborate conceits, so genuine low-entropy surprise moments are rare.

---

## The Gertrude Stein Paradox

Stein is known as one of the most radical experimenters in English poetry. Yet she has the lowest Type I rate (2.4%) in the corpus. This is not a failure of the measure — it is a revelation of the *type* of experiment she conducts.

Stein creates **Type II** surprises: unexpected choices against uncertain contexts. "Susie Asado" has avg entropy 6.90 bits, well above the corpus median. The model can never get confident about what comes next because the repetitive, self-referential syntax violates the dependency structure GPT-2 was trained on. When Stein surprises (36% Type II), it is surprise on top of uncertainty — the Straussian gap in the technical sense is unavailable because the certainty precondition is never met.

This distinguishes two senses of "experimental":
- **Lexical experiment** (Edson, Merwin): unusual words in conventional contexts → high Type I
- **Syntactic/structural experiment** (Stein, Donne): conventional words in unconventional syntax → high ambient entropy, low Type I, high Type II

---

## Conclusions and Next Steps

**Claim:** S₂ analysis benefits from decomposing the metric along two independent axes. A single S₂ value conflates Straussian surprise (Type I), ambient uncertainty (Type II), and conventional choice (Type III/IV). 

**Interpretive key:**  
- High Type I / low Type III + low avg entropy = "Straussian Classic" (Edson, Merwin)
- Low Type I / high Type II + high avg entropy = "Ambient Uncertainty" (Stein, Donne)
- The I−III contrast is the cleanest summary of "net poetic force" against prose

**Next steps:**
1. **Within-poem dynamics**: Does a poem shift between quadrant types across stanzas? A poem that begins as Type III and ends as Type I would have classical volta structure.
2. **Type I word categories**: What semantic fields dominate the high-Type I positions? Are they verbs, nouns, adjectives? How do they relate to the poem's central image?
3. **Cross-era entropy trends**: Does the avg_H of poetry change across literary history (earlier eras = higher or lower entropy)?
4. **The Cummings effect**: E.E. Cummings appears frequently in the top Type I positions via typographic/visual device rather than lexical choice. Should typographic surprise be classified separately?
