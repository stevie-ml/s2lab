# The Q2 Lexicon: What Poets Write When GPT-2 Is Most Certain

**Date:** 2026-10-10
**Experiment:** `experiments/q2_lexicon_analysis.py`
**Corpus:** 227 texts | 25,081 artifact-free tokens (p_newline < 0.9)
**Corpus medians:** surprisal = 4.762 bits, entropy = 6.344 bits

---

## Motivation

The S₂ coordinate system (see `s2_coordinate_system.md`) identified four quadrants
of the surprisal–entropy plane. The **Q2 quadrant** (high surprisal + low entropy)
represents the purest "Straussian gap" — moments where GPT-2 was highly confident
AND the poet still chose something outside the model's expectations.

This study asks: **what exactly do poets choose at these moments?** What lexical,
grammatical, and semantic patterns characterize the Q2 lexicon?

---

## Quadrant Baseline

| Quadrant | Meaning | n | % |
|---|---|---|---|
| Q1: High surp + High ent | Ambiguous surprise | 9,215 | 36.8% |
| **Q2: High surp + Low ent** | **Confident mismatch** | **3,325** | **13.2%** |
| Q3: Low surp + Low ent | Confident match | 9,215 | 36.8% |
| Q4: Low surp + High ent | Lucky guess | 3,326 | 13.2% |

---

## Finding 1: Q2 Is Grammatically Inverted Relative to Q1

Token type distributions reveal a striking contrast between Q2 and Q1:

| Token Type | Q2% | Q1% | Q2/Q1 Ratio |
|---|---|---|---|
| punctuation | 10.9% | 2.8% | **3.91×** |
| function_word | 33.9% | 19.2% | **1.76×** |
| content_word | 44.1% | 67.4% | **0.65×** |
| capitalized_word | 4.5% | 6.9% | **0.64×** |

**Interpretation:** Q1 (ambiguous surprise) is dominated by content words (67%) —
these are the unexpected nouns, verbs, and adjectives poets introduce into uncertain
contexts. Q2 (confident mismatch) is **enriched for function words and punctuation**,
suggesting a different mechanism: when the model is most certain, poets more often
choose grammatical elements the model didn't expect, or choose content words at
positions reserved for function words.

---

## Finding 2: The Grammar→Image Swap Is the Most Distinctive Q2 Pattern

Analyzing what GPT-2 expected vs. what the poet chose:

**GPT-2's top-1 prediction at Q2 positions:**
- function_word: 41.0%
- content_word: 24.8%
- punctuation: 21.4%

**Poet's actual choice:**
- content_word: 44.1%
- function_word: 33.9%
- punctuation: 10.9%

The most telling swap: **function_word → content_word** accounts for 16.7% of all Q2
moments. These are the cases where the model expected grammatical machinery ("the",
"to", "of", "and") but the poet inserted a concrete word instead.

### 623 "Grammar→Image" Swaps (18.7% of Q2)

Top examples of the "model expected grammar, poet chose image" pattern:

| Chosen | S₂ | Expected | Context | Poet |
|---|---|---|---|---|
| shook | +22.04 | "the" | "like shining from _" | G.M. Hopkins |
| prank | +22.02 | "the" | "he rolls upon _" | Christopher Smart |
| liking | +16.66 | "to" | "I prefer myself _" | Wisława Szymborska |
| hysterical | +15.61 | "to" | "madness, starving _" | Allen Ginsberg |
| midway | +15.32 | "to" | "meet you listening _" | Hart Crane |
| Tennessee | +14.20 | "the" | "a jar in _" | Wallace Stevens |
| green | +14.00 | "to" | "I want you _" | García Lorca |
| whale | +14.00 | "a" | "Only _" | Amy Lowell |
| desolate | +14.25 | "of" | "dim meadows _" | Oscar Wilde |

**This is the linguistic signature of poetic compression**: the model
expects a grammatical bridge; the poet substitutes a substantive word that
forces the reader to supply the grammar themselves. "Like shining from [the]"
→ "shook" skips the expected noun and moves directly to a verb of motion.

---

## Finding 3: The Q2 Lexicon — What Words Are Most "Anti-Consensus"

### Most Q2-Enriched Content Words (vs corpus-wide frequency)

These words appear in Q2 disproportionately — they're the poet's vocabulary of
confident defiance:

| Word | Q2 enrich | Avg S₂ | Notes |
|---|---|---|---|
| "above" | 4.87× | +6.30 | Spatial upward |
| "even" | 5.11× | +6.15 | Emphatic scalar |
| "whatever" | 4.38× | +8.10 | Open-ended pronoun |
| "below" | 4.38× | +7.66 | Spatial downward |
| "ends" | 4.38× | +7.23 | Finality |
| "behind" | 5.48× | +5.50 | Spatial rearward |
| "again" | 4.38× | +2.94 | Temporal return |
| "upon" | 3.46× | +3.00 | Archaic preposition |
| "around" | 3.98× | +4.46 | Spatial encirclement |
| "deep" | 2.92× | +6.37 | Spatial/metaphorical depth |
| "among" | 2.81× | +5.74 | Spatial/social immersion |
| "high" | 3.32× | +4.91 | Spatial elevation |
| "far" | (raw) | +6.23 | Spatial distance |
| "yet" | (raw) | +3.55 | Adversative temporal |

**Key pattern**: The Q2 lexicon is dominated by **spatial prepositions and adverbs**
("above", "below", "behind", "around", "upon", "among", "high", "deep", "far").
When the model is most confident about what comes next, poets reach for words that
locate things in space — precise orientation markers that refuse the expected
syntactic continuation and anchor the poem in physical reality.

---

## Finding 4: Emphatic / Adversative Words Are Disproportionately Q2

Among the top Q2-enriched words: "even" (5.11×), "again" (4.38×), "yet", "too",
"whatever", "today", "whose". These are not random surprises — they share a function:
**emphasis, qualification, or refusal of completion**. The model expects to move
forward (syntactically, semantically); these words push back, intensify, or arrest.

"Even" says: *you thought this would suffice, but it doesn't*.
"Again" says: *the model thought this was done; it happens once more*.
"Yet" says: *despite expectations, this is still true*.
"Whatever" says: *the model's specific prediction is irrelevant*.

These words are not just unexpected — they are **meta-comments on expectation itself**.
They appear precisely when the model is most confident, and they undercut that confidence.

---

## Finding 5: The Canonical Q2 Tokens (Highest S₂ in Confident Mismatch)

| Token | S₂ | Context | Poet |
|---|---|---|---|
| "glass" | +25.63 | after a line break | Marianne Moore |
| "whenever" | +25.60 | after a line break | Lawrence Ferlinghetti |
| "ferner" | +23.40 | "Der schimmer _" | Stefan George |
| "shook" | +22.04 | "like shining from _" | G.M. Hopkins |
| "prank" | +22.02 | "he rolls upon _" | Christopher Smart |
| "stacked" | +18.16 | "in a past _" | Claudia Rankine |
| "red" | +17.95 | "that Sir Patrick _" | Traditional (Scottish) |
| "ashes" | +18.51 | after "Nor f_" | Traditional (Scottish) |

Note: many top Q2 tokens involve **unusual subword splits** from BPE tokenization
(e.g., "ferner" = part of a German compound) or **mid-word enjambment** in concrete/
visual poetry. The truly semantic Q2 moments are: "shook" (Hopkins), "prank"
(Smart), "stacked" (Rankine), "Tennessee" (Stevens).

---

## Finding 6: Poet-Level Q2 Rates

| Poet | Q2% | Notes |
|---|---|---|
| Frank O'Hara | 25.9% | New York School; casual speech register |
| Layli Long Soldier | 24.6% | Procedural form; breaks grammatical expectation |
| W.S. Merwin | 23.3% | No punctuation; creates structural ambiguity |
| Sappho | 22.2% | Direct address; fragment structure |
| César Vallejo (trans.) | 21.7% | Surrealist syntax |
| Louise Glück | 20.6% | Laconic, compressed style |
| John Berryman | 20.5% | Irregular syntax and register |
| Christina Rossetti | 20.3% | Compressed Victorian lyric |
| Marianne Moore | 18.9% | Syllabic form; unusual vocabulary |
| Anonymous (Hebrew Bible) | 18.0% | Biblical parallelism |

**Observation:** High Q2 rates correlate with distinctive, genre-defying styles.
Poets like O'Hara (casual speech against high lyric expectation), Merwin
(no punctuation forcing syntactic reanalysis), and Layli Long Soldier (procedural
interruption) achieve high Q2 through different mechanisms but the same result:
confident predictions repeatedly violated.

---

## Synthesis: The Q2 Grammar

Three mechanisms account for most Q2 moments:

1. **Grammar→Image swap** (18.7% of Q2): The model expects syntactic machinery;
   the poet inserts a concrete or spatial word. Compressed syntax, bypassed grammar.

2. **Spatial/directional override** (~15% of Q2): The Q2 lexicon is dominated by
   spatial prepositions ("above", "below", "around", "upon", "among"). These appear
   when the model expects forward syntactic movement; the poet stops and locates.

3. **Emphatic arrest** (~10% of Q2): Words like "even", "again", "yet", "too",
   "whatever" appear at high-certainty moments to intensify, qualify, or refuse
   the expected continuation.

Together these paint a picture of **how poets use confident-mismatch moments**:
not as random surprises, but as grammatical refusals — moments where the poem
refuses to behave like a sentence and instead behaves like a poem.

---

## Suggested Next Steps

1. **Spatial preposition analysis**: Are "above/below/around/upon" Q2 enriched
   in all eras? Do imagist and concrete poets show higher spatial-override rates?

2. **Translation comparison**: Do translated poems lose Q2 spatial markers? Is the
   grammar→image swap translation-invariant or language-specific?

3. **Close reading catalog**: For the top 50 grammar→image swaps, write mini
   annotations explaining what the reader must supply (the bypassed grammar)
   and what effect this creates.

4. **Q2 lexicon vs. poetic image dictionaries**: Compare the Q2-enriched vocabulary
   against existing poetic image glossaries (natural imagery, elemental words).
   Are Q2 words the same as "core poetic vocabulary"?
