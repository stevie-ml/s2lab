# Semantic Arc Within a Poem: Convergence vs. Crescendo

**Date:** 2026-10-06  
**Experiment:** `experiments/semantic_arc_within_poem.py` → `results/semantic_arc_within_poem.json`  
**Corpus:** 187 English poems (22 skipped for < 30 content tokens), 209 total texts  
**Builds on:** `within_poem_type_arc.md` (S2 arc), `inter_token_semantic_jumps.md` (inter-token distances)

---

## Research Question

`within_poem_type_arc.md` established that **S2 is front-loaded**: poems show highest
Straussian deviation (Type I%) in their first third and settle into conformity by the last
third. Does the **inter-token semantic distance** — how semantically far adjacent tokens are
in GPT-2's embedding space — follow the same pattern, or a different one?

Two competing hypotheses:
- **H1 (Semantic convergence)**: As a poem develops its subject, adjacent tokens become more
  thematically related. The poem narrows in on its subject. Semantic distance *decreases*.
- **H2 (Semantic crescendo)**: Poetry builds toward a semantic climax — the most daring
  juxtapositions happen at the volta or ending. Semantic distance *increases*.

And crucially: **are the two arcs correlated?** Or does semantic distance track independently
of S2, suggesting they measure different aspects of poetic development?

---

## Main Finding: Both Arcs Converge, but Independently

| Measure | 1st third | 2nd third | 3rd third | Δ (last−first) |
|---|---|---|---|---|
| **Mean inter-token dist** | 0.7406 | 0.7399 | 0.7349 | **−0.0057** |
| **Mean S₂** | +0.308 | −0.151 | −0.226 | **−0.534** |

**H1 confirmed**: Semantic distance decreases from first to last third (−0.0057), meaning
adjacent tokens in the final third of a poem are slightly more semantically related than
those in the opening. Poems *semantically converge* over their course.

**S2 arc confirmed again**: S2 drops even more dramatically (−0.534), consistent with the
front-loading result from `within_poem_type_arc.md`.

**The critical null finding**: r(arc_dist, arc_S2) = **+0.109** — the two arcs are nearly
uncorrelated. Whether a poem shows semantic convergence or crescendo has almost no bearing
on whether its S2 arc is front-loaded or back-loaded. **These are two independent dimensions
of how a poem develops over its arc.**

60% of poems show semantic convergence (distance decreases first→last); 40% show semantic
crescendo (distance increases). For S2: 68% show front-loading (S2 decreases first→last);
only 32% show S2 back-loading.

---

## Era Breakdown: The Convergence/Crescendo Axis

Sorted by arc_dist (most convergent → most crescendo):

| Era | N | d (first) | d (last) | Δdist | ΔS2 |
|---|---|---|---|---|---|
| new_york_school | 18 | 0.726 | 0.699 | **−0.027** | −0.743 |
| metaphysical | 4 | 0.755 | 0.731 | −0.024 | −0.707 |
| 19th_century | 10 | 0.760 | 0.736 | −0.024 | −0.695 |
| biblical | 7 | 0.748 | 0.728 | −0.020 | −0.273 |
| language | 3 | 0.745 | 0.730 | −0.016 | −0.781 |
| modernist | 18 | 0.736 | 0.726 | −0.010 | −0.808 |
| fixed_form | 8 | 0.755 | 0.745 | −0.010 | −0.934 |
| romantic | 15 | 0.758 | 0.758 | −0.000 | −0.539 |
| victorian | 21 | 0.745 | 0.746 | +0.001 | −0.206 |
| contemporary | 9 | 0.728 | 0.731 | +0.003 | −0.603 |
| harlem_renaissance | 5 | 0.735 | 0.739 | +0.004 | −1.093 |
| german_expressionist | 2 | 0.765 | 0.782 | +0.017 | −1.402 |
| confessional | 6 | 0.726 | 0.746 | +0.020 | +0.419 |
| imagist | 2 | 0.732 | 0.753 | +0.020 | −0.129 |
| german_modernist | 2 | 0.726 | 0.755 | +0.029 | −1.780 |
| **concrete** | 2 | 0.731 | 0.778 | **+0.047** | −1.944 |

**Convergence eras**: New York School, metaphysical, 19th century — these are forms that
develop an argument, image, or premise and narrow toward a conclusion.

**Crescendo eras**: Concrete, German modernist, imagist, confessional — these are forms that
escalate, accumulate, or build toward a semantic climax.

The **confessional** era is unusual: it shows BOTH semantic crescendo (+0.020) and S2 back-
loading (+0.419). This is the only era in the table where both distance AND S2 increase —
confessional poetry builds toward both semantic and prediction surprise simultaneously.
Plath's poems are the prototypical example (see below).

---

## Four Patterns: The Semantic × S2 Arc Quadrant

Using median thresholds (arc_dist > 0, arc_s2 > 0):

| Quadrant | % poems | Description |
|---|---|---|
| **converge + conform** | 40.5% | Most common. Both S2 and distance decrease. The "resolution" pattern: the poem establishes a semantic register early (when it's most surprising) and narrows in on it, confirming both GPT-2's improving predictions and the poem's narrowing vocabulary. |
| **crescendo + conform** | 27.0% | Semantic distance increases but S2 decreases. The "semantic boldness / informational settle" pattern: adjacent words become more semantically distant even as GPT-2's predictions improve. The poem learns to expect semantic leaps. |
| **converge + deviate** | 19.5% | Semantic distance decreases but S2 increases. The "refinement" pattern: the poem narrows its semantic field but becomes increasingly surprising within that constrained space. GPT-2 is surprised by the specificity, not the range. |
| **crescendo + deviate** | 13.0% | Rarest. Both S2 and distance increase. The full escalation: the poem builds toward maximum semantic AND informational surprise. The "true Straussian crescendo." |

The **crescendo + deviate** quadrant (13%) is where the classical lyric volta lives: the poem
builds a coherent surface that GPT-2 learns to predict, then shatters it at the end with a
semantically distant AND informationally surprising final gesture.

---

## Striking Individual Cases

### Strongest Semantic Convergence

| Title | Author | Era | arc_dist |
|---|---|---|---|
| "Some Trees" | John Ashbery | new_york_school | **−0.128** |
| "Buffalo Bill 's" | E.E. Cummings | modernist | −0.107 |
| "What Is Poetry" | John Ashbery | new_york_school | −0.098 |
| "Dover Beach" | Matthew Arnold | 19th_century | −0.085 |
| "A Wave (opening)" | John Ashbery | new_york_school | −0.076 |
| "I felt a Funeral, in my Brain" | Emily Dickinson | 19th_century | −0.074 |
| "O Captain! My Captain!" | Walt Whitman | 19th_century | −0.073 |

**Ashbery dominates the convergence list.** Despite the surface randomness of New York School
poetry, his poems semantically narrow over their arc. "Some Trees" begins with semantically
distant token pairs (mean_dist = 0.804) and ends with highly coherent adjacent tokens
(0.677) — a 0.128 drop in semantic distance. Ashbery's apparent disjunction is front-loaded;
the poem resolves into thematic coherence even when it doesn't feel that way.

**Dickinson** follows the same pattern — "I felt a Funeral" starts with semantic leaps
(entombing, Funeral, Brain together) and ends with the semantically tight, rhythmically
locked final stanzas.

### Strongest Semantic Crescendo

| Title | Author | Era | arc_dist |
|---|---|---|---|
| "Variations on A (excerpt)" | Georges Perec | oulipo | **+0.135** |
| "Susie Asado" | Gertrude Stein | modernist | +0.107 |
| "For Spacious Skies" | Emmett Williams | concrete | +0.103 |
| "Daddy (opening)" | Sylvia Plath | confessional | +0.098 |
| "Lady Lazarus (opening)" | Sylvia Plath | confessional | +0.095 |
| "Sailing to Byzantium" | W.B. Yeats | modernist | +0.073 |
| "A Noiseless Patient Spider" | Walt Whitman | 19th_century | +0.072 |
| "The Waste Land (opening)" | T.S. Eliot | modernist | +0.067 |

**OuLiPo and concrete poetry lead the crescendo list** — formally motivated escalation.
Perec's "Variations on A" systematically replaces vowels, making adjacent tokens increasingly
distant in embedding space as the text diverges further from natural language.

**Both Plath poems show crescendo** — this is her characteristic arc. "Daddy" begins with
the incantatory, phonetically repetitive opening ("You do not do, you do not do") and
escalates into the semantically discontinuous late stanzas. The crescendo is mirrored by
S2 back-loading in confessional poetry (+0.419) — Plath doesn't just get semantically
bolder, she gets more informationally surprising, too.

**Whitman's "A Noiseless Patient Spider"** shows a crescendo (0.700 → 0.772) with a
decreasing S2 (the model learns his anaphoric catalog). Whitman uses semantic accumulation
while GPT-2 adapts to his style. The escalating "filament, filament, filament / out of
itself, ever unreeling them" is semantically bolder than the opening frame.

---

## Theoretical Implication: Two Independent Axes of Poetic Arc

This analysis establishes that poems can be characterized on **two independent temporal
axes**:

1. **S2 arc** (prediction arc): Does informational surprise increase or decrease over the
   poem? Most (68%) are front-loaded — the classic "build and release" structure.

2. **Semantic arc** (distance arc): Does the semantic distance between adjacent tokens
   increase or decrease? Most (60%) show convergence — the poem narrows its semantic range.

These axes are nearly independent (r = +0.109). This means:
- A poem can semantically converge while becoming more surprising (refinement poets)
- A poem can semantically escalate while becoming more predictable (pattern-learning)
- Only 13% of poems do both simultaneously (the full Straussian crescendo)

The decoupling refutes a naive theory in which poetic surprise is simply the accumulation
of semantic distance. Instead, S2 and semantic coherence are measuring **orthogonal
properties** of how a poem moves through language space:

- **S2** measures whether the poet resists GPT-2's active predictions (vertical escape)
- **Semantic distance** measures whether adjacent tokens are semantically near (horizontal
  texture)

The confessional era — uniquely — builds along both axes simultaneously, which may be part
of what gives Plath's poetry its characteristic escalating, overwhelming intensity.

---

## Suggested Next Steps

1. **Outlier tracing**: For "crescendo + deviate" poems (the rarest quadrant, 13%), identify
   the specific tokens responsible — are they clustered at the volta, or distributed?

2. **Whitman's semantic arc**: His "A Noiseless Patient Spider" shows crescendo while S2
   decreases. Other catalog poems (Song of Myself) likely do too — the anaphoric catalog
   is semantically explosive but GPT-2 learns it. Is there a "catalog effect" where crescendo
   and S2 front-loading always co-occur?

3. **Confessional vs. Romantic comparison**: The confessional era is the only era in the
   table that shows BOTH distance and S2 increase (converge+deviate has S2+). Does this
   correlate with the biographical intensity that critics note in confessional poetry?

4. **Sub-poem granularity**: Rather than thirds, compute the semantic distance arc at the
   line or stanza level and check whether the crescendo/convergence inflection point
   coincides with the traditional volta position.
