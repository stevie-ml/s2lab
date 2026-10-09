# Alternatives Architecture: Ambush vs. Fog — Two Types of Poetic Surprise

**Date:** 2026-10-09  
**Experiment:** `experiments/alternatives_architecture.py` → `results/alternatives_architecture.json`  
**Corpus:** 227 texts, 25,081 artifact-free tokens (p_newline < 0.9)  
**Builds on:** `straussian_gap_taxonomy.md`, `entropy_conditioned_deviation.md`, `prediction_field_homogeneity.md`

---

## Research Question

Prior work has shown that high-S₂ tokens come in two entropy regimes: the "Straussian" 
(low entropy, high surprisal — defying a confident prediction) and the "high-entropy 
deviation" (high entropy, poet still outdid the uncertainty). But entropy is a scalar 
that collapses the *structure* of the prediction distribution.

This experiment asks: does the **shape** of GPT-2's top-10 prediction distribution — 
specifically, how dominant the top prediction is over the second — create two meaningfully 
different types of poetic surprise?

**AMBUSH**: The model's top prediction dominates (top_ratio = p₁/p₂ > 2.0) AND the poet 
chose something with S₂ ≥ 2.0. The poet laid in wait and struck where language was 
most predictable.

**FOG**: The top-10 predictions are competitive (top_ratio ≤ 2.0) AND S₂ ≥ 2.0. 
The poet surprised in a zone where the model was already uncertain — outdoing even the 
fog of possibilities.

---

## Finding 1: Ambush Outperforms Fog — But Both Tower Over Baseline

| Category | n | Mean S₂ | Pos% | Description |
|---|---|---|---|---|
| **ambush** | 2,244 | **+5.896** | 100% | defied dominant prediction |
| **fog** | 2,556 | **+5.049** | 100% | defied diffuse field |
| neutral | 3,554 | +0.511 | 68.6% | moderate departure |
| compliance | 1,329 | −1.881 | 0% | strongly conformed |
| **near_miss** | 15,398 | **−2.289** | 7.7% | chose within top-10 (rank ≤ 10) |

The Ambush–Fog S₂ gap (+5.90 vs +5.05) is **0.85 bits** — a meaningful premium for 
defying a confident prediction over defying an uncertain one. When GPT-2 was most 
sure of what came next, the poet's deviation was more informationally extreme.

The most striking number: **15,398 tokens** fall in the "near_miss" category, where 
the poet chose within the model's top-10 predictions but not the top-1. These have 
mean S₂ = −2.289. Poets conform to the model's predictions more than they rebel — but 
when they rebel, the force is overwhelming.

---

## Finding 2: Exemplary Fog Moments — Ginsberg as the Paradigm

Fog moments are conceptually the richest: the model was offering many plausible 
continuations, and the poet bypassed all of them.

| Author | Token | S₂ | Model's Top Prediction | Top Alt Prob | top_ratio |
|---|---|---|---|---|---|
| Gerard Manley Hopkins | ` shook` | 22.04 | ` the` | 0.39 | 1.20 |
| Christopher Smart | ` prank` | 22.02 | ` the` | 0.45 | 1.24 |
| Emily Dickinson | ` Fun` | 18.90 | ` little` | 0.19 | 1.61 |
| John Ashbery | `L` | 17.73 | `playing` | 0.60 | 1.85 |
| Gregory Corso | ` neb` | 16.56 | ` you` | 0.33 | 1.33 |
| Allen Ginsberg | ` hysterical` | 15.61 | ` to` | 0.26 | 1.78 |

Ginsberg's "hysterical" in "Howl" ("starving hysterical naked") is the fog paradigm: 
the model was offering many verbs and function words, none with a clear lead. Ginsberg 
chose none of them — inserting an adjective sequence (" hysterical", " naked") that 
transforms the model's expected verbal phrase into an accumulating catalog of states.

---

## Finding 3: The Ambush/Fog Ratio as a Poetic Fingerprint

The ratio ambush_rate / fog_rate captures a poet's **preference for where to strike**:
- **High ratio (> 1.5)**: "Precision rebels" — they prefer to defy GPT-2's most 
  confident predictions, not its uncertain ones.
- **Low ratio (< 0.7)**: "Uncertainty explorers" — they dive into the model's most 
  ambiguous zones and find what it missed.

### Poet Profiles

| Poet | ambush% | fog% | ratio | mean S₂ | Style |
|---|---|---|---|---|---|
| Bruce Andrews | **25.0%** | 6.8% | **3.67** | +0.74 | Precision rebel |
| Marianne Moore | 13.9% | 6.9% | 2.00 | −0.06 | Precision rebel |
| Frank O'Hara | 13.6% | 6.8% | 2.00 | −0.03 | Precision rebel |
| Hart Crane | 16.6% | 14.2% | 1.17 | +0.97 | Balanced |
| Emily Dickinson | 11.9% | 11.2% | 1.06 | −0.09 | Balanced |
| Walt Whitman | 12.5% | 11.1% | 1.12 | −0.29 | Balanced |
| Seamus Heaney | 12.6% | **15.0%** | 0.84 | +0.17 | Uncertainty explorer |
| Thomas Hardy | 11.8% | **14.4%** | 0.82 | +0.21 | Uncertainty explorer |
| Allen Ginsberg | 14.2% | **16.2%** | 0.87 | +0.69 | Uncertainty explorer |

**Bruce Andrews** stands out sharply: 3.67 ratio, meaning he is nearly 4× more likely 
to strike in a "winner-take-all" zone than a competitive one. His Language poetry 
proceeds by maximally defying GPT-2's most confident expectations — not by working in 
the seams of ambiguity, but by shattering certainty.

**Ginsberg** is the opposite: ambush=14.2% but fog=16.2%. His characteristic move 
is to find the moments of genuine linguistic uncertainty and then push beyond all the 
model's plausible options.

---

## Finding 4: Era Analysis — The Genre Fingerprint

| Era | ambush% | fog% | ratio | n |
|---|---|---|---|---|
| language | 13.2% | 8.3% | **1.58** | 144 |
| oulipo | 10.0% | 4.0% | **2.50** | 50 |
| beat | 14.2% | 16.2% | 0.87 | 148 |
| deep_image | 11.5% | **16.4%** | 0.70 | 61 |
| german_expressionist | 11.0% | **17.0%** | **0.65** | 283 |
| confessional | 9.3% | **14.9%** | 0.63 | 397 |
| harlem_renaissance | 10.0% | 8.9% | 1.12 | 549 |
| metaphysical | 9.0% | 9.9% | 0.91 | 533 |

**Oulipo** (constrained writing, n=50) has the highest ambush/fog ratio: 2.50. 
Constrained poets like Perec and Queneau — forced to work within tight rules — 
tend to produce their surprises in zones where language is most predictable. 
The constraint itself creates the certainty the poet then shatters.

**German Expressionism** has the lowest ratio at 0.65: Trakl, Georg, Heym 
overwhelmingly work in the fog — their characteristic ambiguity and dissolution of 
stable referents means they produce surprise in already-uncertain linguistic territory.

**Language poetry** has a high ratio (1.58), consistent with Andrews' profile: 
the movement's project of defamiliarizing conventional grammar produces ambush-type 
surprises (breaking confident functional predictions).

**Confessional poetry** has a ratio of 0.63 — the lowest among major traditions. 
Plath, Sexton, Lowell prefer to work in the fog, perhaps because their subject matter 
(internal emotional states) naturally involves high linguistic uncertainty.

---

## Finding 5: The Near-Miss Economy

The largest single category is **near_miss**: 15,398 tokens where the poet chose 
from within the model's top-10 predictions (but not the top-1). This has mean 
S₂ = −2.289.

This is a profound finding: **the bulk of poetic language operates in a zone of 
near-compliance** — the poet reaches for something slightly less expected than the 
model's top choice but stays within the prediction field. The rare moments of true 
ambush or fog (combined: 4,800 tokens, or ~19% of high-S₂ tokens) are embedded 
in a vast sea of near-misses.

The poem's information architecture is thus:
1. **Near-compliance**: ~60% of tokens — sustaining the linguistic context
2. **Neutral/moderate deviation**: ~14% — gentle divergence
3. **Fog**: ~10% — surprising in uncertain territory  
4. **Ambush**: ~9% — shattering confident predictions
5. **Compliance**: ~5% — stronger-than-expected conformity

---

## Interpretation: Two Theories of Poetic Defamiliarization

The ambush/fog distinction maps onto two theories of how poetry achieves 
defamiliarization:

**Ambush theory (high ratio poets)**: Poetry works by finding where language is most 
grammatically determined — where articles, prepositions, and function words are near-
inevitable — and substituting an image, a proper noun, or a radical content word. 
The surprise is proportional to what was suppressed. (Andrews, Moore, O'Hara, Language poetry, Oulipo)

**Fog theory (low ratio poets)**: Poetry works by exploring the semantic thresholds 
where language is already uncertain — the branch points in the prediction tree — 
and finding the option the model's uncertainty couldn't anticipate. The surprise 
is the discovery of an unimagined possibility. (Ginsberg, Hardy, Heaney, Expressionism, 
Confessional)

These may correspond to the distinction between **syntactic** and **semantic** 
defamiliarization: ambush breaks grammatical expectations; fog exceeds semantic ones.

---

## Next Steps

1. **Test the hypothesis quantitatively**: classify tokens at high-S₂ moments by whether 
   the "suppressed" top prediction is a function word (syntactic ambush) or content word 
   (semantic fog). Does this split predict the ambush/fog ratio?

2. **Within-poem arc**: do ambush moments concentrate in different positions (line 
   endings, stanza beginnings) than fog moments?

3. **Reader model**: ambush = high risk, high reward; fog = lower individual impact 
   but cumulative disorientation. Do ambush-heavy poems get better remembered/cited?

4. **Adding new poems**: add more Oulipo and German Expressionist examples to sharpen 
   the ratio estimates for these underrepresented eras.
