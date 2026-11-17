# The Grammar Escape: Classifying Poetic Deviation by Category Jump

**Date:** 2026-11-17  
**Experiment:** `experiments/category_jump_analysis.py` → `results/category_jump_analysis.json`  
**Corpus:** 431 texts, 56,827 artifact-free tokens (artifact threshold: p(newline) ≥ 0.90)  
**Builds on:** `genuine_surprise_catalog.md`, `stanza_break_artifact.md`

---

## Research Question

At genuine (non-artifact) high-S₂ positions, **what KIND of deviation does the poet make?** When GPT-2 predicted something with high confidence and the poet chose otherwise, can we classify the gap by the grammatical/semantic *category* of what was expected vs. what was written?

This experiment classifies every token and its top GPT-2 alternative into four categories:
- **GRAMMAR**: function words, articles, pronouns, prepositions, auxiliaries (*the, to, is, it, and, ...*)
- **CONTENT**: lexical/content words (everything else)
- **PUNCTUATION**: commas, periods, semicolons, etc.
- **WHITESPACE**: spaces and newlines (residual after main artifact filter)

The "category jump" is `EXPECTED_CAT→ACTUAL_CAT`.

---

## Main Finding: The Grammar Escape Dominates

At all 4,983 genuine high-S₂ positions (s₂ > 5.0 bits, after artifact filter):

| Category Jump | Count | % | Interpretation |
|---|---|---|---|
| **GRAMMAR→CONTENT** | 1,971 | **39.6%** | poet suppressed grammar, chose content |
| **CONTENT→CONTENT** | 1,191 | **23.9%** | semantic substitution |
| **PUNCTUATION→CONTENT** | 586 | **11.8%** | poet suppressed punctuation, chose content |
| WHITESPACE→CONTENT | 327 | 6.6% | partial artifact residual |
| GRAMMAR→GRAMMAR | 266 | 5.3% | chose different function word |
| other | 642 | 12.9% | minor types |

**The dominant move in genuine poetic surprise is GRAMMAR→CONTENT (40%).**
When a poet achieves a high-information deviation, the most common pattern is: GPT-2 expected a function/grammar word (`the`, `to`, `is`, etc.) and the poet substituted a content word instead. This is the **grammar escape** — refusing to write the structural scaffolding of ordinary language in favor of a direct semantic choice.

The second most common move is **CONTENT→CONTENT (24%)** — the poet chose an unexpected content word where a different content word was expected. This is **semantic substitution**: the grammatical category is correct but the specific word is unexpected.

---

## The Jump Distribution Is Stable Across S₂ Levels

Strikingly, the distribution of category jumps barely changes as S₂ increases:

| S₂ range | n | Dominant jump | % | CONTENT→CONTENT% |
|---|---|---|---|---|
| moderate (5–90th pct) | 2,841 | GRAMMAR→CONTENT | 37% | 25% |
| 90th–95th pct | 2,273 | GRAMMAR→CONTENT | 42% | 23% |
| top 1% (mean S₂ = 13.86) | 568 | GRAMMAR→CONTENT | 39% | 24% |

The same categorical mechanisms produce both moderate and extreme surprise. High S₂ is not a qualitatively different phenomenon — it is the same grammar-escape and semantic-substitution operations, executed in higher-probability positions (where GPT-2 was more confident).

---

## Examples of Each Jump Type

### GRAMMAR→CONTENT (the grammar escape)

| Author | Context | GPT-2 expected | Poet wrote | S₂ |
|---|---|---|---|---|
| Charles Bukowski | `...but I` | `'m` (99.7%) | ` pour` | 27.73 |
| Anonymous (Beowulf trans.) | `...that he` | ` may` (39.3%) | `riot` | 22.73 |
| Christopher Smart | `...he rolls upon` | ` the` (45.5%) | ` prank` | 22.13 |
| Gerard Manley Hopkins | `...like shining from` | ` the` (38.7%) | ` shook` | 22.04 |

Pattern: GPT-2 expected an article, auxiliary, or preposition. The poet dropped the grammatical frame and placed a content word directly.

### CONTENT→CONTENT (semantic substitution)

| Author | Context | GPT-2 expected | Poet wrote | S₂ |
|---|---|---|---|---|
| Robert Browning | `...clap your` | ` hands` (96.0%) | ` torches` | 19.69 |
| Emily Dickinson | `...felt a` | ` little` (19.1%) | ` Fun` | 18.90 |
| Elizabeth Bishop | `...the hour` | `glass` (83.6%) | ` badly` | 20.59 |
| Jean Lescure | `...he called Night` | `time` (78.4%) | `jar` | 22.97 |

Pattern: GPT-2 expected a specific content word (often a collocate of the preceding word — `clap your hands`, `hourglass`, `Nighttime`). The poet refused the conventional collocation.

### GRAMMAR→GRAMMAR (function word substitution)

| Author | Context | GPT-2 expected | Poet wrote | S₂ |
|---|---|---|---|---|
| Edgar Allan Poe | (start) | ` is` (73.4%) | `at` | 17.66 |
| Traditional (Scottish ballad) | `Why do` | ` you` (50.7%) | `is` | 17.47 |
| Kenneth Koch | `, "Do` | ` you` (92.4%) | ` most` | 14.42 |

Pattern: Rare but interesting — the poet chose a *different* function word, not content at all. These tend to be archaic or dialectal grammatical constructions.

---

## Poet Profiles: Grammar Escape vs. Semantic Substitution

| Poet | G→C% | C→C% | n | Dominant Strategy |
|---|---|---|---|---|
| Alfred Lord Tennyson | 61% | 18% | 124 | Strong grammar escape |
| John Donne | 59% | 18% | 39 | Strong grammar escape |
| John Milton | 54% | 14% | 37 | Strong grammar escape |
| William Blake | 54% | 21% | 52 | Strong grammar escape |
| Thomas Hardy | 54% | 28% | 97 | Grammar escape |
| **Georg Trakl** | **0%** | **63%** | **35** | Pure semantic substitution |
| Christina Rossetti | 22% | 42% | 40 | Semantic substitution |
| Emily Dickinson | 38% | 34% | 68 | Mixed |
| John Ashbery | 46% | 35% | 106 | Mixed, slight grammar |
| Traditional (Scottish ballad) | 29% | 35% | 69 | Semantic substitution |

**Georg Trakl is the strongest outlier**: 0% grammar escape, 63% semantic substitution. His German Symbolist/Expressionist poetry achieves all its major surprises through unexpected semantic choices — placing the wrong noun, the wrong verb — without avoiding grammatical structure at all. English Romantic and metaphysical poets (Tennyson, Donne, Milton) show the opposite pattern: they escape grammar far more than they substitute content.

---

## Era Breakdown

| Era | Dominant jump | % | n |
|---|---|---|---|
| classical_chinese | GRAMMAR→CONTENT | 75% | 20 |
| deep_image | GRAMMAR→CONTENT | 83% | 6 |
| 18th_century | GRAMMAR→CONTENT | 56% | 124 |
| dramatic_monologue | GRAMMAR→CONTENT | 52% | 329 |
| **black_arts** | CONTENT→CONTENT | 56% | 16 |
| **ballad** | CONTENT→CONTENT | 33% | 83 |
| **concrete** | CONTENT→CONTENT | 27% | 22 |
| beat | GRAMMAR→CONTENT | 31% | 108 |

Classical and 18th-century poetry show the strongest grammar-escape profiles. Black Arts movement poetry (Gwendolyn Brooks, Sonia Sanchez) shows the strongest semantic-substitution profile — surprise comes not from avoiding grammar but from choosing unexpected content words within conventional structures.

---

## Interpretation

The **grammar escape** (GRAMMAR→CONTENT) is the statistical signature of a poet breaking the *articulation* of language: the moment when instead of writing "and then the..." they write "rivers." This is what it looks like, informationally, when a poet strips out the connective tissue and forces the reader directly into sense-data.

The **semantic substitution** (CONTENT→CONTENT) is a different operation: honoring the grammatical role of a position but refusing the expected collocation. "Clap your torches" (Browning) keeps the verb-object structure but shatters the cliché. This is surprise within convention.

The fact that both types are present, with consistent proportions across S₂ levels and eras, suggests these are **two fundamental operations of poetic deviation** — not just two points on a spectrum, but distinct strategies for managing reader expectation.

---

## Suggested Next Steps

1. **Within-poem analysis**: Does a single poem alternate between grammar-escape and semantic-substitution, or does a poet tend to use one strategy throughout?
2. **Training data hypothesis**: Are GRAMMAR→CONTENT positions more likely at structurally important moments (volta, turn, final line)?
3. **Cross-model validation**: Would GPT-2 medium / large show the same distribution? Do bigger models shift more surprises into CONTENT→CONTENT (because they learn grammar so thoroughly it's rarely an escape route)?
4. **Georg Trakl deep dive**: The 0% grammar escape finding is striking — verify with a full text analysis of his German originals vs. English translations.
