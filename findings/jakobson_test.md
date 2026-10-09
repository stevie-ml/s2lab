# The Jakobson Test: Selection vs. Combination Surprise in Poetry

**Date:** 2026-10-09
**Experiment:** `experiments/jakobson_test.py`
**Corpus:** 227 texts

---

## Motivation

Roman Jakobson's 1956 paper "Two Aspects of Language" identifies two fundamental axes of language:
- **Selection (metaphoric axis)**: choosing one item from a paradigmatic set of equivalents
- **Combination (metonymic axis)**: linking items in a sequential chain

Jakobson argued that poetry foregrounds the selection axis — the unexpected CHOICE replaces a predictable one. This has been the dominant model in poetics for 70 years.

Information theory offers an empirical test. Using the Q2/Q1 distinction from the S₂ coordinate system (see `s2_coordinate_system.md`):

- **Q2 (confident mismatch)**: the model was CERTAIN about what should come next (low entropy = stable syntactic frame), but the poet chose something unexpected. This is **selection surprise** — paradigmatic substitution in a clear syntactic slot.
- **Q1 (ambiguous surprise)**: the model was UNCERTAIN (high entropy = unstable combinatorial context), AND the poet still surprised it. This is **combination surprise** — the sequence itself was unusual.

**Jakobson Index** = Q2/Q1 ratio. High = selection-dominant (metaphoric). Low = combination-dominant (metonymic).

---

## Results: Poet Rankings by Jakobson Index

Medians (artifact-filtered): surprisal = 4.76 bits, entropy = 6.34 bits.

### Top Metaphoric Strategists (highest Q2/Q1)

| Poet | n | Q2% | Q1% | Q2/Q1 | C/C rate |
|---|---|---|---|---|---|
| Thomas Jefferson (found text) | 148 | 10.8 | 5.4 | **2.00** | 6.2% |
| Emmett Williams | 55 | 20.0 | 10.9 | **1.83** | 9.1% |
| **W.S. Merwin** | 60 | 23.3 | 13.3 | **1.75** | 21.4% |
| Russell Edson | 241 | 22.0 | 16.2 | **1.36** | 20.8% |
| Charles Baudelaire (trans.) | 146 | 21.2 | 17.8 | **1.19** | 12.9% |
| **Frank O'Hara** | 162 | 25.9 | 22.8 | **1.14** | 4.8% |

### Top Metonymic Strategists (lowest Q2/Q1)

| Poet | n | Q2% | Q1% | Q2/Q1 |
|---|---|---|---|---|
| Eugen Gomringer | 47 | 0.0 | 4.3 | **0.00** |
| Ernest Dowson | 81 | 2.5 | 44.4 | **0.06** |
| Ron Silliman | 50 | 4.0 | 56.0 | **0.07** |
| Vachel Lindsay | 91 | 3.3 | 39.6 | **0.08** |
| John Donne | 172 | 7.6 | 49.4 | **0.15** |
| William Blake | 567 | 8.5 | 45.5 | **0.19** |
| John Milton | 161 | 9.9 | 50.9 | **0.20** |
| Gerard Manley Hopkins | 544 | 11.0 | 47.2 | **0.23** |
| John Keats | 399 | 10.8 | 48.4 | **0.22** |
| Emily Dickinson | 312 | 14.1 | 44.2 | **0.32** |

---

## Finding 1: Jakobson Was Half-Right

The mapping of poets to the metaphoric/metonymic distinction partly confirms Jakobson's framework but with surprising reversals.

**Confirmed**: Merwin (1.75), O'Hara (1.14), Edson (1.36) are high-Jakobson poets — clear, colloquial syntax with surprising lexical choices. Their GPT-2 encounters **stable syntactic frames** (low entropy) and then gets a word it didn't expect.

**Reversed**: The poets classically associated with "metaphor-richness" — Keats (0.22), Hopkins (0.23), Blake (0.19), Milton (0.20), Donne (0.15) — score as strong **metonymic** strategists. These are among the lowest Jakobson indices in the corpus.

**Why?** Keats, Hopkins, Donne, and Milton use highly unusual syntax — Latinate inversions, archaic word orders, compressed appositions. Their unusual sequences raise GPT-2's entropy BEFORE the surprise, making their shocks Q1 (ambiguous) rather than Q2 (confident mismatch). Their innovation is combinatorial/sequential first, then lexical.

Merwin and O'Hara, by contrast, use simple, modern English syntax. The model becomes highly confident about what word should appear. Then the poet substitutes unexpectedly.

**The Jakobson Paradox**: The poets we call "metaphoric" in literary tradition (Keats, Hopkins, Donne) are informationally *metonymic* — they defamiliarize at the level of sequence/syntax. The poets we'd call "plain style" (Merwin, O'Hara, Edson) are informationally *metaphoric* — they defamiliarize at the level of word choice within clear syntactic frames.

---

## Finding 2: What Confident Mismatches Are Made Of

In Q2 (confident mismatch) positions, the substitution breakdown is surprising:

| Substitution type | Q2 count | Q2 % | Q1 % |
|---|---|---|---|
| Function → Function (different structural word) | 712 | **36.6%** | 19.2% |
| Function ← Content (de-lexicalization) | 582 | **29.9%** | 32.0% |
| Content ↔ Content (lexical swap) | 531 | **27.3%** | 44.5% |
| Content → Function (syntax-defy) | 123 | **6.3%** | 4.2% |

**Most striking finding**: The dominant mode of confident mismatch (Q2) is NOT "surprising content word" but **function-for-function shifts (36.6%)** — the model expected one preposition, pronoun, or conjunction and got a different one. The second largest category is de-lexicalization (29.9%) — a structural/function word replacing an expected content word.

In ambiguous-surprise positions (Q1), the dominant mode IS content-for-content (44.5%) — surprising nouns and verbs in already-uncertain contexts.

**Implication**: When poets have the model's full "attention" (Q2 = certain context), they most often choose unusual structural/relational words. When the model is already uncertain (Q1), poets mostly surprise at the content-word level.

This inverts the naive Jakobson prediction. Confident contexts are where poets do their most subtle structural work — choosing the "wrong" preposition, pronoun, or conjunction. Uncertain contexts are where they deploy striking content words.

---

## Finding 3: Era-Level Jakobson Index

| Era | n | Q2% | Q1% | Jakobson Index |
|---|---|---|---|---|
| concrete | 117 | 11.1 | 12.0 | **0.93** |
| biblical | 883 | 18.0 | 20.6 | **0.87** |
| prose_poetry | 934 | 18.8 | 24.0 | **0.79** |
| found_poetry | 952 | 14.6 | 20.3 | **0.72** |
| contemporary | 813 | 16.0 | 30.9 | **0.52** |
| german_expressionist | 283 | 13.4 | 49.8 | **0.27** |
| haiku | 293 | 11.9 | 47.1 | **0.25** |
| romantic | 2081 | 11.3 | 45.7 | **0.25** |
| surrealist | 57 | 8.8 | 42.1 | **0.21** |
| metaphysical | 533 | 9.8 | 47.1 | **0.21** |

**Pattern**: Prose-adjacent traditions (prose poetry, found poetry, biblical, concrete) have the highest Jakobson indices — they use clear syntactic frames where the model is confident, then violate expectations. More "literary" traditions (Romantic, metaphysical, surrealist, German expressionist) have the lowest — their defamiliarization begins at the syntactic level.

**Romantic is metonymic (0.25)**: Despite being associated with "imagination" and metaphor in literary history, the Romantic era shows strong combination-surprise dominance. Blake, Keats, Shelley, Coleridge all use unusual syntax that creates high-entropy contexts. Their "imaginative" leaps occur in syntactically uncertain terrain.

**Metaphysical is the most metonymic era (0.21 tied with surrealist)**: Donne's conceits work by unexpected combinations of distant semantic domains — this is informationally metonymic, not metaphoric.

---

## Finding 4: The Merwin Paradox Resolved

W.S. Merwin (Jakobson Index 1.75) has the highest index among poets with substantial corpora. His dominant Q2 substitution is content-for-content (21.4% C/C rate). This makes his strategy precise:

**Merwin's method**: Remove punctuation → model builds high confidence about sentence structure because it must rely on word-order cues alone → at moments of confident syntactic expectation, substitute an unexpected content word.

This is the most purely "Jakobsonian" strategy in the corpus in the classical sense — paradigmatic substitution (unexpected lexical item) in a clear paradigmatic slot. The punctuation removal doesn't introduce random chaos; it paradoxically sharpens the model's syntactic confidence while leaving the lexical slot open for defamiliarization.

---

## Suggested Next Steps

1. **Expand the Merwin sample**: Get more Merwin poems (currently only 60 tokens) to validate the Q2/Q1 = 1.75 finding with a larger corpus.

2. **The function-for-function mystery**: Identify which specific function word substitutions are most common in Q2. Are they preposition swaps (in → through), pronoun perspective shifts (he → she), or conjunction-type changes (and → but)? Each would have different interpretive implications.

3. **Test the Jakobson Paradox directly**: Take Hopkins poems and artificially flatten their syntax (regularize word order). Does this increase their Jakobson Index? This would confirm that Hopkins's low index comes from syntactic complexity rather than lexical conservatism.

4. **Map Q2/Q1 onto Jakobson's own examples**: Jakobson's 1956 paper analyzes specific poet pairs (metaphoric: Romanticism, Symbolism; metonymic: Realism). How do those eras score here? Symbolism (Stefan George: 0.29) and Romanticism (0.25) are both low — but Jakobson called them metaphoric!
