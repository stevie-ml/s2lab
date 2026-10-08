# Prediction Field Homogeneity: The Grammar-vs.-Image Gap

**Date:** 2026-10-08  
**Experiment:** `experiments/prediction_field_homogeneity.py`  
**Corpus:** 25,081 artifact-free tokens across 222 poems (control excluded)  
**Builds on:** `findings/semantic_field_of_surprise.md`

---

## Research Question

When GPT-2's top-10 predicted tokens all belong to the same *lexical class* (function word,
punctuation, or content word), does breaking that coherent prediction field yield systematically
higher S₂ than breaking a split prediction field? And does it matter which class the model
expects — grammar vs. content?

This asks not just *whether* the poet surprises, but *what structure of expectation* they
are breaking.

---

## Method

For each artifact-free token, the top-10 alternatives were classified into:
- **Function words**: grammatical infrastructure (articles, conjunctions, prepositions, pronouns, auxiliaries)
- **Punctuation**: commas, periods, colons, dashes, etc.
- **Content words**: nouns, verbs, adjectives, adverbs — lexical items
- **Whitespace/newlines**: line-break tokens

"Prediction field homogeneity" = probability mass concentration in the dominant class.
- **High** (>70% mass in one class): GPT-2 strongly expects a specific lexical type
- **Medium** (45–70%): moderate preference
- **Low** (<45%): prediction field is split across classes

"Matches" means poet wrote a token in the same class as the dominant predicted class.
"Breaks" means poet crossed into a different class.

---

## Central Finding: The Grammar-vs.-Image Gap Is Asymmetric

### S₂ by Field Type × Poet's Class Choice

| GPT-2 Expected | Poet Chose | n | Mean S₂ | Median | Pos% |
|---|---|---|---|---|---|
| function word | function word | 6,390 | **−1.889** | −2.289 | 18.6% |
| function word | content/other | 4,547 | **+1.619** | +1.121 | 60.2% |
| punctuation | punctuation | 2,106 | **−1.994** | −2.165 | 9.9% |
| punctuation | content/other | 1,415 | **+1.356** | +0.543 | 56.2% |
| content word | content word | 7,234 | **−0.040** | −0.560 | 37.8% |
| content word | function/punct | 1,038 | **−0.613** | −1.183 | 35.5% |
| whitespace | whitespace | 1,768 | **−2.126** | −1.989 | 0.5% |
| whitespace | content/other | 583 | **+3.228** | +1.746 | 65.9% |

### The Consensus-Break S₂ Premium

When GPT-2 strongly predicts function words (high homogeneity, >70% mass), and the
poet installs a content word instead:

| Behavior | n | Mean S₂ |
|---|---|---|
| Break strong function consensus | 2,615 | **+2.656** |
| Match strong function consensus | 5,107 | **−1.921** |
| Mixed prediction field (low homogeneity) | 725 | **−0.809** |

**Consensus-break S₂ premium: +4.578 bits**

---

## The Asymmetry: Grammar-Breaking vs. Image-Breaking

The data reveals a fundamental asymmetry:

1. **Breaking grammar expectation → high S₂** (+1.619 for function field break, +2.656 for strong consensus break)
2. **Breaking content expectation → near-zero or negative S₂** (−0.613 when GPT-2 expected content word but poet writes function)

When GPT-2 expects structural scaffolding (function words) and the poet installs an image
instead, the information gain is enormous. But when GPT-2 expects an image and the poet
installs structural scaffolding, the S₂ is actually *negative* — the poet has chosen something
more predictable than the context warranted.

This directional asymmetry shows that **poetic surprise is not symmetric between grammatical
and lexical choices**. The Straussian gap is primarily a *grammar-vs.-image gap*: language
statistics expect connective tissue, and poets substitute concrete vision.

---

## S₂ by Number of Lexical Classes in Top-10 Predictions

Counterintuitively, tokens where GPT-2's top-10 predictions belong to only **one lexical class**
show the *highest mean S₂* — not the lowest:

| Classes in top-10 | n | Mean S₂ | Pos% |
|---|---|---|---|
| 1 (maximum coherence) | 8,129 | **−0.109** | 30.3% |
| 2 | 11,066 | −0.435 | 35.6% |
| 3 | 5,126 | −0.649 | 34.6% |
| 4 (maximum diversity) | 760 | −0.996 | 31.7% |

This seems paradoxical — shouldn't a unified prediction field be easier to confirm (lower S₂)?
But the answer lies in **asymmetric variance**: a coherent single-class field creates two extreme
outcomes — either the poet confirms it (very low S₂, often < −2) or breaks it (very high S₂,
often > +2). The high-S₂ cases dominate the mean because of their extreme values. When
the prediction field is split across 4 classes, the poet can't create as large a contrast in
either direction — entropy is already high, so even a surprising choice yields lower S₂.

---

## Content-Word Consensus: What Do Poets Choose?

When GPT-2 strongly expects a content word (6,523 positions), what do poets write?

| Poet chose | n | Mean S₂ |
|---|---|---|
| content word (same class) | 6,046 | −0.116 |
| function word | 309 | +0.462 |
| punctuation | 93 | +0.653 |
| whitespace/newline | 75 | +2.181 |

When GPT-2 expects a content word and the poet chooses to break with a line break instead,
S₂ = +2.181 — this is the enjambment-at-content-expectation effect. The model expected
the poem to continue with vocabulary; instead the poet turned to white space.

---

## Interpretation

The grammar-vs.-image gap has a specific information-theoretic structure:

**Grammar has narrower prediction fields.** When GPT-2 expects a function word, its top
predictions are tightly clustered (high field homogeneity), leaving little entropy "budget"
for the poet. The poet's content word choice is therefore maximally surprising — they have
violated not just the specific prediction but the entire syntactic category.

**Content has wider prediction fields.** When GPT-2 expects a content word, its top predictions
are spread across many specific words (high entropy), reducing the "gap" between surprisal and
entropy. Even a genuinely unusual content word doesn't push S₂ as high, because the model was
already allocating probability mass across many options.

**Poetic surprise is structurally grammar-defying, not content-selecting.** The deepest
Straussian gaps emerge not from choosing an unusual image but from refusing to supply the
grammatical infrastructure that language statistics demand.

---

## Connection to Prior Findings

- `findings/semantic_field_of_surprise.md` showed that COLOR and SOUND words
  are over-represented at high-S₂ positions. This finding explains *why*: at those positions,
  GPT-2 expected a function word (grammar), and the poet delivered a sensory image instead.
  The surprise is the category switch, not the specific image choice.

- `findings/straussian_gap_taxonomy.md` characterized what was suppressed. This finding
  reveals the *structural context* of that suppression: the suppressed alternatives were
  grammatically coherent (all function words), while the poet's choice was grammatically
  incoherent with the field.

---

## Suggested Next Steps

1. **Verify the directional asymmetry by era**: Do experimental poets (Language, Surrealist)
   show proportionally more content→grammar substitutions (which yield *lower* S₂) than
   traditional poets? If so, they may be practicing the *opposite* of the Straussian move.

2. **Map the grammar-vs.-image gap across line positions**: Does the grammar-vs.-image
   gap correlate with enjambment? At line breaks, is the grammar-vs.-image substitution
   most common at line-initial positions (where the poet can avoid expected connectives)?

3. **Test the premium by homogeneity tier**: Does the +4.578 bit premium increase with
   homogeneity? A prediction field with 90%+ function word mass should yield an even larger
   premium than 70–90%.
