# S₂ Zone Topology: Isolated Spikes vs. Sustained High-S₂ Zones

**Date:** 2026-09-21  
**Experiment:** `experiments/s2_zone_topology.py`  
**Corpus:** 155 poems (160 total, 5 prose controls excluded)  
**Threshold:** S₂ ≥ 0.5 for "high surprise"

---

## Research Question

Previous S₂ analyses in this project used an *isolation criterion* — only studying
spikes surrounded by at least ±8 low-S₂ tokens. This was methodologically clean, but it
systematically excluded clustered events.

When we remove that constraint and look at the raw topology of surprise, we can ask:

> Are high-S₂ moments in poetry predominantly **isolated single-token events**, or do they
> cluster into **sustained zones** of consecutive deviance?

A zone is defined as a maximal run of ≥2 consecutive tokens all above S₂ ≥ 0.5.
A spike is a single-token event (run length = 1).

---

## Global Finding: One-Third of All Surprise is Zoned

| Metric | Value |
|--------|-------|
| Total high-S₂ events | 3,625 |
| Isolated spikes (length = 1) | 2,449 (**67.6%**) |
| Sustained zones (length ≥ 2) | 1,176 (**32.4%**) |
| Mean zone length | 2.47 tokens |
| Median zone length | 2.0 tokens |
| Maximum zone length | 11 tokens |
| Mean S₂ within zones | 5.12 |
| Mean S₂ at isolated spikes | 5.61 |

**Zones carry slightly lower mean S₂ than isolated spikes** (5.12 vs 5.61),
suggesting that zone events "share" the surprise budget across tokens rather than
concentrating it at a single moment.

---

## Zone Length Distribution

Zones are almost always short — the distribution is extremely right-skewed.

| Zone Length | Count | % of all zones |
|-------------|-------|----------------|
| 2 tokens | 788 | 67.0% |
| 3 tokens | 266 | 22.6% |
| 4 tokens | 88 | 7.5% |
| 5 tokens | 29 | 2.5% |
| 6 tokens | 3 | 0.3% |
| 8 tokens | 1 | 0.1% |
| 11 tokens | 1 | 0.1% |

The median zone is just 2 tokens — a pair of mutually unexpected words. Zones of ≥5
tokens are rare (34 total, ~3% of all zones), and a zone of 10+ is exceptional.

---

## Zone Length vs. Zone Intensity: No Correlation

A striking null finding: **zone length has essentially zero correlation with zone
intensity** (Pearson r = −0.006, n = 1,176).

This means longer zones are not more intense climaxes — they are sustained *plateaus*
at whatever intensity they happen to start at. The "build-up" model of poetic surprise
(tension accumulates across several tokens before release) is not supported here. Instead,
zones appear as flat patches of deviance, not ascending gradients.

---

## Closest-Neighbor Structure: Surprise Clusters Tightly

Even between distinct events, high-S₂ tokens cluster densely:

| Metric | Value |
|--------|-------|
| Mean gap between consecutive events | 3.01 tokens |
| **Median** gap | **2.0 tokens** |
| Gaps ≤ 3 tokens (tightly clustered) | 71.7% of all inter-event gaps |
| Maximum gap | 54 tokens |

The median of 2 tokens confirms what the zone topology suggests: at the local level,
high-S₂ events are nearly always neighbors. The "isolation criterion" in previous work
was protecting against this reality — a majority of surprise events occur in a
neighborhood of other surprise events.

---

## Longest Zones (Top 15)

The single longest sustained zone in the corpus is a remarkable 11-token run in
Thomas Wyatt's "They flee from me" (early_modern, mean S₂ = 6.01):

> *"me that sometime did me seek / With naked foot stalking in my chamber"*

This is grammatically dense and tonally unsettling — the subject switching from "me"
to "me" while the archaic predication structure ("naked foot stalking") maintains
continuous informational surprise.

| Len | Mean S₂ | Author | Era | Text (preview) |
|-----|---------|--------|-----|----------------|
| 11 | 6.01 | Thomas Wyatt | early_modern | *me that sometime did me seek / With naked foot st...* |
| 8 | 3.19 | Rainer Maria Rilke | german_modernist | *verginge von seinem / stärkeren Dasein* |
| 6 | 5.90 | Walt Whitman | 19th_century | *I mark'd where on a* |
| 6 | 5.35 | E.E. Cummings | modernist | *up so floating many bells down* |
| 6 | 5.75 | Philip Larkin | contemporary | *at four to soundless dark* |

Larkin's "at four to soundless dark" is from "Aubade" — notably, this phrase covers the
transition "matured in darkness" where the conventional predicate has been displaced.

---

## Most Intense Zones (length ≥ 3, ranked by mean S₂)

| Len | Mean S₂ | Max S₂ | Author | Text |
|-----|---------|--------|--------|------|
| 3 | 17.98 | 35.40 | Bruce Andrews | *patriotic / duty* |
| 3 | 15.80 | 25.69 | Traditional (Scottish) | *Nor fashes* |
| 4 | 14.41 | 29.66 | David Antin | *being wrong / being* |
| 3 | 13.30 | 27.33 | Gerard Manley Hopkins | *Times told lo-* |
| 3 | 12.41 | 18.35 | Robert Burns | *In proving fore-* |
| 3 | 12.06 | 28.03 | Langston Hughes | *Or fester* |
| 4 | 12.01 | 34.00 | Thomas Hardy | *Cold currents thrid* |
| 3 | 11.83 | 31.92 | Thomas Hardy | *Our childhood used* |
| 4 | 11.36 | 25.07 | William Carlos Williams | *depends / upon /* |

The Bruce Andrews zone "patriotic / duty" stands alone — a mean S₂ of 17.98 across
three tokens makes this the densest sustained zone of surprise in the corpus. Andrews is
a Language poet whose technique involves deliberately breaking syntactic contract; these
enjambed noun phrases clearly register as maximal violations of GPT-2's generative grammar.

Hopkins's zone "Times told lo-" (from "The Windhover" — "brute beauty and valour and act,
oh, air, pride, plume, here / Buckle! AND the fire that breaks from thee then, a billion /
Times told lovelier") is the compressed late-syllable zone before a key compound adjective.

---

## Era Breakdown: Zone Rates Vary Considerably

Eras are ranked by "Zone%" — the fraction of high-S₂ events that are zoned rather than
isolated:

| Era | Poems | Zone% | Avg Zone S₂ |
|-----|-------|-------|-------------|
| mid_century | 3 | **49.0%** | 5.00 |
| beat | 2 | 40.0% | 5.51 |
| german_symbolist | 3 | 39.6% | 3.93 |
| haiku | 8 | 39.3% | **7.14** |
| confessional | 6 | 38.1% | 5.91 |
| … | | | |
| metaphysical | 4 | 26.5% | 4.06 |
| language | 3 | 26.5% | 6.36 |
| spoken_word | 2 | 26.2% | 4.64 |
| song_lyrics | 3 | 22.0% | 5.53 |
| oulipo | 1 | **16.7%** | 6.84 |

**Mid-century poets** (Olson, Bishop, Lowell) have the highest zone rate (49%) — nearly
half their surprise events are clustered. This may reflect the denser, more compressed
syntax typical of 1950s–60s American poetry.

**Haiku** is notable: high zone rate *and* highest average zone S₂ (7.14). In haiku, every
token is weight-bearing, and the juxtaposition structure (kireji effect) creates sustained
surprise precisely because the semantic bridge between images is maximal.

**Oulipo** (Perec/Queneau in this corpus) has the lowest zone rate (16.7%) but the second-
highest average zone S₂ (6.84) — suggesting that when constrained-writing does surprise, it
concentrates the surprise in isolated high-voltage moments rather than sustained zones.

**Song lyrics** are noteworthy: low zone rate (22%) consistent with a genre that prioritizes
resolution and melodic expectation over sustained deviance.

---

## Poet-Level Zone Rates

| Author | Zone% | Avg Zone S₂ |
|--------|-------|-------------|
| Matsuo Bashō | **58.3%** | 6.10 |
| E.E. Cummings | 41.3% | 6.82 |
| Allen Ginsberg | 40.0% | 5.51 |
| Walt Whitman | 39.7% | 4.70 |
| Stefan George | 39.6% | 3.93 |
| Sylvia Plath | 34.3% | **8.10** |
| Traditional (Scottish ballad) | 34.1% | 6.49 |
| Matthew Arnold | 31.2% | 4.12 |
| George Herbert | 31.3% | 4.10 |

Bashō's 58.3% zone rate is striking and consistent with the haiku finding above. In the
three-line form, a single image-pivot can generate back-to-back high-S₂ tokens because the
entire phrase is unexpected relative to conventional descriptive language.

**Sylvia Plath** has modest zone frequency (34.3%) but the highest average zone S₂ of any
poet with ≥2 poems (8.10). Her zones are rare but extremely intense when they occur — bursts
of sustained extreme deviance rather than a continuous elevated baseline.

---

## Synthesis: Two Modes of Poetic Surprise

The topology analysis reveals two structurally distinct modes of surprise in poetry:

**Mode 1 — The Spike (67.6% of events):** A single token that violates expectation within
a field of lower surprise. The canonical "Straussian moment." Previous analyses in this
project focused almost entirely on this mode.

**Mode 2 — The Zone (32.4% of events):** A run of 2–11 consecutive tokens, each above the
threshold. The zone carries total surprise distributed flatly (r ≈ 0 between length and
intensity), not concentrated at a climax. Zones tend to occur at dense syntactic nodes:
the crossing of a line break during a metaphor, a compound archaic construction, or the
pivot between two images in a juxtaposition.

These modes are not simply "big spikes" vs. "small spikes." They represent qualitatively
different informational gestures: the spike is punctual, the zone is durational.

---

## Theoretical Note

The near-zero correlation between zone length and intensity (r = −0.006) is consistent
with a **plateau model** of sustained surprise, not a **buildup-release model**. This
challenges an intuitive narrative about poetic tension: the poem does not "accumulate
surprise toward a release." Rather, it switches between two regimes — conventional flow
and sustained deviance — at a roughly constant intensity level within each regime.

The tight inter-event gap (median = 2 tokens, 71.7% within 3 tokens) further suggests that
"conventional" and "deviant" tokens are not strictly alternating in isolation but form local
neighborhoods of similar information-density.

---

## Suggested Next Steps

1. **Manual annotation of zones by linguistic category**: Are long zones always complex
   predications? Always enjambments? Cataloguing the grammar of zones would extend the
   straussian taxonomy from single tokens to phrase-level structures.

2. **Zone rate as a stylometric fingerprint**: The poet-level zone rate varies from ~16% to
   ~58%. This could be a stable, model-independent stylometric feature distinguishing tight
   vs. sustained surprise strategies.

3. **Haiku-specific zone analysis**: Haiku's high zone S₂ combined with high zone rate
   warrants a dedicated study — the kireji cut may be measurable as an engineered zone event.

4. **Time-within-poem zone distribution**: Do zones cluster at line beginnings, middles,
   ends? At stanza transitions? Connecting zone topology to structural position would bridge
   two lines of existing research.
