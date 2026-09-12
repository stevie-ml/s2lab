# Emotional Valence and S₂: The Affective Dimension of Poetic Surprise

**Date:** 2026-09-12  
**Experiment:** `experiments/emotional_valence_s2.py`  
**Corpus:** 110 English poems, 526 tokens matched to AFINN-111 lexicon  
**Builds on:** `straussian_gap_taxonomy.md`, `sonic_substitution_vs_s2.md`

---

## Research Question

When poets make high-S₂ choices — deviating from what GPT-2 predicts — do those deviations tend to be emotionally charged? And in which direction?

The **Affective Gap hypothesis**: The Straussian gap is not purely an information-theoretic phenomenon but also an *affective* one. Poets surprise the model not randomly but by choosing words with distinct emotional valence relative to what syntactic/statistical convention would have placed there. The deviation from expectation is also a deviation from emotional baseline.

Two sub-hypotheses:
1. High-S₂ tokens have higher emotional intensity (|valence|) than low-S₂ tokens
2. At high-S₂ moments, the *direction* of the emotional deviation is systematic — toward negativity (the dark sublime) or positivity (transcendence/affirmation)

---

## Method

- Loaded token-level S₂ data from `corpus_results.json` (110 English poems)
- Used AFINN-111 lexicon (Finn Årup Nielsen) — ~2,477 English words rated −5 (very negative) to +5 (very positive)
- Matched alphabetic tokens of length ≥ 3, including simple stemming (remove -ing, -ed, -ly, -er, -s)
- **Affective gap**: for tokens where both the actual word *and* GPT-2's top prediction have AFINN ratings, computed `gap = valence(actual) − valence(predicted)`
  - Positive gap → poet chose more positive than the model expected
  - Negative gap → poet chose more negative than expected
  - |gap| → magnitude of affective divergence, regardless of direction

---

## Results

### 1. Emotional Intensity Does Not Monotonically Track S₂

| S₂ bin | n | mean \|val\| | mean val | % positive | % negative |
|---|---|---|---|---|---|
| Very low S₂ (< −3) | 102 | 1.559 | +0.343 | 62.7% | 35.3% |
| Low S₂ (−3 to −1) | 102 | 1.559 | +0.598 | 62.7% | 29.4% |
| Neutral S₂ (−1 to 1) | 117 | **1.812** | +0.479 | 60.7% | 35.0% |
| High S₂ (1 to 3) | 75 | 1.627 | +0.507 | 60.0% | 32.0% |
| Very high S₂ (≥ 3) | 130 | 1.708 | +0.246 | 57.7% | **40.0%** |

**Counterintuitive finding**: Emotional intensity peaks at *neutral* S₂ (−1 to 1), not at extreme S₂. This suggests that emotionally charged words are often *expected* — love, death, beauty — i.e., they are semantically saturated enough that GPT-2 finds them neither especially surprising nor especially predictable. Emotion is not inherently a source of surprise.

---

### 2. The Affective Gap Is Largest at Maximum Surprise

For tokens where both actual and top-predicted words have AFINN ratings (n=119 paired):

| S₂ bin | n | mean gap | mean \|gap\| | % pos gap | % neg gap |
|---|---|---|---|---|---|
| Very low S₂ (< −2) | 71 | −0.211 | 0.380 | 5.6% | 14.1% |
| Low S₂ (−2 to 0) | 24 | −0.500 | 1.750 | 25.0% | 45.8% |
| High S₂ (0 to 2) | 15 | −0.467 | 1.800 | 26.7% | 40.0% |
| **Very high S₂ (≥ 2)** | 9 | **+0.333** | **2.778** | 44.4% | 44.4% |

**The key finding**: When poets make their *most* surprising choices (S₂ ≥ 2), the mean absolute affective gap is **2.778** — nearly 7× larger than at predictable moments (0.380 for S₂ < −2). Surprise and affective divergence co-occur: poets who deviate maximally from expectation do so with words emotionally far from what the model predicted.

At predictable moments (low S₂), the affective gap is nearly zero and skewed slightly negative (the model's expected word tends to be more positive than what the poet actually writes — convention is cheerful; poetry is darker).

At maximum surprise, the gap is large but nearly balanced between positive and negative directions (44.4% each) — the poet deviates emotionally in either direction, but always deviates far.

---

### 3. The Twenty Most Surprising Emotionally Charged Tokens

| Word | S₂ | Valence | GPT-2 expected | Author |
|---|---|---|---|---|
| die | 36.38 | −2 | ⟨newline⟩ | Gwendolyn Brooks |
| sun | 22.69 | +2 | ⟨newline⟩ | E.E. Cummings |
| death | 12.86 | −2 | a | Emily Dickinson |
| bright | 12.14 | +2 | — | Sylvia Plath |
| angel | 12.13 | +3 | — | Allen Ginsberg |
| grave | 11.78 | −2 | my | Seamus Heaney |
| lonely | 11.37 | −2 | into | William Wordsworth |
| spirit | 10.01 | +2 | the | W.B. Yeats |
| disaster | 9.59 | −3 | longer | Elizabeth Bishop |
| ruined | 9.55 | −2 | ly | William Shakespeare |
| sweet | 9.49 | +2 | . | Sappho |
| funny | 9.12 | +2 | you | John Ashbery |
| god | 8.86 | +2 | it | Charles Baudelaire |
| envy | 8.68 | −2 | i | John Ashbery |
| sin | 8.68 | −3 | . | Gwendolyn Brooks |
| sad | 8.49 | −2 | d | Traditional |
| hollow | 8.45 | −2 | only | T.S. Eliot |
| freedom | 8.05 | +2 | of | Wallace Stevens |
| hunger | 7.75 | −2 | good | Lucille Clifton |
| kindly | 7.58 | +2 | was | Emily Dickinson |

**Pattern**: The highest-S₂ emotionally charged tokens are almost evenly split positive (sun, bright, angel, spirit, sweet, funny, god, freedom, kindly) and negative (die, death, grave, lonely, disaster, ruined, envy, sin, sad, hollow, hunger). What unites them is that *GPT-2 consistently expected something structurally trivial* — a newline, a conjunction, a punctuation mark, a common preposition. The poet answered with mortality or radiance.

This is the affective face of the Straussian gap: where syntax opens a slot for `the`, the poet writes `death`. Where syntax expects a line-break, the poet writes `sun`.

---

### 4. Emotional Charge by Era

| Era | n | all \|val\| | high-S₂ \|val\| | mean val |
|---|---|---|---|---|
| prose_poetry | 28 | **2.036** | 2.125 | +0.964 |
| beat | 12 | 2.000 | 2.000 | +0.333 |
| harlem_renaissance | 35 | 1.829 | 1.889 | **−0.343** |
| new_york_school | 50 | 1.760 | **2.050** | +1.000 |
| romantic | 64 | 1.719 | 1.550 | +0.219 |
| mid_century | 17 | 1.706 | **2.750** | −0.765 |
| ballad | 20 | 1.650 | 1.333 | +0.050 |
| victorian | 126 | 1.627 | 1.757 | +0.675 |
| confessional | 10 | 1.600 | 1.800 | 0.000 |
| contemporary | 23 | 1.565 | 1.500 | −0.435 |
| 19th_century | 33 | 1.515 | 1.545 | +0.485 |
| modernist | 83 | 1.494 | 1.346 | +0.458 |

**Notable patterns**:
- **Prose poetry** and **beat** use the most emotionally charged words overall (|val| ≈ 2.0), likely because their looser syntactic structure allows more emotional vocabulary to enter freely
- **Harlem Renaissance** and **mid-century** (Plath, Bishop, Lowell) have the most negative mean valence — they write the darkest poems in AFINN terms
- **New York School** high-S₂ moments are among the most emotionally charged (2.050) despite the movement's reputation for playful detachment — surprise in Frank O'Hara and Ashbery tends to be emotionally freighted
- **Mid-century** shows the highest emotional charge at high-S₂ moments (2.750) — confessional-adjacent poets land their most surprising tokens in maximally charged emotional territory

---

### 5. Valence Asymmetry: Poets Surprise Toward Darkness

| Group | n | mean val | % positive | % negative |
|---|---|---|---|---|
| All high-S₂ (≥ 2.0) | 163 | **+0.252** | 55.8% | **39.9%** |
| All low-S₂ (≤ −2.0) | 148 | **+0.392** | **62.2%** | 33.1% |

**Finding**: Predictable choices (low S₂) are more positive than surprising ones (high S₂). The 6.4 percentage-point difference in negative valence (39.9% vs. 33.1%) reveals a systematic asymmetry: **statistical convention in language skews positive; poetic surprise skews toward darkness**.

When a poem meets the model's expectations, it tends toward positive words. When it deviates, the negative direction is proportionally more likely. This aligns with longstanding observations about the tragic/negative bias in lyric poetry (Keats's "Beauty is truth" aside) and with the information-theoretic logic of the Straussian gap: the unexpected is often the difficult thing, and difficult things are often dark.

---

## Limitations

- **Sparse coverage**: AFINN matched only 526 of ~30,000 corpus tokens (≈1.7%). The lexicon covers common emotional vocabulary but misses much poetic vocabulary (proper nouns, uncommon words, coinages).
- **Paired analysis**: n=119 for the affective gap analysis, with only 9 tokens at very high S₂. Results are directionally suggestive but not statistically robust.
- **Stemming is imprecise**: Simple suffix removal may misidentify words; "ruined" → "ruin" is correct, but other cases may be noisy.
- **AFINN is prose-calibrated**: The lexicon was trained on tweets and web text, not poetry. Poetic words like "hollow," "grave," and "dark" carry richer negative charge in context than AFINN captures.

---

## Key Findings

1. **Emotional intensity ≠ surprise**: High-S₂ tokens are not the most emotionally charged — mid-range S₂ words are. Emotion is *expected* in poetry; it only becomes surprising in context.

2. **The affective gap peaks at maximum surprise**: When poets deviate most from GPT-2's expectation, they diverge most in emotional direction (|gap| = 2.778 vs. 0.380 at predictable moments). Extreme poetic surprise is also extreme affective divergence.

3. **The Straussian gap has a dark bias**: High-S₂ tokens are 6.4pp more likely to be negatively valenced than low-S₂ tokens. Convention is cheerful; poetry is darker.

4. **The structural "slot" produces the most striking emotional surprises**: GPT-2 expects a newline or a conjunction; the poet writes "die" or "sun." The greatest affective surprises happen when formal structure (line breaks, clause completions) meets emotional intensity — the slot that opens for a function word is filled with the word for death or radiance.

---

## Suggested Next Steps

- **Expand the lexicon**: Use NRC Word-Emotion Association Lexicon (>14,000 words, 8 emotion categories) for richer coverage
- **Arousal vs. valence**: Test separately — does high S₂ correlate with *arousal* (intensity) more than *valence* (direction)?
- **Sentence-level sentiment arcs**: How does the cumulative sentiment arc of a poem relate to its S₂ arc? Do they mirror each other or diverge?
- **Cross-linguistic**: Do German poems (Rilke, Trakl) show the same dark-surprise bias? The German corpus already exists in `corpus_results.json`
- **"Slot and fill" analysis**: Systematically catalog what syntactic slots (noun, verb, adjective following predeterminer, etc.) produce the most emotionally surprising fills
