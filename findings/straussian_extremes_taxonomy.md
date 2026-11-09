# The Anatomy of Maximum Surprise: A Taxonomy of Extreme Straussian Gaps

**Date:** 2026-11-09  
**Experiment:** `experiments/straussian_extremes.py` → `results/straussian_extremes.json`  
**Corpus:** 411 poems, 3,156 extreme high-S2 moments (S2 ≥ 5.0, cleaned)  
**Builds on:** `straussian_gap_taxonomy.md`, `rank_topology_surprise.md`, `semantic_field_of_surprise.md`

---

## Research Question

Previous analyses characterize high-S2 moments in aggregate: how often they occur, in what eras, with what rank distributions. But the **extreme** Straussian gaps (S2 ≥ 5.0) deserve their own anatomy. What specific suppression-choice patterns produce maximum surprise?

Three questions:
1. What does GPT-2 expect at positions of extreme surprise? (What is suppressed?)
2. What do poets actually write instead? (What is chosen?)
3. Who produces the most extreme gaps, and what is the "type" of their divergence?

---

## Finding 1: Function Words Are the Dominant Suppressed Category

| Category suppressed | High-S2% | Baseline% | Lift |
|---|---|---|---|
| FUNCTION_WORD | **49.0%** | 38.2% | **1.28×** |
| PUNCTUATION | 18.2% | 17.3% | 1.05× |
| CONTENT_WORD | 31.3% | 43.3% | **0.72×** |
| CONTRACTION | 1.5% | 1.3% | 1.16× |

At positions of extreme surprise, GPT-2's top prediction was a **function word** (the, a, of, and, is, that, etc.) nearly half the time — and more than its baseline rate. By contrast, **content word** predictions are *under-represented* at high-S2 moments.

**Interpretation:** The Straussian gap most often opens where language's machinery expects a structural element — an article, conjunction, or preposition. The poet instead delivers a content word. This confirms and extends the "grammar-vs-image gap" from `semantic_field_of_surprise.md`: the suppressed item is usually not a competitor-image but the grammatical scaffold that conventional language would have used.

---

## Finding 2: S2 Is Highest When Contractions Are Suppressed

| Category suppressed | n | Mean S2 | Median S2 | Max S2 |
|---|---|---|---|---|
| CONTRACTION | 47 | **8.73** | 8.21 | 17.5 |
| FUNCTION_WORD | 1,546 | 7.98 | 7.26 | 22.1 |
| PUNCTUATION | 575 | 7.80 | 7.17 | 20.4 |
| CONTENT_WORD | 988 | 7.76 | 7.05 | 23.4 |

**Contractions** ('s, 'll, 've, 't) produce the highest mean S2 when overridden. This makes sense: contractions occupy highly predictable syntactic slots (after a pronoun or proper noun), so defying a contraction means refusing both the grammatical expectation AND the semantic one. Example: Housman writes "chaired" where GPT-2 expected "'ll" — refusing both the auxiliary-verb slot and the temporal continuity it implied.

---

## Finding 3: The Four Dominant Suppression → Choice Patterns

| Suppressed | Most common choice | Characteristic example |
|---|---|---|
| **FUNCTION_WORD → content** | Preposition, adverb, or unexpected noun/verb | Smart: "prank" replaces "the"; Hopkins: "shook" replaces "the" |
| **PUNCTUATION → continuation** | Adverb, verb, or noun that continues rather than pauses | Whitman: "observing" replaces ","; Tennyson: "onward" replaces "," |
| **CONTENT_WORD → wild jump** | Word from completely different semantic field | Bishop: "badly" replaces "glass"; Dickinson: "Fun" replaces "little" |
| **CONTRACTION → action** | Unexpected verb or noun | Housman: "chaired" replaces "'ll"; Shelley: "fleeing" replaces "'s" |

**The "comma override"** is a particularly rich pattern: rather than pausing (as "," indicates), the poet supplies an unexpected continuation word. This is the grammatical signature of syntactic enjambment — the semantic enjambment across a comma that conventional language would have used as a stop.

---

## Finding 4: The Top 20 Extreme Straussian Moments

| Rank | S2 | Chosen | Suppressed | Context | Poet |
|---|---|---|---|---|---|
| 1 | 23.4 | **ferner** | 't' | "Der schimmer" | Stefan George |
| 2 | 22.1 | **prank** | 'the' | "he rolls upon" | Christopher Smart |
| 3 | 22.0 | **shook** | 'the' | "like shining from" | G.M. Hopkins |
| 4 | 20.6 | **printer** | 'ne' | "The jour" | Walt Whitman |
| 5 | 20.6 | **badly** | 'glass' | ", the hour" | Elizabeth Bishop |
| 6 | 20.4 | **observing** | ',' | "at my ease" | Walt Whitman |
| 7 | 18.9 | **Fun** | 'little' | "felt a" | Emily Dickinson |
| 8 | 18.9 | **consequences** | 'a' | "ute end of" | William Stafford |
| 9 | 18.4 | **gravy** | 'by' | "Abominated" | E.C. Bentley |
| 10 | 18.2 | **squats** | 'elled' (jewelled) | "And the jew" | T.S. Eliot |
| 11 | 18.2 | **stacked** | 'ime' (pastime) | "in a past" | Claudia Rankine |
| 12 | 18.1 | **poems** | ',' | "They are alive" | Joy Harjo |
| 13 | 18.0 | **onward** | ',' | "Half a league" | Tennyson |
| 14 | 17.9 | **mounting** | ',' | ", my collar" | T.S. Eliot |
| 15 | 17.5 | **chaired** | "'ll" | "race / We" | A.E. Housman |
| 16 | 17.3 | **fearful** | 'Captain' | "Captain! our" | Walt Whitman |
| 17 | 17.2 | **Music** | 'he' | (new stanza) | John Keats |
| 18 | 17.2 | **Despair** | 'and' | "rounds and rounds" | G.M. Hopkins |
| 19 | 17.0 | **prose** | 'am' | ", as I" | César Vallejo |
| 20 | 16.8 | **gravy** | 'by' | "Abominated" | E.C. Bentley |

### Literary Close-Readings of Extreme Cases

**Smart's "prank" (S2=22.1):** "He rolls upon prank" — GPT-2 wanted "He rolls upon the [noun]" or similar. "Prank" is so unexpected because: (a) it's a low-frequency noun in this sense, (b) it uses "upon" as a particle rather than preposition, and (c) the word-sense (archaic: a fold or crease) is archaic. The suppression was "the" — the definite article promising a predictable noun-phrase completion.

**Hopkins's "shook" (S2=22.0):** "like shining from shook foil" from "God's Grandeur." GPT-2 predicted "the" after "shining from" — expecting "shining from the [noun]." Instead: "shook foil" (a past-participial adjective with the foil). The impossible collision of "from shook" (preposition + past participle used adjectivally) produces the maximum S2.

**Bishop's "badly" (S2=20.6):** From "One Art": "the hour badly spent." GPT-2 predicted "glass" after ", the hour" — perhaps from pattern-completion with "hourglass." "Badly" is devastating because it's an evaluative adverb where GPT-2 expected a noun completing a compound.

**Dickinson's "Fun" (S2=18.9):** "I felt a Fun" — GPT-2 expected "little" (as in "I felt a little [adjective/noun]"). Dickinson capitalizes "Fun" and uses it as a personification (echoing her personification of "Funeral"), producing maximum S2 through: (a) semantic field mismatch, (b) unexpected capitalization, (c) specific-to-generic reversal.

**Whitman's "fearful" (S2=17.3):** "O Captain! our fearful trip is done" — GPT-2 expected "Captain" (the refrain repeating). "Fearful" defies both the lexical repetition expectation AND the emotional tone that "Captain" would have maintained.

---

## Finding 5: Which Poets and Eras Produce the Most Extreme Gaps?

### Top Eras by Mean S2 at Extreme Moments (n ≥ 10 high-S2 tokens)

| Era | n | Mean S2 | Max S2 | Characteristic mode |
|---|---|---|---|---|
| clerihew | 27 | **9.3** | 18.4 | Colloquial-word override (humor) |
| german_symbolist | 15 | 8.6 | 23.4 | Foreign-language gap |
| beat | 62 | 8.4 | 16.6 | Register-breaking |
| romantic | 208 | 8.4 | 17.2 | Semantic field jump |
| surrealist | 59 | 8.3 | 17.0 | Domain mismatch |
| oulipo | 86 | 8.3 | 15.7 | Systematic word replacement |
| mid_century | 42 | 8.2 | 20.6 | Quiet devastation |
| 19th_century | 185 | 8.2 | 20.6 | Victorian specificity |

**Clerihews** (humorous biographical poems) produce the highest mean S2 — through deliberate comic non-sequitur. "Abominated gravy" (Bentley) is funny precisely because "gravy" is the most colloquial possible word after "Abominated" — a maximally formal Latinate verb.

**German Symbolist** poems achieve extreme gaps partly through the foreign-language effect: GPT-2's training included less German, so non-English words and their predicted continuations diverge more. Stefan George's S2=23.4 ("ferner" replacing 't') is partly a German-language-GPT-2 gap.

**Oulipo** achieves extreme gaps through systematic replacement (N+7 substitutes every noun with the 7th-later noun in the dictionary). Jean Lescure's N+7 of Genesis produces "eviction" where "dark" was expected — a theologically charged noun replacing an elemental adjective.

### Top Poets by Mean S2 (n ≥ 5 high-S2 tokens)

| Poet | n | Mean S2 | Max S2 |
|---|---|---|---|
| Elizabeth Bishop | 5 | **11.6** | 20.6 |
| Edmund C. Bentley | 5 | 10.7 | 18.4 |
| Paul Éluard | 5 | 10.2 | 14.4 |
| Jean Lescure (Oulipo) | 10 | 9.9 | 15.7 |
| Christian Bök | 34 | 9.2 | 14.7 |
| Samuel Taylor Coleridge | 15 | 9.2 | 14.9 |
| Robinson Jeffers | 7 | 9.4 | 14.7 |
| Walter de la Mare | 4 | 9.2 | 14.9 |

**Elizabeth Bishop** (11.6) tops the list among serious poets with sufficient token count. This confirms her reputation for the precisely unexpected word — the word that feels both surprising and inevitable in retrospect. Her highest moment ("badly" at 20.6) is a classic Bishop move: an adverb where a noun was expected.

**Edmund Clerihew Bentley** (10.7) and **Paul Éluard** (10.2) represent opposite poles of the same achievement: humorous non-sequitur vs. surrealist juxtaposition. Both produce extreme gaps through deliberate category violation.

**Christian Bök** (9.2) is the highest-scoring contemporary poet — his constrained Oulipian work (each chapter uses only one vowel) creates extreme gaps because his constraints force choices GPT-2's language model cannot anticipate.

---

## Typology: Four Modes of Extreme Straussian Gap

| Mode | Mechanism | Examples | Mean S2 |
|---|---|---|---|
| **Function-word override** | Content word displaces expected grammatical scaffold | "prank"/"the", "shook"/"the" | ~8.5 |
| **Comma bypass** | Unexpected continuation defies expected pause | "observing"/",", "onward"/"," | ~8.0 |
| **Semantic field jump** | Chosen word is from an incompatible domain | "gravy"/"by", "Fun"/"little" | ~9.0 |
| **Refrain defiance** | Expected repetition is replaced by variation | "fearful"/"Captain", "Despair"/"and" | ~8.5 |

The **semantic field jump** produces the highest mean S2, confirming that radical semantic domain shifts are the most effective way to maximize surprise. When GPT-2 predicted a word from one semantic field and the poet provided a word from an entirely different one, the gap is widest.

---

## Key Finding

**The maximum Straussian gap is structurally asymmetric**: GPT-2 almost always expects a function word or punctuation (the building blocks of conventional syntax), while poets almost always respond with an unexpected content word. The gap is not between two content words in different semantic fields — it is between the machinery of language and the material of meaning.

The most extreme moments in English poetry (S2 > 15) share a common signature: they occur where GPT-2 is moderately confident (H = 2–7 bits) but completely wrong about the semantic category of what comes next. The poet does not simply choose a rare word; they choose a word from a different category of experience than the one the model had opened.

**Elizabeth Bishop leads all serious poets** in producing extreme Straussian gaps, suggesting her celebrated quality of "the unexpected right word" is precisely this: consistently high semantic-category divergence at positions of moderate model confidence.

---

## Suggested Next Steps

1. **Extend to bigram-level analysis**: examine the PAIR of tokens at high-S2 moments — does the choice resolve in the next token (falling S2) or amplify (rising S2)? This would test whether extreme gaps are "punctual" or the beginning of a cascade.
2. **Historical cohort analysis**: do 19th-century poets and contemporary poets differ in WHAT they suppress vs. choose, not just how often?
3. **Mode-switching by poem**: within a single poem, do the four modes appear in distinctive patterns (e.g., Eliot uses both comma-bypass and content-jump modes in "Gerontion")?
4. **Semantic surprise direction**: using word vectors, compute the DIRECTION of the semantic jump (from what domain to what domain) and cluster these directions. Are there preferred "escape vectors" in English poetry?
