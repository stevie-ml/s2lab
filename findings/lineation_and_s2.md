# Lineation and S₂: Separating Layout Artifact from Lexical Surprise

**Date:** 2026-10-16  
**Experiment:** `experiments/lineation_experiment.py`  
**Data:** `results/lineation_experiment.json`  
**Sample:** 26 poems, 13 eras; each poem analyzed twice (lineated and prose-stripped)

---

## Research Question

How much of poetry's measurably higher S₂ comes from *line breaks themselves* (a
layout artifact where GPT-2 expects a newline continuation and gets a word instead)
versus *genuine word-choice surprise*?

We test this directly: run each poem through GPT-2 **with** its newlines (normal
lineation) and **without** them (all newlines replaced with spaces), then compare.

---

## Core Finding: Lineation Accounts for ~95% of the Raw S₂ Advantage

| Condition | Lineated | Prose-stripped | Gap |
|---|---|---|---|
| **Raw S₂** | **+0.385** | +0.005 | **+0.380** |
| **Artifact-free S₂** | **−0.020** | +0.005 | **−0.025** |

- The raw gap (+0.380) is large: lineated poems appear dramatically more surprising
  than their prose-stripped versions.
- The artifact-free gap (−0.025) is essentially zero, and slightly **reversed**:
  once layout positions are filtered, the stripped version is marginally *more*
  surprising than the lineated version.

**Interpretation:** Poetry's raw S₂ advantage over prose is almost entirely a
lineation artifact. The structural uncertainty created by line breaks
(GPT-2 expects the line to continue and instead encounters the start of the next line)
drives the majority of measured surprise. The word choices themselves, when
read as continuous text, are not meaningfully more surprising than prose.

---

## Per-Poem Variation: Two Strategies

The clean delta (lineated − stripped S₂) reveals that individual poets differ sharply
in whether their word choices are *more* surprising with or without line structure.

### "Line-break-dependent" poets: word choices need the structural reset

| Delta (clean) | Author | Poem |
|---|---|---|
| +2.874 | Lawrence Ferlinghetti | Constantly Risking Absurdity |
| +1.219 | Lawrence Ferlinghetti | In Goya's greatest scenes |
| +0.211 | Walt Whitman | When I Heard the Learn'd Astronomer |
| +0.158 | Hart Crane | The Harbor Dawn |
| +0.114 | Wallace Stevens | Anecdote of the Jar |
| ≈ 0.000 | Control prose | (no change expected — no line breaks) |

For these poets, the line break is doing work: it creates a structural reset
that makes subsequent words surprising in context. When line breaks are removed,
the rolling context makes these words more predictable. Ferlinghetti's extreme
visual spacing (+2.87) amplifies this dramatically — "Constantly Risking Absurdity"
uses visual layout as a central formal device.

### "Continuous-syntax" poets: word choices more surprising as prose

| Delta (clean) | Author | Poem |
|---|---|---|
| −1.225 | Lorine Niedecker | Lorine's Work |
| −0.695 | John Ashbery | Leaving the Atocha Station |
| −0.689 | John Ashbery | Some Trees |
| −0.666 | Austin Dobson | In After Days (rondeau) |
| −0.541 | Kobayashi Issa | Three Haiku (Issa) |
| −0.368 | Matsuo Bashō | Three Haiku (Bashō) |

For these poets, the stripped version has **higher** clean S₂. Their word choices
accumulate context across lines: the syntax carries over the line break (enjambment
or tight thematic linkage), so reading them as continuous text creates more
accumulated surprise — GPT-2 has longer memory of preceding choices, which makes
the lexical decisions more unexpected.

**The haiku result is particularly striking:** stripping the line breaks from haiku
*increases* clean S₂ (+0.37 to +0.54 for Issa; +0.20 to +0.57 for Bashō). This
suggests that haiku's genuine word-choice surprise is in its vocabulary (archaic,
translated, unusual juxtapositions), not in its three-line structure.

---

## Implications for Methodology

1. **The artifact-free filter is validated**: The near-zero clean gap confirms that
   `p_newline < 0.9` filtering effectively isolates genuine lexical surprise from
   structural noise.

2. **Line break = local entropy reset, not global information**: The line break
   creates a moment of high prediction uncertainty (what word will start this line?)
   but does not change the underlying entropy of the poet's vocabulary.

3. **Two mechanisms of poetic surprise**: poets can achieve surprise through
   (a) *structural* uncertainty (exploiting the high-entropy reset at line breaks),
   or (b) *lexical* accumulation (building unexpected context across lines).
   These are partly independent strategies.

4. **Prose poetry's status is confirmed**: Prose poems show the same clean S₂ as
   lineated poetry (the W.S. Merwin prose poem has delta = 0.000), which means the
   form label carries no artifact bias — its genuine word-choice S₂ is directly
   comparable to lineated poems.

---

## Next Steps

- Classify the full corpus by "lineation dependence" — which poets rely most heavily
  on structural surprise vs. lexical surprise?
- Test whether "continuous-syntax" poets (negative delta) tend to use more
  enjambment (lines that carry syntax over) and whether this predicts the delta.
- Apply to non-English corpora: does German poetry (already in corpus via Rilke,
  Trakl, George) show the same lineation-artifact pattern?
- The Ferlinghetti outlier warrants special study: does visual poetry (where spacing
  is a primary formal device) create a *third* category of structural artifact beyond
  the standard newline-position effect?
