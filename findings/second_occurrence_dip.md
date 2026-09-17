# The Second-Occurrence Dip: Lexical Habituation vs. Structural Surprise in Poetry

**Date:** 2026-09-17  
**Experiment:** `experiments/second_occurrence_dip.py`  
**Corpus:** 120 English poems from `results/corpus_results.json`  
**Builds on:** `hapax_legomena_s2.md`, `repetition_and_entropy.md`, `enjambment_two_strategies.md`

---

## Research Question

When a word appears for the second time in a poem, does its S₂ drop? GPT-2 reads left-to-right, so by the time a word recurs, the model has already "seen" it in this context. If GPT-2 now assigns it higher probability, S₂ will fall — a measurable **lexical habituation effect**. Conversely, if the word appears in a structurally surprising position (line opening, after a break), structural surprise might *overcome* habituation, producing an S₂ *rise* on the second occurrence.

This tests whether poets "educate" their own model as the poem proceeds — and whether anaphora works partly by exploiting, partly by defeating, this habituation.

---

## Method

1. For each token in each English poem, track its occurrence number (1st, 2nd, 3rd…)
2. Aggregate S₂ by occurrence position
3. For words appearing exactly twice, compute Δ = S₂₂ − S₂₁
4. Identify words where S₂ *rises* on second occurrence (structural override of habituation)
5. Trace multi-occurrence trajectories for anaphoric words (3+ uses)
6. Compare across eras

---

## Key Results

### 1. The Overall Dip is Massive

| Occurrence | n | mean S₂ | median S₂ | % positive |
|---|---|---|---|---|
| **1st** | 6,250 | **+1.37** | +0.17 | **51.7%** |
| **2nd** | 1,253 | **−0.94** | −1.93 | **21.4%** |
| **3rd** | 520 | **−1.14** | −2.24 | **16.9%** |
| **4th** | 276 | **−0.22** | −1.96 | **15.6%** |
| **5th** | 155 | **−1.61** | −2.51 | **11.0%** |
| **6th** | 94 | **−1.34** | −2.94 | **11.7%** |

**First occurrences average +1.37 S₂; second occurrences average −0.94.** That is a swing of **2.31 S₂ units** between a word's debut and its repeat. After the second occurrence, S₂ stabilizes in negative territory (the poem has "trained" GPT-2 to expect this word).

Positive-S₂ rate collapses from 51.7% (first occurrence) to 21.4% (second). By the sixth occurrence, only 11.7% of tokens are positively surprising.

---

### 2. Two-Occurrence Words: Direction of Change

Among 733 word pairs that appear exactly twice in a poem:

| Direction | N | % | Mean change |
|---|---|---|---|
| S₂ DROPS (2nd < 1st) | 461 | **62.9%** | −4.58 |
| S₂ RISES (2nd > 1st) | 272 | **37.1%** | +3.91 |
| Mean Δ overall | 733 | — | **−1.43** |

The dip is real and directional: nearly two-thirds of repeated words become less surprising on the second use. The mean drop (−4.58) is substantially larger than the mean rise (+3.91), confirming that **lexical habituation is the dominant force**.

However, 37% of repeated words *become more surprising* on second use — these are the cases where **structural position defeats habituation**.

---

### 3. Largest S₂ Drops (Habituation Wins)

These words had extremely high S₂ on first use (likely at a structurally surprising position, e.g., after a line break), then became predictable:

| Word | Poem | S₂ 1st | S₂ 2nd | Δ |
|---|---|---|---|---|
| 'so' | This Is Just to Say (Williams) | +25.4 | −4.9 | **−30.3** |
| 'when' | Nursery Rhymes (compilation) | +26.9 | −1.3 | **−28.2** |
| 'when' | Barbara Allen (ballad) | +25.3 | −2.1 | **−27.4** |
| 'and' | What Is Poetry (Ashbery) | +23.6 | −2.1 | **−25.7** |
| 'red' | Sir Patrick Spens (ballad) | +18.0 | −5.8 | **−23.8** |

**Pattern**: The biggest drops cluster in ballads and short poems. A word that first appears at a line-breaking position (high S₂) subsequently occupies a metrically expected slot — the structural context explains both the peak and the trough.

---

### 4. Largest S₂ Rises (Structural Surprise Beats Habituation)

These words were *less* surprising on first use but became dramatically more surprising on the second:

| Word | Poem | S₂ 1st | S₂ 2nd | Δ |
|---|---|---|---|---|
| 'he' | Digging (Heaney) | −5.0 | +26.1 | **+31.0** |
| 'between' | I heard a Fly buzz (Dickinson) | +3.7 | +32.7 | **+29.0** |
| 'and' | The Tyger (Blake) | −2.7 | +24.8 | **+27.4** |
| 'into' | Three Haiku (Basho) | −0.7 | +25.2 | **+25.9** |
| 'my' | I felt a Funeral (Dickinson) | −2.7 | +22.7 | **+25.4** |

**Pattern**: These are cases where the second occurrence is at a structurally critical position — a line break, a clause boundary — that GPT-2 strongly expects to be a newline. The structural surprise overrides lexical habituation. Heaney's "he" in "Digging" appears first in a syntactically expected position (subject pronoun) then recurs after a line break where GPT-2 predicted a line end.

---

### 5. Multi-Occurrence Trajectories: Anaphora in Action

For words appearing 3+ times, the trajectory after the second occurrence is relatively flat (−1.1 to −1.6). The big news is the first-to-second drop; subsequent occurrences neither recover much nor fall further:

| Occurrence | n | mean S₂ |
|---|---|---|
| 1st | 520 | **+0.20** |
| 2nd | 520 | **−1.29** |
| 3rd | 520 | **−1.14** |
| 4th | 276 | **−0.22** |
| 5th | 155 | **−1.61** |

The most striking anaphoric trajectories:

| Word | Poem | S₂ by Occurrence |
|---|---|---|
| 'being' | a list of the delusions... (O'Hara) | 3.7 → **34.6** → 31.1 → 29.9 → 32.5 → 29.2 |
| 'does' | Harlem (Hughes) | 1.1 → **31.1** → −1.8 |
| 'like' | Harlem (Hughes) | 27.7 → −2.2 → −1.9 → **23.6** → 5.6 |
| 'where' | Lord Randal (ballad) | 4.2 → −5.2 → −1.6 → **29.5** |
| 'or' | Harlem (Hughes) | **28.0** → 26.0 → −3.5 |

**Frank O'Hara's "being"** is the most extreme case: the second occurrence is *higher* S₂ than the first (+34.6 vs. +3.7). This is anaphora working at maximum force — a list poem where each "being" appears after a line break, and GPT-2 learns the pattern just slowly enough to keep being surprised. The sustained high S₂ across six occurrences (average ~30) suggests GPT-2 never fully habituates to this structural use.

**Hughes's "does"** shows the opposite collapse: the anaphoric "Does it dry up?" is maximally surprising on the second use (+31.1) but the poem ends before a third anaphoric "does" would have solidified the pattern.

---

### 6. Era-Level Comparison

How much do eras differ in the magnitude of the first-to-second drop?

| Era | avg S₂ (1st) | avg S₂ (2nd) | Δ |
|---|---|---|---|
| beat | +2.41 | −1.85 | **−4.26** |
| haiku | +4.49 | +0.32 | **−4.17** |
| modernist | +1.77 | −1.46 | **−3.23** |
| mid_century | +1.76 | −1.36 | **−3.12** |
| ballad | +2.52 | −0.43 | **−2.95** |
| romantic | +1.36 | −0.45 | **−1.81** |
| harlem_renaissance | +1.16 | −0.63 | **−1.79** |
| prose_poetry | +0.64 | −1.19 | **−1.83** |
| confessional | +1.82 | +1.05 | **−0.78** |

**Haiku** and **beat** poetry show the largest habituation drops — their first occurrences are highly surprising, and repetition drains that energy dramatically. **Confessional** poetry (Plath, Sexton) shows the *smallest* drop (−0.77): repeated words in confessional poems remain near their first-occurrence S₂, suggesting that confessional anaphora maintains surprise through structural positioning. **Prose poetry** shows a muted first occurrence (+0.64) and large drop, consistent with its more conventional syntax.

---

## Key Findings

1. **The second-occurrence dip is real and large**: S₂ falls from +1.37 to −0.94 between first and second use, a swing of 2.31 units. Positive-S₂ rate collapses from 52% to 21%.

2. **Lexical habituation is the dominant force (63%)**, but structural position can override it (37%). When a word recurs at a line-breaking position, structural surprise exceeds the "I've seen this" discount.

3. **Anaphora's information dynamics split into two types**:
   - *True anaphora* (structural position maintained): S₂ stays high across repetitions (O'Hara's "being", Hughes's "does") — the poet wins the structural lottery each time
   - *Lexical repetition* (not at structural positions): S₂ collapses after first use and stays negative

4. **Era signature**: Haiku and Beat poetry have the largest first-occurrence premiums *and* the largest habituation drops — their surprise is intense but fragile. Confessional poetry is most resistant to habituation, suggesting a poetics of sustained anaphoric pressure.

5. **The fundamental asymmetry**: Mean drop when S₂ falls (−4.58) is larger in magnitude than mean rise when S₂ rises (+3.91). You can lose more than you gain — the poet's "spent" surprise is harder to recover than new structural surprise is to create.

---

## The Mechanism

These results reveal a two-factor model of word-level S₂:

**S₂(word, occurrence_n) ≈ S₂_structural(position) + S₂_lexical(word) − habituation(n)**

- `S₂_structural`: the bonus from structural position (line-start, after break)
- `S₂_lexical`: the base surprisal of the word itself
- `habituation(n)`: a penalty that grows with occurrence number (≈ −2.3 for n=2, stabilizing thereafter)

When `S₂_structural` is large enough, it can overcome `habituation(n)`. This is how anaphora works: the structural position penalty is paid (the line break), and the repeated word gets the structural bonus.

---

## Suggested Next Steps

1. **Separate the structural and lexical components**: For words that appear at line-start positions on *both* occurrences, does the habituation effect disappear? Testing this directly would separate the two mechanisms.
2. **Confessional vs. Language poetry**: Both use repetition differently — run this experiment on Plath vs. Ashbery specifically to see if the anaphoric signature differs.
3. **The decay curve**: Fit a decay function to S₂ vs. occurrence number. Does S₂ decay exponentially? Is the half-life 1 occurrence or 2?
4. **Word length and frequency**: Do high-frequency words (function words) show faster habituation than low-frequency content words?
5. **Compare to prose**: Does the same habituation effect operate in Hemingway's repetitive style? If S₂ in prose doesn't show the structural override on second occurrence, that would confirm that the structural mechanism is distinctly poetic.
