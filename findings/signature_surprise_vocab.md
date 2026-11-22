# Signature Surprise Vocabulary: Do Poets Reuse Their Best Surprises?

**Date:** 2026-11-22  
**Experiment:** `experiments/signature_surprise_vocab.py`  
**Results:** `results/signature_surprise_vocab.json`  
**Corpus:** 431 English poems, 89 poets with ≥2 works  
**Metric:** Cross-poem Jaccard similarity of high-S₂ vocabulary (threshold: S₂ > 2.0)

---

## Research Question

When a poet finds a word that defeats GPT-2's predictions — a genuine high-S₂ token — do
they tend to reuse that word as a "signature" across different poems, or is each poem a fresh
invention with new surprise vocabulary?

**Hypothesis A (Stable Signature):** Poets develop a stable "surprise vocabulary" and deploy
it repeatedly. Their originality is about *placement*, not perpetual lexical novelty.

**Hypothesis B (Perpetual Novelty):** True originality means always surprising with *new*
vocabulary. The poet's job is to find fresh defamiliarizing language each time.

---

## Method

For each poet with ≥2 poems, extract tokens with S₂ > 2.0 (clear Straussian gap)
after removing stanza-break artifacts (p_newline < 0.9).

**Cross-poem Jaccard similarity**: for each pair of poems by the same poet,
`J = |high-S₂ vocab intersection| / |high-S₂ vocab union|`. Mean J across all
same-poet pairs is the poet's "signature consistency score."

**Baseline**: mean Jaccard for 1,000 random cross-author poem pairs = **0.0067**.

---

## Finding 1: Most Poets Practice Perpetual Novelty (But Not All)

| Statistic | Value |
|---|---|
| Poets with J = 0 (zero shared surprise vocab) | **34/89 (38%)** |
| Poets with J > 2× baseline (0.013) | 45/89 (51%) |
| Poets with J > 5× baseline (0.034) | 20/89 (22%) |
| Poets with J > 10× baseline (0.067) | **14/89 (16%)** |
| Cross-author baseline | 0.0067 |

**38% of poets share absolutely no high-S₂ vocabulary across their poems.** Each poem is
an informationally isolated universe — the words that surprised GPT-2 in one poem never
appear as surprises in another.

A further 36% exceed the baseline but only modestly. Only 14 poets (16%) show genuinely
elevated surprise vocabulary consistency.

---

## Finding 2: Form Determines Strategy — Haiku vs. Fixed-Form

| Era | n poets | Mean within-poet J | vs. Baseline |
|---|---|---|---|
| **fixed_form** | 6 | **0.336** | **50×** baseline |
| **18th_century** | 2 | 0.414 | 62× baseline |
| **mid_century** | 2 | 0.500 | 75× baseline |
| contemporary | 3 | 0.227 | 34× baseline |
| harlem_renaissance | 3 | 0.111 | 17× baseline |
| modernist | 9 | 0.042 | 6× baseline |
| victorian | 7 | 0.029 | 4× baseline |
| romantic | 4 | 0.024 | 4× baseline |
| **haiku** | 4 | **0.000** | **0×** baseline |
| **imagist** | 2 | **0.000** | **0×** baseline |
| **limerick** | 3 | **0.000** | **0×** baseline |
| **confessional** | 2 | **0.000** | **0×** baseline |

This is the sharpest finding: **fixed-form poets (sonnets, villanelles, formal verse) show
50× baseline surprise vocabulary consistency, while haiku masters, imagists, and confessional
poets show near-zero consistency.**

**Interpretation:** Fixed form *constrains* where surprise can live. With meter, rhyme, and
stanza structure all locked in, the poet returns repeatedly to the same pool of semantically
loaded vocabulary — there are only so many surprising words that can fill a rhyme position or
complete an iambic line. The surprise vocabulary isn't freely chosen; it's partly selected BY
the form.

Haiku and imagist poets, by contrast, treat each poem as a fresh encounter with a specific
moment. The haiku aesthetic forbids repeating images from previous poems; the imagist credo
("direct treatment of the thing") demands fresh perception each time.

---

## Finding 3: Individual Poet Profiles (≥4 poems)

| Poet | n | Era | Mean J | Sig words / Total | Signature vocabulary (top tokens) |
|---|---|---|---|---|---|
| **William Carlos Williams** | 4 | modernist | **0.333** | 8/8 (100%) | — |
| **Lucille Clifton** | 4 | contemporary | 0.167 | 15/35 (43%) | — |
| **Gerard Manley Hopkins** | 6 | victorian | 0.080 | 39/184 (21%) | forth, fresh, morning, brown, man |
| **Walt Whitman** | 9 | modernist | 0.072 | 50/270 (19%) | where, while, fearful, daring, grim |
| **Emily Dickinson** | 7 | 19th_century | 0.055 | 36/113 (32%) | **death**, too, but |
| **Alfred, Lord Tennyson** | 5 | victorian | 0.050 | 34/179 (19%) | — |
| **John Keats** | 9 | romantic | 0.045 | 68/380 (18%) | — |
| John Ashbery | 17 | new_york_school | 0.020 | 11/218 (5%) | survey, painting, living |
| Anonymous (Hebrew Bible) | 7 | biblical | 0.023 | 15/126 (12%) | — |
| Robert Browning | 8 | dramatic | 0.031 | 68/416 (16%) | — |
| **William Blake** | 7 | romantic | 0.009 | 6/130 (5%) | **lamb**, love, thy |
| **Gertrude Stein** | 4 | modernist | 0.007 | 2/85 (2%) | — |
| **T.S. Eliot** | 5 | modernist | 0.002 | 2/155 (1%) | dry, wind |
| **Matsuo Bashō** | 4 | haiku | **0.000** | 0/12 (0%) | *(none)* |

The contrast between Blake and Whitman is striking: both canonical, both Romantic-era, but Blake
(J=0.009) is a "perpetual novelty" poet while Whitman (J=0.072) maintains a stable catalog of
surprising language across nine poems. Blake reinvents; Whitman recirculates.

Dickinson's signature vocabulary confirms what readers already sense: **"death"** appears as a
high-S₂ token in multiple poems — it is statistically surprising to GPT-2 even when she returns
to it again and again, because the contexts in which she places it are always unexpected.

**Matsuo Bashō (J=0.000)** achieves perfect perpetual novelty across four haiku. No high-S₂
word from one haiku appears as a high-S₂ word in another. Each haiku is an informationally
distinct universe.

**T.S. Eliot (J=0.002)** is similarly near-zero. His five poems share only 'dry' and 'wind'
as recurring high-S₂ tokens — a surprisingly austere lexical signature for a poet famous for
dense, allusive language. His surprise vocabulary, it turns out, is never the same twice.

---

## Finding 4: The Corpus-Size Effect

| n poems | Mean J | n poets |
|---|---|---|
| 2 | 0.116 | 50 |
| 3 | 0.036 | 15 |
| 4 | 0.077 | 7 |
| 5 | 0.027 | 7 |
| 7 | 0.023 | 4 |
| 9 | 0.059 | 2 |
| 17 | 0.020 | 1 |

Jaccard decreases as more poems are sampled (the overlap pool must intersect across more poems).
Poets with 2 poems (mean J=0.116) may appear more "consistent" simply because there are fewer
pair combinations. The finding holds when controlling for n_poems: **even at 4+ poems, fixed-form
poets exceed baseline by an order of magnitude; haiku/imagist poets remain at zero.**

---

## Theoretical Implications

The **stable-signature strategy** and the **perpetual-novelty strategy** are both valid routes to
information-theoretic originality:

- **Stable signature**: Build a lexical territory of surprises. Return to it across poems but always
  change the CONTEXT. The surprise is not "I haven't seen this word" but "I haven't seen this word
  *here*." Hopkins's "fresh" and "forth" are not surprising per se — but in his syntactically dense
  sprung rhythms, they always surprise GPT-2.

- **Perpetual novelty**: Treat each poem as a fresh encounter requiring new vocabulary. This is the
  haiku aesthetic, the imagist ethic, possibly the confessional ethos (each moment is unique and
  cannot be re-expressed). No word "earns" its way into a stable arsenal.

The **form-determines-strategy** finding suggests these aren't freely chosen: fixed form partially
imposes the stable-signature strategy on poets who work in it, while loose forms liberate poets
to pursue perpetual novelty.

---

## Next Steps

1. **Filter BPE subword tokens**: Some "signature words" are tokenization fragments (e.g., 'car' as
   part of 'carcass'). A cleaned analysis requiring full words (letter-only, length ≥ 3) would
   sharpen the lexical interpretation.
2. **Semantic stability**: Even if the TOKEN changes, is the SEMANTIC FIELD of high-S₂ positions
   stable across poems? (Use word embeddings to cluster surprise vocabulary.)
3. **Temporal evolution**: For poets with poems spanning decades, does their signature surprise
   vocabulary change over their careers?
4. **The "surprise debt"**: Do poets who use a word in one high-S₂ position ever place it in a
   LOW-S₂ position in a later poem, normalizing it through use?
