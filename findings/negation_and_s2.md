# Negation and S₂: The Paradox of the Poetic "Not"
**Date:** 2026-09-08  
**Experiment:** `experiments/negation_s2.py`  
**Corpus:** 95 poems, 31 containing clear negation tokens  

---

## Question

When a poet says "not X," they invoke X while denying it. The negated term
is both present and absent — a pure Straussian structure where what is
*suppressed* (the affirmation) bleeds through the denial. Does information
theory capture this paradox?

Specifically: do negation tokens and the words that follow them show
systematically different S₂ values compared to the corpus baseline?

---

## Method

Identified six core negation words: **not, no, never, nothing, none, neither, nor, without**.
For each occurrence in the corpus, computed:
- S₂ of the negation token itself
- S₂ of the immediately following token (the "negated term")
- GPT-2's top predicted token at both positions

Corpus baseline: mean S₂ = **+0.289** across all 95 poems.

---

## Key Results

### 1. Negation tokens are themselves near-baseline (slightly below)

| Position | Mean S₂ | vs. Baseline |
|---|---|---|
| Negation token | -0.005 | -0.294 |
| Token after negation | -0.676 | -0.965 |
| Global baseline | +0.289 | — |

Both the negation word and what follows it are on average **below baseline**. This
makes structural sense: once a sentence has a certain shape, negation is often
grammatically expected, and the negated noun/verb is constrained to a
predictable semantic field. The model "expects" the cliché: "no *longer*",
"not *here*", "nothing *can*."

### 2. BUT: negation word choice itself varies enormously

| Negation word | Count | Own S₂ | Post S₂ |
|---|---|---|---|
| nor | 5 | **+4.074** | -2.389 |
| never | 4 | **+1.602** | +0.036 |
| nothing | 5 | +0.560 | +0.404 |
| no | 14 | +0.992 | +0.890 |
| without | 3 | -0.943 | -1.165 |
| **not** | 24 | **-1.774** | **-1.430** |
| neither | 1 | +1.679 | -2.733 |

**"nor"** (S₂ = +4.074) is the most surprising negation word in the corpus — 
it appears rarely and in contexts where GPT-2 strongly expects something else.
"**not**" (S₂ = -1.774) is the most predictable negation — so common and
grammatically expected that the model has high confidence at those positions.

**Implication**: poets who reach for "nor" or "neither" are making a higher-S₂
choice than those who rely on "not." The mere word selection signals whether
the negation is stylistically marked.

### 3. Top high-S₂ post-negation moments

| Neg | Token After | S₂ | GPT-2 Expected | Poem |
|---|---|---|---|---|
| no | disaster | **+9.587** | "longer" | *One Art* (Bishop) |
| No | head | **+6.994** | "one" | *The Listeners* (de la Mare) |
| not | God | **+5.952** | "." | *Yet Do I Marvel* (Cullen) |
| no | chalk | **+4.663** | "more" | *Self-Portrait in a Convex Mirror* (Ashbery) |
| not | reject | **+4.422** | "forget" | *The One Thing That Can Save America* (Ashbery) |
| never | read | **+4.335** | "to" | *My Last Duchess* (Browning) |
| Nothing | beside | **+3.945** | "can" | *Ozymandias* (Shelley) |

These are the moments where **the poet's chosen negated term is maximally
unexpected**. GPT-2 predicted "no longer" (Bishop), "No one" (de la Mare),
"nothing can" (Shelley) — the canonical phrases. The poets detonated
something else entirely.

---

## Case Studies

### Elizabeth Bishop's "no disaster" (*One Art*, S₂ = +9.587)

The refrain "The art of losing isn't hard to master" establishes a low-entropy
channel. When Bishop writes "no disaster," GPT-2 expects "no longer" (the
conventional phrase for modulated loss). "Disaster" — with its overtones of
catastrophe — is maximally unexpected as the negated term. The irony compounds:
she says "no disaster" in a context where disaster is exactly what has occurred.
The high S₂ enacts the poem's repression: the affirmation of disaster bleeds
through its own denial.

### Countee Cullen's "not God" (*Yet Do I Marvel*, S₂ = +5.952)

GPT-2 predicts a sentence-closing punctuation "." at this position. Instead,
Cullen invokes the divine as the *object* of the negation — "I do not marvel...
at God." The high S₂ captures the audacity of the move: not only is "God" an
unusual post-negation token; it's unexpected as a direct object at all. The
sonnet's entire meditative structure depends on this high-S₂ invocation of what
is both denied and affirmed.

### Shelley's "Nothing beside remains" (*Ozymandias*, S₂ = +3.945)

GPT-2 predicts "Nothing can" — a conventional expression of limitation. Shelley
writes "Nothing beside remains," where "beside" (as preposition/adverb) is
genuinely strange in this position. The entropy of the ruins is embedded in the
syntax's unexpectedness.

---

## The "Negation Channel" Hypothesis

Results suggest a two-stage structure in poetic negation:

1. **The channel opens**: The negation word (especially "not") lowers entropy
   by signaling a grammatical frame. The reader (and GPT-2) now expect a
   predictable semantic field: "no more," "not here," "nothing can."

2. **The poet detonates**: The actual negated term either conforms (low S₂,
   conventional) or violates (high S₂, Straussian). When it violates, the
   contrast is amplified by the low-entropy channel that preceded it.

The cliché "no longer" sets up the expectation so that "no disaster" lands
harder. The negation *frame* does rhetorical work precisely because it's
predictable. 

This is a compressed instance of the general S₂ arc: local entropy suppression
followed by surprise.

---

## Poet Profiles

| Author | Neg. count | Rate (%) | Baseline S₂ | Post-neg S₂ |
|---|---|---|---|---|
| Baudelaire | 5 | 3.38 | -0.342 | **-2.172** |
| Rossetti | 4 | 2.86 | +0.086 | +0.150 |
| T.S. Eliot | 4 | 1.61 | +0.060 | **-1.770** |
| Ashbery | 16 | 1.24 | -0.259 | -0.864 |
| Dickinson | 3 | 0.92 | +0.635 | -0.610 |

**Baudelaire and Eliot** have the lowest post-negation S₂, suggesting their
negations fall into conventional patterns — the negated terms are expected even
when the surrounding poetry is unpredictable. **Rossetti's** post-negation S₂
closely tracks her baseline, meaning negation doesn't alter her information
profile. **Ashbery** uses the most negations but they cluster at moderate
post-neg S₂, consistent with his mid-register information strategy.

---

## Summary Finding

> **Negation creates a low-entropy channel that amplifies downstream surprise.**
> The most common negation word ("not") is itself strongly predictable (S₂ = -1.77).
> But within this channel, poets can choose negated terms of extreme unexpectedness.
> The highest-S₂ post-negation moments — Bishop's "no disaster," Cullen's "not God,"
> de la Mare's "No head" — are all cases where the poet chose the last thing
> the model would expect after a negation. The negation itself may be the setup,
> not the punch.

---

## Next Steps

- Analyze the *semantic relationship* between GPT-2's predicted negated term and
  the poet's choice: are they antonyms? The same semantic field? Unrelated?
- Test whether poets who use negation strategically (high post-neg S₂) also show
  higher overall S₂ signatures
- Compare negation in prose vs poetry: does the "negation channel" effect differ?
- Look at morphological negation (un-, dis-, non-) — these create negation inside
  the token rather than syntactically, hiding the negation structure from GPT-2
