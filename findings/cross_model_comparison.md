# Cross-Model Comparison: GPT-2 Small vs Medium
**Date:** 2026-09-02  
**Experiment:** `experiments/cross_model_comparison.py`

## Research Question

Does a more capable language model (GPT-2 medium, 345M params) reduce the 'Straussian gap' in poetry — i.e., predict poetic choices better and lower S₂? Or do poets remain equally surprising against a smarter model?

The stakes: if S₂ drops with model size, the effect might be a statistical artifact of underpowered language modeling. If S₂ holds or *increases*, it suggests poets are doing something irreducibly surprising — something that resists even better models.

## Method

Compared GPT-2 small (117M params, `gpt2`) vs GPT-2 medium (345M params, `gpt2-medium`) on 5 poems from the corpus representing different eras and styles. Both models processed identical tokenized inputs; S₂ computed as surprisal − entropy at each token.

## Results

| Poem | Author | Era | S₂ (small) | S₂ (medium) | ΔS₂ | Δsurprisal | Δentropy |
|---|---|---|---:|---:|---:|---:|---:|
| Ode to a Nightingale | Keats | Romantic | -0.363 | -0.076 | **+0.287** | -0.478 | -0.765 |
| Because I could not stop for Death | Dickinson | 19th C. | +0.537 | +0.782 | **+0.245** | -0.020 | -0.265 |
| The Love Song of J. Alfred Prufrock | Eliot | Modernist | -0.209 | -0.129 | **+0.080** | -0.508 | -0.588 |
| The Red Wheelbarrow | Williams | Modernist | +3.594 | +3.375 | **-0.219** | -0.541 | -0.323 |
| Howl (opening) | Ginsberg | Beat | +1.414 | +0.945 | **-0.469** | -0.709 | -0.240 |
| **Aggregate** | | | | | **-0.015** | **-0.451** | **-0.436** |

## Key Finding: The Confidence Trap

The average ΔS₂ across poems is essentially **zero (−0.015 bits)**. The larger model does not substantially reduce the Straussian gap. But *why* is more interesting than *whether*.

**GPT-2 medium reduces both surprisal and entropy, but by nearly identical amounts.** When a better model becomes more confident before each decision (lower entropy), its errors on the poet's actual choices cost exactly as much in S₂ as before.

The deeper pattern: in 3/5 poems (Keats, Dickinson, Eliot), S₂ *increases* with the larger model. This is the **confidence trap**:

> The larger model narrows the probability distribution before each prediction. When the poet then chooses something outside that distribution, the model has committed harder to the wrong answer. The Straussian gap widens.

Formally: `ΔS₂ = Δsurprisal − Δentropy`. When the model's entropy drops faster than surprisal falls, S₂ rises. For Keats: Δentropy = −0.765 vs Δsurprisal = −0.478 → S₂ rises by +0.287.

## The Howl and Red Wheelbarrow Exceptions

Only Ginsberg and Williams show reduced S₂ with the larger model:

- **Howl (Ginsberg):** The medium model better anticipates cataloguing syntax and accumulative list structures (Whitman-style anaphora). Its entropy drops only slightly (−0.24) while surprisal drops substantially (−0.71), meaning it genuinely catches up to Ginsberg's style.

- **The Red Wheelbarrow (Williams):** Still the highest-S₂ poem by a wide margin (3.38 even for medium). The Imagist compression remains maximally surprising regardless of model size.

## Top High-S₂ Tokens (GPT-2 Medium)

| Poem | Token | S₂ | Model expected |
|---|---|---:|---|
| The Red Wheelbarrow | `upon` | +30.58 | newline |
| The Red Wheelbarrow | `bar` | +29.10 | newline |
| The Red Wheelbarrow | `water` | +28.72 | newline |
| Howl | `dr` | +25.83 | newline |
| The Love Song of Prufrock | `When` | +20.50 | newline |
| Ode to a Nightingale | `My` | +18.12 | newline |

**Observation:** The model's most confident wrong prediction is almost always "newline." This reveals a meta-level Straussian gap: **poets systematically continue where language models expect them to stop.** The line break is the canonical expectation; continuation is the suppressed alternative.

## Interpretation

Poets' choices resist scaling. Moving from 117M to 345M parameters does not substantially reduce average S₂, and in the majority of cases *increases* it. This has two implications:

1. **S₂ is not a modeling artifact.** It does not simply measure GPT-2's limitations; it measures something about poetic choice that persists as models improve.

2. **The confidence trap as poetic mechanism.** As language models become more sophisticated, the *cost* of the Straussian gap increases. A smarter model can be wrong more specifically — the poet who violates a high-confidence prediction creates a bigger information shock than the poet who violates a low-confidence one.

This suggests a hypothesis: the most information-dense poetic moments (highest S₂) will remain high-S₂ across model scales, because they exploit the *structure* of language prediction rather than any particular model's blind spots.

## Limitations

- Only 5 poems analyzed (those matching selection criteria in corpus)
- Newline tokenization artifacts dominate top-S₂ lists; filtering these would clarify analysis
- Would benefit from GPT-2 large (774M) and XL (1.5B) to see if the trend holds

## Suggested Next Steps

- **Scaling experiment**: Add GPT-2 large/XL to see if S₂ converges or diverges further
- **Filter newline tokens** from high-S₂ lists to isolate semantic surprises
- **Poem-level clustering**: Do high-S₂ poets (Williams, Ginsberg) cluster differently from negative-S₂ poets (Keats, Eliot) when comparing cross-model behavior?
- **Test hypothesis**: Plot S₂_medium vs S₂_small per token — do the highest-S₂ tokens (top 10% per poem) hold their rank across models?
