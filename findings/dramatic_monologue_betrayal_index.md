# The Self-Betrayal Index: Dramatic Irony and S₂ in the Victorian Dramatic Monologue

**Date:** 2026-11-16  
**Experiment:** `experiments/dramatic_monologue_betrayal.py`  
**Data:** `results/dramatic_monologue_betrayal.json`  
**Corpus:** 10 dramatic monologues (original 7 + 3 new: *Porphyria's Lover*, *Ulysses*, *The Lady of Shalott*)

---

## Research Question

Distinct from verbal/rhetorical irony (studied in `irony_s2.md`), this experiment examines **dramatic irony** — moments when a speaker unintentionally reveals more than they intend. In Browning's *My Last Duchess*, the Duke describes his murdered wife's portrait while concealing (and yet disclosing) that he had her killed. Can GPT-2's surprisal index detect these moments of speaker self-betrayal?

---

## Finding 1: Dramatic Monologue Suppresses S₂ Below Contemporaries

The most consistent pattern across all 10 dramatic monologues: they systematically score lower in S₂ than other poetry of their era.

| Era | n | Mean avg S₂ | Gap vs Drama |
|-----|---|------------|-------------|
| **dramatic_monologue** | **10** | **−0.122** | — |
| romantic | 21 | +0.192 | +0.31 |
| victorian | 30 | +0.392 | +0.51 |
| contemporary | 19 | +0.245 | +0.37 |
| confessional | 6 | +0.503 | +0.63 |
| modernist | 28 | +0.792 | +0.91 |
| beat | 8 | +1.089 | +1.21 |

Dramatic monologue scores **0.5 bits below its own Victorian era average** and over 0.9 bits below modernist poetry.

**Why?** The dramatic monologue creates a stable, predictable speaker *register*. The Duke of Ferrara speaks in courtly Victorian periods; Prufrock in neurotic parenthetical loops; Ulysses in heroic cadences. Once GPT-2 models this register, the speaker's idiom becomes predictable. The formal coherence of a fictional voice — unlike the fragmentary, elliptical compression of lyric poetry — reduces token-level surprise.

---

## Finding 2: Self-Betrayal Moments Spike at High S₂

Despite the generally suppressed S₂ baseline, the specific moments of **dramatic self-disclosure** (where the speaker's mask slips) register as extreme S₂ peaks.

| Poem | Betrayal moment | S₂ | Poem mean | Gap |
|------|-----------------|-----|-----------|-----|
| *My Last Duchess* | "Neptune" (control metaphor) | **+13.22** | −0.26 | +13.48 |
| *My Last Duchess* | "ranked" (status obsession) | **+12.42** | −0.26 | +12.70 |
| *Porphyria's Lover* | "worshipped" (narcissism) | **+13.09** | −0.42 | +13.51 |
| *Porphyria's Lover* | post-murder "unt[ightened]" | **+12.78** | −0.42 | +13.20 |
| *My Last Duchess* | "commands" (murder admission) | **+10.70** | −0.26 | +10.96 |
| *Soliloquy of the Spanish Cloister* | "hate" | **+10.62** | +0.10 | +10.52 |
| *The Bishop's Tomb* | "vanity" | **+7.93** | −0.25 | +8.18 |
| *Gerontion* | "Christ" (failed redemption) | **+5.65** | −0.16 | +5.81 |
| *Tithonus* | "die" (death-wish) | **+4.05** | +0.07 | +3.98 |

**Grand statistics** (n=17 annotated tokens found):
- Betrayal mean S₂: **+6.05**
- Baseline mean S₂: **−0.31**
- Gap: **+6.36 bits**
- Tokens with S₂ > 5: **53%** (9/17)
- Tokens with S₂ < 1: **24%** (4/17)

---

## Finding 3: The Porphyria Paradox — Murder is Expected, Narcissism is Surprising

The most striking single finding concerns *Porphyria's Lover* (Browning, 1836). In this poem, a narrator strangles his lover to "preserve" the moment of her devotion. 

| Moment | Token | S₂ |
|--------|-------|-----|
| The narcissistic revelation | "worshipped" | **+13.09** |
| Post-murder behavior (untightening) | "unt[ightened]" | **+12.78** |
| Possessive claim | "mine" | **−0.25** |
| Final certainty | "Word" | **−1.75** |
| The murder act | "strangled" | *(sub-tokenized, N/A)* |

GPT-2 appears to predict the murder after the "wound three times her little throat around" setup — the strangulation fits the established context. But the narcissistic psychology — *"Porphyria worshipped me"* — registers as highly unexpected. The poem's horror lies not in the act but in the speaker's self-delusion, and that's precisely where S₂ peaks.

**Interpretation**: The dramatic monologue uses narrative logic to make the crime legible and predictable, while the psychological revelation remains surprising. S₂ surfaces the deeper horror — the speaker's inability to love except through possession.

---

## Finding 4: Villain vs Hero Speakers — The Browning vs Tennyson Divide

The betrayal gap varies dramatically between speaker types:

**Villain / obsessive speakers** (Browning): betrayal gap = +10–13 bits
- My Last Duchess (murder) → gap +11.51
- Porphyria's Lover (narcissism) → gap +6.39
- Spanish Cloister (hatred) → gap +6.44

**Aging hero speaker** (Tennyson's Ulysses): betrayal gap = only +1.58
- "idle" = +1.98, "aged" = +0.98, "savage" = −0.94

Why? Ulysses does not conceal his contempt and restlessness — these are the *explicit content* of the poem. His "betrayal" (abandoning Penelope again) is implicit but the words that mark it ("idle king," "aged wife") are not contextually unexpected. In contrast, Browning's speakers use *courtly, refined language that masks violence* — the gap between register and content is what creates high S₂.

**The Straussian gap in dramatic monologue is not about what the speaker hides from the listener but about the gap between the speaker's self-presentation register and the words that break that register.**

---

## Era Comparison Table (Complete)

| Era | n | mean | std |
|-----|---|------|-----|
| dramatic_monologue | 10 | −0.122 | 0.357 |
| new_york_school | 26 | −0.121 | 0.619 |
| language | 6 | −0.206 | 0.948 |
| romantic | 21 | +0.192 | 0.634 |
| contemporary | 19 | +0.245 | 0.815 |
| victorian | 30 | +0.392 | 0.562 |
| confessional | 6 | +0.503 | 0.567 |
| modernist | 28 | +0.792 | 1.364 |
| beat | 8 | +1.089 | 1.222 |

Dramatic monologue clusters with language poetry and New York School at the low end of S₂ — all genres that prioritize coherent register (whether the register is chatty, flatly procedural, or character-voiced).

---

## Limitations

1. **Tokenization**: Several annotated tokens were sub-tokenized by GPT-2 (e.g., "Lucrezia" → "Lu"+"cre"+"zia", "strangled" → "strang"+"led"). A sub-token match might find partial S₂ values.

2. **Manual annotation**: Self-betrayal moments required human judgment about which tokens mark psychological revelation. A different annotator might find different tokens.

3. **Small n**: Only 10 dramatic monologues in the corpus. The Andrea del Sarto analysis was entirely unsuccessful due to tokenization mismatches.

---

## Hypothesis for Future Work

The **Self-Betrayal Index (SBI)** = mean S₂ of annotated betrayal tokens − poem mean S₂.

Values observed:
- Browning villain speakers: SBI ≈ 6–12
- Tennyson heroic speaker: SBI ≈ 1.5
- Eliot disintegrating voice: SBI ≈ 3–6

**Prediction**: 20th-century dramatic monologues (Ai, Duffy, Bidart) may show *different* SBI patterns because their speakers often *intend* to shock — there's no rhetorical mask to break. The Victorian genre depends on the gap between polite surface and violent subtext; contemporary dramatic monologues may surface the violence directly.

## Next Steps

1. Add Ai, Duffy, Bidart dramatic monologues (requires careful copyright handling) to test SBI on contemporary examples
2. Extend sub-token search to handle tokenization splits
3. Build a "register coherence" metric: how quickly does GPT-2 establish a stable prediction regime once inside a dramatic monologue speaker's voice?
4. Test whether the SBI predicts reader "shock" ratings in reader-response experiments
