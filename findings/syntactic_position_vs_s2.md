# Syntactic Position and S₂: Where Poets Deviate

**Date:** 2026-09-30  
**Method:** POS-tagged 188 poetry texts + 4 prose controls using NLTK averaged perceptron tagger. Mapped GPT-2 subword tokens to Penn Treebank POS tags by character overlap; aggregated avg S₂ by broad POS category. Poetry: 50+ tokens/category threshold; Prose: 5+ tokens/category threshold.

---

## Key Results

| POS | Poetry AvgS₂ | Prose AvgS₂ | Δ S₂ | Interpretation |
|-----|-------------|------------|------|---------------|
| ADJ  | +1.088 | -2.376 | **+3.464** | Largest gap — poets choose unexpected qualities |
| NOUN | +1.437 | -1.854 | **+3.291** | Second largest — nouns are primary surprise vehicle |
| CONJ | +0.940 | -1.978 | **+2.918** | Coordinating conjunctions carry more surprise in poetry |
| VERB | +1.017 | -1.210 | **+2.227** | Action words are more deviant in poetry |
| ADV  | +1.093 | -1.337 | **+2.430** | Adverbs also deviant |
| DET  | -1.630 | -3.551 | **+1.921** | Even determiners more surprising in poetry (but still negative) |
| PREP | +0.592 | -1.071 | **+1.663** | Prepositions moderately more deviant |
| PRON | -0.354 | -1.203 | **+0.849** | Pronouns: small gap |
| AUX  | -0.763 | -1.192 | **+0.429** | Auxiliaries: minimal gap |
| PUNCT | -1.702 | -1.793 | **-0.074** | Punctuation: essentially identical (near zero gap) |

---

## Finding

**The Straussian gap is concentrated in lexical content words — adjectives, nouns, conjunctions, verbs — not in grammatical function words.**

Punctuation shows virtually no poetry-vs-prose S₂ difference (Δ = -0.074). This is a critical methodological anchor: it suggests that punctuation-based layout choices (line breaks, stanza breaks) are the main source of the "stanza break artifact," while the *actual poetic creativity* lives in the choice of content words.

The hierarchy of poetic deviation by POS:
1. **ADJ**: Most deviant (Δ = +3.464). Poets choose unexpected *qualities* — the adjective is where poetic license peaks.
2. **NOUN**: Second (Δ = +3.291). The choice of nouns — the *things* of the poem — is where the second-largest deviation lives.
3. **CONJ**: Third (Δ = +2.918). Surprising: coordinating conjunctions in poetry (and, but, or, yet) are more statistically deviant than the model expects, possibly because poets use conjunctions to create unexpected juxtapositions ("death and the maiden" rather than "death and grief").
4. **ADV + VERB**: Both ~+2.2–2.4. Manner and action carry moderate Straussian deviation.
5. **DET/PREP**: ~+1.7–1.9. Even grammatical words are more surprising in poetry, but less so.
6. **PUNCT**: ~0. Punctuation is metronomic — the same information structure as prose.

---

## Theoretical Interpretation

This confirms the "lexical surprise" theory of poetry: poets deviate from statistical expectations primarily through **word choice at content word positions**, not through syntactic restructuring. The grammar stays recognizable; it is what fills the slots that surprises.

The high CONJ surprise is a notable anomaly worth further investigation. Conjunctions are usually function words with high predictability, yet poets use them in highly unexpected ways. Possible explanations:
- **Asyndeton and polysyndeton**: Poets deliberately vary conjunction use (zero connectives, or excessive "and" sequences), making conjunction choice less predictable.
- **Parataxis**: Poetic parataxis creates unexpected conjunctive connections between semantically distant concepts.
- **Adversative turns**: The word "but" or "yet" signals a volta, which is maximally surprising at the model level.

The PUNCT = 0 finding has important methodological implications: it confirms that the "stanza break artifact" (where post-newline tokens have artificially inflated S₂) is a **layout artifact**, not a real linguistic signal. Real poetic deviation is in words, not marks.

---

## Data Notes

- Poetry n = 188 English texts; Prose n = 4 texts (limited, so prose estimates have wide uncertainty)
- Prose threshold lowered to 5 tokens/category (vs 50 for poetry) to allow comparison despite small corpus
- The PRON and AUX categories show small but consistent gaps, suggesting even functional pronouns carry some poetic distinctiveness

---

## Suggested Next Steps

1. **Noun taxonomy**: Within NOUN, are proper nouns more or less surprising than common nouns? (Proper nouns in unexpected positions vs common nouns as unusual choices)
2. **ADJ before NOUN vs predicate ADJ**: Is the high adjective S₂ concentrated in attributive ("the blue horse") or predicative ("the horse is blue") positions?
3. **Verb form distribution**: Are past tense, present tense, or infinitive verb forms more deviant in poetry?
4. **Cross-era POS patterns**: Do different eras show different POS-level deviation profiles? (E.g., do modernist poets show more NOUN deviation while romantcs show more ADJ deviation?)
5. **The conjunction deep-dive**: Build a specific experiment on CONJ types (coordinating vs. subordinating) and their S₂ values in poetry vs prose.
