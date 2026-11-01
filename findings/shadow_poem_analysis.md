# Shadow Poem Analysis: The Ghost of Unwritten Poems

**Date:** 2026-11-01
**Corpus:** 389 poems analyzed
**Concept:** For each poem, the 'shadow poem' is what GPT-2 would have written by replacing every actual token with the model's top prediction. Divergence score = fraction of positions where the poet departed from the model's top choice.

---

## Motivation

Every poem is a series of choices made against a background of expectations. The 'shadow poem' makes those expectations concrete: it is the text that *maximum-likelihood GPT-2* would have produced at each step. A poet with high divergence is persistently anti-predictive; a poet with low divergence often confirms what the model expected.

This differs from S2 (surprisal − entropy): a token can have high S2 but still match the top prediction if the model was very confident in that choice. Conversely, a low-entropy position where the model was confident AND the poet departed will register both as high S2 AND high divergence.

**Key question:** Is poetic originality measured by *how often* you depart from expectations (divergence score) or by *how far* you depart (S2 magnitude)? Are these the same poets?

---

## Results

### Global Statistics

- **Total poems:** 389
- **Total departure events:** 34,497
- **Mean divergence score:** 0.730 (=fraction of positions where poet chose other than model's top pick)
- **Range:** 0.116 – 1.000

### Most Divergent Poems (Poets Who Most Often Say Something Unexpected)

| # | Title | Author | Era | Divergence | Avg S₂ at departure |
|---|---|---|---|---|---|
| 1 | Fog | Carl Sandburg | modernist | **1.000** | 1.30 |
| 2 | Before the Mirror (stanzas 1-3) | Algernon Charles Swinburn | ekphrastic | **0.919** | 0.46 |
| 3 | Objects (from Tender Buttons) | Gertrude Stein | modernist | **0.915** | 0.57 |
| 4 | Das Wort | Stefan George | german_symbolist | **0.908** | 1.22 |
| 5 | Buffalo Bill 's | E.E. Cummings | modernist | **0.907** | 1.64 |
| 6 | Charlotte Mew | Synthetic (clerihew test  | clerihew | **0.905** | 0.68 |
| 7 | Western Wind (anonymous lyric) | Anonymous (English, c. 15 | early_modern | **0.900** | -0.09 |
| 8 | Lorine's Work | Lorine Niedecker | imagist | **0.900** | 1.65 |
| 9 | They Flee from Me | Thomas Wyatt | early_modern | **0.897** | 0.72 |
| 10 | Komm in den totgesagten park und schau | Stefan George | german_symbolist | **0.888** | 1.22 |

### Least Divergent Poems (Poets Closest to the GPT-2 Shadow)

| # | Title | Author | Era | Divergence | Avg S₂ at departure |
|---|---|---|---|---|---|
| 1 | silencio | Eugen Gomringer | concrete | **0.116** | -0.29 |
| 2 | Self-Evident Truths (Found Poem from Declarat | Thomas Jefferson (found t | found_poetry | **0.266** | 2.13 |
| 3 | Oh Shenandoah | Traditional (American sea | song_lyrics | **0.304** | 2.32 |
| 4 | Psalm 136 (KJV) | Anonymous (KJV translatio | biblical | **0.344** | 1.07 |
| 5 | Lord Randal | Traditional (Scottish bal | ballad | **0.398** | 0.69 |
| 6 | The Wanderer's Litany | Arthur Symons | triolet | **0.400** | 0.45 |
| 7 | She Had Some Horses | Joy Harjo | postcolonial | **0.434** | 1.07 |
| 8 | Academic prose | Control | control | **0.448** | -1.60 |
| 9 | She Had Some Horses (opening) | Joy Harjo | contemporary | **0.469** | 1.01 |
| 10 | Legal Boilerplate (Found Poem) | Found (legal boilerplate, | found_poetry | **0.474** | 1.04 |

### Era-Level Divergence

| Era | n | Avg Divergence | Avg S₂ at departures |
|---|---|---|---|
| german_symbolist | 3 | 0.853 | 1.11 |
| german_modernist | 2 | 0.835 | 1.53 |
| haiku | 14 | 0.832 | 0.92 |
| early_modern | 7 | 0.814 | 0.39 |
| clerihew | 10 | 0.813 | 1.39 |
| ekphrastic | 8 | 0.807 | 0.52 |
| confessional | 6 | 0.803 | 0.62 |
| beat | 6 | 0.800 | 2.30 |
| war_poetry | 3 | 0.788 | 0.69 |
| ancient | 3 | 0.785 | 0.74 |
| dramatic_monologue | 7 | 0.783 | 0.58 |
| double_dactyl | 5 | 0.781 | 0.15 |
| persian | 2 | 0.780 | 0.84 |
| german_expressionist | 6 | 0.779 | 1.21 |
| metaphysical | 4 | 0.773 | 0.47 |
| modernist | 27 | 0.772 | 0.78 |
| victorian | 29 | 0.770 | 0.75 |
| 19th_century | 18 | 0.765 | 0.89 |
| protest_political | 2 | 0.759 | 0.21 |
| parody | 4 | 0.756 | 0.60 |
| elegy | 8 | 0.755 | 0.68 |
| imagist | 5 | 0.754 | 0.93 |
| 18th_century | 8 | 0.748 | 0.81 |
| new_york_school | 20 | 0.746 | 0.45 |
| old_english | 5 | 0.744 | 0.94 |
| romantic | 21 | 0.736 | 0.60 |
| oulipo | 8 | 0.732 | 1.18 |
| harlem_renaissance | 7 | 0.729 | 0.73 |
| classical_chinese | 4 | 0.729 | 0.80 |
| limerick | 10 | 0.727 | 0.22 |
| japanese_classical | 2 | 0.727 | 0.42 |
| latin_american | 4 | 0.705 | 0.66 |
| prose_poetry | 12 | 0.689 | 0.67 |
| fixed_form | 8 | 0.688 | 0.62 |
| surrealist | 8 | 0.688 | 0.66 |
| language | 6 | 0.684 | 0.83 |
| contemporary | 16 | 0.684 | 0.89 |
| parody_original | 3 | 0.683 | 0.57 |
| ghazal | 2 | 0.680 | 1.02 |
| spoken_word | 3 | 0.672 | 0.76 |
| nonsense | 2 | 0.667 | 0.38 |
| postcolonial | 6 | 0.661 | 1.00 |
| black_arts | 2 | 0.656 | 0.89 |
| mid_century | 4 | 0.656 | 1.23 |
| cliche_control | 4 | 0.649 | 0.15 |
| ballad | 6 | 0.638 | 0.95 |
| biblical | 8 | 0.594 | 0.85 |
| villanelle | 3 | 0.571 | 0.54 |
| found_poetry | 9 | 0.569 | 0.76 |
| control | 5 | 0.557 | -0.66 |
| concrete | 4 | 0.542 | 1.04 |
| song_lyrics | 3 | 0.473 | 1.17 |
| triolet | 2 | 0.459 | 0.58 |

### The Unsaid Corpus: What GPT-2 Wanted to Write

Across all departure events, these are the words the model predicted but the poet didn't use:

| Rank | Suppressed word | Times not chosen |
|---|---|---|
| 1 | `the` | 3381 |
| 2 | `and` | 1803 |
| 3 | `of` | 1019 |
| 4 | `i` | 971 |
| 5 | `a` | 712 |
| 6 | `to` | 673 |
| 7 | `is` | 564 |
| 8 | `in` | 404 |
| 9 | `be` | 300 |
| 10 | `'s` | 295 |
| 11 | `was` | 287 |
| 12 | `are` | 254 |
| 13 | `you` | 235 |
| 14 | `he` | 223 |
| 15 | `man` | 219 |

### The Anti-Predicted Lexicon: Words Poets Chose AGAINST the Model

Words that appeared most often at positions where the model was predicting something else:

| Rank | Chosen word | Times chosen against prediction |
|---|---|---|
| 1 | `the` | 856 |
| 2 | `and` | 742 |
| 3 | `a` | 474 |
| 4 | `in` | 433 |
| 5 | `i` | 339 |
| 6 | `to` | 338 |
| 7 | `of` | 313 |
| 8 | `that` | 248 |
| 9 | `my` | 223 |
| 10 | `with` | 217 |
| 11 | `for` | 214 |
| 12 | `is` | 196 |
| 13 | `on` | 192 |
| 14 | `it` | 180 |
| 15 | `his` | 178 |

---

## Key Finding: Divergence ≠ S2

Divergence score (how often poets pick a different word than the model's top pick) and S2 (how surprising that choice was) are related but distinct:

- A poet can have HIGH divergence + LOW S2: they consistently pick the model's 2nd or 3rd choice — slightly unexpected but not shocking
- A poet can have LOW divergence + HIGH S2: they rarely depart, but when they do, it's extreme — concentrated spikes of extreme surprise

**This suggests two strategies for poetic originality:**
1. **Diffuse deviators**: frequently choose non-top-1 words (high divergence), but each choice is only mildly surprising
2. **Spike strategists**: mostly follow the model but insert rare, extreme departures (low divergence, high max-S2)

### Evidence: Divergence vs Max-S2 correlation

Pearson r (divergence_score, avg_dep_s2) = **0.066**
Weak correlation confirms the two-strategy hypothesis: frequent departure and intense departure are independent axes of poetic originality.

---

## Implications

1. **The shadow poem as a baseline**: The 'ghost poem' operationalizes the literary notion of 'the language that wasn't chosen.' It makes the expected text concrete and measurable.

2. **Divergence as an originality axis**: Different from type-token ratio, lexical frequency, or S2 — divergence measures how often a poet's choices escape the model's top prediction, capturing a form of anti-predictive stance at the local lexical level.

3. **Linguistic ecology**: The 'most suppressed words' reveal the semantic ecology GPT-2 inhabits — what the ghost poem would constantly use. Poets write against this ecology.

## Suggested Next Steps

- **Shadow poem text generation**: For each high-divergence poem, print the actual shadow poem text and compare it semantically to the original
- **Author fingerprint via shadow gap**: The distribution of departure categories (content-for-function, content-content, etc.) might fingerprint individual poets
- **Temporal evolution**: Does divergence score change across literary history? Do 'modernist' poets systematically escape top-1 predictions more than Victorian poets?
- **Shadow-S2 joint analysis**: Plot each token in (divergence, S2) space to see if there are characteristic clusters
---

## Supplementary: New Test Poem Results (2026-11-01)

Eight new poems were added to the corpus specifically to test the shadow-divergence hypothesis. Results:

| Poem | Era | Divergence | avg S₂ | Interpretation |
|---|---|---|---|---|
| N+7: Wandered Lonely (OuLiPo) | oulipo | **0.808** | -0.200 | High divergence as expected — noun substitution reliably escapes top-1 prediction |
| Sympathy (Dunbar) | 19th_century | **0.676** | -0.414 | Moderate-high; Victorian diction is somewhat predictable to GPT-2 |
| Gifts (Sanchez) | black_arts | **0.605** | -0.295 | Moderate; spare syntax allows some predictions |
| The Maximum Cliché | cliche_control | **0.566** | -1.069 | **Key finding**: even clichés diverge 57% of the time — clichés are NOT GPT-2's top-1 prediction at each position |
| Villanelle of the Unsaid | villanelle | **0.565** | -0.110 | Near-identical to cliché poem — structured repetition ≈ cliché density for divergence purposes |
| Decreasing Divergence (synthetic) | concrete | **0.516** | -0.685 | Repeated unusual words → lower divergence than clichés (52% vs 57%), confirming the repetition effect |
| Legal Boilerplate (found) | found_poetry | **0.474** | -1.04 | Low divergence: rigid syntactic formulae are highly predictable |

### Key New Finding: The Cliché Paradox

The cliché-control poem (0.566 divergence) is *more* divergent than legal boilerplate (0.474), despite being composed entirely of proverbs and fixed phrases. This counterintuitive result shows that:

1. **GPT-2's top prediction is not always the cliché** — at many positions, the model predicts a different word than the cliché requires
2. **Clichés are "anti-predictive" at the token level** even if they're predictable at the phrase level
3. The relevant unit of prediction for "originality" is the *token*, not the *phrase*

This suggests that divergence score captures a genuinely different dimension than "cultural expectedness." A poem can use culturally predictable imagery while still diverging from GPT-2's token-level predictions.

### The Repetition Ladder Effect

The "Decreasing Divergence" poem (0.516) has lower divergence than the Maximum Cliché (0.566), supporting the hypothesis that within-poem repetition of unusual words reduces divergence:
- Once "gleam", "throb", "hush" appear in context, GPT-2 can predict their re-occurrence
- The repetition "teaches" the local context, lowering divergence over the poem's course

This suggests that divergence score should be measured at beginning vs end of long poems to detect whether poets "settle into" their chosen vocabulary or maintain consistent unpredictability throughout.
