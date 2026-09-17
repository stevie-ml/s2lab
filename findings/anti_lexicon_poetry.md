# The Poetry Anti-Lexicon: What Language Expects and Poets Refuse
**Date:** 2026-09-17  
**Experiment:** `experiments/anti_lexicon.py`  
**Corpus:** 128 texts, 13,341 tokens, 4,327 S2>0.5 events

---

## Research Question

When a poet's word choice diverges from GPT-2's expectation (S2 > 0.5), something is *refused*. 
This experiment inverts the usual Straussian analysis: instead of cataloguing what poets *chose*, 
it asks **what language kept expecting but never received** — the negative vocabulary of poetry.

If there's a systematic anti-lexicon, it tells us what *prose logic* is, and how poetry escapes it.

---

## Key Finding 1: The Comma Is Poetry's Most-Rejected Word

| Rank | Word    | Rejections | Avg Prob | Total Prob Mass |
|------|---------|-----------|----------|----------------|
| 1    | `,`     | 409       | 0.236    | 96.5           |
| 2    | `the`   | 329       | 0.217    | 71.4           |
| 3    | `and`   | 168       | 0.174    | 29.3           |
| 4    | `.`     | 132       | 0.259    | 34.2           |
| 5    | `of`    | 116       | 0.285    | 33.1           |
| 6    | `I`     | 113       | 0.190    | 21.4           |
| 7    | `a`     | 78        | 0.193    | 15.1           |
| 8    | `to`    | 74        | 0.309    | 22.9           |
| 9    | `is`    | 52        | 0.235    | 12.2           |
| 10   | `was`   | 48        | 0.191    | 9.2            |

The **comma** accounts for 409 rejections and 96.5 units of total probability mass — 
far more than any single content word. When language "breathes" with commas, 
poetry often refuses the breath. 

The **definite article** ("the") is the second most rejected word. Poetry prefers 
indefiniteness, directness, or nothing — consistent with the lyric tendency to name 
things outside their usual frames.

---

## Key Finding 2: "To" and "That" Are Rejected with the Most Confidence

| Rejected Word | Avg Probability When Rejected |
|---------------|------------------------------|
| `that`        | 0.324                        |
| `you`         | 0.311                        |
| `to`          | 0.309                        |
| `of`          | 0.285                        |
| `.`           | 0.259                        |
| `'s`          | 0.250                        |
| `the`         | 0.217                        |

When GPT-2 expects **"that"** (a subordinating conjunction) or **"to"** (an infinitive marker), 
it is *very* confident — average probability ~31-32%. Yet poets regularly refuse these. 
This suggests that poetry systematically declines the subordination and instrumentality 
that prose grammar requires ("he said *that*...", "she wanted *to*...").

---

## Key Finding 3: What Poets Choose Instead

When poets refuse the most common expected words, these are their substitutions:

| Refused    | Top 5 Substitutions                                                  |
|------------|----------------------------------------------------------------------|
| `,`        | *(nothing/line break)* (15), `:` (12), `!` (9), `;` (7), `—` (7)   |
| `the`      | *(nothing)* (10), `a` (6), `upon` (4), `me` (4), `these` (3)       |
| `and`      | *(nothing)* (23), `which` (3), `as` (2), `fl` (2)                   |
| `.`        | *(nothing/enjambment)* (13), `;` (4), `and` (4), `you` (3)          |
| `of`       | *(nothing)* (13), `;` (4), `,` (3), `that` (3), `a` (2)            |
| `is`       | `lies` (2), *(nothing)* (2), `runs` (2)                             |

Three structural patterns emerge:

**A. Enjambment preference**: The most common substitute for commas, full stops, "and", and "of" 
is *nothing* — a line break or direct continuation. Poetry converts expected punctuation into breath.

**B. Upgrading the pause**: When commas are rejected, poets most often use `:`, `!`, `;`, or `—` — 
all more emphatic or semantically loaded than the comma.

**C. The kinetic substitution**: When the copula `is` (a statement of being) is rejected, 
poets choose *kinetic* verbs: `lies`, `runs`. Poetry prefers action to state.

---

## Key Finding 4: Era-Level Anti-Lexicons

Different poetic eras have different refusal patterns:

| Era               | Top Rejected Word | Count | Signature                              |
|-------------------|-------------------|-------|----------------------------------------|
| Victorian         | `,`               | 72    | Maximal comma-refusal — resists pause  |
| Romantic          | `,`               | 46    | Similar anti-comma tendency            |
| Ballad            | `,`               | 48    | Oral rhythm resists prose punctuation  |
| New York School   | `the`             | 50    | Avoids the definite; prefers openness  |
| Modernist         | `the`             | 53    | Refuses ordinary definiteness          |
| Harlem Renaissance | `the`            | 16    | Refusing definiteness / "not"          |
| Language Poetry   | `.`               | 5     | Resists closure / full stops           |
| Prose Poetry      | `.`               | 24    | Resists the very punctuation it uses   |
| Beat              | `,` / `and`       | 9/5   | Breathless, conjunctive avoidance      |

**Victorian vs. Language poetry**: Both resist their era-typical discourse patterns.
Victorian poetry refuses the comma (elaborate syntax without obvious pause), while 
Language poetry most distinctively refuses the **period** — resisting semantic closure.

**Prose poetry paradox**: Prose poetry's top rejection is the full stop (`.`), rejecting 
the very punctuation that defines prose. It uses prose's form while defeating its finality.

---

## Key Finding 5: The Dodge Sequence — GPT-2's Persistence

A "dodge sequence" occurs when GPT-2 wants the same word for N consecutive positions 
but the poet keeps refusing it:

| Poem                            | Poet          | Avoided Word | Length | Poet's Choices |
|---------------------------------|---------------|-------------|--------|----------------|
| A Noiseless Patient Spider      | Walt Whitman  | `the`       | 4×     | `'d`, `where`, `on`, `a` |
| Yet Do I Marvel                 | Countee Cullen | `the`      | 3×     | `if`, `merely`, `brute` |
| The Road Not Taken              | Robert Frost  | `,`         | 3×     | `them`, `really`, `about` |

**Whitman's 4-token "the" dodge** is the longest in the corpus. This confirms his 
characteristic cataloguing style: Whitman builds enumeration through anaphora, 
consistently refusing the article-based definiteness that prose grammar insists on.

**Cullen's "the"-dodge in "Yet Do I Marvel"**: GPT-2 wants "the" but instead gets 
`if` → `merely` → `brute` — a sequence that escalates from conditional to emphatic 
to raw. The article's domesticity is rejected in favor of ontological weight.

---

## Summary Interpretation

The Poetry Anti-Lexicon reveals that the most consistently rejected words in poetry 
are not random. They cluster into three categories of prose grammar that poetry refuses:

1. **Pause markers** (`,` `.` `;`): Prose breathes on grammar's schedule; poetry breathes on its own.
2. **Definiteness markers** (`the`, `a`, `of`, `'s`): Prose locates things in reality; poetry suspends location.
3. **Subordination/continuity markers** (`and`, `to`, `that`, `is`): Prose connects clauses; poetry juxtaposes.

The anti-lexicon is, in effect, a portrait of **prose logic** — the grammar of explanation, 
causation, and definiteness that poetry systematically transcends.

---

## Suggested Next Steps

1. **Anti-lexicon over time**: Track whether the rejected words shift across literary history 
   (the 19th-century comma-refusal vs. the 20th-century article-refusal).
2. **Individual poet anti-lexicons**: Do specific poets have signature refusals? 
   (Whitman refuses "the"; Dickinson might refuse "and"; Celan might refuse articles differently.)
3. **Quantify the prosification test**: Given a poem, compute its "anti-lexicon compliance score" —
   how often does it accept what GPT-2 predicts vs. refuse it. A high compliance score might 
   detect prose poetry or weak verse masquerading as poetry.
4. **Cross-language anti-lexicons**: German poetry shows its own refusal patterns (rejecting 
   `die`, `und`, `der`). Are these structurally analogous to English rejections, or different?
