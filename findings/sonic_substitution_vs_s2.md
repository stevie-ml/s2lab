# Sonic Substitution: When Poets Surprise, Do They Sound Like What Was Expected?
**Date:** 2026-09-07
**Experiment:** `experiments/sonic_substitution.py`

## Question
When a poet makes a high-S₂ choice (unexpectedly defying the model's prediction), does the chosen word bear orthographic/phonetic resemblance to what GPT-2 predicted? Are high-surprise moments "sonic substitutions" — formally similar to the expected word but semantically different — or are they complete formal breaks?

## Method
- Analyzed 4,022 alphabetic token pairs (actual token + top prediction) from 95 English poems
- Computed character-level similarity (`difflib.SequenceMatcher`) between actual and predicted tokens
- Computed suffix/prefix overlap (rhyme-like similarity)
- Computed defection ratio: P(actual) / P(top prediction) — how much the poet defects from the probability peak
- Split into High S₂ (≥ 2.0), Mid S₂, and Low S₂ (≤ −2.0) groups

## Key Results

### 1. Mean Similarity by S₂ Group

| Group | n | Char sim | Best CS | Sfx ovlp | Pfx ovlp | Def ratio |
|-------|---|----------|---------|----------|----------|-----------|
| High S₂ | 954 | 0.1991 | 0.4708 | 0.13 | 0.12 | 0.004311 |
| Mid S₂ | 1577 | 0.3551 | 0.6992 | 0.61 | 0.61 | 0.259545 |
| Low S₂ | 1491 | 0.6593 | 0.9612 | 1.60 | 1.59 | 0.745591 |

Low S₂ tokens (predictable choices) have **character similarity of 0.66** to the top prediction — they look and sound almost the same. High S₂ tokens (surprising choices) have character similarity of only **0.20** — a completely different word in form.

### 2. Sonic Substitution Rate

| Group | % matching top pred (CS ≥ 0.6) | % matching any top-10 (CS ≥ 0.6) |
|-------|-------------------------------|----------------------------------|
| High S₂ | 2.8% | 16.9% |
| Mid S₂ | 20.9% | 55.2% |
| Low S₂ | 59.0% | 94.1% |

Only **2.8%** of high-S₂ moments produce a word that sounds like the top prediction. The overwhelming pattern is that surprise breaks form as well as expectation.

### 3. Strong Negative Correlations

- **S₂ vs character similarity: r = −0.47** — the more surprising a word, the less it resembles the prediction
- **S₂ vs defection ratio: r = −0.67** — higher S₂ means the poet chooses something with near-zero probability relative to the model's top choice

## Main Finding: High S₂ Choices Are Formally Alien

The Straussian gap is not just semantic — it is formal. When poets surprise us, they almost never choose a word that *sounds like* what the model expected. Instead, they make complete breaks: a different word family, a different phonetic shape, a different syntactic slot.

This tells us something important: **poetic surprise is orthogonally organized from sound**. The "deviation axis" runs along meaning and semantic field, not phonetic or morphological form. Alliteration, assonance, and rhyme patterns are a separate constraint system — poets manage sound and surprise independently.

## Exceptions: True Sonic Substitution

About 2.8% of high-S₂ moments are genuine sonic substitutions — surprisingly unexpected yet formally similar. Notable examples:

| Token | Predicted | S₂ | CS | Poem |
|-------|-----------|----|----|------|
| `moon` | `door` | 14.90 | 0.50 | The Listeners |
| `hear` | `the` | 11.68 | 0.57 | The Oxen |
| `cloud` | `child` | 8.10 | 0.60 | I Wandered Lonely as a Cloud |
| `lies` | `is` | 7.99 | 0.67 | Dover Beach |
| `nest` | `not` | 7.05 | 0.57 | Citizen |
| `gaze` | `case` | 6.61 | 0.50 | Self-Portrait in a Convex Mirror |

These are cases where a poet finds an unexpected word that still echoes the predicted word's shape — a kind of "acceptable disguise." Wordsworth choosing "cloud" where the model expected "child" has both phonetic overlap (c-l) and semantic distance; Arnold choosing "lies" where "is" was expected retains the verb morphology.

## Quasi-Rhyme Substitution (Suffix Overlap ≥ 2)

A subset of high-S₂ moments shows surprising words that **rhyme with** the top prediction (share ≥ 2 trailing characters):

| Token | Predicted | S₂ | Suffix Overlap | Poem |
|-------|-----------|----|----|------|
| `disaster` | `longer` | 9.59 | 2 | One Art |
| `makers` | `ors` | 9.13 | 2 | Rivers and Mountains |
| `descended` | `answered` | 8.31 | 2 | The Listeners |
| `weave` | `have` | 5.77 | 3 | The Oxen |
| `God` | `blood` | 2.48 | 2 | Daddy |

These moments suggest a **rhyme-with-the-unsaid** strategy: the poet substitutes something the model didn't expect, but the substitution rhymes with what was expected — an invisible internal rhyme scheme locked to the suppressed alternative.

## Era Breakdown: Which Eras Rely on Sonic Substitution?

| Era | % High-S₂ tokens with sonic similarity |
|-----|----------------------------------------|
| Ancient (Sappho) | 22.2% |
| Confessional | 16.7% |
| Oulipo | 16.7% |
| Deep Image | 15.4% |
| Harlem Renaissance | 10.0% |
| Modernist | 9.8% |
| New York School | 7.2% |
| Language poetry | **0.0%** |
| Surrealist | **0.0%** |

Language poetry and Surrealism show **zero sonic substitution** — when they surprise, they break entirely from the expected word's form. This aligns with those movements' explicit aesthetics: non-referential language (Language poetry), non-rational associative leaps (Surrealism).

Ancient/confessional poetry shows the most sonic substitution — possibly because formalist constraints (meter, sound patterning) force the poet to find unexpected words that still fit a sonic slot.

## Poet Signatures

| Poet | High-S₂ n | % Sonic | Mean Def Ratio |
|------|-----------|---------|----------------|
| Lucille Clifton | 5 | 40.0% | 0.0089 |
| Vachel Lindsay | 5 | 40.0% | 0.0020 |
| Sappho | 9 | 22.2% | 0.0111 |
| Sylvia Plath | 17 | 17.6% | 0.0047 |
| Emily Dickinson | 48 | 2.1% | 0.0023 |
| Hopkins | 22 | 0.0% | 0.0019 |
| Language poets | ~14 | 0.0% | 0.0015 |

Emily Dickinson is striking: **48 high-S₂ moments but only 2.1% sonic substitution**. Her surprises are pure semantic detonations — the chosen word has nothing to do with the predicted word's form. Hopkins at 0% sonic substitution despite his fame for sound patterning — when he deviates from expectation, his sound choices serve a completely different logic from the model's predictions.

## Interpretation

**The sonic and semantic surprise axes are independent.** When poets surprise us (high S₂), they are not using sound as a bridge — they break cleanly in form AND meaning. When they write predictably (low S₂), the word also *sounds* like what was coming.

This suggests a two-tier model of poetic choice:
1. **Semantic track**: managed by the Straussian gap — whether to confirm or disrupt model expectations
2. **Sonic track**: managed by alliteration, rhyme, and meter constraints — operating independently of surprisal

The rare cases of sonic substitution (2.8%) may represent a third strategy: **camouflaged surprise** — a word that breaks semantic expectation while maintaining formal innocence.

## Suggested Next Steps
- Build a corpus of known "sonic punning" cases (words that replace other words of similar sound but different meaning) and test whether they show systematically different S₂ profiles
- Investigate whether the quasi-rhyme-with-the-unsaid pattern is intentional: are there poets who seem to systematically rhyme their choices with the suppressed alternative?
- Look at whether Clifton and Lindsay's high sonic substitution rates correlate with their use of oral/performance traditions (their poetry was written partly for the ear)
- Test whether GPT-2's sonic similarities align with human phonetic judgments
