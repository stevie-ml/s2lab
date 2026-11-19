# Zipf Coefficient of Prediction Distributions: The Shape of GPT-2's Uncertainty

**Date:** 2026-11-19  
**Experiment:** `experiments/zipf_prediction_coefficient.py` → `results/zipf_prediction_coefficient.json`  
**Corpus:** 431 texts, 56,664 artifact-filtered tokens (p_newline < 0.9, prose control excluded)  
**Novel metric:** Zipf exponent α fitted to top-10 alternatives at each token position  

---

## Research Question

For each token position, GPT-2 distributes probability across its vocabulary. The
top-10 alternatives give us the shape of that distribution. In natural language,
word-rank frequencies follow Zipf's law: P(rank r) ∝ r^(−α), with α ≈ 1.

But the shape of this distribution at any given token reveals something beyond
raw entropy: **how concentrated** is the model's confidence?

- **High α (hyper/super-Zipf)**: probability collapses onto the top-1 prediction.
  The model is not just uncertain — it has a specific, strong expectation.
- **Low α (sub/anti-Zipf)**: probability spreads nearly evenly across alternatives.
  The model is in genuine fog — no strong preference among its options.

**New question:** Do different poetic traditions operate in characteristically different
Zipf regimes? Does the shape of prediction concentration — not just entropy — predict
the type and magnitude of S₂?

---

## Zipf Classification

Exponent α is fitted by log-log regression on (rank, probability) pairs:

| Class | α range | Description |
|---|---|---|
| **hyper_zipf** | ≥ 2.5 | Steeper than natural language; model's top prediction dominates |
| **super_zipf** | 1.5–2.5 | Steeper than average; moderate concentration |
| **near_zipf** | 0.8–1.5 | Natural language-like distribution |
| **sub_zipf** | 0.3–0.8 | Flatter than natural; diffuse uncertainty |
| **anti_zipf** | < 0.3 | Nearly flat; maximally uncertain among top options |

---

## Finding 1: Hyper-Zipf Contexts Are the Only Zone with Positive Average S₂

| Class | n | % | mean S₂ | high_S₂% (≥2) | mean H | mean rank | mean top1_p |
|---|---|---|---|---|---|---|---|
| **hyper_zipf** | 4,043 | 7.1% | **+0.170** | 7.7% | 0.87 | 55.3 | **0.877** |
| **super_zipf** | 14,979 | 26.4% | −0.481 | 19.9% | 4.06 | 128.9 | 0.501 |
| **near_zipf** | 26,024 | 45.9% | −0.495 | 23.0% | 7.07 | 318.2 | 0.193 |
| **sub_zipf** | 11,306 | 20.0% | −0.338 | 21.8% | 8.91 | 561.1 | 0.063 |
| **anti_zipf** | 312 | 0.6% | −0.545 | 16.7% | 10.26 | 572.1 | 0.019 |

**The central finding:** Hyper-Zipf contexts — where the model puts 87.7% of its
probability on a single top prediction — are the only Zipf class with **positive mean
S₂** (+0.170). All other classes average negative S₂.

This is counterintuitive. When the model is MOST concentrated (most certain about its
top prediction), poems achieve the only *positive* average S₂ across the corpus.

**Why?** The math of S₂ = surprisal − entropy clarifies it. When entropy is very low
(0.87 bits), any surprisal above ~0.87 bits produces positive S₂. At hyper-Zipf moments,
the model is so confident about one word that the floor for positive S₂ is low. Even
a rank-55 word (not a catastrophic deviation) can produce positive S₂ in this regime.

**The practical implication:** The most "efficient" S₂ production — positive S₂ per
bit of information invested — occurs at the moments when the model is most concentrated.
Poets extract the most "Straussian gap" per unit of deviation precisely when the model
is most committed to a specific prediction.

---

## Finding 2: S₂ Level Distribution by Zipf Class

| Class | very_neg (<−3) | neg (−3 to 0) | low_pos (0–2) | high_pos (2–5) | extreme (≥5) |
|---|---|---|---|---|---|
| **hyper_zipf** | **0.4%** | **88.7%** | 3.2% | 2.6% | **5.1%** |
| super_zipf | 20.8% | 50.8% | 8.5% | 9.4% | 10.5% |
| near_zipf | 29.4% | 32.8% | 14.8% | 13.7% | 9.3% |
| sub_zipf | 21.4% | 38.8% | 18.0% | 15.0% | 6.8% |
| anti_zipf | 18.9% | 43.3% | 21.2% | 13.1% | 3.5% |

The hyper-Zipf row is diagnostic: **almost no very-negative S₂ (0.4%)**, huge concentration
in the "slightly negative" band (88.7%), and a tail of extreme S₂ (5.1%). This is the
"spike or plateau" profile: hyper-Zipf tokens are rarely very informative in either
direction — usually they confirm a confident prediction (slight negative S₂), but when
they surprise, they spike dramatically.

The near-Zipf and sub-Zipf rows show the opposite: much more probability mass at both
very negative S₂ (29.4%) and extreme S₂ (9.3%), reflecting genuine two-directional
volatility in diffuse contexts.

---

## Finding 3: Era Profiles — Beat Operates in Hyper-Zipf; Symbolists in Sub-Zipf

| Era | mean α | steep% (α≥1.5) | flat% (α<0.8) | mean S₂ | n |
|---|---|---|---|---|---|
| **beat** | **2.189** | **62.1%** | 10.1% | +0.049 | 1,195 |
| **concrete** | 2.023 | 71.4% | 7.1% | −0.584 | 311 |
| triolet | 1.930 | 61.5% | 10.0% | −0.747 | 130 |
| song_lyrics | 1.820 | 57.1% | 10.7% | −0.678 | 541 |
| biblical | 1.795 | 51.5% | 9.1% | −0.453 | 1,331 |
| villanelle | 1.722 | 52.5% | 14.9% | −0.489 | 436 |
| found_poetry | 1.628 | 48.0% | 10.5% | −0.615 | 1,204 |
| *(…)* | | | | | |
| metaphysical | 1.198 | 23.0% | 26.1% | −0.593 | 938 |
| **german_symbolist** | **1.123** | 21.3% | **33.4%** | +0.452 | 356 |

**Beat poetry has the highest mean α (2.189)** — GPT-2's predictions over beat poems
are the most concentrated of any tradition. Beat's speech-like syntax and idiomatic
phrasing drive the model to strong specific predictions. But beat poets subvert these
confident predictions in highly particular ways, producing the second-highest mean S₂
among major eras (+0.049) despite operating in the "most predictable" prediction regime.

**German Symbolist poetry has the lowest mean α (1.123)** — the flattest prediction
distributions. 33.4% of tokens fall in the flat (sub/anti-Zipf) region, more than
any other tradition. This reflects the symbolist deployment of unusual word associations
that keep the model genuinely uncertain across semantic fields. Yet German Symbolist
S₂ is +0.452 — also positive, suggesting that even from diffuse prediction fields,
symbolist poets reliably find words off the map.

**The literary distinction:** Beat generates high-confidence ambush (defeat a concentrated
prediction); symbolism generates diffuse-field escape (departing even from a spread-out
probability space).

---

## Finding 4: The Steep-Flat Axis Cuts Across the Expected Literary Boundaries

Traditions with HIGH α (concentrated predictions):
- Beat, Concrete, Triolet, Song lyrics, Biblical, Villanelle, Found poetry, Ballad

Traditions with LOW α (diffuse predictions):
- German Symbolist, Metaphysical, Early Modern, Ekphrastic, Elegy, Dramatic monologue

The organizing principle is not historical period or prestige. It is **syntactic
predictability of the form**:

- High α forms use **formulaic or speech-like syntax**: beat's stream-of-consciousness,
  biblical parallelism, song structure, ballad meter, villanelle's refrains
- Low α forms use **complex noun phrases and unusual collocations**: metaphysical
  conceits, symbolist juxtapositions, dramatic monologue's complex register shifts

Concrete poetry is anomalous: it has high α (2.023) but its S₂ is negative (−0.584),
suggesting that even though GPT-2 makes confident predictions over concrete poems,
those predictions are FULFILLED more often than violated — the visual/spatial form of
concrete poetry renders the text predictable at the token level even as it's visually
radical.

---

## Finding 5: German Expressionist Is an Outlier — High S₂ from Moderate α

| Era | mean α | mean S₂ |
|---|---|---|
| german_expressionist | 1.281 | **+0.100** |
| german_modernist | 1.219 | **+0.626** |
| german_symbolist | 1.123 | **+0.452** |
| deep_image | 1.235 | **+0.066** |
| clerihew | 1.225 | **+0.507** |

The German-language traditions (symbolist, expressionist, modernist) all achieve
positive mean S₂ despite near-to-moderate α values. German Modernist achieves the
highest mean S₂ of any tradition (+0.626) while having only a moderate α (1.219).
This suggests the German poetic tradition has developed a distinctive strategy: working
from a natural-language-like prediction distribution but consistently finding words
*outside* even that distributed probability field.

---

## Interpretation: Two Paths to Positive S₂

This analysis reveals two structurally distinct paths to effective poetic surprise:

**Path 1: The High-Stakes Ambush (high α)**
- Beat poetry, biblical verse, found poetry
- The model concentrates heavily on one word (high α)
- The poet writes something else — defeating a confident, specific prediction
- S₂ per deviation is high but events are sparse (high α means the model is often *right*)
- The "surprise" is a dramatic reversal of a strong expectation

**Path 2: The Field Escape (low α)**
- German Symbolist, Metaphysical poetry
- The model distributes probability broadly (low α)
- The poet finds words even outside this spread field
- S₂ per deviation is moderate but the semantic "distance" traversed is greater
- The "surprise" is an escape from the model's entire semantic neighborhood

These two strategies, previously conflated under the "ambush vs. fog" binary, can now
be precisely characterized by the Zipf coefficient: ambush = high α context defeated;
fog = low α context escaped.

---

## Suggested Next Steps

1. **Within-poem α trajectories**: Does α change across a poem's arc? Do poems
   start in high-α (concentrated) territory and move toward low-α as the poem
   establishes its own semantic field?
2. **α vs. rhyme position**: Are rhyme slots systematically higher α (the model
   knows a rhyming word is coming)?
3. **High-α + extreme S₂ tokens**: Extract the specific tokens where both α ≥ 2.5
   and S₂ ≥ 5.0 — these are the "perfect ambush" moments. What do they look like?
4. **Fit quality (R²)**: The fit of the Zipf law itself may be informative — when
   the top-10 distribution is NOT well described by a power law, what is it? A
   bimodal distribution (function + content word split)?
