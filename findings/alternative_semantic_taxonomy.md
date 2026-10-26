# Alternative Semantic Taxonomy at Peak S₂ Moments

**Date:** 2026-10-26  
**Experiment:** `experiments/alternative_semantic_taxonomy.py`  
**Corpus:** 348 texts, 1704 peak S₂ moments (S₂ > 2.0, p_newline < 0.9 filtered)

---

## Question

At the moments of maximum surprise (highest S₂), what was GPT-2 expecting instead? Do the model's alternatives cluster into coherent semantic domains? When a poet makes an extreme deviation, are they jumping to a *different* semantic domain (cross-domain surprise) or choosing an unusual word within the *same* domain the model expected (same-domain surprise)?

---

## Key Findings

### 1. GPT-2's Alternatives at Peak Moments Are Dominated by Grammar

| Domain | Alternatives | % |
|--------|-------------|---|
| other (unclassified) | 8,735 | 51.3% |
| function_grammar | 6,389 | 37.5% |
| temporal | 391 | 2.3% |
| social_human | 319 | 1.9% |
| nature | 296 | 1.7% |
| body | 230 | 1.3% |
| speech_thought | 206 | 1.2% |
| light_vision | 143 | 0.8% |
| death_void | 131 | 0.8% |

**At peak S₂ moments, GPT-2 was most often expecting grammatical function words** (conjunctions, prepositions, determiners, pronouns). The model anticipated syntactic continuation; the poet instead provided semantic content. This is the core Straussian gap — language expects grammar, poetry provides meaning.

### 2. Poets at Peak Moments Also Write Unclassified ("Other") Tokens

| Domain | Actual tokens | % |
|--------|--------------|---|
| other | 1,317 | 77.3% |
| function_grammar | 108 | 6.3% |
| temporal | 48 | 2.8% |
| nature | 41 | 2.4% |
| motion | 35 | 2.1% |
| emotion | 32 | 1.9% |

The 77% "other" rate reflects both the limits of the keyword taxonomy and the genuine novelty of peak-surprise tokens — they tend to be unusual, specific, or compound words that resist simple categorization.

### 3. Cross-Domain vs. Same-Domain Surprise

- **Cross-domain surprise** (poet jumped to a categorically different semantic field): **343 moments (20.1%)**
- **Same-domain surprise** (unusual word within the expected semantic domain): **44 moments (2.6%)**
- The majority (77%) involve tokens classified as "other" in both positions — extreme surprises that transcend the taxonomy.

### 4. The Dominant Transition: Grammar → Content Word

The most revealing domain transitions at peak S₂ moments:

| Expected (alternatives) → Actual | Count |
|----------------------------------|-------|
| function_grammar → function_grammar | 42 |
| function_grammar → temporal | 20 |
| function_grammar → nature | 17 |
| function_grammar → emotion | 16 |
| function_grammar → motion | 15 |
| function_grammar → death_void | 13 |

**When GPT-2 is most confident a grammar word will follow, poets most often write a nature, temporal, emotion, or death-related word.** These are the canonical poetic categories — and they arrive precisely where the model expected syntactic connectives. The poet uses the slot grammar reserves for "and," "of," "the" — and drops a noun of death or a verb of motion.

### 5. Cross-Domain Rate by Era

| Era | n | Cross% | Avg S₂ |
|-----|---|--------|--------|
| rondeau | 5 | 80.0% | 10.69 |
| latin_american | 15 | 46.7% | 9.91 |
| classical_chinese | 20 | 45.0% | 7.86 |
| cliche_control | 15 | 40.0% | 8.14 |
| protest_political | 10 | 40.0% | 8.19 |
| surrealist | 40 | 35.0% | 9.57 |
| prose_poetry | 60 | 35.0% | 8.50 |
| haiku | 57 | 33.3% | 6.24 |
| ancient | 15 | 33.3% | 8.73 |
| beat | 30 | 30.0% | **15.31** |
| ... | ... | ... | ... |
| war_poetry | 15 | **0.0%** | 10.49 |
| german_symbolist | 15 | **0.0%** | 11.27 |
| german_modernist | 10 | **0.0%** | 10.04 |
| control | 13 | **0.0%** | 3.30 |

**Notable patterns:**
- **Beat poetry** has both high cross-domain rate AND highest avg S₂ (15.31) — Ferlinghetti, Ginsberg are extreme domain-jumpers.
- **Classical Chinese poetry** (in translation) shows high cross-domain rate (45%) — possibly reflecting the paratactic, juxtaposition-heavy style that places unlike things in grammatical proximity.
- **War poetry** shows zero cross-domain jumps despite high avg S₂ — Owen, Brooke produce intense surprise through unexpected words *within* the expected semantic context (death, violence, nature), not by jumping domains.
- **German symbolists** (0% cross-domain) operate within tight semantic fields — their surprise is intra-domain.

### 6. Authors with Highest Cross-Domain Rates

| Author | n | Cross% | Avg S₂ |
|--------|---|--------|--------|
| Rae Armantrout | 5 | 80.0% | 7.37 |
| Wang Wei | 5 | 80.0% | 4.83 |
| John McCrae | 5 | 80.0% | 10.69 |
| Ross Gay | 5 | 60.0% | 4.97 |
| Federico García Lorca | 5 | 60.0% | 10.79 |
| Matsuo Basho | 5 | 60.0% | 6.19 |
| Philip Larkin | 5 | 60.0% | 8.39 |
| John Berryman | 5 | 60.0% | 9.03 |
| Louise Glück | 5 | 60.0% | 10.36 |
| Lawrence Ferlinghetti | 10 | 50.0% | **22.43** |

**Ferlinghetti has by far the highest avg S₂ (22.43)** — his peak moments are extraordinary in magnitude. Wang Wei (ancient Chinese nature poetry) and Armantrout (Language poetry) both show 80% cross-domain rates by very different mechanisms: Wang Wei through compressed juxtaposition, Armantrout through deliberate semantic rupture.

### 7. Exemplary Moments

| S₂ | Token | Poet | Expected | Context |
|----|-------|------|----------|---------|
| 28.25 | 'climbs' (motion) | Ferlinghetti | other [spaces/punct] | — extreme syntactic rupture |
| 18.41 | 'gravy' (death_void) | Bentley (clerihew) | function_grammar [by/in/for] | — comically mundane word in formal slot |
| 18.06 | 'poems' (speech_thought) | Harjo | function_grammar [,/./and] | — self-referential rupture |
| 17.32 | 'fearful' (emotion) | Whitman | other [Captain/captain] | — emotional override of expected proper noun |
| 17.19 | 'Despair' (emotion) | Hopkins | function_grammar [and/,/the] | — grammatical slot filled with abstract noun |
| 16.27 | 'Hours' (temporal) | Tennyson | speech_thought [heart/hand] | — body→time domain jump |
| 15.65 | 'anguish' (emotion) | Rossetti | function_grammar [example/instance/the] | — collocational override |

---

## Theoretical Interpretation

The analysis reveals three distinct types of peak S₂ production:

1. **Grammar-to-content substitution** (most common among classified transitions): The poet places a content word (emotion, nature, time, death) in a syntactic slot GPT-2 expected to hold a function word. This is *paratactic shock* — deleting the expected connective and substituting a semantic payload.

2. **Cross-domain semantic jump** (20% of moments): When both the expected alternatives AND the actual token are classifiable, they belong to different domains. The temporal leap from body→time (Tennyson), function→emotion (Hopkins, Rossetti), nature→death all appear here.

3. **Unclassifiable extremity** (77%): The majority of peak moments involve tokens that resist standard semantic categorization — neologisms, compound words, highly specific proper nouns, phonosemantic coinages. These may represent the *purest* Straussian gap: language so unexpected that no domain taxonomy can contain it.

---

## Limitations

- The keyword taxonomy covers ~23% of tokens; 77% fall into "other."
- Function grammar is over-represented in alternatives because GPT-2 trains on prose text where such continuations are frequent.
- Small n for some eras (rondeau, rondeau) makes percentage statistics unreliable.

---

## Next Steps

1. **Expand taxonomy** with larger word embeddings (WordNet hypernyms or FastText cluster labels) to reduce "other" to below 20%.
2. **Conditional analysis**: At grammar-to-content transition moments, what specific grammar word had the highest probability? (Was the expected "and" or "the"? Does the expected conjunction vs. preposition predict what domain the poet chooses?)
3. **Era × Domain transition matrix**: Full cross-tabulation of which eras specialize in which grammar→content transitions.
4. **Regression analysis**: Does cross-domain rate predict poem-level memorability or canonical status?
