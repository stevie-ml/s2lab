# Grammar of the Unsaid: POS Substitution Patterns in the Straussian Gap

**Date:** 2026-10-11  
**Method:** For each token in the corpus (excluding stanza-break artifact positions), classify both the actual token and GPT-2's top prediction by POS. Build a substitution matrix and analyze by era, S2 magnitude, and grammatical category.

---

## Research Question

When a poet deviates from GPT-2's expectations, do they systematically change the *grammatical category* of the predicted word — not just the specific word chosen? If poetry were mere lexical substitution (replacing one noun with a rarer noun), we'd see high POS-identity rates. But if poets work at the *grammatical* level — choosing an adjective where a pronoun was expected, or a verb where punctuation was expected — that reveals a deeper structural subversion.

**S2 = surprisal − entropy.**  
Grammatical substitution (actual POS ≠ expected POS) should produce higher S2 than lexical substitution (same POS, different word), because syntactic frame violations are more unexpected than rare word choices within the expected frame.

---

## Key Finding: Poetry Operates at the Grammatical Level

**Control prose POS-identity: ~63%**  
**Poetry average POS-identity: ~48%**

Poetry departs from GPT-2's grammatical predictions **one-third more often** than prose. This gap is not just lexical difficulty — it is syntactic reframing. Poets don't merely choose unusual words; they change the *grammatical slot* the language was pointing toward.

---

## The POS Substitution Matrix

*Rows = what the poet wrote; Columns = what GPT-2 expected. Values = % of occurrences.*

| Wrote → Expected | NOUN | VERB | ADJ | ADV | PRON | PUNCT | NEWLINE |
|---|---|---|---|---|---|---|---|
| **NOUN** | 47.2% | 5.3% | 5.2% | 1.8% | 12.8% | 7.7% | 3.3% |
| **VERB** | 9.6% | 33.7% | 2.1% | 2.0% | 11.7% | 7.3% | 3.3% |
| **ADJ** | 19.6% | 5.8% | 24.5% | 3.2% | 19.3% | 6.5% | 4.8% |
| **ADV** | 4.8% | 4.1% | 2.8% | 23.1% | 19.1% | 13.8% | 4.8% |
| **PRON** | 1.5% | 1.7% | 0.6% | 1.4% | 69.4% | 5.4% | 5.7% |
| **PUNCT** | 2.1% | 1.0% | 0.3% | 1.2% | 3.5% | 72.3% | 5.0% |

Reading the off-diagonal: when poets write a **VERB** where a NOUN was expected (9.6%), they force a reinterpretation of the sentence's syntactic trajectory. When they write **ADJ** where a PRON was expected (19.3%), they create a moment of grammatical displacement.

---

## Highest-S2 POS Substitution Pairs

Which grammatical substitutions produce the most extreme surprisal?

| Poet wrote | GPT-2 expected | Avg S2 | n |
|---|---|---|---|
| PROPN | NEWLINE | **+6.25** | 46 |
| PROPN | PART | **+5.75** | 14 |
| NOUN | SCONJ | **+5.51** | 7 |
| VERB | SCONJ | **+5.06** | 13 |
| NOUN | PART | **+4.84** | 29 |
| ADJ | AUX | **+4.21** | 21 |
| VERB | NEWLINE | **+4.23** | 91 |
| ADV | NEWLINE | **+4.10** | 51 |
| ADJ | CCONJ | **+4.03** | 27 |
| PROPN | PRON | **+3.98** | 189 |

**Interpretation:** The highest-S2 substitutions involve **proper nouns** — writing a proper name where GPT-2 expected a newline, a particle, or a pronoun. This makes sense: proper nouns are maximally specific (they pick out unique referents), while pronouns and particles are maximally relational. When a poet writes "Jesus" where the model expected a pronoun, or "Fun" where it expected "little," the S2 spike captures the ontological specificity that proper names carry.

The second pattern is **verbs appearing after structural subordinators** (SCONJ): writing a verb where a conjunction-completion was expected, effectively hijacking a subordinate clause structure. High S2 = 5.06 for this pattern.

---

## Era-Level Grammatical Strategies

**POS-identity rate by era** (lower = more grammatical substitution):

| Era | POS-Identity | Interpretation |
|---|---|---|
| early_modern | **39.4%** | Most grammatically disruptive — archaisms create POS ambiguity |
| haiku | **40.9%** | Compression forces non-standard syntactic slots |
| confessional | **41.3%** | Fragmented syntax, unexpected grammatical pivots |
| ancient | **42.1%** | Translation creates grammatical reframings |
| romantic | **44.2%** | Inversions and archaic constructions |
| ... | ... | ... |
| control (prose) | **63.2%** | Baseline: prose conforms to expected grammatical categories |
| found_poetry | **59.9%** | Near-prose, minimal grammatical subversion |
| song_lyrics | **62.1%** | Close to prose baseline |
| surrealist | **65.4%** | Surprisingly high — surrealist collocation keeps POS intact |

**Surprising finding:** Surrealist poetry (65.4%) has the HIGHEST POS-identity of any poetic category — *higher than prose*. This suggests that surrealism operates through *lexical* surprise (unexpected word choices within the expected POS slot) rather than *grammatical* surprise. Breton's "exquisite corpse" technique pairs words from unexpected semantic fields but preserves syntactic structure: adjective + noun, verb + adverb. The grammatical frame is conventional; only the semantic content violates expectation.

In contrast, **early modern poetry** (Wyatt, Spenser, Shakespeare) is most grammatically disruptive. This reflects the genuine syntactic plasticity of Early Modern English (flexible word order, verb-second constructions, hyperbaton) — GPT-2, trained on modern English, cannot anticipate these patterns.

---

## Dominant Substitution Strategy by Era

| Era | Dominant substitution |
|---|---|
| confessional | VERB when AUX expected — finite verbs replacing auxiliaries (raw action over modal hedging) |
| beat | VERB when AUX expected — Ginsberg's declarative catalog style |
| spoken_word | VERB when AUX expected — performative directness |
| imagist | VERB when NOUN expected — the imagist shift from nouns to verbs (cf. Fenollosa's Chinese Written Character) |
| romantic | NOUN when PRON expected — concrete noun substituting for pronoun reference |
| victorian | NOUN when PRON expected — same pattern, elaborated reference |
| new_york_school | PRON when NEWLINE expected — Frank O'Hara's run-on address style |
| concrete | ADP when NEWLINE expected — spatial prepositions as structural elements |

The **confessional/beat/spoken-word cluster** shares one strategy: replacing expected auxiliary verbs (would, could, should, might) with finite main verbs. This creates a rhetorical effect of directness and necessity — *happening* rather than *might happen*, *is* rather than *would be*. It's a grammatical expression of emotional commitment.

The **imagist pattern** (VERB where NOUN expected) matches Ezra Pound's famous prescription to use fewer nouns and more verbs, and Ernest Fenollosa's theory that the image lives in action, not stasis.

---

## Notable Examples: Grammatical Substitution at High S2

```
S2=+22.0  ' shook' (VERB) where ' the' (PRON) expected
          [Hopkins, 'God's Grandeur']
          — The world is charged with the grandeur of God / It will flame out,
            like shining from shook foil
          GPT-2 expected "the" (pronoun/article); Hopkins writes "shook" (participle used as adjective)

S2=+20.6  ' badly' (ADV) where 'glass' (NOUN) expected
          [Bishop, 'One Art']
          — The art of losing isn't hard to master [...]
          GPT-2 expected a noun continuation; Bishop's "badly" is an adverb modifying the upcoming loss

S2=+19.5  ' list' (NOUN) where 'ever' (ADV) expected
          [Wyatt, 'Whoso List to Hunt']
          — "Whoso list to hunt" — "list" is an archaic verb (desire), but GPT-2 reads it as NOUN
          Classic POS ambiguity in Early Modern English
          
S2=+18.9  ' Fun' (PROPN) where ' little' (ADJ) expected
          [Dickinson, 'I felt a Funeral, in my Brain']
          — The model expects an adjective; Dickinson capitalizes an abstract noun (Fun) as proper name
          Dickinson's signature capitalization grammar confounds modern POS expectations
```

---

## The Surrealist Paradox

Surrealist poetry achieves the highest POS-identity (65.4%) but simultaneously produces high individual S2 spikes at specific moments. This resolves what we might call the **surrealist paradox**: the style *systematically* obeys grammatical form (adjective + noun, subject + verb) while placing *semantically alien* words in each slot. 

GPT-2 cannot tell that "silk umbrella" and "operating table" are semantically incompatible — it only models lexical co-occurrence probability. So surrealism looks *grammatically conformist* to the model but *semantically impossible*. The information-theoretic signature of surrealism is:
- Low POS substitution
- High lexical surprisal at individual positions
- Low structural S2, high content S2

This is the inverse of haiku/confessional poetry, which achieves surprise through grammatical disruption.

---

## Hypothesis for Future Work

**The Grammatical Depth Hypothesis**: Different poetic traditions work at different "depths" of the linguistic system:

1. **Surface lexical level** (surrealism): Change the word, keep the grammar
2. **Grammatical category level** (confessional, haiku): Change what grammatical slot is occupied  
3. **Structural level** (early modern, concrete): Change the syntax itself

Each deeper level produces higher S2, but also more cognitive processing cost. The most effective poems may achieve surprise at the deepest level they can sustain without losing the reader — a tradeoff between grammatical disruption and comprehensibility.

**Measure**: POS-identity rate as a metric of "grammatical conformism" could discriminate between poetic schools better than raw S2, since it captures *where* the surprise operates in the linguistic hierarchy.

---

## Next Steps

1. Extend POS analysis to trigrams: what are the most common 3-POS sequences in poetry vs prose, and where do poets deviate from expected POS sequences?
2. Test the grammatical depth hypothesis with a reading difficulty metric (sentence parse depth)
3. Analyze POS substitution patterns within individual poets across their careers — do poets develop toward more or less grammatical conformism over time?
4. Cross-reference with known stylistic claims (Olson's projective verse, Fenollosa's verbal theory) — does information theory confirm these formalist intuitions?
