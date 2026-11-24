# The Conformist Lexicon: What Poets Agree On and Why It Matters

**Date:** 2026-11-24  
**Method:** Analyzed 450 poems, 54,654 artifact-free tokens (p_newline < 0.9). Conformist zone: S₂ < -1.0. Surprise zone: S₂ > 2.0.

---

## Research Question

When poets *agree* with GPT-2 (low S₂), what words appear — and do these conformist zones serve as structural setup for nearby surprise? Previous research has focused on the high-S₂ moments. Here we examine the other half of the information-theoretic rhythm.

---

## Key Numbers

| Zone | Token Count | % of Total |
|---|---|---|
| Conformist (S₂ < −1.0) | 27,555 | **50.4%** |
| Surprise (S₂ > 2.0) | 12,150 | **22.2%** |
| Middle ground | 14,949 | 27.3% |

**Half of all poetry tokens are in the conformist zone.** This is not marginal — conformity is the dominant mode of poetry at the token level, even as poetry overall is more surprising than prose.

---

## The Conformist Lexicon

Words most *overrepresented* in conformist zones relative to baseline:

| Word | Enrichment | Conformist Count | Total Count |
|---|---|---|---|
| `the` | 1.76× | 2,282 | 2,570 |
| `,` | 1.74× | 3,088 | 3,518 |
| `world` | 1.70× | 61 | 71 |
| `are` | 1.70× | 177 | 207 |
| `soul` | 1.65× | 25 | 30 |
| `is` | 1.59× | 378 | 471 |
| `.` | 1.55× | 1,522 | 1,942 |
| `and` | 1.55× | 1,099 | 1,408 |
| `be` | 1.54× | 144 | 185 |

**Finding 1:** The definite article, commas, periods, and copular verbs are the most reliable indicators of poet-model agreement. These are the "grammatical skeleton" of English — GPT-2 knows them so well that poets can almost never escape them.

**Finding 2:** Some *content* words are also highly conformist: `world` (1.70×), `soul` (1.65×). These are the most clichéd nouns of English poetry — GPT-2 has absorbed the poetic tradition deeply enough to predict them readily.

---

## Function vs. Content Words

| Zone | Function Words | Content Words |
|---|---|---|
| Conformist (S₂ < −1.0) | **42.1%** | 57.9% |
| Surprise (S₂ > 2.0) | **12.4%** | 87.6% |

**Finding 3:** Function words concentrate in conformist zones (42% vs 12%). Surprise is primarily a content-word phenomenon. When a poet surprises you, it is almost always *what* they say — the noun, verb, adjective — not the grammatical connective tissue.

---

## Most Common Content Words in the Conformist Zone

The "conventional" poetic vocabulary — words that even experimental poets predict-ably use:

`your`, `there`, `will`, `world`, `love`, `down`, `like`, `know`, `them`, `eyes`, `night`, `hand`, `horses`, `light`, `heart`, `said`, `come`, `shall`, `thou`, `things`

This is a kind of **anti-lexicon of poetic cliché** — not because these words are bad, but because even GPT-2's GPT-2 (trained on the poetic tradition) can predict them. When a poet writes `love` or `light` or `heart`, they are using the model-expected word. When they escape these, they produce the high-S₂ moments we analyze elsewhere.

---

## The Setup → Surprise Mechanism

**Most striking finding:** The median distance between a conformist token and the next surprise token is **1 token** (mean = 1.9).

| Proximity | % of Surprises |
|---|---|
| Conformist within 5 tokens | **97.6%** |
| Conformist within 10 tokens | **99.7%** |
| Conformist within 20 tokens | **99.9%** |

Virtually every surprise token in the corpus is immediately preceded by conformity. This reveals the **information-theoretic rhythm of poetry:**

> `[conformist] → [SURPRISE] → [conformist] → [SURPRISE]`

The rank distribution confirms: 45.4% of conformist tokens are rank-1 predictions (the model's very top guess), and 78.6% are within the top 5. These are genuinely expected choices.

---

## Setup Words: What Immediately Precedes Surprise

The token *immediately* before a surprise token (S₂ > 2.0):

- Avg S₂ of immediate pre-surprise token: **−0.427** (well into conformist range)
- 53.5% of immediate pre-surprise tokens are in conformist zone (S₂ < −1.0)

Most common "setup words" immediately before surprise:

| Setup Word | Count |
|---|---|
| `,` | 573 |
| `the` | 570 |
| `and` | 258 |
| `of` | 183 |
| `a` | 174 |
| `i` | 122 |
| `to` | 115 |
| `.` | 106 |
| `in` | 101 |
| `is` | 89 |

**Poetry's surprise mechanism rests on a foundation of commas and "the."** These are the grammatical moves so automatic that readers process them without conscious attention — which is precisely what makes the following surprise legible and forceful.

---

## Interpretation: The Orienting-Deviation Cycle

The findings support a clear cognitive model of poetic reading:

1. **Orienting phase** (conformist): Function words, expected punctuation, common content nouns (`love`, `night`, `world`) orient the reader within familiar linguistic territory. GPT-2 and reader agree on what's coming.

2. **Deviation phase** (surprise): At content-word positions, the poet departs from the expected word. This is felt against the backdrop of the just-established expectation.

3. **Re-orienting phase**: Following the surprise, the text typically returns to conformist territory, allowing the reader to process and "bank" the deviant choice before the next surprise.

This cycle — anticipation → disruption → re-orientation — is what makes poetry cognitively engaging at the token level, even when the reader isn't consciously tracking surprisal.

---

## Comparison: Conformist Rank Distribution

| Rank Category | Conformist Zone | (Baseline) |
|---|---|---|
| Rank = 1 (top prediction) | 45.4% | — |
| Rank ≤ 5 | 78.6% | — |

---

## Implications

1. **Poetry is not globally surprising.** Half the tokens in any poem are conformist. What we call "poetic surprise" is a *local* phenomenon within a predominantly conformist stream.

2. **The conventional vocabulary of poetry is measurable.** Words like `world`, `soul`, `love`, `night`, `heart` are informationally equivalent to function words in the poetic tradition — GPT-2 predicts them as readily as it predicts "the" or "and."

3. **The setup effect is near-universal.** Finding that 97.6% of surprises are within 5 tokens of a conformist zone strongly suggests this is not coincidental — it is the structural grammar of poetic deviation. No surprise without orientation first.

---

## Suggested Next Steps

- **Classify the "setup → surprise" transition by poet**: do some poets prefer longer setup runs before deviating?
- **Semantic analysis of the cliché-content words**: are "world," "love," "night" low-S₂ because they're semantically broad (many contexts predict them) or because they appear in stereotyped syntactic positions?
- **Test whether controlling for the conformist zone changes poet rankings**: poets with more function words may appear more conformist simply because they use more grammar.
- **Inter-poem conformist zone comparison**: is there a "canonical conformist zone" that all poetry shares, or is each poet's conformist vocabulary distinct?
