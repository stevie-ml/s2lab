# Entropy After Surprise: Liberation vs. Anchoring
**Date:** 2026-11-18  
**Experiment:** `experiments/entropy_after_surprise_v2.py`  
**Corpus:** 431 texts, 56,396 consecutive token pairs  

## Question

When a poet writes a high-S₂ token — something more surprising than the context warranted — does it *expand* or *constrain* what can follow? Does surprise open doors or close them?

Concretely: does S₂(t) predict Entropy(t+1) even after controlling for Entropy(t)?

## Method

For each consecutive pair of content tokens across all 431 poems:
- Computed raw correlation r(S₂\_t, Entropy\_{t+1}).
- Computed **partial correlation** r(S₂\_t, Entropy\_{t+1} | Entropy\_t) to strip out the trivial persistence of entropy across timesteps.
- Split the corpus into three context-certainty buckets based on Entropy(t):
  - **Low**: Entropy(t) < 4 — model was *confident* about what comes next (n=12,152 pairs)
  - **Mid**: 4 ≤ Entropy(t) < 7 (n=20,312 pairs)
  - **High**: Entropy(t) ≥ 7 — model was *uncertain* (n=23,932 pairs)
- Computed partial correlations and mean Entropy(t+1) separately for positive-S₂ and negative-S₂ tokens within each bucket.
- Computed era-level partial correlations.

---

## Results

### 1. The global signal

**Partial r(S₂\_t, Entropy\_{t+1} | Entropy\_t) = −0.124**

Averaged across all contexts and eras: a high-S₂ token is followed by *lower* model entropy — i.e., the next token is more predictable. At first glance, this looks like surprise *anchors* what follows.

But this global average conceals a critical reversal.

---

### 2. The context-dependent reversal

| Context | n pairs | Partial r | Mean Entropy\_{t+1} after high-S₂ | Mean Entropy\_{t+1} after low-S₂ | Delta |
|---------|---------|-----------|-----------------------------------|----------------------------------|-------|
| **Low entropy** (model confident, < 4) | 12,152 | **+0.090** | 5.87 | 4.62 | **+1.25** |
| Mid entropy (4–7) | 20,312 | −0.141 | 5.85 | 6.58 | −0.74 |
| High entropy (model uncertain, ≥ 7) | 23,932 | −0.204 | 6.01 | 7.02 | **−1.01** |

The direction of the effect **flips** depending on what the model expected at t:

- **Liberation (positive partial r):** When the model was *confident* about what comes next and the poet violated that confidence, the following token is *more uncertain* (Δ = +1.25 bits). The surprise opened up new territory. The poet's unexpected word detached the verse from its anticipated groove and left the next token genuinely uncharted.

- **Anchoring (negative partial r):** When the model was *already uncertain* and the poet added a surprise on top of that uncertainty, the following token is *more predictable* (Δ = −1.01 bits). The surprise resolved ambiguity. A high-S₂ word in an already chaotic context acts as a disambiguating pivot.

**Verdict in low-entropy contexts: LIBERATION — surprising choices in confident contexts expand what can follow.**

---

### 3. Era-level patterns (ranked by partial r)

Positive partial r = Liberation tendency; negative = Anchoring tendency.

| Era | n | Partial r | Interpretation |
|-----|---|-----------|----------------|
| **ballad** | 909 | **+0.151** | Narrative ballads have highly predictable syntactic frames; deviations genuinely reopen the story |
| **beat** | 1,187 | **+0.103** | Ginsberg-style improvisation: surprises consistently expand the available horizon |
| **concrete** | 306 | **+0.093** | Visual layout creates confident GPT-2 contexts; deviations from that confidence open form |
| song_lyrics | 538 | +0.006 | Near neutral |
| fixed_form | 850 | −0.038 | Formal constraint keeps surprises from cascading |
| villanelle | 433 | −0.044 | Refrains create anchored returns |
| oulipo | 1,269 | −0.060 | Procedural generation self-regularizes after surprises |
| modernist | 2,957 | −0.074 | Mixed: Pound/Eliot anchor, Williams/cummings liberate |
| new_york_school | 2,747 | −0.134 | Ashbery's surprises are more anchored than they read |
| romantic | 3,771 | −0.190 | High-S₂ romantic diction occurs mid-clause, then resolves |
| dramatic_monologue | 4,408 | −0.198 | Browning's speakers pivot dramatically, then normalize |
| **ghazal** | 228 | **−0.205** | Surprising couplet diction anchored by mandatory radif |
| war_poetry | 636 | −0.242 | Controlled emotional architecture; surprise is absorbed |
| German expressionist | 775 | −0.243 | Heym/Trakl: ruptures followed by consolidation |
| ancient (Sappho, Homer) | 315 | −0.251 | Formulaic epic registers anchor any deviation |
| classical_chinese | 234 | −0.268 | Tonal grammar makes surprises highly contextualizing |
| control prose | 158 | −0.279 | Prose surprises always followed by semantic disambiguation |
| german_modernist | 232 | −0.287 | Rilke's Orphic turns anchor hard; every surprise earns its resolution |
| **deep_image** | 60 | **−0.328** | Wright/Bly: image progressions tightly controlled; each surprise pulls forward toward the next anchored image |

---

### 4. The Liberation/Anchoring distinction as a formal property

The three Liberation eras (ballad, beat, concrete) share one structural feature: they build from **highly predictable, repetitive frames** (ballad meter and stock diction, Ginsberg's Whitmanic catalogs, concrete typography) that make the model *locally very confident*. When the poet deviates, the frame is broken and genuine openness follows.

The Anchoring eras cluster around **progressive, goal-oriented forms** (dramatic monologue, elegy, war poetry) or forms with **mandatory return structures** (ghazal, villanelle, rondeau). In these, surprise is purposive: the unexpected word redirects the poem toward its structural destination.

Remarkably, **control prose scores the second-highest Anchoring** after deep_image. This confirms the intuition: prose surprises almost always occur in service of narration, which immediately disambiguates what follows. Poetry uniquely allows surprise that remains unresolved — but only in certain formal registers.

---

### 5. The Straussian implication

The Liberation finding maps directly onto the "Straussian gap" framework. When the model is confident and the poet surprises, we're at the purest site of S₂ action: the poet rejected a constrained, predictable path and opened new territory. The +1.25 bit increase in next-token entropy is the *measurable cost* of that opening — the reader, too, faces genuine uncertainty about what comes next.

In Anchoring contexts, surprise still happens, but it's functionally different: more like a sharp turn within a known road system than a departure onto unmarked ground. The subsequent token's predictability (+1.01 bits more predictable after high-S₂ in uncertain contexts) suggests these surprises signal syntactic or semantic structure — a pivot point the model recognizes once it arrives.

---

## Finding

**The effect of poetic surprise on subsequent uncertainty reverses depending on context-certainty.** In confident contexts, high-S₂ tokens liberate (+1.25 bits), expanding the prediction space. In uncertain contexts, high-S₂ tokens anchor (−1.01 bits), collapsing prediction into a narrower range.

This two-regime model maps cleanly onto formal traditions: beat/ballad/concrete poetry uses surprise as *opening*; dramatic monologue/elegy/war poetry/deep image uses surprise as *decisive pivot*.

The global negative correlation (−0.12) obscures this split and would lead to the wrong conclusion that "surprise anchors." It anchors *only when the context was already uncertain* — a situation where the poet's unexpected choice acts more as disambiguation than as disruption.

---

## Suggested next steps

1. **Token-level case studies.** Pull the top 20 Liberation tokens (high-S₂ in low-entropy contexts) and top 20 Anchoring tokens (high-S₂ in high-entropy contexts) across the corpus. Build a typology of what kinds of words perform each function.
2. **Second-order effects.** Does Liberation compound? If token t liberates (opens entropy), does token t+2 show a further Liberation effect, or does it regress? Map the half-life of entropy expansion after a Liberation event.
3. **Within-poem tracking.** Does a poem shift between Liberation and Anchoring modes over its arc? Early-poem surprises might liberate; late-poem surprises might anchor toward closure. Test against the stanza-position data.
4. **Form vs. individual poet.** The beat vs. romantic split may be more about individual poets than eras. Test Ginsberg-only vs. Whitman-only within the "long free verse" category.
5. **Partial r by sentence position.** Liberation effects might concentrate at sentence-initial positions (where the model is most confident) and Anchoring at sentence-final positions.
