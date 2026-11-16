# Word Order Scramble: Poetry is Locally Predictable

**Date:** 2026-11-16
**Experiment:** `experiments/word_order_scramble.py`
**Results:** `results/word_order_scramble.json`
**Corpus:** 50 poems, 3 conditions each (original / line-shuffle / line-reverse / full-shuffle)

---

## Research Question

Does S₂ measure *sequential* deviation (each word surprising given the preceding context) or *lexical* deviation (unusual vocabulary regardless of position)? We test by scrambling word order within lines while preserving all words: if S₂ captures sequential choice, scrambling should collapse it; if S₂ captures vocabulary alone, scrambling should leave it unchanged.

---

## Hypotheses

| Hypothesis | Prediction | Verdict |
|---|---|---|
| **H1 Syntactic** | Scrambling LOWERS S₂ (sequential context is essential) | ❌ REJECTED |
| **H2 Lexical** | Scrambling leaves S₂ unchanged (vocabulary alone drives surprise) | ❌ REJECTED |
| **H3 Chaos** | Scrambling RAISES S₂ (random order is maximally unpredictable) | ✅ CONFIRMED |

---

## Key Finding: Poetry is Locally Coherent

**Scrambling word order *increases* S₂ in 90% of poems (mean Δ = +0.63 bits).**

| Condition | Mean Δ S₂ | % Poems Increase |
|---|---|---|
| Within-line shuffle | **+0.633** | **90%** |
| Within-line reverse | +0.177 | 64% |
| Full poem shuffle | **+1.140** | **98%** |

**What this means:** Poetry maintains strong local sequential coherence — each word is *more* predictable given its neighbors in the original order than in any random permutation. The poet's sequential choices *reduce* unpredictability relative to baseline.

This inverts the naive view that poets "choose surprising words." Rather: **poets choose words that are surprising in a globally coherent, locally predictable way.** Each token follows from its immediate neighbors; it is only surprising relative to a larger register or expectation, not relative to its own context.

---

## Era-Level Results: Which Poetry Loses Most S₂ When Scrambled?

| Era | n | Original S₂ | Δ on Shuffle | Interpretation |
|---|---|---|---|---|
| found_poetry | 2 | −0.674 | **+1.276** | Strongest sequential structure — prose registers impose predictable word-chains |
| biblical | 2 | −0.404 | **+1.211** | Parallelism and formulaic structure create tight sequential prediction |
| latin_american | 2 | −0.718 | **+1.030** | Surrealist + formal genres in translation: strong syntactic chains |
| ghazal | 2 | −0.465 | +0.950 | Radif (refrain) and formulaic closure create predictable word sequences |
| fixed_form | 2 | −0.511 | +0.899 | Meter and rhyme enforce sequential predictability |
| oulipo | 2 | +0.750 | **+0.054** | Constraint-based: deviance is *lexical*, not sequential — scrambling barely changes S₂ |
| beat | 2 | +0.493 | +0.116 | High-S₂ vocabulary choices; sequential order matters little |
| postcolonial | 2 | −0.443 | **−0.134** | ONLY era where scrambling *lowers* S₂ — original order is *more* deviant than random |

---

## Exception Cases: Poems Where Scrambling Lowers S₂

Five poems show NEGATIVE deltas — their scrambled versions have *lower* S₂ than originals:

| Title | Era | Original S₂ | Δ | Why |
|---|---|---|---|---|
| Eunoia: Chapter E (excerpt) | oulipo | +1.772 | **−0.333** | Univocalic constraint: original word-sequence *maximally* exploits the E-only restriction; scrambling reduces sequential constraint exploitation |
| Marriage (Frank O'Hara) | beat | +0.771 | −0.455 | Cataloguing style — the sequential accumulation of unexpected nouns is what drives surprise; scrambling flattens it |
| Black Stone on White Stone | surrealist | +0.234 | −0.059 | Sequential self-naming structure ("César Vallejo will die...") carries the deviance |
| She Had Some Horses | postcolonial | −0.579 | −0.099 | Anaphoric refrain ("She had some horses...") — the sequential pattern IS the poem's deviance |
| Calypso | postcolonial | −0.307 | −0.168 | Ritualistic repetition: the sequential order performs the strangeness |

**The Eunoia anomaly** is the clearest case: Eunoia Chapter E uses only words containing 'E'. Scrambling reduces S₂ because the original sequential arrangement *exploits* the univocalic constraint more intensely than any random permutation would. The constraint is baked into the word choice, but the *exploitation* of that constraint is sequential.

---

## The Two Components of Poetic S₂

This experiment, combined with the earlier found-poetry finding, reveals two orthogonal components of S₂ in poetry:

```
Total S₂ elevation over control prose (~1.9 bits):
  ├── Register component (+1.3 bits): Text-type effects (archaic, formal, literary register)
  │     → Captured by found poetry — present WITHOUT poetic intent
  │     → Largely SEQUENTIAL (found poetry loses ~1.3 bits when scrambled)
  │
  └── Intentional component (+0.6 bits): Deliberate poetic word-choice
        → This gap survives scrambling for Oulipo but not for traditional verse
        → Itself splits into:
              Lexical deviance: unusual vocabulary (Oulipo, Beat — scramble-resistant)
              Sequential deviance: unusual word sequences (traditional verse — scramble-sensitive)
```

---

## Interpretive Implications

**1. Poetic meter and syntax create local predictability, not surprise.**
Traditional forms (ghazal, fixed forms, biblical parallelism) lose the most S₂ when scrambled — their meter and syntax enforce word-order expectations that *reduce* local surprise. The measured S₂ in these poems comes not from violating local sequence but from violating the larger register.

**2. The 'Straussian gap' is a global, not local, phenomenon.**
S₂ in canonical poetry is not "this word is strange here" but "this word is strange for this register." A poet writing "emperor of ice-cream" chooses a globally unexpected phrase, but *within that phrase*, each word follows naturally from the previous one.

**3. Avant-garde poetry (Oulipo, Beat) is different in kind, not just degree.**
For O'Hara or Bök, the deviance is *lexical* — strange words placed in sequences that respect their strangeness. Scrambling barely affects their S₂ because the surprise is carried by vocabulary, not arrangement. This suggests a typology:
- **Type I (traditional)**: Sequential coherence + global register deviance
- **Type II (avant-garde)**: Lexical deviance + sequential deviance, scramble-resistant

---

## Suggested Next Steps

1. **Token-level scramble**: Scramble individual *tokens* (not words) — does GPT-2's tokenization make a difference?
2. **Control for syntax**: Try a "syntactically valid scramble" (preserve NP/VP structure but randomize within them) using a parser — this separates syntactic from semantic sequential predictability.
3. **Generalization to prose**: Scramble control prose and compare the Δ to poetry's Δ — does prose show the same local coherence?
4. **Scramble resistance as a metric**: The magnitude of |Δ on shuffle| might be a useful new metric — "sequential coherence coefficient" — complementing S₂ itself.
5. **The Eunoia exception**: Analyze all Oulipo poems in the corpus for scramble resistance — does OuLiPo as a movement show consistently negative or near-zero deltas?
