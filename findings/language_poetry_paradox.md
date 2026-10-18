# The Language Poetry Paradox: Entropy-Flooding vs. Lexical Defiance

**Date:** 2026-10-18  
**Experiment:** `experiments/language_poetry_paradox.py`  
**Data:** `results/language_poetry_paradox.json`

---

## Research Question

Why does **Language Poetry** — theoretically the most experimental, anti-normative
movement in 20th-century American poetry — have *lower* artifact-free mean S2 than
**Beat poetry**, which is considered more accessible and emotionally direct?

From the era comparison (artifact-free S2):

| Era | S2 (clean) |
|-----|-----------|
| Beat | **+0.07** |
| Confessional | −0.23 |
| Modernist | −0.34 |
| Language Poetry | −0.56 |
| New York School | −0.57 |

Language Poetry, which disrupts grammar and resists semantic coherence, scores
*lower* than Beat poetry, which uses long confessional narratives and colloquial
urgency. This is the paradox.

---

## Hypothesis: Entropy-Flooding

The S2 framework decomposes as:

> **S2 = S − H**
>
> S = surprisal (−log p of chosen token)  
> H = entropy of the full prediction distribution

A poet produces positive S2 by choosing a token whose individual probability is
much *lower* than the model expects on average (high S, moderate H).

The hypothesis: Language Poetry **floods** the model with entropy — by fragmenting
syntax, eliminating connectives, and juxtaposing incompatible semantic fields,
it drives H upward. The model is equally uncertain about everything. In this state,
even common words yield near-zero S2, because S barely exceeds H.

Beat Poetry, by contrast, uses long cumulative syntax ("I saw the best minds…")
that allows GPT-2 to form real expectations about what comes next — and then
Ginsberg, Corso violate those expectations at the lexical level.

---

## Results

### By Era: S, H, and S2 Decomposed

| Era | n | avg S | avg H | avg S2 | σ(S2) | Hi-H% | Rank1% | avg Rank |
|-----|---|-------|-------|--------|--------|--------|--------|----------|
| Language Poetry | 5 | 5.905 | 6.330 | **−0.424** | 3.729 | 14.5% | 32.7% | 344 |
| Beat | 6 | 5.482 | 5.203 | **+0.279** | 4.306 | 17.2% | 43.8% | 615 |
| New York School | 18 | 6.045 | 6.644 | −0.599 | 3.566 | 17.0% | 25.5% | 334 |
| Surrealist | 8 | 5.460 | 6.070 | −0.609 | 3.490 | 15.2% | 34.1% | 230 |
| Confessional | 6 | 6.491 | 6.791 | −0.300 | 3.864 | 19.9% | 21.7% | 343 |
| Modernist | 25 | 6.198 | 6.599 | −0.400 | 3.793 | 21.7% | 29.6% | 403 |
| Romantic | 16 | 6.325 | 6.795 | −0.470 | 3.672 | 24.8% | 27.6% | 409 |
| Control prose | 5 | 3.854 | 5.590 | **−1.736** | 2.261 | 12.5% | 44.3% | 46 |

*Hi-H% = fraction of tokens where H > 9 bits (model in maximally confused state)*

### Core Test: Language Poetry vs. Beat

| Measure | Language Poetry | Beat | Δ |
|---------|----------------|------|---|
| avg S (surprisal) | 5.905 | 5.482 | **+0.423** |
| avg H (entropy) | 6.330 | 5.203 | **+1.127** |
| avg S2 | −0.424 | +0.279 | **−0.703** |

**ΔH (+1.127) >> ΔS (+0.423) → entropy-flooding confirmed.**

Language Poetry raises H by 1.13 bits while raising S by only 0.42 bits. S2 collapses
because the entropy gain outpaces the surprisal gain.

---

## Per-Poem Breakdown

### Language Poetry

| Poem | avg S | avg H | S2 | Hi-H% | Rank1% | avg Rank |
|------|-------|-------|-----|--------|--------|---------|
| Lyn Hejinian, *My Life* | 5.665 | 6.566 | −0.901 | 10% | 28% | 339 |
| Charles Bernstein, *Dysraphism* | 5.105 | 5.860 | −0.755 | 9% | 38% | 166 |
| Charles Bernstein, *Sheds of Our Webs* | 4.741 | 5.503 | −0.762 | 5% | 42% | 46 |
| Ron Silliman, *Ketjak* | 7.077 | 7.515 | −0.438 | 30% | 24% | 459 |
| Bruce Andrews, *Islets/Irritations* | 6.939 | 6.204 | **+0.735** | 18% | 32% | 711 |

### Beat Poetry

| Poem | avg S | avg H | S2 | Hi-H% | Rank1% | avg Rank |
|------|-------|-------|-----|--------|--------|---------|
| Allen Ginsberg, *Howl* | 7.892 | 6.939 | **+0.953** | 24% | 24% | 686 |
| Gregory Corso, *Marriage* | 6.665 | 5.894 | **+0.771** | 13% | 26% | 567 |
| Allen Ginsberg, *A Supermarket* | 6.934 | 6.397 | **+0.536** | 18% | 25% | 694 |
| Gregory Corso, *Bomb* | 7.338 | 7.651 | −0.313 | 36% | 26% | 1191 |
| Lawrence Ferlinghetti, *Constantly Risking* | 2.325 | 2.466 | −0.141 | 7% | 78% | 301 |
| Lawrence Ferlinghetti, *In Goya's* | 1.741 | 1.871 | −0.130 | 5% | 84% | 252 |

---

## Findings

### 1. Entropy-Flooding Confirmed

Language Poetry drives H upward (+1.13 bits vs Beat) without proportionally raising S.
The result is negative S2: the model is more uncertain, but the poet's choices aren't
proportionally more defiant. Language Poetry *exhausts* the model's capacity for
confident prediction rather than *defeating* specific predictions.

### 2. Two Routes to Low S2

Two mechanisms produce negative S2 in poetry:

| Route | Mechanism | Example |
|-------|-----------|---------|
| **Entropy-flooding** | Destroy syntactic expectations → H rises, S barely follows | Language Poetry, New York School |
| **Lexical smoothing** | Follow expectations closely → S stays low | Ferlinghetti, control prose |

Ferlinghetti is a striking outlier within Beat: his two poems show **78–84% rank-1 tokens**
(the model usually predicts exactly what he writes), yet he is grouped with Beat.
His "experimentalism" is conceptual (open form on the page) but not lexically
surprising. Compare Ginsberg: **24–25% rank-1**, avg rank ~690, S2 strongly positive.
**Ginsberg defies predictions; Ferlinghetti writes what language expects.**

### 3. The Avg Rank Reversal

Despite Language Poetry appearing "more experimental," its average token rank (344)
is *lower* than Beat's (615). The model ranks Language Poetry tokens closer to first
— because in high-entropy contexts, all tokens are roughly equally probable,
so the "winner" tends to be a common word near the top.

Beat Poetry's higher avg rank reflects **low-entropy violations**: the model was
*confident* about something specific, and the poet chose something else entirely
(rank 615 = the chosen word was deep in the distribution when the model had clear
expectations).

### 4. The Andrews Exception

Bruce Andrews (*Islets/Irritations*) is the one Language poet with *positive* S2
(+0.735). His work relies on radical semantic juxtaposition that even high-entropy
contexts can't absorb — he forces genuinely low-probability combinations. Andrews
is doing something structurally different from Hejinian or Bernstein:
**syntactic disruption + lexical shock**, not just syntactic disruption alone.

### 5. Theoretical Implication

Language Poetry achieves defamiliarization through **epistemic exhaustion**: by
destroying the model's ability to form expectations at all. Beat achieves it through
**epistemic violation**: setting up clear expectations and then defying them.

From the S2 framework's perspective, epistemic violation (high S2) is the more
"Straussian" gesture — it requires a gap between what language expected and what
the poet chose. Epistemic exhaustion collapses that gap: there is no expected
word to suppress.

This suggests a **typology of poetic surprise**:

> Type A (Straussian): The model knows what should come. The poet refuses.
> → Ginsberg, Dickinson, Hopkins, WCW
>
> Type B (Exhaustion): The model doesn't know what should come. The poet chooses
> something ordinary. → Language Poetry, New York School, much of Surrealism
>
> Type C (Affirmation): The model knows what should come. The poet agrees.
> → Ferlinghetti, ballads, clichés, control prose

---

## Suggested Next Steps

1. **Expand Language Poetry corpus**: Add Susan Howe, Barrett Watten, Carla Harryman
   — do they cluster with Bernstein/Hejinian (Type B) or Andrews (Type A)?
2. **The Silliman H-spike**: Ketjak has 30% Hi-H tokens (H > 9). What grammatical
   structures create these maximum-confusion zones? Are they the asyndetic lists?
3. **Entropy trajectory within Language poems**: Does H peak at the start (as the
   model is still calibrating) or stay uniformly high throughout?
4. **Compare Surrealism**: Surrealist S2 (−0.61) is similar to Language Poetry. Do
   they use the same mechanism (entropy-flooding via incongruous juxtaposition)?
5. **Beat without Ferlinghetti**: Recalculate Beat S2 excluding Ferlinghetti's two
   outlier poems. Does Beat S2 rise dramatically, overtaking confessional?
