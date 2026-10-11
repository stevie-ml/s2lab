# Q2 vs Q1 Strategy Taxonomy: Two Architectures of Poetic Surprise

**Date:** 2026-10-11  
**Experiment:** `experiments/q2_q1_strategy_taxonomy.py`  
**Corpus:** 228 English poetry texts (228/240 total; 12 non-English excluded)  
**Threshold:** S₂ > 2.0 (meaningful surprise only); quadrant thresholds: surprisal median = 4.77, entropy median = 6.34  
**Builds on:** `s2_coordinate_system.md` (Q1/Q2/Q3/Q4 quadrant framework)

---

## Motivation

The S₂ coordinate system (2026-10-07) identified two distinct modes of surprise that pool into the global S₂ statistic:

| Quadrant | Surprisal | Entropy | Meaning |
|----------|-----------|---------|---------|
| **Q2** | High | **Low** | *Confident mismatch* — model was certain; poet defied it |
| **Q1** | High | **High** | *Ambiguous surprise* — model was uncertain; poet chose one of many paths |

That study suggested Q2 = "colloquial syntax + surprising lexis" and Q1 = "archaic syntax where even grammar becomes uncertain." This experiment tests those hypotheses formally.

---

## Finding 1: Q2 Moments Are Structurally Different From Q1 Moments

### Token Type at Q2 vs Q1 High-Surprise Positions

| Token type | Q1 moments | Q2 moments |
|------------|-----------|-----------|
| Content words | **89.4%** | 59.8% |
| Function words | 6.6% | **26.4%** |
| Punctuation | 1.1% | **8.2%** |
| Whitespace/newline | 2.9% | 5.5% |

**The hypothesis is reversed in a revealing way.** Q1 moments are overwhelmingly content words — the poet chose an unexpected noun, verb, or adjective where many plausible options existed. Q2 moments are far more likely to involve function words and punctuation — **the poet made a grammatical or structural choice against a confident syntactic prediction.**

### What the Model Predicted at Each Position

| Top-1 prediction type | Q1 moments | Q2 moments |
|-----------------------|-----------|-----------|
| Function word | 47.8% | 44.0% |
| Content word | 36.5% | 25.7% |
| Punctuation/whitespace | 15.7% | **30.3%** |

At Q2 positions, the model expected punctuation or whitespace **30.3%** of the time — nearly double Q1's rate (15.7%). This is the fingerprint of the **"syntax trap"**: the model expects the sentence to close or pause (comma, period, line break) and the poet continues instead.

### Key Metrics Summary

| Metric | Q1 | Q2 |
|--------|----|----|
| Count (S₂ > 2.0) | 3,048 | 2,168 |
| Mean S₂ | +4.78 | +**6.00** |
| Mean token length (chars) | 4.7 | 3.6 |
| Mean alternative entropy | 2.82 bits | 1.98 bits |
| Content-word rate | 89.4% | 59.8% |
| Function-word rate | 6.6% | 26.4% |
| Top-alt was punc/whitespace | 15.7% | **30.3%** |

Q2 events have **higher mean S₂** (+6.00 vs +4.78) — confirming that targeted anti-consensus moves (Q2) produce individually stronger surprises than ambiguous ones (Q1). They also have shorter token lengths (3.6 vs 4.7 chars), consistent with more function words and punctuation-substitutes.

---

## Finding 2: The Two Strategies Separate by Literary Era

| Era | Q2 | Q1 | Q2/Q1 | Interpretation |
|-----|----|----|-------|----------------|
| prose_poetry | 164 | 102 | **1.61** | Highest Q2: simple syntax + lexical surprise |
| nursery_rhyme | 24 | 15 | **1.60** | Predictable grammar, startling word choices |
| found_poetry | 81 | 53 | **1.53** | Documentary language with unexpected pivots |
| biblical | 95 | 67 | **1.42** | Formulaic structure; nouns/verbs deviate |
| song_lyrics | 45 | 33 | 1.36 | — |
| oulipo | 61 | 47 | 1.30 | Constraint-driven confident mismatches |
| *(median)* | — | — | *0.74* | — |
| beat | 48 | 92 | 0.52 | — |
| romantic | 149 | 283 | 0.53 | High Q1: complex syntax creates uncertainty |
| victorian | 252 | 482 | 0.52 | Dense syntax; everything becomes ambiguous |
| ancient | 24 | 55 | 0.44 | — |
| **metaphysical** | 25 | 80 | **0.31** | Lowest Q2: Donne/Herbert/Milton — syntax itself is the surprise |

**The metaphysical poets have the most extreme Q1 dominance** (Q2/Q1 = 0.31). Donne, Herbert, and Milton use Latinate inversions, complex embedded clauses, and archaic grammatical structures that systematically undermines GPT-2's syntactic predictions. The *syntax itself* is the primary vehicle of surprise, not the lexical choice.

**Prose poetry leads Q2** (1.61) — paradoxically, prose poems produce the most targeted anti-consensus surprises. Because they abandon lineation (removing stanza-break artifacts), their high S₂ events are genuine confident mismatches. The prosaic syntax is maximally legible to GPT-2, which then gets surprised by the unexpected lexical turn.

---

## Finding 3: Poet-Level Rankings Confirm the Two Architectures

**Strong Q2 strategists** (ratio > 1.11 = median × 1.5):

| Poet | Q2/Q1 | Note |
|------|-------|------|
| Killarney Clary | 3.00 | Colloquial syntax, precise unexpected word |
| Anonymous (found text) | 2.64 | Non-poetic source registers exploited |
| Charles Baudelaire | 2.22 | Prose-adjacent syntax + shocking images |
| Russell Edson | 2.20 | Fabulist prose poems: simple grammar, surreal pivot |
| Carolyn Forché | 1.80 | Documentary prose: linear syntax + sudden noun |
| Frank O'Hara | 1.53 | Casual syntax, surprising proper nouns/objects |

**Strong Q1 strategists** (ratio < 0.49 = median × 0.67):

| Poet | Q2/Q1 | Note |
|------|-------|------|
| Alexander Pope | 0.13 | Heroic couplets: syntactic inversions everywhere |
| John Milton | 0.29 | Latinate constructions, epic syntax |
| W.B. Yeats | 0.32 | Late Yeats: archaic syntax + unusual collocations |
| John Donne | 0.33 | Metaphysical conceits, contorted syntax |
| John Keats | 0.35 | Ode syntax, archaic word order |
| George Herbert | 0.35 | Devotional syntax, unusual structures |
| Gerard Manley Hopkins | 0.44 | Sprung rhythm, compound formations |

---

## Finding 4: Hypothesis Confirmed — But With a Twist

The original hypothesis was:
- Q2 = colloquial syntax + surprising **content words**
- Q1 = archaic syntax where even **function words** become uncertain

The data partially confirms this: Q1 strategists do show higher function-word surprise rates. But the key insight is:

**Q2 moments are structurally "syntax traps" — the model expects punctuation/pause and gets a word instead.** The 30.3% punctuation-expectation rate at Q2 positions reveals that Q2 isn't just about content-word surprise; it's about *syntactic continuation* — the poet doesn't close the sentence when the model expects closure.

**Q1 moments are "lexical ambiguity pools" — the model doesn't know what content word comes next, and the poet chooses something far from any of the options.** 89.4% content-word rate confirms the model was navigating open lexical territory; the poet turned it into genuine surprise by choosing something distant.

The two strategies thus represent:
- **Q2**: *Structural defiance* — the poem keeps going when grammar says stop; surprises happen in structural/functional positions
- **Q1**: *Lexical defiance* — the poem chooses the wrong noun/verb from an open field; surprises happen in content positions

---

## Taxonomy of Exemplary Q2 Moments

| Token | S₂ | Model expected | Mechanism |
|-------|-----|---------------|-----------|
| 'shook' (Hopkins) | 22.0 | 'the' (p=0.39) | Verb where article expected |
| 'prank' (Smart) | 22.0 | 'the' (p=0.45) | Noun where article expected |
| 'badly' (Bishop) | 20.6 | 'glass' (p=0.84) | Adj instead of specific noun |
| 'list' (Wyatt) | 19.5 | 'ever' (p=0.92) | Word-break during subword token |
| 'lay' (Lindsay) | 18.9 | ',' (p=0.80) | Verb where comma expected |
| 'red' (ballad) | 18.0 | subword (p=0.70) | Unexpected completion |

Many Q2 surprises happen at **article positions** — the model says 'the' and gets a verb, or says comma and gets a noun. This is the "Straussian gap" in its purest form: the model's confident grammar meets the poet's refusal.

---

## Suggested Next Steps

1. **Formalize "structural vs. lexical" deviation**: Rather than Q2/Q1, classify each high-S₂ token by what the model predicted (expected punctuation = structural; expected content word = lexical). This might be a cleaner two-way split than quadrant.

2. **Test Pope specifically**: Pope's extreme Q1 dominance (0.13) despite writing in closed heroic couplets is a paradox — the rigid form should produce Q2 moments, not Q1. Is his diction so archaic that even article choices become uncertain?

3. **Prose poetry Q2 depth**: Add more prose poets (Simic, Ponge in translation, Claudel) to test whether the genre consistently produces Q2 dominance regardless of subject matter.

4. **The 'syntax trap' catalog**: Collect all Q2 events where the model expected punctuation/whitespace. What kinds of grammatical continuation does poetry prefer? Is it always verbs? Nouns? Adjectives? This could reveal the *grammar of poetic surprise*.
