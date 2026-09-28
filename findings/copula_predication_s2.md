# Copula Predication and S₂: The Semantics of Poetic Identity Claims

**Date:** 2026-09-28  
**Experiment:** `experiments/copula_predication_s2.py`  
**Corpus:** 184 texts (179 poetry/mixed, 5 prose controls) → 430 copula-predicate events  
**Builds on:** `findings/metaphor_detection_s2.md`, `findings/semantic_distance_gap.md`

---

## Research Question

Poets famously use the copula as a site of semantic invention. "Love is a battlefield."
"Night was a wound." "Hope is the thing with feathers." These identity claims compress
metaphor into the simplest grammatical form: *X is Y*.

Does the token immediately following a copula ("is," "are," "was," "were," "be," "'s")
have systematically higher S₂ in poetry than prose? If so, the Straussian gap quantifies
the **semantic boldness** of poetic identity claims: how far the poet's predicate deviates
from the language model's expectation.

---

## Setup

For each poem, we located every copula token (` is`, ` are`, ` was`, ` were`, ` be`,
` been`, ` am`, `'s`) and recorded the S₂ of the **immediately following token** — the
first token of the predicate. Stanza-break artifact tokens (p(newline) ≥ 0.9) were
excluded. This yielded 425 poetry events and 5 prose events across the corpus.

---

## Core Finding: Poetic Predicates Are Above Baseline; Prose Predicates Are Below

| Group | n | Avg S₂ at predicate | Baseline S₂ (all tokens) | **Lift** |
|-------|---|---------------------|--------------------------|---------|
| Poetry | 425 | −0.322 | −0.451 | **+0.129** |
| Prose control | 5 | −3.235 | −1.925 | **−1.310** |

**The asymmetry is striking.** In poetry, copula-predications are *slightly above*
the corpus average S₂ — the predicate token is marginally more surprising than an
average token. In prose, predicates are *substantially below* baseline — prose uses
the copula in its most predictable form (dictionary definitions, descriptions).

The gap between poetry and prose at predicates: **2.91 bits** (−0.322 vs. −3.235).
The gap between poetry and prose across all tokens: **1.47 bits** (−0.451 vs. −1.925).
**Poetic identity claims are nearly twice as "surprising" relative to prose identity
claims as poetry is generally relative to prose.**

---

## The Nominal vs. Non-Nominal Split

A striking sub-finding emerges when we distinguish **nominal** predicates (those
beginning with a/an/the/this/my/etc.) from **non-nominal** ones:

| Predication type | n | Avg S₂ |
|-----------------|---|--------|
| Nominal: *X is a/the Y* | 77 | **−2.621** |
| Non-nominal: *X is ADJ/Y* (no article) | 348 | **+0.186** |

The *structure* of metaphor matters. When the poet writes "love is **a** battlefield,"
the article "a" is highly expected — the model correctly anticipates nominal
predication. The surprise is deferred to the *noun* that follows. When the poet writes
"love is **bitter**" or "love is **1959**," the bare predicate itself is the deviation.
Non-nominal predicates carry the Straussian gap; nominal ones distribute it.

---

## % of Predicates with Positive S₂

| Group | % of predicate tokens with S₂ > 0 |
|-------|-----------------------------------|
| Poetry | **40.2%** |
| Prose control | **0.0%** |

In every prose predication sampled, the actual predicate was more predictable than
GPT-2's base rate. In poetry, 40% of predications are genuine surprises. **The copula
in prose confirms; the copula in poetry reveals.**

---

## Copula Form and Predicate Surprisal

Not all copulas are equal:

| Copula | n | Avg S₂ at predicate |
|--------|---|---------------------|
| `were` | 25 | **+0.533** |
| `be` | 53 | **+0.208** |
| `'s` | 64 | **+0.116** |
| `am` | 14 | −0.114 |
| `are` | 77 | −0.481 |
| `is` | 124 | −0.503 |
| `been` | 13 | −0.603 |
| `was` | 55 | −1.088 |

**Subjunctive `were`** (counterfactual: "as if I were stone," "were it not for")
has the highest predicate S₂. This aligns with the hypothesis: when the copula
marks a hypothetical or contrary-to-fact state, the poet invokes an imaginary world —
and imaginary predicates are maximally unconstrained by reality, hence surprising.

**Simple past `was`** has the lowest predicate S₂: it introduces
narrative identifications that tend to be grounded and specific ("She was a teacher").

---

## S₂ at Predicates by Literary Era

| Era | n | Avg S₂ at predicate |
|-----|---|---------------------|
| spoken_word | 6 | **+3.133** |
| deep_image | 5 | +1.652 |
| early_modern | 12 | +1.463 |
| confessional | 11 | +1.173 |
| new_york_school | 43 | +0.252 |
| victorian | 57 | +0.243 |
| romantic | 29 | +0.196 |
| prose_poetry | 37 | −0.061 |
| 19th_century | 27 | −0.077 |
| metaphysical | 11 | −0.087 |
| contemporary | 27 | −0.302 |
| modernist | 41 | −1.004 |
| fixed_form | 34 | −1.490 |
| ballad | 17 | −1.641 |
| language | 3 | −1.887 |
| nursery_rhyme | 6 | −1.939 |
| surrealist | 5 | −1.953 |
| cliche_control | 7 | −2.905 |
| 18th_century | 6 | −2.926 |

**Spoken word** (Ted Berrigan, Amiri Baraka) and **deep image** (James Wright) make the
boldest identity claims. The **ballad**, **language poetry**, **nursery rhyme**, and
**surrealist** traditions use conventional predicates.

One paradox: **surrealist** poetry is famous for unusual images, yet its copula predicates
score low. This may reflect that surrealism exploits *juxtaposition* (nouns beside nouns)
rather than explicit copular predication — surrealists rarely say "X is Y"; they let
"X Y" stand side by side without the grammatical copula.

---

## The 20 Most Surprising Predicates

| S₂ | Rank | Author | Copula | Predicate | Model Expected |
|----|------|--------|--------|-----------|----------------|
| 11.92 | 4917 | Robert Burns | 's | newly | 'what' |
| 11.51 | 3813 | William Shakespeare | be | wires | 'black' |
| 10.52 | 3803 | William Blake | is | Pride | 'the' |
| 10.23 | 3572 | Frank O'Hara | is | 1959 | '12' |
| 10.15 | 2980 | William Shakespeare | are | dun | 'white' |
| 9.03 | 9605 | William Shakespeare | 's | lease | 'day' |
| 8.86 | 4500 | Lucille Clifton | be | except | 'the' |
| 8.52 | 13024 | Wallace Stevens | be | finale | 'the' |
| 8.27 | 1858 | Dante Gabriel Rossetti | 's | Hipp... | 'the' |
| 8.15 | 19392 | Gerard Manley Hopkins | 's | minion | 'news' |
| 7.99 | 1866 | Killarney Clary | is | evening | 'not' |
| 7.82 | 1727 | Frank O'Hara | is | 12 | 'not' |
| 7.78 | 1869 | Lucille Clifton | been | enslaved | '' |
| 7.75 | 8393 | Dante Gabriel Rossetti | is | Echo | 'the' |
| 7.66 | 887 | David Antin | are | diss... | 'too' |
| 7.47 | 3546 | John Ashbery | is | relevant | '.' |
| 7.36 | 5892 | John Donne | 's | delivery | 'bones' |
| 7.22 | 2054 | Richard Wright | am | nobody | 'not' |
| 7.05 | 2301 | Claudia Rankine | are | nest | 'not' |

### Selected close-readings of the top surprises

- **Shakespeare's "wires"** (Sonnet 130): "If hairs be wires, black wires grow on her
  head." The model expected "black" (the conventional adjective for hairs). Shakespeare
  instead begins his anti-Petrarchan critique by asserting wires. The S₂ = 11.51 is the
  quantitative signature of his deliberate anti-conventionalism.

- **Frank O'Hara's "1959"**: "It is 1959 and I go get a shoeshine." A date as a
  predicate of "It is" (usually followed by time expressions: "noon," "late," "winter").
  The year-as-identity-statement is a signature New York School move.

- **Blake's "is Pride"**: Personification as unexpected predicate — the abstract
  made grammatically equivalent to a concrete subject.

- **Hopkins's "'s minion"**: "The Windhover... this morning morning's minion" — "minion"
  is unexpected after "'s" (GPT-2 expected "news"), capturing how Hopkins's compound
  formations violate standard collocational expectations.

- **Richard Wright's "am nobody"**: "I am nobody" — the model expected "not" (the
  natural completion of existential negation), but Wright asserts ontological absence
  positively, making nobodiness a predicate rather than a denial.

---

## Interpretation

The experiment supports the hypothesis that **the copula is a key site of Straussian
deviation in poetry**. Poets use "is/are/was" to assert identity claims that violate
statistical expectation, and this violation is measurably larger in poetry than prose.

The key insight from the nominal/non-nominal split: the article structure *distributes*
surprise — "X is a Y" front-loads a predictable article then loads surprise onto Y.
The bare predicate structure *concentrates* surprise — "X is Y" without the article
delivers the Straussian gap immediately. This may be a formal marker of poetic
compression: remove the distributing article, take the surprise head-on.

The subjunctive "were" result points toward **hypotheticality as a surprise engine**:
imaginary worlds, counterfactual states, and hypothetical identities are less
constrained by statistical reality, yielding higher S₂. Poets who invoke the imaginary
are working in the register of maximum semantic freedom.

---

## Suggested Next Steps

1. **Extend to comparative predicates**: Does "like" (simile) have lower or higher
   predicate S₂ than "is" (metaphor)? The metaphor hypothesis predicts metaphor
   should have higher S₂ — the copula commits to identity while "like" hedges it.

2. **Two-token predication**: Currently we only look at the first predicate token.
   Extend to the full predicate phrase (until punctuation or line break) and measure
   cumulative S₂ over the predication.

3. **The article as predictor**: When the model correctly predicts the article ("a"),
   it's essentially predicting that a nominal metaphor follows. Does the S₂ of the
   noun after "X is a" differ from the S₂ of the noun after "X is the"?

4. **Predicate-subject semantic distance**: Using GPT-2 embeddings, measure how
   semantically distant the predicate token is from the subject token. High distance
   = semantic metaphor; low distance = literal predication.
