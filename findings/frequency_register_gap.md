# Word Frequency and the Straussian Gap: Rare Words vs. Common Words in Unusual Positions

**Date:** 2026-10-26  
**Experiment:** `experiments/frequency_register_gap.py`  
**Results:** `results/frequency_register_gap.json`  
**Corpus:** 336 texts, 41,168 clean tokens (artifact-free: p_newline < 0.9)

---

## Research Question

The Straussian gap (S2 > 0) marks moments where a poet chose something more surprising than the context warranted. But *what kind* of surprise is it? Two fundamentally different strategies could generate high S2:

1. **Rare-word strategy**: Choose an intrinsically unusual/infrequent word (long, rare token) in a position where GPT-2 was confident *something* would appear — just not *that* word.
2. **Common-word-in-unusual-position strategy**: Choose a short, high-frequency word (like "dark", "blood", "bone") in a context where GPT-2 expected something elaborated or syntactically different.

These strategies have different literary implications. The rare-word strategy is the vocabulary-driven approach: surprise through lexical selection. The common-word strategy is the syntactic/semantic placement approach: surprise through relational positioning of simple materials — closer to Imagism's "no ideas but in things."

**Proxy for word frequency**: GPT-2 tokenizes via BPE; shorter tokens tend to correspond to higher-frequency words (Zipf's law). We use token length as a proxy for unconditional frequency, comparing the actual token's length vs. the top expected alternative's length.

---

## Key Findings

### 1. Token Length Increases Monotonically with S2

| S2 Bin | n | Mean Token Length | % Short (≤2 chars) | % Long (≥7 chars) | Mean Conditional Rank |
|---|---|---|---|---|---|
| Very Low S2 (< -2) | 15,652 | **2.38** | 52.9% | 2.0% | 3.3 |
| Low S2 (-2 to 0) | 11,526 | 2.64 | 50.2% | 3.5% | 19.0 |
| Near-zero S2 (0 to 1) | 2,930 | 3.43 | 33.6% | 6.3% | 98.6 |
| High S2 (1 to 3) | 4,505 | 3.72 | 28.8% | 9.3% | 246.9 |
| Very High S2 (> 3) | 6,555 | **4.30** | 19.9% | 16.0% | 1,666.1 |

The gradient is striking: very high S2 tokens are nearly **2 full characters longer** on average than very low S2 tokens. Long words are 8× more prevalent at very high vs. very low S2 positions (16.0% vs. 2.0%).

### 2. The Rare-Word Strategy Dominates (but Is Not Universal)

At high-S2 moments (S2 > 1.5, n=9,770), poets' choices relative to GPT-2's top expectation:

| Strategy | Count | % |
|---|---|---|
| Chose **LONGER** (rarer) word than expected | 4,772 | **48.8%** |
| Same length class (±1 char) | 3,864 | 39.5% |
| Chose **SHORTER** (commoner) word | 1,134 | **11.6%** |

- Mean length difference (actual − expected) at **high-S2 moments**: **+1.47 chars**
- Mean length difference **overall**: +0.53 chars

The Straussian gap is primarily created through vocabulary selection: poets choose longer, rarer words than GPT-2 expected. The common-word strategy is a minority pattern (11.6%) — but a meaningful one when it occurs.

### 3. Function Words Are Depleted at High-S2 Positions

| Context | Function Word Rate |
|---|---|
| Overall corpus | 26.3% |
| High-S2 positions (S2 > 1.5) | 11.2% |
| Enrichment ratio | **0.43×** (depletion) |

Function words (the, a, in, and, is...) are strongly avoided at high-S2 moments. This confirms that the Straussian gap is predominantly a **content word phenomenon** — nouns, verbs, adjectives in unexpected positions.

**However**, look at the raw frequency table: punctuation and function words do appear at high-S2 positions, just less than expected. The em-dash (—), colon (:), and semicolon (;) are the #1, #2, #3 most common tokens at high-S2 positions. Punctuation as surprise: poets use punctuation to create structure where GPT-2 expected to continue a clause.

### 4. What GPT-2 Expected vs. What Poets Chose

At high-S2 moments, GPT-2 most commonly expected these tokens:
`,` (1,015 times), `the` (980), `\n` (711), `and` (449), `of` (308), `.` (291), `i` (290)...

These are the **default connecting tissues of English prose**. The model constantly anticipates commas, articles, conjunctions. Poets systematically violate these expectations — choosing content words, unusual punctuation, or syntactically unexpected continuations.

---

## Poet Profiles: Two Strategies

### Common-Word Strategists (mean token length ≤3.2 at high-S2 moments)

| Author | Era | n | Mean Length | % ≤3 chars |
|---|---|---|---|---|
| William Carlos Williams | modernist | 12 | **2.92** | 58.3% |
| Lorine Niedecker | modernist | 10 | 2.80 | 70.0% |
| H.D. (Hilda Doolittle) | modernist | 11 | 3.18 | 63.6% |
| Yosa Buson | haiku | 12 | 3.00 | 66.7% |
| Masaoka Shiki | haiku | 10 | 2.90 | 60.0% |
| Anne Carson | contemporary | 24 | 3.12 | 66.7% |
| Layli Long Soldier | contemporary | 22 | 3.14 | 63.6% |

**Pattern**: The common-word strategists cluster in **Imagist and haiku traditions**. Williams, Niedecker, H.D., and the Japanese haiku masters surprise by placing short, concrete, everyday words in positions where GPT-2 expected elaboration. This is the Imagist aesthetic in information-theoretic terms: simple words, devastating placement.

### Rare-Word Strategists (mean token length ≥5.0 at high-S2 moments)

| Author | Era | n | Mean Length | % ≤3 chars |
|---|---|---|---|---|
| Samuel Johnson | 18th_century | 40 | **4.97** | 35.0% |
| Du Fu | classical_chinese | 21 | 5.14 | 9.5% |
| Wislawa Szymborska | contemporary | 30 | 5.17 | 20.0% |
| Lyn Hejinian | language | 10 | 5.20 | 10.0% |
| Louise Glück | contemporary | 42 | 5.24 | 21.4% |
| Allen Ginsberg | beat | 54 | 5.39 | 27.8% |
| Isaac Newton (found text) | found_poetry | 28 | 5.50 | 28.6% |

**Pattern**: Long-word strategists span neoclassical (Johnson), academic modern (Glück, Szymborska), and Language Poetry (Hejinian). Their surprise comes through vocabulary itself — choosing the specific, technical, or polysyllabic word where GPT-2 expected something generic. Ginsberg's surprise is catalogic: long compound nouns and adjectives in his "Howl"-style lists.

---

## Era Analysis: Register at Surprise Moments

Sorted by mean token length at high-S2 positions (short = common-word strategy):

| Era | Mean Len | % ≤3 chars | Interpretation |
|---|---|---|---|
| ballad | 3.22 | 58.5% | Oral tradition: short, concrete |
| imagist | 3.68 | 43.5% | Programmatic common-word strategy |
| haiku | 3.70 | 46.9% | Minimal vocabulary, precise placement |
| harlem_renaissance | 3.90 | 45.8% | Blues/spiritual register influence |
| victorian | 3.97 | 39.3% | Mixed strategies |
| beat | 4.65 | 36.6% | Catalog mode: long nouns |
| language | 4.55 | 29.8% | Systematic defamiliarization |
| old_english | 4.58 | 28.7% | Kennings and compound words |
| prose_poetry | 4.51 | 29.7% | Expanded vocabulary range |

---

## Implications

### The Two Faces of Poetic Surprise

1. **Imagist/Haiku mode**: Surprise through placement of common materials — "a red wheelbarrow" where a complex modifier was expected. The Straussian gap here is about syntactic/semantic positioning.

2. **Academic/Baroque mode**: Surprise through vocabulary selection — "the irrefragable beauty" where something simpler was expected. The Straussian gap here is about lexical density.

Both are real strategies. The corpus skews toward the rare-word strategy overall (48.8% longer vs. 11.6% shorter at high-S2 moments), which makes sense: most poetry in the Western tradition values specific, rare diction as a marker of poetic authority.

### What GPT-2's "Unsaid" Reveals

At high-S2 moments, GPT-2 almost always expects: commas, articles (the), conjunctions (and), or continuation markers (of, in). These are the connective tissue of elaborated prose. Poets systematically refuse these continuations, choosing either:
- A content word that breaks the syntactic expectation
- An unusual punctuation mark (em-dash, colon) that creates structure

The Straussian gap is fundamentally about **refusing grammatical elaboration** — either by choosing rare content words OR by choosing unexpected structural markers.

---

## Suggested Next Steps

1. **Phonemic frequency analysis**: Use the CMU Pronouncing Dictionary to test if high-S2 words also tend to have rarer phoneme sequences (combining lexical and phonological rarity).
2. **Common-word strategists under the microscope**: Do the Imagist poets (Williams, H.D.) show specific SYNTACTIC positions where they deploy short words at high-S2 moments? (e.g., always at line endings? always as nouns rather than verbs?)
3. **The punctuation finding**: The em-dash and colon as high-S2 tokens deserve their own analysis. Are these structural surprises associated with volta-like semantic shifts?
4. **Cross-era comparison**: Does the ratio of common-word to rare-word strategy change across literary history? (Hypothesis: the Romantic era relies more on rare words; Modernism shifts toward common-word strategy.)
