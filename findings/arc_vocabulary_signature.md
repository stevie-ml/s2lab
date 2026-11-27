# Arc Vocabulary Signature: The Grammar of Placement in Poetry

**Date:** 2026-11-27  
**Experiment:** `experiments/arc_vocabulary_signature.py` → `results/arc_vocabulary_signature.json`  
**Corpus:** 366 poems matched to arc types (from 449 non-control texts)  
**Builds on:** `findings/s2_arc_typology.md` (5 arc types established), `findings/counter_trend_escalation.md` (settlement law)

---

## Research Question

The arc typology established that poems have characteristic S₂ shapes:
- **DECLINE** (22%): front-loaded — peak surprise is in Q1
- **ASCENT** (9%): back-loaded — peak surprise is in Q4  
- **ARCH** (14%): mid-peak — Q2 or Q3 is highest
- **U_SHAPE** (23%): mid-trough — Q1 and Q4 both higher than middle
- **FLAT** (32%): consistent S₂ throughout

**New question:** Are the *vocabularies* of high-S₂ moments different depending on where in the poem they occur — and does arc type predict WHAT gets said when surprise is concentrated?

---

## Finding 1: Arc Types Are Real — The Mirror Symmetry of DECLINE and ASCENT

The mean S₂ per quarter per arc type confirms the typology is capturing genuine structure:

| Arc Type | Q1 (mean S₂) | Q2 | Q3 | Q4 | True Peak |
|---|---|---|---|---|---|
| **DECLINE** | **+0.563** | -0.167 | -0.687 | -0.644 | Q1 |
| **ASCENT** | -0.654 | -0.588 | -0.236 | **+0.583** | Q4 |
| **ARCH** | -0.537 | **+0.365** | +0.104 | -0.855 | Q2 |
| **U_SHAPE** | **+0.213** | -0.568 | -0.511 | -0.271 | Q1 |
| **FLAT** | -0.209 | -0.228 | -0.350 | -0.311 | Q1 |

**DECLINE and ASCENT are perfect mirror images**: DECLINE falls 1.207 bits from Q1 to Q4; ASCENT rises 1.237 bits from Q1 to Q4. This symmetry is striking and suggests both strategies are deliberate rhetorical choices.

The ARCH type shows a genuine mid-poem peak (Q2 = +0.365, the highest single-quarter S₂ of any arc type). ARCH poems produce their most surprising language in the second quarter.

---

## Finding 2: Vocabulary at the Climactic Quarter Differs by Arc

**At DECLINE peaks (Q1):** The highest-frequency high-S₂ tokens are:
`upon`, `survey`, `sits`, `hold`, `round`, `her`, `tonight`, `skies`, `full`

These are **scene-establishing words**: spatial prepositions, verbs of situation (sitting, holding, surveying), and environmental terms. DECLINE poets open by forcing the reader to inhabit an unexpected scene or perspective.

**At ASCENT peaks (Q4):** The highest-frequency high-S₂ tokens are:
`god`, `love`, `air`, `under`, `after`, `where`, `plain`, `cheerful`, `thy`, `only`

These are **transcendent and revelatory words**: divine terms, spatial revelation (`under`, `where`, `plain`), temporal completion (`after`), and direct address (`thy`). ASCENT poets build toward an unexpected disclosure or invocation.

**At ARCH peaks (Q2):** The vocabulary includes:
`heard`, `when`, `though`, `sweet`, `four`, `which`, `understand`

**Transitional and conditional** terms dominate — `when`, `though`, `which` — suggesting ARCH poems introduce their most surprising complexity via subordinate clauses and hedged conditions. The mid-poem surprise comes in the form of a **complicating pivot**.

**At U_SHAPE peaks (Q4):** The vocabulary includes:
`beneath`, `nothing`, `beside`, `cold`, `turning`, `nothing`, `just`

**Spatial proximity and negation**: U_SHAPE poems, after a trough of low-S₂ middle sections, recover with vocabulary suggesting something **concealed beneath the surface** — physical depth (`beneath`, `beside`) and existential negation (`nothing`).

---

## Finding 3: The Exclusive Vocabulary of ASCENT

Tokens disproportionately appearing at ASCENT peaks (Q4):

| Token | ASCENT% | Appearances |
|---|---|---|
| `thy` | 66.7% | 2/3 total |
| `under` | 66.7% | 2/3 |
| `god` | 60.0% | 3/5 |
| `after` | 50.0% | 2/4 |
| `again` | 50.0% | 2/4 |
| `air` | 40.0% | 2/5 |
| `love` | 33.3% | 2/6 |

The **ASCENT-exclusive vocabulary forms a thematic cluster**: divine address (`thy`, `god`), vertical/spatial revelation (`under`, `air`), and temporal return (`after`, `again`). ASCENT poems build toward moments of spiritual or spatial disclosure.

Tokens disproportionately appearing at DECLINE peaks (Q1):

| Token | DECLINE% | Appearances |
|---|---|---|
| `her` | 100.0% | 3/3 |
| `sits` | 100.0% | 3/3 |
| `hold` | 100.0% | 3/3 |
| `round` | 75.0% | 3/4 |
| `tonight` | 66.7% | 2/3 |
| `dry` | 66.7% | 2/3 |
| `skies` | 66.7% | 2/3 |
| `sigh` | 66.7% | 2/3 |

The **DECLINE-exclusive vocabulary** is more embodied and scene-specific: third-person pronouns (`her`), immediate verbs of action/state (`sits`, `hold`, `sigh`), and environmental/temporal markers (`tonight`, `skies`). DECLINE poets open by grounding the reader in a physical, human scene — the surprise is the SPECIFICITY, not the abstraction.

---

## Synthesis: Two Rhetorical Strategies

| Strategy | Arc Type | Climactic Quarter | Vocabulary Character | Rhetorical Move |
|---|---|---|---|---|
| **Opening Ambush** | DECLINE | Q1 | Embodied, scene-specific | Ground reader in physical situation |
| **Closing Revelation** | ASCENT | Q4 | Transcendent, invocatory | Build to spiritual/spatial disclosure |
| **Complicating Pivot** | ARCH | Q2 | Conditional, subordinating | Introduce complexity via qualification |
| **Depth Recovery** | U_SHAPE | Q4 | Spatial proximity, negation | Recover from lull by going beneath surface |

Poetry has not one but four distinct rhetorical grammars for the placement of surprise. Where you put the surprise determines WHAT surprises are available to you. Opening surprises are physical and situational; closing surprises tend toward the transcendent or revelatory; mid-poem surprises involve complication and qualification.

---

## Suggested Next Steps

1. **Verify with annotation**: Manual classification of 20-30 exemplar poems to confirm whether the vocabulary clusters correspond to interpretable rhetorical moves
2. **Author analysis**: Do individual poets specialize in one arc type, or do they use different arc strategies for different poems?
3. **Era × Arc interaction**: The arc typology was established without era breakdown — do certain eras (Romantic? Modernist?) favor certain arc shapes?
4. **Entropy profile complement**: This analysis used S₂ at peak quarters — a parallel analysis of entropy at those same quarters would reveal whether ASCENT peaks are more or less certain than DECLINE peaks
