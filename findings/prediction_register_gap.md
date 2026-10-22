# Prediction Register Gap: Function vs. Content Word Expectations

**Date:** 2026-10-22  
**Experiment:** `experiments/prediction_register_gap.py` → `results/prediction_register_gap.json`  
**Corpus:** 321 texts, 37,878 English tokens; 22,288 qualifying (|S₂| ≥ 2.0)  

---

## Research Question

When GPT-2 predicts a **function word** but the poet writes a **content word** (or vice versa), what are the information-theoretic signatures? Can we classify the type of Straussian gap by the lexical register of both the model's top prediction and the poet's actual choice?

This experiment classifies every qualifying token into three registers:
- **punct** — pure punctuation (`,`, `.`, `—`, `'`, etc.)
- **function** — articles, prepositions, conjunctions, pronouns, auxiliaries
- **content** — nouns, verbs, adjectives, adverbs (semantically loaded)

Then builds a 3×3 matrix: GPT-2's prediction register × poet's actual register.

---

## Core Finding: Content Words Are the Engine of Surprise

The 3×3 mean S₂ matrix reveals a strikingly **asymmetric structure**:

| Predicted → Chose | punct | function | content |
|---|---|---|---|
| **Predicts punct** | −2.867 | −0.105 | **+4.269** |
| **Predicts function** | −0.916 | −2.529 | **+4.273** |
| **Predicts content** | −0.320 | −0.119 | −0.042 |

**The content-word column contains all the positive S₂.** Regardless of what register the model predicted, if the poet writes a *content word*, mean S₂ is ~+4.27. If the model predicted content but got content, S₂ falls to −0.042 (near neutral). If the model predicted content but got a function word or punctuation, S₂ is slightly negative.

**The diagonal pattern**: same-register choices are strongly negative:
- punct→punct: −2.867 (only 6.5% positive — almost always conformist)  
- function→function: −2.529 (only 13.8% positive)
- content→content: −0.042 (41.2% positive — near neutral)

---

## The Two-Part Model of Poetic Surprise

This clarifies what the Straussian gap actually *is* at the register level:

**Positive S₂ overwhelmingly comes from "semantic invasion"**: placing a content word where grammar (function word) or punctuation was expected. This is the poet *refusing to close* a syntactic unit — inserting semantic charge where the machinery demands maintenance, closure, or pause.

**Negative S₂ comes from grammatical conformity**: following the expected grammatical pattern (function→function at −2.529, punct→punct at −2.867). Punctuation is the most "expected" act possible — when the model predicts a comma and gets a comma, it represents the deepest information valley in poetry.

---

## Count Matrix

| Predicted → Chose | punct | function | content | Total |
|---|---|---|---|---|
| **Predicts punct** | 2,230 | 831 | 897 | 3,958 |
| **Predicts function** | 569 | 8,487 | 3,585 | 12,641 |
| **Predicts content** | 146 | 598 | 4,945 | 5,689 |

29.7% of qualifying tokens are cross-register violations; 70.3% stay within the same register. The most common cross-register event is **function → content** (3,585 cases) — the dominant form of poetic surprise in this corpus.

---

## Striking Exemplars: Semantic Invasion (function → content)

When GPT-2 predicted a function word (` `, `'m`, etc.) and the poet wrote a content word:

| Token | Predicted | S₂ | Author | Era |
|---|---|---|---|---|
| ` gro` | ` ` | +36.66 | Lawrence Ferlinghetti | beat |
| ` climbs` | ` ` | +28.25 | Lawrence Ferlinghetti | beat |
| ` pour` | `'m` | +27.73 | Charles Bukowski | spoken_word |
| ` hum` | ` ` | +25.65 | Kamau Brathwaite | postcolonial |
| ` glass` | ` ` | +25.63 | Marianne Moore | modernist |

Note: Ferlinghetti's extreme cases (` `, a bare space) represent GPT-2 predicting whitespace continuation inside a broken word — and the poet cutting into a new semantic unit mid-token. This is the typographic enjambment exploit.

---

## Punctuation Invasion (punct → content)

When GPT-2 predicted punctuation and the poet wrote a content word — the "comma interrupted":

| Token | Predicted | S₂ | Author | Era |
|---|---|---|---|---|
| ` observing` | `,` | +20.40 | Walt Whitman | 19th_century |
| `lay` | `,` | +18.85 | Vachel Lindsay | modernist |
| ` poems` | `,` | +18.06 | Joy Harjo | postcolonial |
| ` onward` | `,` | +18.04 | Alfred, Lord Tennyson | victorian |
| ` mounting` | `,` | +17.93 | T.S. Eliot | dramatic_monologue |

This is the **Whitmanic catalog**. The model expects a pause after the first item; the poet delivers the next item. Whitman's ` observing` after a predicted comma (+20.40) perfectly exemplifies "the catalog that does not stop."

---

## Era Breakdown: Who Violates Registers Most?

Eras ranked by **total cross-register rate** (including all violation types):

| Era | N | %Cross | Mean S₂ | %Func→Content |
|---|---|---|---|---|
| clerihew | 78 | 39.7% | 4.205 | 20.5% |
| early_modern | 719 | 35.6% | 2.198 | 17.8% |
| 18th_century | 720 | 34.6% | 3.044 | 21.0% |
| war_poetry | 384 | 33.9% | 2.754 | 18.8% |
| harlem_renaissance | 405 | 33.8% | 2.647 | 19.0% |
| romantic | 1,446 | 32.7% | 2.696 | 17.0% |
| beat | 433 | 23.8% | **5.363** | 16.9% |
| language | 234 | 23.1% | 3.275 | 12.8% |
| control (clichés) | 74 | 16.2% | **−1.067** | 9.5% |

**Beat poetry paradox**: Beat shows the lowest cross-register rate (23.8%) but the *highest mean cross-register S₂* (5.363). Beat poets cross registers *less often*, but when they do, they go further. This contrasts with early modern and neoclassical poetry: high cross-register rate but more moderate S₂.

**Cliché control baseline**: 16.2% cross-register, and mean S₂ of −1.067 — confirming that formulaic texts stay within register almost completely, and their cross-register "violations" are still below expectation.

---

## Author Signature: Semantic Invasion Rate

Authors ranked by **func → content invasion rate** (content words placed in grammatical slots):

| Author | N | %Invasion | %Retreat | Mean Invasion S₂ |
|---|---|---|---|---|
| Ko Un | 64 | 31.2% | 0.0% | 1.812 |
| Maya Angelou | 56 | 26.8% | 1.8% | 3.837 |
| John Dryden | 90 | 25.6% | 0.0% | 4.310 |
| **Hart Crane** | 98 | 24.5% | 1.0% | **6.362** |
| Gregory Corso | 139 | 24.5% | 2.9% | 4.406 |
| Samuel Taylor Coleridge | 127 | 24.4% | 0.8% | 5.667 |
| Robert Bly | 38 | 23.7% | 0.0% | 5.611 |
| Marianne Moore | 223 | 22.4% | 1.3% | 5.344 |

**Hart Crane** stands out: not just high invasion rate (24.5%) but the highest mean invasion S₂ (6.362). When Crane fills a grammatical slot with a content word, the word is *maximally unexpected*. His notorious difficulty is precisely this: putting wildly surprising nouns and verbs where the syntax demands transitions.

**John Dryden** at 25.6% is counterintuitive for a neoclassical poet — but cross-tabulates with the 18th-century era's overall high cross-register rate. Dryden's heroic couplets use dense periodic syntax, creating many grammatical slots that content words can invade.

**The grammatical retreat (content → function)** is nearly zero for many poets (0.0% for Ko Un, Dryden, Bly). The asymmetry is absolute: poets invade grammatical slots with semantic content, but almost never substitute function words for expected content. **Choosing a function word where content is expected is not a poetic strategy.**

---

## The Two Rules of Poetic Information Management

This experiment reveals that poetic surprise at the register level follows two asymmetric rules:

1. **The Content Invasion Rule**: Place a content word where a function word or punctuation is expected → S₂ ≈ +4.27 (82% of cases positive). This is the primary mechanism of surprise across all poets and eras.

2. **The Grammar-Following Rule**: Follow the predicted register (especially punct→punct, function→function) → S₂ deeply negative. Grammatical conformity *accelerates the reader's processing* — it's not neutral, it's actively anti-surprising.

**The corollary**: poets manage reader surprise not primarily by choosing *unusual content words* in content slots (content→content is near-neutral, −0.042), but by *misaligning the register of their word choice with the structural slot*. The grammar expects maintenance; the poet delivers meaning.

---

## Relationship to Previous Findings

- **surprise_asymmetry.md** showed post-spike valleys are deeper than pre-spike setups. This experiment shows that those valleys correspond primarily to punct→punct and function→function sequences — the grammar reasserts itself.
- **straussian_gap_taxonomy.md** classified gap types semantically. This adds a structural grammar layer: the dominant gap type is register invasion (function slot → content word).
- **opening_salvo.md** showed first-line S₂ is elevated. This suggests opening lines disproportionately use the content-invasion strategy — seizing grammatical structure to assert meaning early.

---

## Suggested Next Steps

1. **Diachronic invasion rates**: Does the content-invasion rate change across literary history? (Predict: modernism increases invasion; neoclassicism channels it differently into syntactic density)
2. **Intraline position of invasions**: Do content invasions concentrate at line-initial positions (where grammar is most open) or mid-line?  
3. **Syntactic slot specificity**: Among function words, which grammatical positions are most invaded? Preposition slots? Conjunction slots? Pronoun slots?
4. **Beat poetry deep dive**: Why does beat have the highest mean cross-register S₂ but lower rate? Is it specific syntactic structures (dropped prepositions, verbless catalogs)?
