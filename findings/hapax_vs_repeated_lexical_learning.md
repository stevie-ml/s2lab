# The Lexical Learning Curve: Hapax Legomena, Repetition, and S₂

**Date:** 2026-10-09  
**Experiments:** `experiments/hapax_vs_repeated_s2.py`, `experiments/second_occurrence_dip.py`  
**Corpus:** 201–219 English poems

---

## Research Question

When a poet repeats a word, does GPT-2 "learn" it — assigning it higher probability after first encountering it — and thus lower its S₂? And if so, do poets who rely on repetition as a structural device (anaphora, refrain) show a different S₂ signature than those who maximize lexical variety?

---

## The Core Finding: Hapax Legomena Have 2+ Bits Higher S₂

Across all English poems in the corpus:

| Token Type | N | Mean S₂ | Std | % Positive |
|---|---|---|---|---|
| **Hapax (used once per poem)** | 8,410 | **+1.742** | 5.131 | — |
| **Repeated (used 2+ times)** | 5,594 | **−0.321** | 5.684 | — |
| **Gap** | — | **+2.064 bits** | — | — |

**89% of poems** show this pattern: their hapax legomena have higher mean S₂ than their repeated words.

---

## The Lexical Learning Curve: S₂ by Occurrence Number

Tracking the same word by how many times it has appeared in the poem so far:

| Occurrence | N | Mean S₂ | Median S₂ | % Positive |
|---|---|---|---|---|
| **1st** | 12,377 | **+1.462** | +0.220 | **52.1%** |
| **2nd** | 2,489 | **−0.759** | −1.901 | 22.2% |
| **3rd** | 1,067 | **−0.865** | −2.148 | 19.0% |
| **4th** | 588 | **−0.601** | −2.056 | 15.8% |
| **5th** | 360 | **−1.442** | −2.327 | 12.8% |
| **6th** | 229 | **−1.460** | −2.571 | 13.1% |

The drop is steep and immediate: from 1st to 2nd occurrence, mean S₂ falls by **2.22 bits** and the positive-S₂ rate collapses from 52% to 22%.

### The Mechanism

GPT-2 reads left-to-right. When a word appears for the first time in a poem, the model has no poem-internal evidence to raise its probability. By the second occurrence, two things have happened:
1. The word is now part of the semantic field the poem has established
2. The token is primed by its own previous use (GPT-2's attention can revisit it)

The result: first occurrences are structurally surprising; repetitions are structurally expected.

---

## The Two-Occurrence Asymmetry: 64.9% Drop, 35.1% Rise

For words used exactly twice (1,422 pairs):

| | Rate | Mean delta |
|---|---|---|
| **S₂ drops on 2nd use** | **64.9%** | −4.59 |
| **S₂ rises on 2nd use** | 35.1% | +3.87 |

The drop cases are the "lexical learning" effect. The **rise cases** are the more theoretically interesting: they reveal the anaphoric reversal.

### Largest S₂ Drops (word "normalized" by 2nd use):

| Word | Poem | S₂ 1st | S₂ 2nd | Δ |
|---|---|---|---|---|
| `four` | The Lady of Shalott | +33.65 | −4.28 | −37.93 |
| `so` | This Is Just to Say | +25.39 | −4.86 | −30.25 |
| `when` | Nursery Rhymes | +26.92 | −1.32 | −28.23 |
| `through` | The Fish | +26.72 | −1.00 | −27.72 |

### Largest S₂ Rises (word GAINS surprise on repetition):

| Word | Poem | S₂ 1st | S₂ 2nd | Δ |
|---|---|---|---|---|
| `he` | Digging (Heaney) | −4.96 | +26.05 | **+31.01** |
| `she` | Tonight I Can Write (Neruda) | −2.28 | +26.90 | **+29.18** |
| `between` | I heard a Fly buzz (Dickinson) | +3.68 | +32.71 | **+29.03** |
| `into` | Three Haiku (Basho, trans.) | −0.70 | +25.18 | +25.89 |
| `and` | Fog (Sandburg) | −3.17 | +22.12 | +25.29 |
| `could` | The Tyger (Blake) | −0.67 | +23.63 | +24.30 |

---

## The Anaphoric Reversal: When Repetition IS the Surprise

The rise-on-repetition cases are almost always structural repetitions — anaphora, catalog, refrain — where the repeated word appears in a position that GPT-2 could not predict from context:

### Case 1: Langston Hughes, "Harlem" / "A Dream Deferred"

Trajectory of `does` across the poem:
```
S₂ = +1.1 → +31.1 → −1.8
```
The first `does` (in "Does it dry up") appears in a position where the model might expect a continuation; S₂ = +1.1. The second `does` (beginning a new stanza after a line break) is MASSIVELY surprising (S₂ = +31.1) because after the question's resolution the model does not expect another question opener. The anaphoric structure deifies the repeated word.

### Case 2: Lyn Hejinian-style catalog (delusions list)

Trajectory of `being` across a catalog poem:
```
S₂ = +3.7 → +34.6 → +31.1 → +29.9 → +32.5 → +29.2
```
Every occurrence after the first has S₂ > 29. The catalog form creates a context where `being` is structurally demanded but contextually never predicted — the preceding phrase (`buried alive`, `being followed`, `laughed at`) provides no evidence for the next `being`. Each new occurrence exploits the gap between structural expectation (we know the list continues) and local unpredictability (what follows `being` is always novel).

### Case 3: Seamus Heaney, "Digging"

`my` trajectory: `−2.7 → −4.6 → −2.2 → +28.9`

The sudden S₂ spike on the 4th use of `my` (in `my grandfather` after two uses of `my` as a possessive in conversational register) marks the structural pivot of the poem — the shift from present to past, from the speaker's physical labor to the grandfather's turf-cutting. The repetition sets up the pivot.

---

## Era-Level Analysis: Who Relies on Hapax vs. Repetition?

| Era | Hapax Gap | Interpretation |
|---|---|---|
| **Beat** (Ginsberg, Corso) | **+4.75** | Maximum lexical variety; catalogic accumulation; each word appears once |
| **Korean Modernist** | **+4.51** | Compressed, precise diction; minimal repetition |
| **Deep Image** | **+4.31** | Single-use concrete nouns; imagistic precision |
| **Imagist** | **+2.98** | Pound's "no word that does not contribute" — no filler repetition |
| **Harlem Renaissance** | **−0.30** | REVERSED: structural anaphora IS the technique (Hughes) |
| **Black Arts** | **−0.08** | Near zero: spoken-word, repetition-heavy tradition |
| **Song Lyrics** | **+1.46** | Small gap: chorus/refrain structure normalizes repetition |

The **Beat poets** maximize the hapax gap: Ginsberg's catalogic style generates enormous lexical diversity where each noun, each face, each street appears exactly once. The **Harlem Renaissance** poets *invert* the pattern because Hughes's technique — anaphoric questions ("Does it dry up / like a raisin in the sun? / Does it stink...") — weaponizes repetition as structural surprise.

---

## Poems with Largest Hapax Gap:

| Poem | Hapax S₂ | Rep S₂ | Δ |
|---|---|---|---|
| Howl (opening) | +3.36 | −4.16 | **+7.52** |
| A Route of Evanescence (Dickinson) | +3.27 | −3.94 | **+7.21** |
| The Convergence of the Twain (Hardy) | +4.91 | −1.08 | **+5.99** |
| Three Haiku (Issa, trans.) | +6.89 | +0.93 | **+5.95** |
| Sunday Morning (Stevens) | +1.47 | −4.16 | **+5.63** |

Ginsberg, Dickinson, Hardy, and Stevens: poets of maximum lexical daring, who approach each noun as unrepeatable.

---

## Theoretical Implication: Two Kinds of Poetic Vocabulary

The hapax/repeated split reveals two distinct poetic strategies:

**Strategy A: Lexical uniqueness** (most poetry, 89% of corpus)  
Each choice is singular — "exact words in exact order" (Pound). S₂ lives in hapax tokens. The poem advances by introduction, never by return. This is the default information structure of poetry.

**Strategy B: Structural repetition** (anaphora, refrain, catalog)  
S₂ lives in repeated tokens placed in structurally novel positions. The poem advances by return to the same word in a changed context. The Harlem Renaissance, much of the ballad tradition, and the oulipo rely on this.

**The Straussian gap thus has two anatomies:**  
- In hapax-dominated poems: surprisal comes from *what has not yet been said*  
- In repetition-dominated poems: surprisal comes from *the return of what has been said, in a structurally impossible position*

---

## Suggested Next Steps

1. Develop an "anaphoric S₂ index" — specifically measure S₂ elevation for structurally repeated words — to distinguish poets who use repetition as suppression vs. as device.
2. Test whether the S₂ rise on 2nd occurrence correlates with positional surprise (the word appears in a new syntactic slot) vs. semantic surprise (the word is paired with new content).
3. The 2nd-to-3rd occurrence trajectory in ballads shows interesting persistence: `lord` in "Recessional" goes `+25.9 → −2.5 → +30.4` — alternating surprise and normalization. Model this as a sawtooth oscillation between habituation and structural recurrence.
4. Investigate whether the hapax gap varies by poem length — do longer poems show stronger differentiation (the model has more time to "learn" repeated words)?
