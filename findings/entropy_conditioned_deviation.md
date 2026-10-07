# Entropy-Conditioned Deviation: The 'True Straussian' Score

**Date:** 2026-10-06
**Low-entropy threshold:** 5.0 bits (model 'confident' below this)

## Research Question

Not all S₂ is equal. A positive S₂ in a *high-entropy* context means the poet chose
something less likely when the model was already uncertain — not very Straussian,
since any word would be moderately surprising. A positive S₂ in a *low-entropy*
context means the poet defied a confident prediction — the model was sure of what
came next, and the poet said something else entirely.

**True Straussian Score** = fraction of low-entropy tokens where S₂ > 0.
This measures *precision deviation*: the ability to defy confident expectations.

**Control prose True Straussian baseline:** 13.9%

## Top 15 Poems by True Straussian Score

| Poem | Author | Era | True Straussian | Uncertainty Exploit | Avg S₂ | n_low_ent |
|---|---|---|---|---|---|---|
| Morning Glory (Chiyo-ni, translated) | Chiyo-ni | haiku | **66.7%** | 45.5% | +2.08 | 3 |
| Howl (opening) | Allen Ginsberg | beat | **60.0%** | 47.4% | +0.95 | 15 |
| anyone lived in a pretty how town | E.E. Cummings | modernist | **56.2%** | 38.8% | -0.02 | 16 |
| The Truth the Dead Know (excerpt) | Anne Sexton | confessional | **55.6%** | 34.3% | -0.37 | 9 |
| Whereas (excerpt) | Layli Long Soldier | contemporary | **53.3%** | 45.2% | +0.16 | 15 |
| On the Roof of Hell (Issa, translated) | Kobayashi Issa | haiku | **50.0%** | 41.7% | +0.28 | 4 |
| Amoretti LXXV: One Day I Wrote Her Name | Edmund Spenser | early_modern | **50.0%** | 42.6% | -0.26 | 22 |
| I heard a Fly buzz — when I died | Emily Dickinson | 19th_century | **48.4%** | 35.3% | +0.14 | 31 |
| Wet Casements | John Ashbery | new_york_school | **47.8%** | 37.7% | +0.17 | 23 |
| Islets/Irritations (excerpt) | Bruce Andrews | language | **46.7%** | 44.8% | +0.74 | 15 |
| The Harbor Dawn (from The Bridge) | Hart Crane | modernist | **45.8%** | 48.8% | +0.97 | 48 |
| Lady Lazarus (opening) | Sylvia Plath | confessional | **45.5%** | 35.7% | -0.21 | 11 |
| Poetry (opening) | Marianne Moore | modernist | **45.5%** | 36.4% | -0.63 | 11 |
| A Route of Evanescence | Emily Dickinson | 19th_century | **45.5%** | 35.6% | -0.07 | 11 |
| Catalog of Unabashed Gratitude (excerpt) | Ross Gay | contemporary | **44.4%** | 21.6% | -0.96 | 18 |

## Bottom 10 Poems (lowest True Straussian)

| Poem | Author | Era | True Straussian | Avg S₂ |
|---|---|---|---|---|
| Some Trees | John Ashbery | new_york_school | **0.0%** | -1.21 |
| Won't You Celebrate With Me | Lucille Clifton | spoken_word | **0.0%** | -0.54 |
| silencio | Eugen Gomringer | concrete | **2.5%** | -0.77 |
| Ulysses (opening) | Alfred Lord Tennyson | victorian | **5.6%** | -0.55 |
| Buffalo Bill 's | E.E. Cummings | modernist | **6.2%** | -0.87 |
| I felt a Funeral, in my Brain | Emily Dickinson | 19th_century | **7.7%** | -0.89 |
| Villanelle of the Poet's Road | Ernest Dowson | fixed_form | **7.7%** | -1.21 |
| I Wandered Lonely as a Cloud | William Wordsworth | romantic | **8.3%** | -0.70 |
| Song: To Celia | Ben Jonson | early_modern | **8.3%** | -0.92 |
| Bonnie George Campbell | Traditional (Scottish ballad) | ballad | **10.0%** | -0.27 |

## Author Rankings by True Straussian Score

| Author | n | True Straussian | Uncertainty Exploit | TS Gap | Avg S₂ |
|---|---|---|---|---|---|
| Chiyo-ni | 1 | **66.7%** | 45.5% | +21.2% | +2.08 |
| Layli Long Soldier | 1 | **53.3%** | 45.2% | +8.1% | +0.16 |
| Edmund Spenser | 1 | **50.0%** | 42.6% | +7.4% | -0.26 |
| Allen Ginsberg | 2 | **46.7%** | 46.2% | +0.4% | +0.74 |
| Bruce Andrews | 1 | **46.7%** | 44.8% | +1.8% | +0.74 |
| Hart Crane | 1 | **45.8%** | 48.8% | -2.9% | +0.97 |
| Ross Gay | 1 | **44.4%** | 21.6% | +22.8% | -0.96 |
| John Berryman | 1 | **43.5%** | 50.0% | -6.5% | +0.42 |
| Anne Sexton | 2 | **40.3%** | 37.1% | +3.1% | -0.65 |
| Yosa Buson | 1 | **40.0%** | 46.7% | -6.7% | -0.14 |
| James Wright | 1 | **38.9%** | 42.9% | -4.0% | -0.35 |
| Thomas Hardy | 3 | **38.1%** | 47.3% | -9.2% | +0.25 |
| Georges Perec | 1 | **37.5%** | 29.4% | +8.1% | -0.44 |
| Philip Larkin | 1 | **37.5%** | 39.5% | -2.0% | -0.25 |
| Marianne Moore | 2 | **36.6%** | 36.2% | +0.4% | -0.30 |
| Frank O'Hara | 2 | **36.2%** | 37.4% | -1.2% | +0.00 |
| Kobayashi Issa | 3 | **36.1%** | 31.8% | +4.3% | -0.91 |
| Emily Dickinson | 4 | **35.8%** | 35.3% | +0.6% | -0.14 |
| H.D. (Hilda Doolittle) | 1 | **35.7%** | 42.3% | -6.6% | -0.14 |
| Austin Dobson | 1 | **35.7%** | 28.3% | +7.4% | -0.70 |
| Walter de la Mare | 1 | **35.3%** | 31.9% | +3.4% | -0.32 |
| W.S. Merwin | 1 | **34.8%** | 24.3% | +10.5% | -1.03 |
| Sappho | 1 | **34.5%** | 36.1% | -1.6% | -0.17 |
| Masaoka Shiki | 2 | **33.3%** | 43.5% | -10.1% | +0.27 |
| Sylvia Plath | 2 | **33.3%** | 34.3% | -1.0% | -0.39 |
| Claude McKay | 1 | **32.5%** | 45.6% | -13.1% | -0.20 |
| Matthew Arnold | 2 | **32.5%** | 39.7% | -7.2% | -0.43 |
| Seamus Heaney | 1 | **32.0%** | 47.1% | -15.1% | +0.17 |
| Robert Lowell | 1 | **32.0%** | 43.8% | -11.8% | -0.13 |
| Paul Laurence Dunbar | 1 | **31.8%** | 39.7% | -7.8% | -0.41 |

## Era Rankings by True Straussian Score

| Era | n | True Straussian | Uncertainty Exploit | TS Gap |
|---|---|---|---|---|
| beat | 2 | **46.7%** | 46.2% | +0.4% |
| confessional | 6 | **37.1%** | 39.4% | -2.3% |
| haiku | 10 | **34.8%** | 39.1% | -4.4% |
| language | 3 | **31.7%** | 36.6% | -4.9% |
| 19th_century | 10 | **31.3%** | 40.4% | -9.1% |
| early_modern | 4 | **30.4%** | 43.4% | -12.9% |
| contemporary | 9 | **30.0%** | 38.1% | -8.1% |
| new_york_school | 18 | **29.1%** | 36.2% | -7.0% |
| prose_poetry | 9 | **28.8%** | 35.7% | -6.9% |
| modernist | 21 | **27.8%** | 40.3% | -12.5% |
| imagist | 2 | **27.4%** | 37.8% | -10.4% |
| victorian | 21 | **25.9%** | 40.1% | -14.2% |
| metaphysical | 4 | **25.9%** | 39.5% | -13.6% |
| biblical | 7 | **25.1%** | 36.5% | -11.4% |
| fixed_form | 8 | **23.4%** | 35.9% | -12.5% |
| harlem_renaissance | 5 | **23.3%** | 39.7% | -16.4% |
| mid_century | 3 | **23.2%** | 39.8% | -16.5% |
| found_poetry | 7 | **22.2%** | 31.6% | -9.5% |
| romantic | 15 | **21.6%** | 39.8% | -18.3% |
| latin_american | 3 | **20.3%** | 36.4% | -16.1% |
| ballad | 6 | **17.9%** | 35.9% | -17.9% |
| concrete | 2 | **16.4%** | 32.5% | -16.1% |
| song_lyrics | 3 | **15.6%** | 33.1% | -17.4% |
| cliche_control | 3 | **15.0%** | 33.3% | -18.2% |
| spoken_word | 2 | **10.7%** | 37.3% | -26.6% |

## Key Findings

1. **Poetry median True Straussian score: 25.6%** vs prose baseline: 13.9%
   The gap (+11.7%) represents the 'confidence-adjusted' Straussian gap.

2. **Poetry median Uncertainty Exploitation: 38.5%** (deviating when model uncertain).
   True Straussian - Uncertainty Exploit gap: -12.8%
   Positive gap means poets preferentially defy *confident* predictions more than uncertain ones.

3. **Highest True Straussian authors:** Chiyo-ni (66.7%), Layli Long Soldier (53.3%), Edmund Spenser (50.0%)
   These poets most consistently deviate *when the model is sure* of what comes next.

4. **Largest TS Gap (precision > uncertainty deviation):** Ross Gay (+22.8%), Chiyo-ni (+21.2%), W.S. Merwin (+10.5%)
   These authors disproportionately defy confident predictions vs. uncertain contexts.

## Interpretation

The True Straussian Score refines the S₂ framework. Standard S₂ averages all deviation,
including 'cheap' deviation in high-entropy contexts where the model has no strong prior.
The True Straussian score isolates *precision deviation* — the poet's ability to say
something unexpected precisely when language has its strongest expectations.

This connects to a craft insight: great poetic surprise often works *against* the grain
of confident syntactic and semantic expectation, not merely in ambiguous contexts.
The TS score distinguishes poets who surprise us *despite* predictability
from those who operate in the more permissive space of lexical ambiguity.

## Next Steps

- Compute TS score for individual lines to find the most 'precisely Straussian' lines
- Test if TS score correlates with reader-rated memorability or critical esteem
- Compare TS score across poem types: are sonnets (highly regular) more 'precisely Straussian'?
- Examine what the model predicted at low-entropy Straussian moments (the 'suppressed' word)