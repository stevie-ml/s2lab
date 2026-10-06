# The Rhetoric of Totality vs. Qualification: Absolute and Hedged Language in Poetry

**Date:** 2026-10-06  
**Experiment:** `experiments/absolute_vs_hedge_s2.py`  
**Corpus:** 204 English poems, 21,439 artifact-free tokens  
**Builds on:** `findings/straussian_gap_taxonomy.md`, `findings/within_poem_type_arc.md`

---

## Research Question

Poetry is famous for totalizing gestures — "I contain multitudes", "Nothing gold can stay",
"Forever and a day." But epistemic hedges appear too: Keats's "seems to me rich", Dickinson's
"probably", Stevens's "seems." Does grand poetic assertion *cost* surprisal or *save* it?
Are hedges surprising because poetry usually speaks confidently?

We tested two classes against the corpus baseline:

**Absolute terms**: "always", "never", "all", "nothing", "everything", "everyone", "nowhere",
"forever", "eternal", "infinite", "immortal", "perfect", "utterly", "no", "every", "whole"

**Hedge terms**: "perhaps", "maybe", "possibly", "probably", "almost", "seems", "seem",
"as", "like", "though", "would", "could", "should", "might", "appear", "seldom"

Baseline mean S₂ across all poetry: **−0.44** (median −1.23, 33.6% positive)

---

## Finding 1: Both Classes Beat the Baseline — But Barely

| Class | n | Mean S₂ | Median | % Positive |
|-------|---|---------|--------|------------|
| **Baseline (all poetry)** | 21,439 | −0.44 | −1.23 | 33.6% |
| **Absolute terms** | 220 | **+0.026** | −0.541 | **43.2%** |
| **Hedge terms** | 233 | **−0.031** | −0.483 | **41.2%** |

Both classes are above baseline by ~0.47 bits, with similar positive-S₂ rates (~42% vs 34%).
This means **both totalizing and qualifying language are equally elevated** relative to
ordinary poetry tokens — a near-symmetry that masks a striking internal split.

---

## Finding 2: The Internal Split — Frequency Predicts Cheapness

The key pattern: **high-frequency tokens in each class are cheap; low-frequency ones are expensive.**

### Absolute Term Breakdown

| Token | n | Mean S₂ | % Positive | Notes |
|-------|---|---------|------------|-------|
| "all" | 72 | **−0.738** | 33.3% | *cheapest* — a function-word absolute |
| "no" | 56 | **−0.500** | 37.5% | also below baseline |
| "never" | 22 | +0.090 | 50.0% | just above 0 |
| "every" | 17 | +0.307 | 41.2% | |
| "nothing" | 17 | **+0.930** | 58.8% | rhetorical absolute |
| "immortal" | 4 | **+0.913** | 50.0% | |
| "always" | 3 | +0.665 | 33.3% | |
| "perfect" | 3 | **+1.100** | 66.7% | *most expensive absolute* |

**All** (n=72) and **no** (n=56) are BELOW baseline — GPT-2 has learned they belong to
the poetic register and predicts them frequently. **Nothing**, **immortal**, and **perfect**
are expensive (+0.9–1.1): rarer, more rhetorical, and therefore more surprising.

### Hedge Term Breakdown

| Token | n | Mean S₂ | % Positive | Notes |
|-------|---|---------|------------|-------|
| "should" | 11 | **−1.964** | 9.1% | *cheapest* — pure modal obligation |
| "as" | 101 | −0.692 | 33.7% | simile marker, expected |
| "could" | 12 | −0.450 | 25.0% | |
| "like" | 41 | −0.300 | 39.0% | |
| "would" | 17 | +0.236 | 47.1% | |
| "though" | 21 | **+0.735** | 66.7% | concessive turn |
| "seem" | 5 | +0.701 | 60.0% | |
| "might" | 3 | **+2.846** | 66.7% | |
| "seems" | 4 | **+2.341** | 50.0% | |
| "probably" | 3 | **+5.479** | 100.0% | *most expensive hedge* |

**Should**, **as**, and **could** are cheap: they function structurally (obligation, comparison,
counterfactual) and GPT-2 predicts them easily. But **seems**, **might**, and **probably** are
extremely expensive — because they import *prose epistemic uncertainty* into poetic space.

---

## Finding 3: "Probably" Is the Most Surprising Hedge in Poetry

The single most surprising hedge token is **Emily Dickinson's "probably"** in
*A Route of Evanescence*, at **S₂ = +14.9**:

> *"The Mail from Tunis, **probably**,"*

The model assigned P("probably") ≈ 0; its top prediction was newline (76.5%):
the poem was expected to end the line there. Dickinson instead inserts "probably" as a
parenthetical — a deadpan bureaucratic qualifier in the middle of a poem about a hummingbird.

This is the register violation thesis in miniature: poetry is expected to speak with
authority; "probably" signals doubt in a register that doesn't permit it.

**Edgar Allan Poe's "somewhat"** (S₂ = +10.9) shows the same mechanism from the Gothic side:

> *"I heard a tapping **somewhat** louder"*

The Gothic mode amplifies dread through certainty; "somewhat" introduces an almost comic
understatement at exactly the wrong moment.

---

## Finding 4: "No" Can Spike When It Inverts a Syntactic Expectation

Despite its average cheapness (mean S₂ = −0.50), **"no"** produces the corpus's highest
absolute-term spike at **S₂ = +11.7** in Rossetti's *Remember*:

> *"Remember me when **no** more day"*

After "when", the model expected "I" (85%) or "you" (9%). "No" does two things at once:
it denies the object of the sentence (day) and performs the poem's entire argument (my
absence will be total). The deviation maps onto the semantic weight of the absolute claim —
"no" is doing real work here, not filling a formula.

---

## Finding 5: Modal Hierarchy Tracks Poetic Register

The cheapest hedge is **"should"** (mean S₂ = −1.964, only 9.1% positive). Modal verbs
follow a clear hierarchy in terms of poetic expectation:

| Modal | Mean S₂ | Register function |
|-------|---------|-------------------|
| should | −1.964 | obligation — expected in instruction |
| could  | −0.450 | counterfactual — expected in subjunctive verse |
| would  | +0.236 | conditional — borderline |
| might  | +2.846 | epistemic possibility — prose-register |

**Should** is effectively invisible — GPT-2 predicts it readily in verse contexts.
**Might** costs more than **nothing** (mean S₂ +0.93): introducing epistemic possibility
is as surprising as making an absolute claim about immortality.

---

## Finding 6: Era and Author Effects

### Era — Absolute Terms

| Era | Abs mean S₂ | n | Hedge mean S₂ | n |
|-----|------------|---|--------------|---|
| 19th_century | +1.146 | 23 | +3.009 | 11 |
| contemporary | +1.155 | 9 | −0.387 | 2 |
| modernist | +0.555 | 19 | −0.303 | 27 |
| new_york_school | −0.107 | 18 | −0.223 | 18 |
| romantic | −0.588 | 25 | −0.678 | 23 |
| victorian | −0.511 | 32 | −1.427 | 43 |
| fixed_form | −1.549 | 11 | −2.927 | 6 |
| metaphysical | −2.268 | 5 | −0.432 | 11 |

Victorian and fixed-form poetry uses BOTH absolute and hedge language cheaply — the
inherited rhetorical forms make these words predictable. The 19th century American corpus
(Dickinson, Poe) produces the most surprising hedges (+3.0) — driven by Dickinson's
"probably" and Poe's "somewhat."

### Author — Absolute Ratio and S₂

| Author | Abs mean | Abs n | Hedge mean | Hedge n | Abs ratio |
|--------|---------|-------|-----------|---------|----------|
| William Blake | −1.611 | 14 | −1.053 | 3 | 0.82 |
| Edgar Allan Poe | **+1.482** | 14 | **+3.987** | 4 | 0.78 |
| Emily Dickinson | +1.091 | 4 | **+2.370** | 6 | 0.40 |
| John Ashbery | −0.107 | 18 | −0.242 | 16 | 0.53 |
| William Shakespeare | −0.244 | 10 | −1.578 | 6 | 0.62 |
| Alfred, Lord Tennyson | −1.428 | 8 | −2.364 | 10 | 0.44 |
| Thomas Wyatt | −1.115 | 4 | −0.240 | 8 | 0.33 |

Blake is the most absolutist (ratio 0.82) but his absolutes are CHEAP (−1.611): formulaic
use of "all", "no", "whole" in prophetic mode. Poe's absolutes are expensive (+1.482):
"never", "certainly" gain their power from surprising placement.

Dickinson uses more hedges than absolutes (ratio 0.40) but both classes are expensive for
her — she earns both kinds of language.

---

## Synthesis: Register Violation, Not Lexical Rarity

The organizing principle is **register violation**, not simple lexical frequency:

- A word is CHEAP when it belongs to the expected poetic register for that context.
  "All" and "should" are cheap because verse discourse normalizes them.
- A word is EXPENSIVE when it imports a foreign register into the poem.
  "Probably" and "somewhat" are prose epistemic markers — their presence in verse
  is itself the violation.

This extends the Straussian Gap taxonomy: the most expensive absolute terms are
not the grandest claims but the most specific ones ("perfect", "immortal"). The most
expensive hedge is not vague ("somewhat") but epistemically precise ("probably").

**Poetic authority is expressed not by the choice of absolute language, but by the
choice of absolute language at moments when the model did not expect it.** A poet who
writes "all" where the model expected "all" has earned nothing; a poet who writes "no"
where the model expected "I" has restructured the poem.

---

## Suggested Next Steps

1. **Absolute+hedge co-occurrence**: Do high-absolute poems also hedge more (oxymoron
   profile) or are absolute and hedging strategies exclusive?
2. **The cost of negation**: Track not-absolute constructions ("not all", "not never")
   — are negated absolutes cheaper than positive ones?
3. **"Probably" as poetic marker**: In which poems does Dickinson use the register
   violation pattern systematically? This may be an unremarked stylistic signature.
4. **Modal trajectory within poems**: Do poems use expensive modals (might, seems) at
   specific positions (openings vs. closures)?
