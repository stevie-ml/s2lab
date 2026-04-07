# Active vs Passive Voice: The Information Trade-Off
**Date:** 2026-04-06
**Experiment:** `experiments/voice_experiment.py`

## Question
Do active and passive voice constructions produce different S₂ profiles? Can information theory reveal *why* poets choose one voice over the other?

## Method
8 matched active/passive sentence pairs analyzed with GPT-2, including poetic constructions from Dickinson and Stevens.

## Results

| Voice | Avg Surprisal | Avg Entropy | Avg S₂ | +S₂ Ratio |
|---|---|---|---|---|
| Active | 7.75 | 7.56 | **+0.19** | 41% |
| Passive | 6.83 | 7.41 | **-0.58** | 33% |
| Δ (passive - active) | -0.92 | -0.15 | **-0.77** | -8% |

Passive S₂ > Active S₂ in only 3/8 pairs.

## Key Finding: Passive voice trades surprise for agent-suppression

Passive voice is **more predictable** overall (lower S₂) because the "was/were + past participle + by" construction is highly formulaic — GPT-2 can predict it easily once it starts. But this predictability is the *mechanism* by which passive voice hides the actor.

### Case study: Dickinson's "Death kindly stopped for me"

**Active:** "Death kindly stopped for me"
- "kindly" → S₂ = 8.47 (massive spike — Death being kind is maximally unexpected)
- Surprise is front-loaded with the agent

**Passive:** "I was kindly stopped by Death"
- "was" → S₂ = -4.98 (very predictable — passive formula kicks in)
- "kindly" → S₂ = 7.18 (still high but reduced)
- "by" → S₂ = -2.20 (formulaic connector)
- "Death" → S₂ = **7.51** (agent revealed — surprise detonates at the end)

### The mechanism

Passive voice creates a **low-entropy channel** (the "was...by..." scaffold) that is highly predictable, but it **defers the surprise to the agent position**. The actor — the *who* — becomes the Straussian "unsaid," held back and revealed at the end where it carries maximum impact.

## Interpretation for poetic technique

Poets can use voice as an information-management strategy:
- **Active voice** = front-load the agent, distribute surprise across the sentence
- **Passive voice** = suppress the agent, create a predictable channel, then **detonate the actor at the end**

This is a form of Straussian writing: passive voice literally performs the act of hiding — the "unsaid" is the agent itself.

## Next steps
- Test this on actual poems that switch between active and passive within the same text
- Analyze Dickinson's full corpus for voice-switching patterns
- Compare with bureaucratic/academic passive (where agent-suppression serves a different purpose)
- Look at whether poets who use more passive voice have different overall S₂ signatures
