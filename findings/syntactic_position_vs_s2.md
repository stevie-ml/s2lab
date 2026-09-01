# Syntactic Position and S₂: The Straussian Gap Lives in Content Words
**Date:** 2026-09-01  
**Experiment:** `experiments/syntactic_position.py`  
**Corpus:** 61 English poetry texts + 4 control prose texts (73 total)

---

## Question

Do nouns, verbs, adjectives, and function words have systematically different S₂ values
in poetry vs prose?  Does the Straussian gap (poetry's tendency toward positive S₂) operate
uniformly across syntax, or is it concentrated in particular grammatical positions?

---

## Method

1. Reconstructed full text from GPT-2 subword tokens (leading space = word boundary).
2. POS-tagged reconstructed text with NLTK's averaged perceptron tagger (Penn Treebank tags).
3. Mapped each GPT-2 token to the NLTK word it overlaps with; inherited that word's broad POS category.
4. Aggregated avg_S₂, avg_surprisal, avg_entropy by POS category for poetry and prose separately.
5. Computed Δ = poetry avg_S₂ − prose avg_S₂ to isolate the poetry-specific Straussian gap per POS.

---

## Results

| POS | Poetry n | Poet AvgS₂ | Poet Surp | Prose AvgS₂ | Pros Surp | **Δ S₂** |
|-----|---------|-----------|----------|------------|---------|---------|
| ADJ | 299 | **+1.192** | 9.19 | −2.376 | 5.92 | **+3.567** |
| NOUN | 1,131 | **+1.686** | 9.03 | −1.855 | 5.27 | **+3.540** |
| ADV | 135 | +1.348 | 7.51 | −1.337 | 4.52 | **+2.686** |
| VERB | 601 | +1.124 | 7.76 | −1.210 | 4.57 | **+2.333** |
| AUX | 22 | +0.879 | 7.26 | −1.192 | 2.59 | **+2.071** |
| DET | 385 | −1.734 | 4.57 | −3.551 | 1.83 | **+1.817** |
| CONJ | 124 | −0.555 | 5.41 | −1.978 | 2.63 | **+1.423** |
| PREP | 391 | +0.111 | 5.59 | −1.071 | 2.85 | **+1.182** |
| OTHER | 716 | −1.015 | 3.75 | −1.939 | 2.82 | **+0.924** |
| PRON | 309 | −0.864 | 5.07 | −1.203 | 3.98 | **+0.340** |
| PUNCT | 509 | −1.856 | 3.11 | −1.793 | 1.65 | **−0.063** |

*Δ S₂ = Poetry avg_S₂ − Prose avg_S₂.  Positive = poetry is more surprising for that POS.*

---

## Key Findings

### 1. The Straussian gap is a content-word phenomenon

Adjectives (Δ = **+3.567**) and nouns (Δ = **+3.540**) show the largest poetry-vs-prose S₂ gaps —
nearly 3.5 nats of additional surprise concentrated in the two POS categories that carry most
of a poem's semantic content.  Adverbs (+2.686) and verbs (+2.333) are next.

**Interpretation**: Poets deviate from statistical expectation primarily by choosing unexpected
*things, qualities, actions, and manners* — not by reordering the grammatical frame.  The lexical
content layer is where the Straussian gap lives.

### 2. Pronouns are the great equalizer

Pronouns show the smallest gap (Δ = **+0.340**) of any open-class category.  Poetry's pronoun
choices (I, you, he, she, it, they) are nearly as predictable as prose's.  This makes sense:
a pronoun's referent is constrained by prior discourse, leaving little room for surprise
regardless of register.

### 3. Punctuation is poetry-agnostic

Punctuation has Δ ≈ **−0.063** — essentially zero.  Poets are no more or less surprising in
their use of periods, commas, and colons than prose writers are.  The poetic license extends
to words, not marks.

### 4. Even determiners show a significant gap

Determiners — the most predictable class — still show Δ = **+1.817**.  Prose determiners are
extremely predictable (avg_S₂ = −3.551), while poetry determiners are only moderately
predictable (−1.734).  This suggests that even the smallest grammatical choices ('a' vs 'the',
definite vs indefinite) carry more information in poetry than in prose.

### 5. Absolute poetry rankings: nouns are the surprisal kings

Within poetry alone, the absolute S₂ ranking by POS:

| POS | Poet AvgS₂ |
|-----|-----------|
| NOUN | **+1.686** |
| ADV | +1.348 |
| ADJ | +1.192 |
| VERB | +1.124 |
| AUX | +0.879 |
| PREP | +0.111 |
| CONJ | −0.555 |
| PRON | −0.864 |
| OTHER | −1.015 |
| DET | −1.734 |
| PUNCT | −1.856 |

Nouns have the highest average S₂ in poetry (+1.686) despite not having the highest
surprisal (adjectives do: 9.19 vs nouns 9.03).  Nouns carry more *net* surprise because
their contexts are less uncertain on average than adjective contexts (7.34 entropy vs 8.00).

---

## Theoretical Implications

This finding supports a **content-frame dissociation** model of poetic deviation:

- **Content layer** (nouns, verbs, adjectives, adverbs): high Straussian gap.
  Poets systematically choose unexpected entities, events, qualities, and modifiers.
- **Grammatical frame** (determiners, conjunctions, prepositions, pronouns):
  lower Straussian gap.  The syntactic skeleton is less distinctive.
- **Punctuation**: zero Straussian gap.  Purely structural; poets don't use
  punctuation to surprise.

In DeDeo's framework, this suggests that poetic *meaning-making* is principally achieved
through lexical substitution into conventional syntactic frames — the frame guides the reader's
expectation, and the unexpected content word at the frame's slot is the Straussian moment.

---

## Suggested Next Steps

1. **Slot-filling analysis**: For the highest-S₂ noun/adj moments, characterize the
   *semantic category* of what GPT-2 expected vs what the poet chose
   (e.g. expected ANIMATE noun → got ABSTRACT noun).
2. **Verb aspect and transitivity**: Do transitive verbs have higher S₂ than intransitive?
   Do action verbs differ from stative verbs?
3. **POS × Era interaction**: Do specific eras exploit particular POS differently?
   (e.g., do imagist poets have especially high-S₂ nouns vs surrealists high-S₂ verbs?)
4. **Syntactic depth**: Does S₂ correlate with depth in the parse tree? (Would need a
   dependency parser like spaCy.)
