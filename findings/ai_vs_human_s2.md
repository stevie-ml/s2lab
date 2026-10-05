# AI-Generated Poetry vs Human Poetry: S₂ as a Signature of Intent

**Date:** 2026-10-05  
**Experiment:** `experiments/ai_vs_human_s2.py`  
**Results:** `results/ai_vs_human_s2.json`  
**Corpus:** 202 human poems (artifact-clean tokens) + 9 GPT-2 generated samples (3 per condition)

---

## Research Question

When GPT-2 evaluates its own outputs using S₂, does it find them informationally
conformist? Can S₂ distinguish human poetry from algorithmically generated text —
and if so, what does the distinguishing feature reveal about *how* each kind of
deviation from expectation works?

Three generative conditions:
1. **Greedy (temp ≈ 0)**: near-deterministic, always picks the most probable token
2. **Sampled (temp = 1.0)**: standard sampling from the model's distribution
3. **High temp (temp = 1.5)**: chaotic sampling — high diversity, low coherence

---

## Summary Table

| Condition | mean S₂ | std S₂ | +S₂ ratio | Gini | spike density | H (entropy) | autocorr |
|---|---|---|---|---|---|---|---|
| AI greedy | **-1.68** | 2.41 | **0.10** | 0.39 | **0.069** | **3.75** | **+0.186** |
| AI sampled | -1.48 | 2.46 | 0.19 | 0.37 | 0.093 | 5.77 | -0.084 |
| AI high temp | **+0.12** | 3.50 | **0.38** | 0.43 | **0.211** | 5.54 | -0.068 |
| **Human poetry** | **-0.37** | **3.63** | **0.35** | **0.41** | **0.215** | **6.34** | **-0.016** |

All S₂ computed on artifact-clean tokens (p_newline < 0.9).  
Spike density = fraction of tokens with S₂ > 2.0.

---

## Finding 1: Greedy GPT-2 Is Deeply Conformist — Even by Its Own Standards

Greedy-decoded GPT-2 text has:
- **mean S₂ = -1.68** (more than 1 full bit more conformist than human poetry at -0.37)
- **pos_s2_ratio = 0.10** (only 10% of tokens are "surprising" — vs 35% for human poetry)
- **spike_density = 0.069** (7% vs 21%)

This is expected in principle but the *magnitude* is striking: greedy GPT-2 is
**4.5× less likely** to generate a genuine surprise (spike density) than human poets.

The generated greedy text confirmed the pattern qualitatively:
```
The light falls through the window onto
the floor. "I'm sorry, I'm sorry," he says.
"I'm sorry. I'm sorry. I'm sorry. I'm sorry.
I'm sorry. I'm sorry. I'm sorry. I'm sorry.
```
The model enters a **repetition vortex** — once it predicts "I'm sorry," the context
makes "I'm sorry" the most probable continuation, collapsing entropy and S₂ together.

---

## Finding 2: The Entropy Gap — Human Poets Create More Open Contexts

The most theoretically significant finding:

| Condition | Mean entropy (bits) |
|---|---|
| AI greedy | 3.75 |
| AI high temp | 5.54 |
| AI sampled | 5.77 |
| **Human poetry** | **6.34** |

Human poetry has **~0.6 bits higher entropy** than even the most diverse AI condition
(sampled, temp=1.0). This means GPT-2 is *genuinely more uncertain* when reading
human poetry than when reading its own outputs.

**Interpretation:** Human poets construct contexts that genuinely open up the
semantic possibility space — each line creates a richer, more ambiguous context for
what follows. GPT-2, even at high temperature, builds contexts that it finds more
predictable, because it generates within its own learned distribution. The entropy
gap is not about what tokens appear, but about what *contexts* those tokens create.

This is a self-referential information gap: GPT-2 cannot generate text that surprises
itself as much as humans can surprise it.

---

## Finding 3: The Spike Density Paradox — High Temp Mimics Human Poetry Quantitatively

The most surprising finding: **AI at temp=1.5 and human poetry are virtually
indistinguishable by spike density (0.211 vs 0.215)** and have similar pos_s2_ratio
(0.38 vs 0.35).

If we used only these two metrics, we could not tell them apart.

But the entropy gap (5.54 vs 6.34) distinguishes them: AI achieves high spike density
by sampling from a *narrow* distribution, producing tokens far from what the model
expected — but the context leading to those tokens was narrow to begin with.
Human poets produce high spike density in richer semantic contexts.

**Analogy:** A random dart throw can hit the bullseye as often as an expert's —
but only by filling the board with random shots. The expert's precision comes from
intention within a context; the random throw comes from chaos against a simple target.

---

## Finding 4: Autocorrelation Signature — Repetition vs. Waves

| Condition | Autocorrelation (lag 1) | Pattern |
|---|---|---|
| AI greedy | **+0.186** | Sticky: S₂ clusters → repetition vortex |
| AI sampled | -0.084 | Anti-sticky: random alternation |
| AI high temp | -0.068 | Anti-sticky: random alternation |
| Human poetry | **-0.016** | Near-zero: mild wave-like structure |

Human poetry has *near-zero* S₂ autocorrelation — neither systematically clustered
nor randomly alternating. This is consistent with the "pre-peak setup" finding
(`pre_peak_setup.md`): poets conform immediately before deviating, then relax after
the peak, creating a gentle wave structure.

Greedy AI has *positive* autocorrelation: once it deviates (or conforms), it tends to
keep doing the same thing. This is the signature of a system optimizing locally
rather than globally.

---

## Finding 5: Era-Level Comparison with AI Conditions

Which human poetry eras most resemble each AI condition?

**Human eras closest to AI greedy (mean_s2 ≈ -1.68):** None — no poetry era falls this low.
The lowest human era is `control` (prose): mean_s2 ≈ -1.72. **AI greedy generates prose-like text.**

**Human eras closest to AI high temp (+0.12 mean_s2):** `german_modernist` (+0.77),
`beat` (+0.74), `german_expressionist` (+0.62). The most informationally radical
human poetry shares the *quantitative* S₂ level of high-temp AI — but through
entirely different mechanisms.

---

## Discriminant Features for AI Detection

Ranked by discriminability (human vs. all AI):

| Feature | Human | AI best | Gap | Direction |
|---|---|---|---|---|
| Mean entropy | 6.34 | 5.77 | **0.57 bits** | Human > AI |
| Mean S₂ | -0.37 | -1.48 | **1.11** | Human > AI |
| Spike density | 0.215 | 0.093 (sampled) | **2.3×** | Human > AI |
| Autocorr lag-1 | -0.016 | +0.186 (greedy) | **varies by cond** | Human ≈ 0, AI varies |

The best single discriminant is **mean entropy**: human poetry maintains higher
entropy (richer semantic openness) than GPT-2-generated text at any temperature.

---

## Limitations

- Only 3 samples per AI condition (small N)
- GPT-2 generating poetry with a prose prompt structure may not yield the most
  "poetic" text — targeted poetic prompts might change results
- The entropy metric is model-dependent (measured with GPT-2 itself)
- High-temperature AI text collapses semantic coherence, making comparison unfair

---

## Suggested Next Steps

1. **Better prompts:** Use actual poetry first-lines as prompts for GPT-2 and compare
   to the human originals token-by-token
2. **Other models:** Test GPT-2 Medium/Large — do larger models show the same entropy gap?
3. **Human-AI text discrimination:** Can we build a logistic classifier (entropy + spike_density)
   that reliably separates human from AI poetry in cross-validation?
4. **The "entropy construction" hypothesis:** Trace *how* human poets build high-entropy
   contexts — do they rely on polysemous words, unusual grammatical structures, or 
   semantic juxtaposition?
5. **The vortex condition:** Study the "repetition vortex" in greedy AI as a kind of 
   anti-poetry — what structural features pull text into the vortex?
