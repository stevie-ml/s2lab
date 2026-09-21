# The Stanza-Break Artifact: A Confound That Inflates Most of This Lab's S₂ Results

**Date:** 2026-09-21
**Experiments:** `experiments/spectral_refrain.py`, `experiments/stanza_break_artifact.py`, `experiments/artifact_corpus_impact.py`
**Corpus:** 168 texts (8 new fixed-form poems added this run), 17,548 tokens
**Status:** ⚠️ Methodological finding. Invalidates or substantially revises several prior findings in `findings/`.

---

## Summary

**31.5% of line-head tokens, and 4.5% of all tokens, sit at positions where GPT-2 assigned ≥90% probability to a newline continuation.** At those positions entropy collapses to ~0.03 bits, so S₂ = surprisal − entropy reduces to S₂ ≈ surprisal, and *any* non-newline token scores ~20 bits regardless of what the poet wrote.

These positions are not measuring poetic choice. They are measuring the model's confidence in the poem's **line-and-stanza layout**.

Removing them:

| Claim as reported | Artifact-free |
|---|---|
| Line-head (post-newline) S₂ = **+6.30** | **−0.10** |
| "haiku has the highest avg S₂" (rank 1) | haiku drops to **rank 12** |
| Poetry avg S₂ = **+0.213** (positive) | **−0.388** (negative) |
| Poetry−prose gap = **+1.849 bits** | **+1.333 bits** (72% survives) |
| Top poem: *The Red Wheelbarrow*, S₂ = **3.59** | **−0.14** |

The project's **central claim survives** — poetry is still measurably less conformist than prose (72% of the gap remains, and it is not artifact-driven). But the absolute framing ("poetry operates in positive S₂ territory") is wrong, and **every era ranking, poem ranking, and line-position result in this lab is contaminated to a degree that varies systematically by poem layout.**

---

## How this was found

The run began as a test of an unrelated hypothesis: do villanelles, ballades and rondeaus — forms built on a *mandatory refrain at a fixed interval* — produce a periodic signal in the S₂ series detectable by Fourier analysis? (`spectral_refrain.py`, 8 new public-domain fixed-form poems added to the corpus.)

The spectral answer was a clean null: fixed-form poems are spectrally indistinguishable from free verse (flatness 0.542 vs 0.567 corpus mean), and no poem's dominant period matched its refrain interval — the ratio was 0.04–0.16 in every case.

But the mechanism sub-test looked spectacular. The head token of a repeated line appeared to gain **+15.7 bits of S₂** on its second occurrence:

| fixed-form refrain head | n | surprisal | entropy | S₂ |
|---|---|---|---|---|
| occurrence #1 | 7 | 12.07 | 5.224 | 6.85 |
| occurrence #2 | 7 | 22.60 | **0.009** | **22.59** |

An entropy of 0.009 bits is the model being 99.9% certain. That is not a plausible reading of a poem. Inspecting Wilde's villanelle token by token showed why:

```
tok  6  'In'     S2=12.01  entropy=0.150  model expected '\n' p=0.991
tok 31  'Where'  S2=15.75  entropy=0.087  model expected '\n' p=0.995
```

**Neither line is a refrain.** `In the dim meadows desolate` and `Where Amaryllis lies in state` are ordinary lines. The spike had nothing to do with repetition.

---

## Mechanism

Poems are stored with blank lines between stanzas (`\n\n`), which GPT-2 emits as two consecutive `\n` tokens. Once the model has seen two or three stanzas it learns the poem's stanza period and becomes near-certain that the token following a line-ending `\n` is a **second `\n`** — the blank line.

At every line head that is *not* a stanza break, the poem instead continues with a word. Surprisal is then enormous and entropy is ~0, so:

$$S_2 = \text{surprisal} - \text{entropy} \approx \text{surprisal} \approx 20\text{ bits}$$

All 792 artifact tokens in the corpus have `'\n'` as the model's top prediction. 63% are at line heads; the remaining 37% are mid-line positions where the model expected the line to end and the poet continued (the class this lab previously labelled `PUNCTUATION_SKIP` in `straussian_gap_taxonomy.md`).

**Why it specifically confounds repetition studies:** a refrain's 2nd occurrence is necessarily *later* in the poem than its 1st, by which point the stanza rhythm is better learned and p(`\n`) is higher. The apparent "surprise grows on repetition" effect was entirely an effect of position. Artifact-free, repeated-line heads go the other way (occurrence #1 = −0.82, #2 = −2.36, n=6).

---

## Non-circularity check

The exclusion rule reads only the model's predictive distribution — probability mass on a newline continuation — and never looks at S₂ or at which token the poet wrote. It does select high-S₂ tokens, and that is precisely the argument: at these positions the S₂ value is fixed by the *position*, not the *choice*.

| | n | mean S₂ | sd | mean entropy |
|---|---|---|---|---|
| artifact (p_nl ≥ 0.9) | 792 | 12.811 | 10.989 | **0.278** |
| clean | 16,756 | −0.401 | 3.636 | 6.283 |

Within the artifact set, S₂ is determined almost entirely by the chosen token's own probability, with very little spread — i.e. the poet's lexical decision contributes nothing beyond "was not a newline":

| p(chosen token) | n | mean S₂ | sd |
|---|---|---|---|
| < 1e−6 | 230 | 25.53 | 3.56 |
| 1e−6 – 1e−5 | 125 | 18.76 | **1.33** |
| 1e−5 – 1e−4 | 97 | 14.94 | **1.07** |
| ≥ 1e−4 | 340 | 1.42 | 4.24 |

A standard deviation of ~1.1 bits around a mean of 15–19 means these numbers are structural, not interpretive.

---

## Line-head S₂ is entirely artifact

`line_position_analysis.md` and the standing report both state: *"Avg S₂ at tokens immediately after newline: 5.65 … enjambment is a key site of Straussian deviation."*

| p(newline) at line head | n | surprisal | entropy | S₂ |
|---|---|---|---|---|
| 0.00–0.10 | 954 | 6.39 | 6.93 | **−0.54** |
| 0.10–0.30 | 42 | 6.01 | 6.10 | −0.08 |
| 0.30–0.60 | 28 | 8.55 | 4.84 | 3.71 |
| 0.60–0.90 | 49 | 8.56 | 2.32 | 6.24 |
| 0.90–0.99 | 52 | 12.45 | 0.54 | 11.92 |
| 0.99–1.00 | 442 | 21.20 | 0.03 | **21.18** |

Overall line-head S₂ = **+6.30**. Artifact-free = **−0.10**. The inflation is **+6.40 bits — 102% of the reported value.** Line heads are, if anything, marginally *below* baseline once the layout effect is removed.

**The enjambment finding does not survive.** Whether a line head spikes depends on whether the model had committed to a stanza break there, not on the poet's word choice.

### Confirmation: the effect requires a learnable stanza pattern

| | n line heads | mean p(newline) | line-head S₂ | % contaminated |
|---|---|---|---|---|
| poems **with** blank-line stanza breaks | 824 | 0.526 | **10.06** | 47.8% |
| poems **without** blank lines | 743 | 0.162 | 2.13 | 13.5% |

### Internal control: the German corpus

German-language poems are analysed with `dbmdz/german-gpt2`, which tokenises newlines differently. They show **0.0% contamination** and are the only poems whose S₂ is unchanged by cleaning (german_symbolist Δ = −0.008, german_expressionist Δ = −0.020). They consequently rise to the top of the artifact-free rankings — not because they became better, but because they were never inflated.

---

## Corpus-wide damage

### Era rankings scramble

| Era | n | S₂ raw | S₂ clean | Δ | % tokens artifact | rank raw → clean |
|---|---|---|---|---|---|---|
| haiku | 8 | 1.645 | **−0.323** | −1.968 | 10.0% | 1 → **12 (−11)** |
| german_modernist | 2 | 0.955 | 0.626 | −0.329 | 2.5% | 2 → 2 |
| beat | 2 | 0.923 | **0.685** | −0.238 | 1.3% | 3 → **1 (+2)** |
| ballad | 6 | 0.732 | −0.421 | −1.153 | 10.1% | 4 → **15 (−11)** |
| fixed_form | 8 | 0.584 | −0.560 | −1.144 | 7.9% | 5 → **19 (−14)** |
| german_expressionist | 2 | 0.582 | 0.562 | −0.020 | 3.7% | 6 → 3 (+3) |
| confessional | 6 | 0.568 | −0.234 | −0.803 | 3.4% | 7 → 10 (−3) |
| german_symbolist | 3 | 0.460 | 0.452 | −0.008 | 2.7% | 8 → 4 (+4) |
| victorian | 14 | 0.317 | −0.204 | −0.521 | 4.2% | 10 → 8 (+2) |
| modernist | 18 | 0.158 | −0.545 | −0.703 | 4.5% | 17 → 18 (−1) |
| romantic | 12 | 0.142 | −0.495 | −0.637 | 5.3% | 18 → 17 (+1) |
| nursery_rhyme | 1 | 0.104 | −0.818 | −0.923 | 8.6% | 19 → 28 (−9) |
| new_york_school | 18 | −0.149 | −0.569 | −0.420 | 2.1% | 24 → 20 (+4) |
| control (prose) | 5 | −1.636 | −1.721 | −0.084 | 0.6% | 29 → 29 |

**The contamination rate tracks poem layout, not poetics.** Haiku (10.0%), ballads (10.1%), fixed forms (7.9%) and nursery rhymes (8.6%) are short-lined, heavily stanza'd, and therefore maximally exposed. Prose control is 0.6%. The era table has been ranking *typographic regularity*.

The headline sentence in every generated report — *"All poetry eras have positive or near-zero avg S₂"* — is false once cleaned. Most poetry eras are **negative**.

### Poem rankings collapse

| Reported | raw S₂ | clean S₂ | % artifact |
|---|---|---|---|
| Williams, *The Red Wheelbarrow* | 3.59 | **−0.14** | 23% |
| Williams, *This Is Just to Say* | 2.61 | **−1.37** | 19% |
| Brooks, *We Real Cool* | 2.18 | **−0.66** | 13% |
| Bashō, *Three Haiku* | 2.14 | **−0.31** | 14% |
| Issa, *Three Haiku* | 2.02 | **−0.85** | 13% |

These are exactly the shortest, most line-broken poems in the corpus. *The Red Wheelbarrow* — the lab's flagship example — is 23% artifact tokens.

Artifact-free top poems are instead Rilke (1.25), Bashō's *Old Pond* (1.18), Ginsberg's *Howl* (0.95), Trakl (0.83), Whitman (0.77).

### What survives

| | raw | clean |
|---|---|---|
| poetry avg S₂ | +0.213 | **−0.388** |
| prose avg S₂ | −1.636 | −1.721 |
| **gap** | **+1.849** | **+1.333** |

**72% of the poetry–prose gap survives.** Poetry really is less statistically conformist than prose, and that result is not an artifact — prose control is only 0.6% contaminated, so the comparison was never driven by it. The positive-vs-negative framing was.

---

## Prior findings requiring revision

| Finding | Status |
|---|---|
| `line_position_analysis.md` — post-newline S₂ = 5.65 | ❌ **Fails.** Artifact-free = −0.10 |
| `enjambment_vs_s2.md`, `enjambment_two_strategies.md` | ❌ Line-head effects need full re-run |
| `stanza_boundary_effects.md` | ❌ Measures the artifact directly |
| Era comparison (all reports) | ⚠️ Rankings invalid; haiku/ballad/fixed_form most affected |
| Top/bottom poem rankings (all reports) | ⚠️ Invalid; biased toward short-lined poems |
| `straussian_gap_taxonomy.md` — `PUNCTUATION_SKIP` class (10.6%, mean S₂ 6.47) | ⚠️ Is this artifact by another name |
| `s2_spikiness_and_ballads.md` — ballads "high spikes" | ⚠️ Ballads are 10.1% artifact, highest in corpus |
| `second_occurrence_dip.md` | ⚠️ Check whether position confounds occurrence |
| Poetry−prose gap (core claim) | ✅ **Survives** at 72% |
| German-corpus results | ✅ **Unaffected** (0% contamination) |

---

## Recommended fix

1. **Add `p_newline` to the engine's per-token output** so every downstream experiment can filter without recomputing from the top-10 alternatives (which only gives a lower bound).
2. **Report S₂ twice** — raw and artifact-free — in `researcher.py`'s standard tables, rather than silently choosing one.
3. **Treat `p(newline) ≥ 0.9` positions as a separate category**, not as poetic deviation. They are real model behaviour and interesting in their own right (the model learns layout fast), but they are a *typographic* signal.
4. **Consider a layout-neutral preprocessing mode**: analyse poems with line breaks normalised to a single separator token, so stanza structure cannot be learned and the lexical signal is isolated.

---

## Next steps

- Re-run the affected experiments above with filtering and republish corrected numbers.
- Test fix (4): if collapsing `\n\n` → `\n` removes the effect entirely, that confirms the diagnosis and gives a clean analysis mode.
- The **spectral null result is itself worth keeping**: structural repetition produces *impulses*, not oscillations, and an impulse has a flat spectrum. But re-run it artifact-free before drawing conclusions — the impulses examined here were artifact impulses.
- Open question now genuinely open: with layout effects removed, is there *any* measurable information signature of poetic form? The cleaned era spread (+0.69 to −1.72) is much narrower than the raw spread and may be mostly noise at current corpus sizes.

---

## Corpus additions this run

8 public-domain fixed-form poems with mandatory refrains, added to test the spectral hypothesis: Wilde *Theocritus* (villanelle), Robinson *The House on the Hill* (villanelle), Dowson *Villanelle of the Poet's Road*, Henley *Villanelle*, Rossetti *The Ballad of Dead Ladies* (ballade), Dobson *In After Days* (rondeau), Poe *Annabel Lee*, Kipling *Sestina of the Tramp-Royal*. Corpus: 160 → 168 texts.
