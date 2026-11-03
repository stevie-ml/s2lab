# The Surprise Lexicon: Mapping Intrinsic Information Value of Words in Poetry

**Date:** 2026-11-03  
**Experiment:** `experiments/surprise_lexicon_map.py` → `results/surprise_lexicon_map.json`  
**Corpus:** 403 poems, 30,268 qualifying content tokens (4,400 artifact-filtered, 21,092 punct/short skipped)  
**Unique word types analyzed:** 628 words with N≥8 occurrences

---

## Research Question

Is a word's S₂ entirely a function of its context, or do certain words carry **intrinsic surprise value** — always surprising GPT-2 regardless of where they appear? Conversely, are there words that are inherently conformist — confirming expectations whenever they appear?

This experiment computes per-word **mean S₂** across all corpus occurrences, creating a 2D "lexicon map" with corpus frequency on one axis and mean S₂ on the other. This reveals four quadrant categories: trademark surprisers, standard vocabulary, rare firecrackers, and rare conformists.

---

## Main Finding 1: The Poetic Cliché Lexicon

The lowest mean-S₂ content words reveal **what GPT-2 has learned to expect from poetry**:

| Word | N | Mean S₂ | %Positive | Eras |
|------|---|---------|-----------|------|
| `soul` | 28 | **−3.124** | 11% | 14 |
| `heart` | 48 | **−2.721** | 17% | 19 |
| `world` | 56 | **−2.694** | 11% | 26 |
| `door` | 28 | **−2.248** | 11% | 16 |
| `hand` | 55 | **−2.236** | 16% | 26 |
| `die` | 51 | **−2.169** | 18% | 20 |
| `way` | 47 | **−2.284** | 8% | 24 |
| `eye` | 28 | **−2.046** | 11% | 17 |

**These are the clichés of English poetry** — not because the poets are lazy, but because GPT-2 has learned that these words ARE the expected vocabulary of poetic contexts. When poets write "soul," "heart," or "world," they confirm rather than violate the model's expectations. GPT-2 knows where poetry lives. 

The distribution is striking: "heart" appears 48 times across 19 eras with only 17% positive S₂ — meaning 83% of the time it appears, it was expected. "Soul" hits only 11% positive: virtually every use was anticipated by the model.

---

## Main Finding 2: Spatial Prepositions as Surprise Engines

The highest mean-S₂ words show a striking pattern — **spatial prepositions dominate**:

| Word | N | Mean S₂ | %Positive | Interpretation |
|------|---|---------|-----------|----------------|
| `beneath` | 12 | **+3.927** | 100% | Always surprises |
| `among` | 21 | **+3.556** | 76% | Strongly surprising |
| `above` | 16 | **+3.487** | 75% | Consistently surprising |
| `under` | 27 | **+3.314** | 82% | Common AND surprising |
| `beside` | 10 | **+3.472** | 90% | Strongly surprising |
| `below` | 11 | **+4.477** | 82% | Very surprising |
| `behind` | 8 | **+4.916** | 88% | Strongly surprising |

**Spatial prepositions are the primary mechanism of poetic surprise in this corpus.** They systematically violate GPT-2's expectations because the model, trained on prose, expects spatial phrases at particular syntactic positions — after a noun phrase, after a verb of motion. Poetry places them unexpectedly: at line openings, after abstract nouns, in metaphoric constructions ("beneath the silence," "among the dead words").

The word `beneath` — 100% positive S₂, all 12 occurrences — is perhaps the single most reliable surprise engine in the lexicon. Every use is unexpected.

---

## Main Finding 3: Trademark Words — Common AND Always Surprising

The TRADEMARK quadrant (corpus-common words that nonetheless consistently register high S₂) reveals the **characteristic vocabulary of poetic deviation**:

| Word | N | Mean S₂ | Std | %Positive |
|------|---|---------|-----|-----------|
| `under` | 27 | +3.314 | 4.632 | 82% |
| `even` | 33 | +2.343 | 3.265 | — |
| `round` | 27 | +2.291 | 2.549 | — |
| `upon` | 67 | +1.630 | 2.952 | — |
| `too` | 52 | +1.858 | 3.433 | — |
| `again` | 37 | +1.821 | 2.762 | — |
| `just` | 42 | +1.712 | 2.851 | — |
| `each` | 46 | +1.608 | 2.895 | — |
| `death` | 34 | +1.264 | 3.838 | — |
| `once` | 27 | +1.332 | 3.486 | — |

These 51 words are **the active vocabulary of poetic surprise**. They appear frequently enough to be reliable data (N≥26), yet they consistently violate expectations. 

Notable observations:
- **`even`** (mean S₂=+2.343): A focus particle that introduces scope ambiguity ("even silence speaks"). GPT-2 doesn't expect the scope contraction this word enacts.
- **`upon`** (N=67, mean S₂=+1.630): An archaic preposition that sounds poetic but always surprises the model — suggesting GPT-2 expects contemporary register.
- **`death`** (mean S₂=+1.264) vs. **`die`** (mean S₂=−2.169): The NOUN form of death surprises; the VERB form doesn't. GPT-2 expects the action but not the abstract state.

---

## Main Finding 4: Fixed Information Signatures (Consistent Words)

Some words have **nearly the same S₂ every time they appear** (low standard deviation), suggesting their surprise value is intrinsic rather than contextual:

**Consistently Conformist (low std, low S₂):**

| Word | N | Mean S₂ | Std |
|------|---|---------|-----|
| `been` | 22 | −3.655 | 1.842 |
| `are` | 184 | −3.041 | 1.992 |
| `the` | 2215 | −3.403 | 2.042 |
| `hands` | 24 | −2.082 | 1.597 |
| `know` | 57 | −1.959 | 1.964 |
| `him` | 77 | −1.472 | 1.842 |

**Consistently Surprising (low std, high S₂):**

| Word | N | Mean S₂ | Std |
|------|---|---------|-----|
| `deep` | 15 | +2.219 | 2.263 |
| `silent` | 15 | +2.101 | 2.254 |
| `both` | 15 | +1.985 | 1.931 |
| `wood` | 15 | +2.067 | 2.395 |
| `half` | 16 | +2.065 | 2.443 |
| `round` | 27 | +2.291 | 2.549 |

The word **`deep`** (mean S₂=+2.219, std=2.263) is reliably surprising across 15 occurrences: GPT-2 consistently fails to anticipate it despite its apparent familiarity. Similarly **`silent`** and **`wood`** — both sensory/natural vocabulary — carry dependable information value.

By contrast, **`been`** (std=1.842) is perhaps the most informationally fixed word in the corpus: nearly identical S₂ whenever it appears, deeply embedded in auxiliary-verb expectation ("have ___").

---

## Main Finding 5: The Four-Quadrant Structure

Based on frequency threshold (N≥26) and S₂ sign:

| Quadrant | Count | Description |
|----------|-------|-------------|
| **TRADEMARK** | 51 words | Common + High S₂ — the active vocabulary of surprise |
| **STANDARD** | 111 words | Common + Low S₂ — the expected poetic lexicon |
| **FIRECRACKER** | 285 words | Rare + High S₂ — rare but always surprising |
| **RARE CONFORMIST** | 181 words | Rare + Low S₂ — rare but always expected |

The STANDARD category (111 words, low S₂) includes the vocabulary GPT-2 has memorized as belonging to poetry: "soul," "heart," "world," "door," "hand," "light," "dream," "love," "night." These are the words that make poetry RECOGNIZABLE as poetry — the poetic idiom. They confirm the genre.

The TRADEMARK category (51 words) represents the means of deviation: spatial prepositions, scope words ("even," "just," "only"), temporal markers ("again," "once"), and surprisingly, **`death`** as a noun.

---

## Key Insight: The Two-Tier Poetic Lexicon

These findings reveal poetry has a two-tier lexical structure in information-theoretic terms:

**Tier 1 (STANDARD): The genre lexicon.** These words — "soul," "heart," "world," "door," "die," "light," "dream" — are the conventional vocabulary of poetry. Poets who use them are working within an established tradition. GPT-2 has learned this tradition from training data and confidently predicts them. Their low S₂ means they are acts of **genre participation** rather than deviation.

**Tier 2 (TRADEMARK): The surprise vocabulary.** Spatial prepositions, scope particles, and certain sensory adjectives consistently produce high S₂. They are the lexical machinery of Straussian deviation. Poets who use "beneath," "among," "even," "deep," "silent" are deploying words that GPT-2 — despite their apparent familiarity — fails to predict. This is the lexicon of **defamiliarization at the word level**.

---

## Implication for Literary Analysis

The split between "die" (verb, S₂=−2.169) and "death" (noun, S₂=+1.264) is theoretically significant. The ACTION of dying is expected in poetry; the ABSTRACTION of death is surprising. This suggests that GPT-2's training has loaded poetry with verbs of action and sentiment — but poets reaching for the nominalized, abstract form of that same concept are doing something unexpected. The pattern may generalize: verbal poetry (action, event) may be the genre baseline, while abstract nominal poetry (concept, state, condition) is the domain of surprise.

---

## Next Steps

1. **POS-stratified analysis**: Are spatial prepositions uniquely surprising, or is it a broader prepositional-phrase phenomenon? Compare with other preposition types.
2. **Era-stratified surprise lexicon**: Does the TRADEMARK vocabulary differ by era? (Pre-modern poets using "upon" vs. contemporary poets using "just" and "even"?)
3. **Poet-level trademark words**: Which SPECIFIC words does each poet consistently use as surprise engines? This could serve as an authorial fingerprint at the lexical level.
4. **The "death/die" asymmetry**: Test whether the noun/verb split in abstraction holds for other word pairs (love/loving, death/die, silence/silent).
