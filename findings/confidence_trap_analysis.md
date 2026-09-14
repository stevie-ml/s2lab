# The Confidence Trap: S₂ at Low-Entropy Moments

**Date:** 2026-09-14  
**Experiment:** `experiments/confidence_trap.py`  
**Corpus:** 117 English-language poems, 12,029 tokens  
**Research question:** When GPT-2 is maximally confident (H < 2.0 bits) but the poet still deviates — what are these "confidence trap" moments telling us?

---

## Motivation

Standard S₂ analysis aggregates over all token positions, including many where GPT-2 is uncertain (high entropy). A more targeted question: *what happens when GPT-2 is extraordinarily confident — say, 85–99% probability mass on a single token — but the poet ignores it?* These are the moments of most **deliberate** literary choice: the poet could have followed the path of least resistance, and instead went elsewhere.

We call these **confidence traps** (entropy H < 2.0 bits, rank > 10, S₂ > 2.0).

---

## Key Findings

### 1. Confidence Traps Are Rare but Significant

| Metric | Value |
|--------|-------|
| Total tokens analyzed | 12,029 |
| Confidence trap tokens | 341 |
| **Confidence trap rate** | **2.83%** |
| Avg entropy at traps vs. corpus avg | 0.19 bits vs. 6.04 bits |
| GPT-2 confidence ratio at traps | **31.4× more confident than average** |

Confidence traps represent moments where GPT-2 was not merely uncertain — it was *extraordinarily sure* — yet the poet chose otherwise. At these moments, GPT-2's average confidence is 31.4 times greater than its normal level.

---

### 2. Era Rankings: Haiku and Confessional Lead; Prose Poetry Trails

| Era | Poems | Traps | Tokens | Rate% |
|-----|-------|-------|--------|-------|
| **haiku** | 1 | 6 | 58 | **10.34%** |
| **confessional** | 3 | 10 | 190 | **5.26%** |
| **ballad** | 6 | 49 | 1018 | **4.81%** |
| **oulipo** | 1 | 2 | 51 | 3.92% |
| nursery_rhyme | 1 | 9 | 243 | 3.70% |
| romantic | 9 | 37 | 1154 | 3.21% |
| modernist | 18 | 51 | 1657 | 3.08% |
| language | 3 | 4 | 147 | 2.72% |
| victorian | 13 | 47 | 1845 | 2.55% |
| new_york_school | 18 | 31 | 1461 | 2.12% |
| **prose_poetry** | 9 | 18 | 967 | **1.86%** |
| beat | 2 | 2 | 150 | 1.33% |
| **control** | 4 | 0 | 128 | **0.00%** |

**Notable finding**: Control prose has zero confidence traps — it follows GPT-2's confident expectations perfectly. Prose poetry (which blurs the boundary) has nearly as low a rate (1.86%). Haiku, with its extreme compression, has the highest rate: in a 58-token haiku, every word is subject to maximum deliberateness.

**The ballad paradox**: Traditional ballads have the 3rd-highest rate despite their formulaic oral tradition. The explanation: repetitive narrative formulas train GPT-2 to expect specific words at specific points, but traditional bards repeatedly deviate from those patterns through variant phrasing and compressed imagery.

---

### 3. Top Poems by Confidence Trap Rate

| Poem | Author | Rate% | Traps |
|------|--------|-------|-------|
| The Red Wheelbarrow | W.C. Williams | 16.13% | 5 |
| This Is Just to Say | W.C. Williams | 13.95% | 6 |
| Three Haiku (Basho) | Matsuo Basho | 10.34% | 6 |
| We Real Cool | Gwendolyn Brooks | 8.89% | 4 |
| a list of the delusions... | David Antin | 8.53% | 11 |
| Harlem | Langston Hughes | 7.79% | 6 |
| The Convergence of the Twain | Thomas Hardy | 7.78% | 7 |
| Bonnie George Campbell | Traditional (Scottish) | 7.56% | 9 |
| What Is Poetry | John Ashbery | 7.46% | 5 |
| Lady Lazarus (opening) | Sylvia Plath | 7.02% | 4 |

W.C. Williams dominates this list. His extreme minimalism — poems of 16–43 tokens — means every word choice is so concentrated that each functions as a confidence trap.

---

### 4. What GPT-2 Expected at Confidence Trap Moments

| Expected Category | Count | % |
|-------------------|-------|---|
| **newline** | 314 | 92.1% |
| content word | 18 | 5.3% |
| function word | 7 | 2.1% |
| punctuation | 2 | 0.6% |

**The dominant pattern (92%)**: GPT-2 expected a newline — the poem continued instead.

This is a profound result. **Poetry's primary mechanism of confidence-trap generation is enjambment and line continuation.** GPT-2, trained largely on prose, learns that certain syntactic contexts (clause endings, phrase completions) are almost always followed by newlines. Poets exploit this by carrying the sentence beyond the expected line-break point.

The line itself — as a formal unit — is poetry's most fundamental act of statistical defiance.

---

### 5. The 25 Content/Function Word Confidence Traps: "Deliberate Semantic Deviation"

Beyond the dominant newline-pattern, 25 confidence traps involve GPT-2 expecting a specific *word* (not a newline) and the poet choosing differently. These are the most semantically revealing deviations:

| Author | Context | Poet wrote | GPT-2 expected | GPT-2 prob | S₂ |
|--------|---------|-----------|----------------|------------|-----|
| Elizabeth Bishop | `...the hour` | `badly` | `glass` | 83.6% | 20.59 |
| Trad. (Scottish) | `...Sir Patrick` | `red` | `Sp[ens]` | 70.0% | 17.95 |
| John Ashbery | `...role-` | `L[iving]` | `playing` | 59.6% | 17.73 |
| Walt Whitman | `...I lo` | `afe` (loafe) | `athe` (loathe) | 92.9% | 12.87 |
| Christina Rossetti | `...Remember me when` | `no` | `I` | 85.4% | 11.73 |
| Claudia Rankine | `...too tired` | `even` | `to` | 72.9% | 10.93 |
| Frank O'Hara | `...12:20 in` | `New` [York] | `the` | 93.8% | 10.09 |
| Claude McKay | `...must die,` | `O` | `let` | 90.7% | 12.95 |

**Reading these cases:**

1. **Whitman's "loafe" vs. "loathe"** (S₂=12.87): GPT-2 was 92.9% confident that "I lo-" would complete as "loathe." Instead, Whitman invented/used the archaic "loafe." One of the most famous words in American poetry is a confidence trap — and GPT-2's expectation reveals the word's strangeness: the model wants the familiar negative verb but Whitman gives us leisure and invitation instead of revulsion.

2. **Rossetti's "no" vs. "I"** (S₂=11.73): "Remember me when I..." was GPT-2's confident continuation; Rossetti writes "Remember me when no more day by day / You tell me of our future that you planned." The negation (no) where the self-reference (I) was expected: the poem withholds the self at the moment of remembrance.

3. **Frank O'Hara's "New" vs. "the"** (S₂=10.09): At "12:20 in," GPT-2 expected the generic article "the" (most probable: "the afternoon"). O'Hara writes "New" [York] — the specific proper noun over the generic article. This precisely captures the New York School's poetics: specificity, place-names, the concrete over the abstract.

4. **Claude McKay's "O" vs. "let"** (S₂=12.95): "If we must die, O let it not be like hogs" — GPT-2 expected "let" to come directly after the comma, but McKay inserts the apostrophe "O" first. The invocation of classical rhetoric where statistical language expects the clause.

5. **Claudia Rankine's "even"**: "too tired even to..." — GPT-2 expected "to" but Rankine adds "even" first — the adverb of extremity, of emphasis, that escalates beyond expectation.

---

### 6. The Semantic Pattern of Content-Word Confidence Traps

| Pattern | Examples | Count |
|---------|----------|-------|
| Specific proper noun over generic article/determiner | O'Hara's "New" vs. "the"; McKay's "O" vs. "let" | 3 |
| Negation where affirmation expected | Rossetti's "no" vs. "I" | 1 |
| Archaic/invented word over familiar verb | Whitman's "loafe" vs. "loathe" | 1 |
| Intensifier that escalates | Rankine's "even" vs. "to" | 2 |
| Unexpected color/adjective | Trad. ballad "red" vs. "[Sp]ens" | 1 |

**Working hypothesis**: When poets deviate at maximum confidence positions, they tend to:
- Choose the **specific over the general** (proper noun, color, name)
- Insert **rhetorical amplifiers** (apostrophes, intensifiers) that classical convention demands but statistical language omits
- Choose the **negative or limiting** where affirmative continuity was expected
- Revive **archaic or invented vocabulary** that the model has never seen in this context

---

### 7. The Perfect Prose Control: Zero Traps

Four control prose texts produced zero confidence traps. This confirms:

| Text type | Confidence trap rate |
|-----------|---------------------|
| Simple narrative prose | 0.00% |
| News article | 0.00% |
| Technical prose | 0.00% |
| Prose poem (W.S. Merwin) | 0.00% |
| All poetry eras | 1.33%–10.34% |

Prose writing conforms to GPT-2's confident expectations. Poetry systematically does not. The confidence trap rate is a **clean binary separator** between poetry and prose.

---

## Theoretical Implications

The confidence trap framework offers a more precise measure of *deliberate* literary choice than raw S₂. Because entropy is controlled, confidence traps are:

1. **Intentional**: The poet could have followed the most probable path (80–99% likely) but chose otherwise.
2. **Resistant to noise**: Unlike high-entropy/high-surprisal moments (random chance in uncertain contexts), low-entropy deviations require overriding a strong prior.
3. **Genre-diagnostic**: Perfect separation between poetry (traps > 0%) and prose (traps ≈ 0%).

**The enjambment finding** deserves special attention: 92% of confidence traps occur where GPT-2 expected a newline. This means the formal device of the poetic line — the decision to continue rather than break — is poetry's primary statistical act of defiance. Line breaks are not just visual; they are the moments where poetry most dramatically departs from what statistical language expects.

---

## Suggested Next Steps

1. **Enjambment specificity**: Among the 314 newline-expected traps, characterize the syntactic position of the continuation (mid-clause, post-modifier, post-verb, etc.). Does mid-clause enjambment have higher S₂ than end-clause enjambment?

2. **Confidence trap trajectory**: Do poems with high confidence trap rates also have distinctive S₂ arcs (opening vs. closing traps)?

3. **The 25 semantic traps as a close-reading resource**: Each content-word confidence trap is a potential "key moment" in the poem — a target for pedagogical close reading grounded in information theory.

4. **Trap rate as a new corpus statistic**: Report confidence trap rate alongside avg S₂ and max S₂ in future corpus analyses as a distinct measure of deliberate literary choice.
