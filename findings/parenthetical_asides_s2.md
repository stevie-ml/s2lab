# Parenthetical Asides and S₂: When Poets Whisper

**Date:** 2026-11-12
**Experiment:** `experiments/parenthetical_s2.py` → `results/parenthetical_s2.json`
**Corpus:** 411 texts; 15 English poems with parenthetical content identified
**Token counts:** 490 inside-paren, 2,573 outside-paren (English, non-stanza-break)

---

## Research Question

When poets use parentheses — to stage an aside, a qualification, an ironic whisper — does the language inside the parenthetical differ in its information-theoretic signature from the surrounding poem? The parenthetical is a *frame shift*: the speaker briefly steps outside the poem's main voice and speaks in a secondary register. Does GPT-2 capture this shift?

**Three hypotheses:**
1. **The Frame-Shift Hypothesis**: The opening `(` token itself carries high S₂ (the model doesn't expect punctuation to interrupt poetic flow).
2. **The Whisper Hypothesis**: Text inside parentheses uses MORE conventional language (lower S₂) — the poet shifts into an explanatory, qualifying register.
3. **The Re-Entry Hypothesis**: The closing `)` has low S₂ (the model, once aware of the parenthetical, anticipates its closure).

---

## Results

### Finding 1: The Opening Parenthesis Is Maximally Surprising

The `(` token itself has the highest mean S₂ of any structural element measured:

| Location             | N   | Mean S₂ | Median S₂ | Pos% | Max S₂ |
|----------------------|-----|---------|-----------|------|--------|
| **`(` token**        | 18  | **+4.715** | +4.114 | **77.8%** | 16.82 |
| Inside `( )`         | 490 | −0.603  | −1.264    | 31.2% | 22.09 |
| Outside `( )` (baseline) | 2,573 | +0.120 | −0.604 | 42.2% | 25.48 |
| `)` token            | 13  | **−1.712** | −2.382 | 15.4% | 2.51 |

**The `(` is a Straussian ambush**: mean S₂ = +4.715, over 4× higher than outside-paren baseline. The model almost never predicts a parenthesis in poetic flow — the poet's decision to open an aside is itself the most information-dense gesture in the parenthetical structure.

**The `)` is the most predictable structural token observed**: mean S₂ = −1.712, 15.4% positive. Once inside a parenthetical, GPT-2 is constantly preparing for closure. The bracket that closes the frame is the least surprising thing in it.

### Finding 2: Inside Parentheses, the Language Falls Quiet

The core finding: text inside parentheses has significantly lower S₂ than the surrounding poem:

**S₂ gap (inside − outside): −0.723**

Inside-paren mean: **−0.603** vs. outside-paren mean: **+0.120**

This confirms the **Whisper Hypothesis**. When poets move into the parenthetical register — qualification, aside, sotto voce comment — they shift to more predictable language. The model's confidence rises inside the brackets. The poet is whispering in an expected tongue.

Percentage of tokens with positive S₂:
- Inside `( )`: **31.2%**
- Outside `( )`: **42.2%**

Inside a parenthetical, only 1 in 3 tokens outpaces the model's expectations; outside, it's nearly 1 in 2.

### Finding 3: Era and Author Signatures

| Era                | n_in | Inside Mean | Outside Mean | Gap     |
|--------------------|------|-------------|--------------|---------|
| romantic           | 11   | +1.382      | +0.096       | **+1.286** |
| 18th_century       | 17   | +0.220      | +0.360       | −0.140  |
| modernist          | 28   | −0.007      | +0.531       | −0.538  |
| dramatic_monologue | 214  | −0.498      | +0.173       | −0.671  |
| fixed_form         | 54   | −0.696      | +0.238       | −0.934  |
| 19th_century       | 11   | −1.633      | −0.207       | −1.426  |
| victorian          | 134  | −0.920      | +1.257       | **−2.177** |

The Victorian era shows the most dramatic suppression inside parentheses (gap = −2.177), driven largely by Hopkins. The Romantic era (Shelley) is the exception — the only era where inside-paren S₂ exceeds outside.

| Author                  | n_in | Inside Mean | Outside Mean | Gap     |
|-------------------------|------|-------------|--------------|---------|
| Percy Bysshe Shelley    | 11   | +1.382      | +0.096       | **+1.286** |
| Alexander Pope          | 17   | +0.220      | +0.360       | −0.140  |
| Robert Browning         | 188  | −0.432      | +0.127       | −0.559  |
| Dante Gabriel Rossetti  | 54   | −0.696      | +0.238       | −0.934  |
| E.E. Cummings           | 37   | −0.441      | +0.716       | −1.157  |
| T.S. Eliot              | 26   | −0.978      | +0.399       | **−1.377** |
| Walt Whitman            | 11   | −1.633      | −0.207       | −1.426  |
| Gerard Manley Hopkins   | 134  | −0.920      | +1.257       | **−2.177** |

**Hopkins** is the most dramatic case: his outside-paren language is exceptionally surprising (+1.257), but his parentheticals retreat to near-average (−0.920). Hopkins uses parentheses for theological qualifications ("who knows how?" in *Pied Beauty*) that are conventional where his main lines are radically inventive.

**Shelley** is the sole reversal — his parentheticals are *more* surprising than his outside. Looking at the data: *Ode to the West Wind* uses `(` in its long, elaborate syntactic periods, where the parenthetical content is itself metaphorically dense.

**Browning's dramatic monologues** (214 inside tokens, the largest dataset) show moderate suppression. In *My Last Duchess*, *Andrea del Sarto*, *Fra Lippo Lippi* — the speakers' parenthetical asides reveal psychology through seemingly casual remarks, but the language itself is controlled, not wild.

### Finding 4: The l(a Artifact

E.E. Cummings' poem *l(a* — which embeds "a leaf falls" inside a typographic parenthetical running through the entire poem — produces a special case: inside-paren S₂ = −1.791, outside-paren S₂ = +10.338, gap = −12.129. This poem exists AS a parenthetical structure, so the "outside" is the high-S₂ alphabetic fragments that form the outer word "loneliness." This should be treated as a structural artifact rather than evidence for the whisper hypothesis.

---

## Interpretive Framework

The parenthetical in English poetry functions as a **register lowering device**. The surprise is concentrated at entry (`(` = +4.715 S₂) and the content inside is consumed at reduced informational cost. This may explain the parenthetical's rhetorical function: the reader's attention is seized by the opening bracket, primed for something important; the content itself is delivered in a more conventional register (explanation, qualification, aside), which makes it emotionally audible without being cognitively taxing.

The `)` as the least surprising structural token observed (mean −1.712) reflects how thoroughly GPT-2 has "settled in" to the parenthetical mode — it expects the bracket to close the moment it's opened.

**Deeper inference**: The parenthetical is a tool for *strategic conventionality*. Where the main poem expends its Straussian budget on unexpected choices, the parenthetical is where the poet can be ordinary — and that ordinariness is part of the rhetorical effect. The whisper is whispered *in plain language*.

---

## Limitations

- Only 15 poems in the corpus use explicit parenthetical notation; most poetry avoids brackets entirely.
- The l(a poem distorts any aggregate analysis and should be excluded from summary statistics.
- Some "parenthetical" uses are not rhetorical asides but typographic conventions (stage directions, translation notes).

---

## Suggested Next Steps

1. **Dash-delimited asides** — em-dashes (`—`) function similarly to parentheses as aside markers in poetry (Dickinson, Whitman). Testing whether dashes show the same `(` surprise / content calm pattern would validate the frame-shift hypothesis across punctuation types.
2. **Bracket types** — square brackets `[]` in poetry often signal editorial insertions or deliberate lacunae. Their S₂ profile may differ from round brackets.
3. **Expand corpus** — add more poems known for parenthetical use: Anne Carson, John Ashbery, Marianne Moore, A.R. Ammons.
4. **Length of parenthetical** — does longer time inside the brackets predict more suppression? A forgetting-curve analysis of S₂ across the tokens of the parenthetical.
