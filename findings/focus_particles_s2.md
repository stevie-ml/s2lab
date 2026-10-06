# Focus Particles and S2: The Information Funnel

**Date:** 2026-10-06  
**Experiment:** `experiments/focus_particles_s2.py`  
**Data:** `results/focus_particles_s2.json`

---

## What We Investigated

**Focus particles** are small function words that intensify, limit, or focus semantic meaning:
`only`, `even`, `still`, `yet`, `just`, `merely`, `never`, `always`, `ever`, `again`, `once`,
`alone`, `also`, `too`, `so`, `both`, `neither`, `either`, `barely`, `hardly`, etc.

In poetry, these words carry disproportionate weight — Stevens' "the nothing that is",
Rossetti's "yet", Dickinson's "just" — yet they are structurally function words.
The question: does S2 capture this semantic importance?

---

## Key Findings

### 1. The Information Funnel

| Measure | S2 |
|---|---|
| Corpus mean | +0.238 |
| Focus particles themselves | **+2.092** |
| Tokens immediately AFTER focus particles | **−0.593** |

Focus particles are **8.8× above corpus mean S2** — they appear at positions where the
model is surprised. But the tokens following them collapse to **well below** corpus mean.

**Interpretation:** The focus particle "uses up" the surprise budget. The particle itself
signals a semantic pivot, which then constrains what comes next. This is an "information funnel":
high-entropy approach, narrow exit.

### 2. Splitting the Funnel: Some Particles Liberate, Others Constrain

Not all particles function the same way. Post-focus S2 varies dramatically by particle:

| Particle | Post-focus Avg S2 | n | Interpretation |
|---|---|---|---|
| `Only` (line-initial) | +3.285 | 7 | Liberating: sets up a singular restriction, but what fills it is free |
| `never` | +0.352 | 21 | Slightly liberating: infinite negation opens semantic space |
| `Yet` (line-initial) | +0.270 | 10 | Slightly liberating: adversative pivot |
| `ever` | +0.232 | 12 | Liberating: temporal infinity allows any complement |
| `just` | −0.029 | 17 | Neutral |
| `still` (lowercase) | −1.331 | 23 | Constraining: continuative context strongly predicts what follows |
| `only` (lowercase) | −2.008 | 16 | Very constraining: mid-sentence "only" locks in the following NP |
| `once` | −2.238 | 6 | Most constraining: temporal uniqueness strongly signals a narrative completion |

**Key insight:** Capitalization and position matter. Line-initial `Only` liberates (+3.29),
while mid-sentence `only` constrains (−2.01). The same word, depending on whether
it opens a line or completes one, has opposite effects on what the poet can do next.

### 3. Top Poems: Focus Particles as Surprise Engines

| Author | Poem | Era | Focus n | Avg post-S2 |
|---|---|---|---|---|
| Shelley | To a Skylark | romantic | 5 | +4.107 |
| Traditional (Scottish) | The Wife of Usher's Well | ballad | 4 | +3.627 |
| E.E. Cummings | anyone lived in a pretty how town | modernist | 3 | +3.567 |
| Christina Rossetti | Remember | victorian | 4 | +2.982 |
| Amy Lowell | Patterns | imagist | 3 | +2.956 |
| Neruda (trans. Merwin) | Tonight I Can Write | latin_american | 5 | +1.847 |

These poets consistently use focus particles as **launchpads** for surprising completions.
The particle signals "pay attention to this" and then delivers something the model cannot predict.

### 4. Most Striking Individual Moments

These are the highest S2 spikes immediately after a focus particle:

| Post-S2 | Particle → Next word | Poet | Poem |
|---|---|---|---|
| +14.88 | `barely` → `three` | Traditional Scottish ballad | The Wife of Usher's Well |
| +14.00 | `Only` → `whale` | Amy Lowell | Patterns |
| +13.06 | `so` → `floating` | E.E. Cummings | anyone lived in a pretty how town |
| +12.53 | `yet` → `turning` | Christina Rossetti | Remember |
| +11.08 | `just` → `begun` | P.B. Shelley | To a Skylark |
| +10.20 | `just` → `Our` | Emily Dickinson | Because I could not stop for Death |
| +10.01 | `merely` → `silence` | John Ashbery | The Painter |
| +8.73 | `ever` → `sing` | Shelley | To a Skylark |
| +8.15 | `Yet` → `beautiful` | Felicia Hemans | Casabianca |
| +8.08 | `again` → `under` | Neruda | Tonight I Can Write |

**"Only whale"** (Amy Lowell) is particularly striking: after the highly constraining `Only`,
the model would predict a confined, singular noun (a small thing). "whale" violates this —
the biggest possible animal fills the most restrictive slot.

**"merely silence"** (Ashbery) is also remarkable: "merely" minimizes, signals something
trivial follows. "Silence" is semantically enormous. The particle and noun are at maximum
semantic tension.

### 5. By Literary Era

| Era | Avg post-focus S2 | n |
|---|---|---|
| ballad | +1.916 | 7 |
| modernist | +0.463 | 20 |
| latin_american | +0.428 | 11 |
| romantic | −0.349 | 26 |
| victorian | −0.511 | 53 |
| cliche_control | −0.532 | 5 |
| new_york_school | −0.599 | 17 |
| prose_poetry | −0.992 | 21 |
| confessional | −1.784 | 6 |
| contemporary | −2.617 | 8 |

Ballads exploit the liberating type of focus particle most aggressively (+1.92).
Contemporary poetry's focus particles are the most constraining (−2.62) — consistent
with the trend toward conversational, low-surprise registers in recent poetry.

The cliché control texts (−0.53) fall near the middle of poetry eras, suggesting
focus particle usage alone doesn't distinguish cliché from genuine poetry;
what matters is what comes *after* the particle.

---

## A New Taxonomy: Two Types of Focus Particle Use

Based on this data, we can distinguish two deployment strategies:

**Type A — The Pivot Particle** (line-initial, often capitalized: `Only`, `Yet`, `Never`):
Appears at the start of a line or clause, high S2, and what follows is also surprising.
The particle signals an adversative or limiting turn, but the content defies prediction.
→ Found in: ballads, modernist poetry, romantic lyric

**Type B — The Constraint Particle** (mid-sentence: `only`, `still`, `once`, `alone`):
Appears mid-clause, high S2 for the particle itself, but constrains what follows.
The particle's semantic narrowing carries over to the grammatical slot it governs.
→ Found in: contemporary, confessional, prose poetry

---

## Hypothesis

The ratio of Type A to Type B focus particle use may be a diagnostic for poetic register:
elevated, song-like poetry (ballads, romantic odes) prefers Type A; more conversational,
"spoken" poetry (contemporary, confessional) prefers Type B. The information-theoretic
fingerprint of lyric elevation may be recoverable through particle position analysis.

---

## Suggested Next Steps

1. **Annotate particle type**: manually classify each particle instance as Type A or B
   and verify the era correlation holds
2. **Expand the particle list**: include comparative particles (`than`, `as`, `like`) and
   degree adverbs (`very`, `quite`, `rather`)
3. **The "only X" construction**: specifically: when a poet writes "only [noun]", is the
   noun systematically in a high-S2 semantic field (body, nature, silence)?
4. **Cross-linguistic**: do French particles (`seulement`, `même`, `encore`) show the same
   funnel pattern in French poetry analyzed with a French LM?
5. **Temporal tracking**: has the shift from Type A to Type B particles happened
   continuously across literary history, or is it an abrupt transition?
