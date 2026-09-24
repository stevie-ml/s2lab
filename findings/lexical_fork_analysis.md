# Lexical Fork Analysis: How Poets Navigate Model Uncertainty
**Date:** 2026-09-24  
**Experiment:** `experiments/lexical_fork_analysis.py`  
**Corpus:** 180 texts (English poems + control prose), 17,895 tokens

---

## Research Question

When GPT-2's probability is genuinely split among multiple competing tokens — a **lexical fork** — what do poets do? Do they take one of the offered paths, or escape the menu entirely? And how does this compare to **confidence traps** (where the model is certain and the poet ignores it)?

**Fork definition:** Top-1 alternative probability < 2.5× top-2 probability AND top-1 < 50%. The model has no clear dominant prediction — it is genuinely uncertain between competing options.

---

## Key Finding: Three Distinct Surprise Strategies

| Strategy | Definition | n | % of tokens | Avg S₂ | % positive S₂ |
|---|---|---|---|---|---|
| **Confidence trap** | H < 3 bits, rank > 10 (certain model defeated) | 565 | 3.2% | **+19.27** | 100% |
| **Fork escape** | Fork position, rank > 10 (all offered paths rejected) | 4,836 | 27.0% | **+1.998** | 70.2% |
| **Fork navigation** | Fork position, rank ≤ 10 (poet chose an offered path) | 5,244 | 29.3% | **−2.771** | 5.3% |
| Neutral | Everything else | 7,250 | 40.5% | **−0.441** | 28.6% |

**The core finding:** Defeating the *certain* model (confidence traps) produces 10× more surprise than escaping the *uncertain* model (fork escapes). But fork escapes are 8.6× more frequent.

When a poet **takes one of the fork's offered paths**, the result is strongly *negative* S₂ (−2.77). The model was uncertain, but the chosen token was still in the top-10 — so entropy exceeded surprisal, and the poet "landed inside the model's uncertainty." This is low-surprise territory.

---

## When Poets Choose from the Fork Menu, Which Option Do They Take?

| Rank chosen | Count | % of fork navigations |
|---|---|---|
| **1** | 1,677 | **32.0%** |
| **2** | 1,191 | **22.7%** |
| 3 | 646 | 12.3% |
| 4 | 455 | 8.7% |
| 5–10 | 1,275 | 24.4% |

Even at fork positions, poets prefer the model's top-1 or top-2 prediction 54.7% of the time. This makes sense: at a genuine fork, the top-2 are both *plausible* paths, and taking either produces a structurally valid but low-S₂ outcome.

---

## Era Comparison: Fork Escape Rate

| Era | Fork positions | Escapes | Esc. % | Avg S₂ (esc.) |
|---|---|---|---|---|
| **surrealist** | 25 | 17 | **68.0%** | 0.937 |
| **harlem_renaissance** | 314 | 180 | **57.3%** | 1.628 |
| **early_modern** | 358 | 205 | **57.3%** | 1.995 |
| **deep_image** | 37 | 21 | **56.8%** | 2.781 |
| **haiku** | 192 | 106 | **55.2%** | 2.035 |
| **romantic** | 1,147 | 630 | 54.9% | 1.727 |
| **victorian** | 1,250 | 651 | 52.1% | 2.081 |
| modernist | 920 | 465 | 50.5% | 2.084 |
| confessional | 269 | 135 | 50.2% | 2.318 |
| beat | 94 | 45 | 47.9% | 3.830 |
| new_york_school | 896 | 379 | 42.3% | 1.779 |
| prose_poetry | 559 | 213 | 38.1% | 2.197 |
| **cliche_control** | 196 | 66 | **33.7%** | 1.428 |
| **found_poetry** | 498 | 165 | **33.1%** | 2.175 |
| **control (prose)** | 76 | 19 | **25.0%** | 0.214 |

**Key gradient:** Prose control escapes only 25% of forks; poetry ranges from 38–68%. **The more "poetic" the register, the more the writer refuses the model's offered menu.** Surrealism escapes 68% of forks — nearly 3× the prose baseline.

**Beat poetry** shows the lowest escape count (45 escapes) but the *highest average S₂ among escapes* (3.83), suggesting Ginsberg et al. escape fewer forks but when they do, they go far.

**Deep image** (Bly, Wright) has the second-highest average S₂ at escapes (2.78): the compressed, imagistic mode tends to choose words that are far outside the model's uncertainty zone.

---

## The Most Striking Fork Escapes

These are positions where the model offered multiple plausible options AND the poet ignored all of them:

| Poem | Token chosen | S₂ | Model's top offerings |
|---|---|---|---|
| God's Grandeur (Hopkins) | *shook* | 22.04 | "the" / "a" / "heaven" |
| For I Will Consider My Cat (Smart) | *prank* | 22.02 | "the" / "his" / "a" |
| I felt a Funeral (Dickinson) | *Fun* | 18.90 | "little" / "bit" / "sense" |
| Citizen (Rankine) | *stacked* | 18.16 | "ime" / "tense" / "life" |
| On First Looking (Keats) | *trave* | 16.51 | "been" / "ever" / "seen" |
| The Fall (Edson) | *indoors* | 16.40 | "the" / "his" / "life" |
| Howl (Ginsberg) | *hysterical* | 15.61 | "to" / "," / "and" |
| The Collar (Herbert) | *abroad* | 15.36 | "not" / "go" / "never" |
| Old Pond (Bashō trans.) | *spl* | 15.27 | "And" / "A" / "The" |
| My Life (Hejinian) | *yellow* | 14.52 | "," / "later" / "." |
| Anecdote of the Jar (Stevens) | *Tennessee* | 14.20 | "the" / "my" / "a" |
| Why I Am Not a Painter (O'Hara) | *needed* | 13.89 | "is" / "'s" / "does" |

**Patterns:**
- Many top offerings are function words ("the", "and", ",") — the model at forks defaults to grammatical connective tissue; poets refuse to be "grammatical."
- Dickinson's "Fun" at "I felt a Funeral, in my Brain / And Mourning after Mourning beat / Till sense broke through — and I dropped down, and down — / And hit a World at every Fun" — the word "Fun" interrupts a grim sequence and escapes ALL of the model's "little/bit/sense" predictions.
- Ginsberg's "hysterical" in "I saw the best minds of my generation destroyed by madness, *hysterical* naked" — the model expected grammatical connectors; Ginsberg gives an adjective pile-up instead.
- Hopkins' "shook" in "the world is charged with the grandeur of God / It will flame out, like shining from shook foil" — the model expected "the/a/heaven" after "from shining" but Hopkins inverts adjective-before-noun order.

---

## Theoretical Interpretation

This analysis reveals **two distinct poetic surprise strategies:**

1. **Trap defeat** (confidence traps): Attack moments of model certainty. Rare (3.2% of tokens), but each instance is dramatic — avg S₂ = 19.3. The poet finds a niche in the language where convention says "this MUST be X" and writes Y.

2. **Fork escape** (fork escapes): At moments of genuine uncertainty, refuse ALL offered options. Common (27% of tokens), moderate effect — avg S₂ = 2.0. The poet systematically expands the menu at every indeterminate junction.

3. **Fork navigation**: Take one of the fork's offered paths. Counter-intuitively, this produces NEGATIVE S₂ (−2.77). The model was uncertain, but the token was predicted — so the outcome "made sense" relative to what the model was tracking. High in prose; lower in experimental/lyric poetry.

The **fork navigation** result is striking: it means poets who "follow the model's uncertainty" are producing *below-average surprise*. Conformity to one of the model's guesses yields negative information.

---

## Relationship to the Stanza-Break Artifact

Note: fork positions at stanza breaks (where GPT-2 is often predicting a newline and the actual token is the next word) may inflate fork escape counts. Future work should apply the stanza-break artifact filter to check whether these era rankings survive cleaning.

---

## Next Steps

1. **Apply stanza-break filter** to fork escape counts to control for the newline artifact.
2. **Cluster fork escape tokens** by semantic category: what kinds of words poets substitute when rejecting the model's menu?
3. **Compare fork escape rate in the first vs. last stanza** of poems — does the escape rate change as the poem progresses?
4. **Case study: "tracking the menu"** — for a single poem (e.g. Hopkins' "God's Grandeur"), trace every fork position and show what was offered vs what was taken.
5. **Cross-model comparison** — does GPT-2 medium offer different fork menus? Do fork escapes shift?
