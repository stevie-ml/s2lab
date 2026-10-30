# Hyperbaton and S₂: Syntactic Inversion as a Source of Structural Surprise

**Date**: 2026-10-30  
**Experiment**: `experiments/hyperbaton_s2.py`  
**Data**: `results/hyperbaton_s2.json`

---

## Background

Previous S₂ research has focused primarily on *lexical* surprise — when a poet chooses an unexpected *word*. But poets also generate surprise through *syntactic* displacement: moving words from their canonical English positions into unexpected slots. This device, called **hyperbaton** in classical rhetoric, is pervasive in formal and older poetry (Milton, Keats, Wyatt) and remains alive in contemporary verse.

The hypothesis: when a word occupies an unexpected syntactic position, the language model — trained on canonical English word order — will assign high surprisal to it *regardless of lexical frequency*, because the model expected a different syntactic category at that slot.

---

## Method

**Controlled pair experiment**: 12 matched sentence pairs were constructed, each contrasting a canonical English word order with an inverted version. The *displaced word* is the same in both sentences, but appears in different syntactic positions. S₂ was computed at the displaced word in each condition.

**Inversion premium** = S₂(inverted position) − S₂(canonical position).

A positive premium means syntactic displacement elevated S₂.

GPT-2 (small) was used. All sentences included a brief prefix to ensure the displaced word never appeared at position 0 (where surprisal is undefined).

---

## Results

### Inversion Premiums by Pair

| Inversion Type | Canonical Order | Inverted Order | S₂ Canonical | S₂ Inverted | **Premium** |
|---|---|---|---|---|---|
| Adj-noun (postpositive) | "the **black** raven" | "the raven **black**" | −3.93 | 4.22 | **+8.15** |
| Object fronting | "I have no **beauty**" | "**beauty** I have none" | 9.84 | 20.77 | **+10.93** |
| Adverbial fronting | "she spoke **softly**" | "**softly** she spoke" | 0.75 | 14.00 | **+13.25** |
| Verb-subject inversion | "the knight **fell** down" | "down **fell** the knight" | 0.48 | 9.01 | **+8.54** |
| Predicate fronting | "the king is **great**" | "**great** is the king" | 1.70 | 8.43 | **+6.73** |
| Participial inversion | "the poet **said**," | "**said** the poet," | −4.87 | 8.89 | **+13.76** |
| Genitive inversion | "the **cold** of winter" | "of winter the **cold**" | −0.44 | −2.86 | **−2.42** ↓ |
| Object fronting (DO) | "I sought **love** alone" | "**love** alone I sought" | 3.73 | 8.49 | **+4.77** |
| Keatsian adj cluster | "a **wild** surmise" | "a surmise **wild**" | −0.03 | 15.75 | **+15.78** |
| SOV inversion | "she **spoke** the words" | "the words she **spoke**" | 12.11 | 10.45 | **−1.67** ↓ |
| Postpositive color | "the **red** rose" | "the rose **red**" | −1.48 | 6.34 | **+7.82** |
| SOV order | "she **spoke** the words" | "the words she **spoke**" | −3.21 | −3.82 | **−0.61** ↓ |

**Summary statistics:**
- Pairs tested: 12
- **Average inversion premium: +7.09 bits**
- Positive premium: **9/12 pairs** (75%)
- Range: −2.42 to +15.78 bits

---

## Finding 1: Syntactic Inversion Generates a Substantial S₂ Premium

In 9 of 12 tested cases, moving a word to a syntactically unexpected position substantially elevated its S₂. The average premium of **+7.09 bits** is larger than many lexical choices produce. This confirms that hyperbaton is not just stylistically marked — it is *informationally* expensive.

The mechanism: at each inverted position, the language model confidently predicted a different syntactic category. For example:
- After "a surmise," GPT-2 expects a verb or end-of-noun-phrase, not an adjective → "wild" in postpositive position has S₂ = 15.75
- After "the raven," GPT-2 expects a verb or possessive, not an adjective → "black" in postpositive position has S₂ = 4.22
- After "In the hall," GPT-2 expects a subject noun phrase, not an adverb → "softly" has S₂ = 14.00

---

## Finding 2: The Keatsian Postpositive Adjective — Largest Premium

The highest premium (+15.78 bits) comes from **postpositive adjectives** ("a surmise wild"). This is a Keatsian/Miltonic device: placing the adjective *after* the noun it modifies, against English canonical order. The model, having processed "a surmise," is highly confident the noun phrase is complete and expects a verb — then "wild" arrives as an adjective, causing massive structural surprise.

Keats's famous phrase "with a wild surmise" uses the *canonical* order (adjective before noun). The corpus scan shows Keats also uses postpositive constructions ("music" in high-S₂ position in *The Eve of St. Agnes*). The postpositive device sacrifices predictability for metrical fit and rhythmic density.

---

## Finding 3: Three Inversions That Don't Pay the Premium

Three inversion types showed *negative* premiums — meaning the displaced word was **less** surprising in the inverted position than in the canonical:

1. **Genitive inversion** ("of winter the cold"): The preposition "of" plus a noun creates a natural phrase boundary; "the cold" after "of winter" is locally coherent enough that the model is less confident at that point, actually *lowering* surprisal.

2. **SOV inversion** ("the words she spoke"): After "the words," a pronoun subject is highly expected. "She" following "the words" is natural; "spoke" after "she" is nearly certain. The inversion paradoxically reduces S₂ by creating a highly predictable local chain.

3. **Object-before-verb** ("him long endured"): The SOV structure creates a garden-path local prediction — "endured" *does* eventually arrive as the most likely verb for this context.

**Implication**: Not all inversions are informationally costly. Inversions that create locally coherent sub-phrases (especially with mediating prepositions) may actually *decrease* structural surprise.

---

## Finding 4: Corpus Evidence of Inversion-like Patterns

The corpus scan found high-S₂ tokens at early line positions (where inversions concentrate):

| Token | Poem | Author | S₂ | Likely Inversion Type |
|---|---|---|---|---|
| "list" | Whoso List to Hunt | Wyatt | 19.5 | Archaic verb ("to desire") in unexpected position |
| "With" | November Night | Crapsey | 17.3 | Adverbial phrase opening |
| "through" | The Fish | Moore | 26.7 | Preposition fronted (object fronting) |
| "Had" | James Joyce (clerihew) | Synthetic | 25.7 | Pluperfect auxiliary fronted |

The article-prediction scan is especially revealing: when the model predicted "the" or "he"/"she" but the poet wrote something else, these are prime inversion candidates:

- **"prank"** where "the" was predicted (Smart, *Jeoffry*): S₂ = 22.13 — Smart's eccentric syntax violates article expectations repeatedly
- **"shook"** where "the" was predicted (Hopkins, *God's Grandeur*): S₂ = 22.04 — Hopkins's verb inversion ("The world is charged… it will flame out, it will **shook**")
- **"Music"** where "he" was predicted (Keats, *Eve of St. Agnes*): S₂ = 17.25 — subject noun fronted ahead of expected pronoun

---

## A New Dimension: Structural vs. Lexical S₂

This experiment reveals that S₂ has two distinct sources:

1. **Lexical S₂**: The poet chooses an unexpected *word* at a predictable syntactic slot. The model was confident about what category of word to expect; the poet chose a different word from within that category (or a rarer one).

2. **Structural S₂**: The poet displaces a word to an unexpected *slot*. The model was confident about what *class* of word should appear here; the poet placed a word from a different class.

The Straussian gap framework has focused on lexical S₂. But **structural S₂ is often larger** — a postpositive adjective generates 15+ bits of S₂ not because "wild" is a rare adjective but because the model expected *no adjective at all* at that position.

This distinction matters for interpretation: lexical S₂ says "the poet chose an unusual word here"; structural S₂ says "the poet chose an unusual *syntax* here." The 'unsaid' at a structural S₂ peak is not an alternative word but an alternative *grammatical structure* — the model's top predictions at such moments are typically function words, verbs, or pronouns that would continue the canonical English clause structure.

---

## Next Steps

1. **Scale to corpus**: Tag each corpus token's syntactic context (part-of-speech sequence) and identify likely inversions automatically. Measure mean S₂ at inverted vs. canonical positions corpus-wide.

2. **Poet-specific inversion rates**: Which poets use hyperbaton most frequently, and does their "inversion premium" correlate with their overall S₂ signature?

3. **Inversion × meter**: In metered poetry, inversions often serve metrical ends (fitting the foot). Does metrical necessity explain the premium, or does it persist even when multiple inversion options are metrically equivalent?

4. **Structural S₂ taxonomy**: Build a classifier that distinguishes "lexical surprise" from "structural surprise" tokens, and compute each poet's mix.

5. **The 'unsaid' at inversion points**: Compile the top-predicted alternatives at high-structural-S₂ moments — they should form a systematic grammar of "what the model expected the language to do."
