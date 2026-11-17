# Grammar Ghosts: What Poets Choose When They Suppress the Expected

**Date:** 2026-11-17  
**Experiment:** `experiments/grammar_ghost_semantics.py` → `results/grammar_ghost_semantics.json`  
**Corpus:** 431 texts, 56,827 artifact-free tokens  
**Builds on:** `category_jump_analysis.md` (GRAMMAR→CONTENT = 39.6% of genuine high-S2 events)

---

## Research Question

When poets make high-S2 choices where GPT-2 predicted a grammar word but the poet wrote a content word, **which grammar words are most suppressed, what replaces them, and what does the pattern of replacement reveal about poetic strategy**?

---

## Overview

Out of 4,984 genuine high-S2 tokens (s₂ > 5.0 bits, p_newline < 0.90), **1,714 are clean grammar ghost events** — cases where the model's top prediction was a function word and the poet wrote a complete-word content word instead.

That's **34.4% of all genuine high-S2 moments** — roughly 1 in 3 times a poet surprises the model, they do it by stripping away expected grammar and planting a content word in its place.

---

## Finding 1: 'The' Is the Dominant Ghost Word

| Suppressed Word | Count | % of Ghosts |
|---|---|---|
| **the** | 448 | **26.1%** |
| of | 132 | 7.7% |
| and | 123 | 7.2% |
| I | 91 | 5.3% |
| a | 85 | 5.0% |
| is | 74 | 4.3% |
| to | 69 | 4.0% |
| And | 60 | 3.5% |
| was | 43 | 2.5% |
| in | 31 | 1.8% |
| be | 31 | 1.8% |
| are | 28 | 1.6% |
| The | 28 | 1.6% |
| not | 27 | 1.6% |
| my | 27 | 1.6% |

The definite article *the* is the single most ghosted grammar word, accounting for **1 in 4** grammar ghost events (476 events combining 'the' and 'The'). This is not simply because 'the' is the most frequent word in English — it reflects something specific about how poets use high-S2 positions.

**What replaces 'the':** `eyes`, `love`, `slow`, `early`, `autumn`, `Fall`, `Things`, `Hell`, `Water`, `among`

The replacements cluster into two types:
1. **Unanchored nouns** ('eyes', 'love', 'autumn', 'Fall') — nouns that, without 'the', become archetypal rather than specific
2. **Unexpected qualifiers** ('slow', 'early', 'among') — words that change the grammatical structure entirely

---

## Finding 2: Five Grammar Strategies

| Grammar Category | Count | % | Dominant Replacement Type |
|---|---|---|---|
| **Article** (the/a/an) | 564 | **32.9%** | Bare nouns, verbs |
| **Preposition** (of/in/to…) | 297 | 17.3% | Verbs, nouns |
| **Pronoun** (I/he/she/you…) | 294 | 17.2% | Nouns, verbs |
| **Auxiliary** (is/was/be…) | 255 | 14.9% | Verbs, nouns |
| **Conjunction** (and/but/or…) | 208 | 12.1% | Abstract nouns, verbs |
| Other function | 96 | 5.6% | Mixed |

Each category represents a distinct poetic maneuver:

### A. Article Suppression → Archetypal Naming
When 'the' or 'a' is ghosted, the replacement noun loses its referential anchoring. "the death" → "Death"; "the sea" → "sea". The stripped article elevates the noun from a particular thing to a universal. This is the most common ghost pattern.

### B. Preposition Suppression → Spatial Jump  
Prepositions (of, in, to, from, over) signal relational structure. When they're ghosted, the replacement creates a spatial or logical rupture — a sudden new object or action where a linking word was expected.

### C. Pronoun Suppression → Lyric Deflection
When 'I', 'he', 'she', or 'you' is ghosted, the speaker/subject vanishes. 191 events where GPT-2 expected a pronoun but the poet wrote a content word. The subject is not carried forward — instead, the poem pivots to an object, a scene, an abstraction. Prominent examples: 'he' → 'Music' (Romantic), 'I' → 'Despair', 'you' → 'throat' (Confessional).

### D. Auxiliary Suppression → Compressed Action
Auxiliaries (is, was, are, be, been) set up predication. When they're ghosted, the replacement is often a past participle or active verb: 'was' → 'carried', 'swung', 'filed', 'swim'. This compresses a two-word verb phrase ('was carried') into a single content word that bypasses the auxiliary — the action without the syntax.

### E. Conjunction Suppression → Asyndeton Shock  
208 events where 'and', 'but', 'or' was expected and a content word appeared. This is computational detection of **asyndeton** — the rhetorical figure of omitting conjunctions for abruptness. The replacements cluster at high-S2 scores: 'Despair' (s₂=17.2, Victorian), 'cliff' (s₂=16.1, contemporary), 'throat' (s₂=14.9, confessional), 'breeding' (s₂=11.2, modernist). Without 'and' or 'but', the two clauses collide rather than connect.

---

## Finding 3: Era Differences — Grammar Ghost Rate per 1,000 Tokens

| Era | Ghost Rate /1k | Total Tokens | Interpretation |
|---|---|---|---|
| **18th_century** | **46.0** | 1,435 | Pope/Dryden: inversion, ellipsis common |
| **old_english** | **44.5** | 629 | Translation artifacts + alliterative compression |
| **oulipo** | **42.1** | 1,282 | Constraint-driven syntax defamiliarization |
| **ancient** | **40.9** | 318 | Translation from non-article languages |
| **nonsense** | **40.0** | 500 | Grammar deployed as pure form |
| **procedural** | **39.1** | 640 | Instruction lists, imperative grammar |
| **early_modern** | **38.3** | 1,801 | Shakespeare: ellipsis and compression |
| **confessional** | **37.8** | 397 | Plath/Sexton: subject deflection |
| **dramatic_monologue** | **37.6** | 4,418 | Browning: speaker's idiosyncratic syntax |
| **harlem_renaissance** | **36.8** | 816 | Hughes/McKay: vernacular syntax |
| ... | ... | ... | ... |
| **german_symbolist** | **2.8** | 356 | Rilke in translation: near-conventional syntax |
| **latin_american** | **17.4** | 461 | Neruda/Paz: more syntactically conventional |

**The 18th century leads** — poets like Pope and Dryden favor inversions and ellipses that create exactly these grammar-ghost moments. Old English's high rate reflects translation artifacts and the radically different syntax of the alliterative tradition. 

Oulipo's high rate is particularly striking: constraint writing (N+7, lipograms) systematically defamiliarizes grammar, generating ghost patterns as a byproduct of method. German symbolist poetry ranks lowest — suggesting either that Rilke's syntax is unusually regular at the grammatical level, or that his surprises operate at the content level rather than via grammar suppression.

---

## Finding 4: The Conjunction Ghost Lexicon

The 20 highest-S2 conjunction suppressions:

| S₂ | Expected | Actual | Era |
|---|---|---|---|
| 17.2 | and | **Despair** | victorian |
| 16.1 | and | **cliff** | contemporary |
| 14.9 | and | **throat** | confessional |
| 12.1 | and/or | **constraint** | elegy |
| 11.6 | and | **alas** | 19th_century |
| 11.3 | and | **angry** | old_english |
| 11.2 | and | **breeding** | modernist |
| 11.1 | and | **Fit** | harlem_renaissance |
| 10.9 | and | **Compare** | early_modern |

"Breeding" in the modernist era is almost certainly Eliot's "breeding / Lilacs out of the dead land" — where the enjambed participle replaces an expected connective. "Despair" and "cliff" and "throat" represent the same move across three centuries: at the moment a conjunction was expected (and two clauses would have been connected, equalized, rationalized), the poet lands on a charged noun instead. The gap becomes a collision.

---

## Theoretical Synthesis: The Grammar Ghost as Poetic Mechanism

The grammar ghost is not random — it follows a logic:

1. **The article ghost** (32.9%) makes nouns archetypal by stripping their definiteness marker
2. **The conjunction ghost** (12.1%) creates asyndeton: collision instead of connection
3. **The pronoun ghost** (17.2%) performs lyric deflection: the subject disappears
4. **The auxiliary ghost** (14.9%) compresses predication: the action without the structure
5. **The preposition ghost** (17.3%) breaks spatial/relational logic: a jump without a bridge

Together, these five maneuvers account for 94.4% of all grammar ghost events. They are not mere accidents of meter or compression — they are **the five core ways that poets substitute information for grammar**, replacing the skeleton of sentence logic with charged semantic material.

The highest-S2 grammar ghosts are not random content words: they tend to be **abstract nouns** (Despair, Death, Silence, Music), **archetypal concrete nouns** (cliff, throat, eyes), or **past participles that compress an action** (carried, swung, breeding). The ghosted grammar word reveals what conventional syntax expected; the actual choice reveals what the poet substituted in its place.

---

## Suggested Next Steps

1. **Confirm the 'The' → archetypal noun hypothesis** with word embedding analysis: do the content words that replace 'the' have higher concreteness/imageability ratings than typical content words?
2. **Conjunction ghost tracking within poems**: do poets that use asyndeton (high conjunction ghost rate) distribute their ghostings evenly, or do they cluster (suggesting a stylistic commitment to asyndeton)?
3. **Build a "grammar ghost index" per poet**: what fraction of a poet's grammar ghosts are article vs. conjunction vs. pronoun? This would distinguish article-strippers (Hopkins, possibly Dickinson) from asyndeton specialists (Whitman) from lyric deflectors (confessional poets).
4. **Cross-reference with known rhetorical figures**: anaphora, asyndeton, ellipsis, apposition — can grammar ghost patterns serve as a statistical detector for these figures?
