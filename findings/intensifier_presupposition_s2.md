# Intensifiers and Presupposition Triggers: S2 Signature of Semantic Setup

**Date:** 2026-10-31  
**Corpus:** 381 texts (195 intensifier tokens, 260 presupposition triggers)  
**Model:** GPT-2 (117M)

---

## Research Question

Do degree adverbs (intensifiers: *very, so, utterly, barely…*) and presupposition triggers (*again, still, even, already…*) create distinctive S2 signatures? Specifically:

1. Are these words themselves surprising (high self-S2)?
2. Do they make the following token more or less surprising?

The hypothesis: these "setup" words in poetry might absorb S2 budget themselves, reducing predictability of what follows — or alternatively act as context-narrowers that make subsequent content more constrained.

---

## Key Results

### Baseline
- Corpus mean S2: **–0.284** (most tokens are predicted better than context warrants)

### Intensifiers (self vs. next)

| Metric | Value | vs. Baseline |
|--------|-------|-------------|
| Intensifier self-S2 | **+0.639** | +0.92 above baseline |
| Next token after intensifier | **–0.424** | –0.14 below baseline |

**Finding:** Intensifiers are themselves mildly surprising (they appear when the model is confident about something else), but they **reduce what follows** — the word they intensify becomes MORE predictable, not less.

### Presupposition Triggers (self vs. next)

| Metric | Value | vs. Baseline |
|--------|-------|-------------|
| Presupposition self-S2 | **+1.194** | +1.48 above baseline |
| Next token after presupposition | **–0.767** | –0.48 below baseline |

**Finding:** Presupposition triggers show a **stronger version of the same pattern** — they are considerably more surprising than intensifiers (the model didn't predict "again" or "even"), and they even more powerfully constrain what follows.

---

## Breakdown by Individual Trigger

### Presupposition Triggers (sorted by self-S2)

| Token | n | Self S2 | Next S2 |
|-------|---|---------|---------|
| *already* | 4 | +4.66 | –1.98 |
| *even* | 24 | +2.28 | –0.73 |
| *again* | 33 | +1.86 | –0.58 |
| *too* | 42 | +1.91 | –0.93 |
| *also* | 15 | +1.49 | –0.53 |
| *still* | 45 | +1.22 | –0.82 |
| *once* | 24 | +1.19 | –0.58 |
| *yet* | 31 | +0.14 | –0.62 |
| *another* | 7 | +0.18 | –1.40 |
| *back* | 25 | –0.40 | –0.55 |

**Note:** "already" and "even" show the sharpest contrast — the trigger is highly surprising, but the following word is deeply predictable. This is the **presupposition paradox**: the word signals existing shared knowledge (implying the content is given), making that content more constrainted.

### Intensifiers by Frequency

| Token | n | Self S2 |
|-------|---|---------|
| *so* | 92 | –0.71 |
| *just* | 32 | +1.80 |
| *only* | 29 | –0.10 |
| *merely* | 3 | +3.34 |
| *somewhat* | 2 | +9.29 |
| *scarcely* | 2 | +7.52 |
| *quite* | 2 | +3.81 |
| *perfectly* | 2 | +6.02 |
| *barely* | 3 | +1.97 |
| *rather* | 3 | +1.95 |

**"So" is predicted by context** (self-S2 = –0.71) — it's the default intensifier. But rare intensifiers (*somewhat, scarcely, perfectly, merely*) carry VERY high S2. When a poet writes "somewhat" or "scarcely," GPT-2 is genuinely startled.

---

## Best Examples: Intensifier → Surprising Next Token

| Era | Author | Sequence | Next S2 |
|-----|--------|----------|---------|
| ballad | Traditional | *barely* → "three" | +14.88 |
| modernist | E.E. Cummings | *so* → "floating" | +13.06 |
| romantic | Shelley | *just* → "begun" | +11.08 |
| 19th_century | Emily Dickinson | *just* → "Our" | +10.20 |
| new_york_school | John Ashbery | *merely* → "silence" | +10.01 |
| 18th_century | Alexander Pope | *just* → "alike" | +8.67 |
| contemporary | Joy Harjo | *only* → "beauty" | +7.04 |
| war_poetry | Rupert Brooke | *only* → "this" | +7.03 |
| early_modern | Robert Frost | *so* → "last" | +5.65 |

These outliers suggest that when intensifiers DO precede high-S2 content, the effect is dramatic — the intensifier creates a tonal signal ("this matters"), and then the content violates expectations.

---

## Era-Level Intensifier Density (per 100 tokens)

Eras with HIGHEST intensifier use:
1. **japanese_classical**: 1.79/100 tokens
2. **song_lyrics**: 1.60/100
3. **clerihew**: 1.28/100
4. **parody**: 1.19/100
5. **korean_modernist**: 1.16/100

Eras with LOWEST use would include imagist, concrete, and haiku forms (which tend to avoid intensifiers on aesthetic grounds — "show, don't tell").

---

## Interpretation: The "Semantic Sponge" Pattern

Both intensifiers and presupposition triggers share a structure:

**[Surprising Setup Word] → [Predictable Payload]**

This is the **semantic sponge**: the setup word absorbs information-theoretic surprise itself, while narrowing the context for what follows. In presupposition triggers, this makes linguistic sense — "again" tells you you're in a repeated event, constraining the content. In intensifiers, the mechanism is subtler: "so floating" (Cummings) uses "so" as familiar/predicted scaffolding before the deviant adjective.

The high S2 on rare intensifiers (*somewhat, scarcely, merely*) suggests poets use these as **double-signal words**: they are surprising in form AND they signal that the following content is noteworthy. The word earns attention before spending it.

---

## Hypothesis for Follow-Up

**The "sponge-then-spring" structure:** Examine 3-token windows [setup → peak → landing]. Do high-S2 tokens that follow intensifiers tend to be followed by low-S2 resolution tokens? This would reveal a micro-arc: [expected] → [setup] → [surprise] → [return to ground].

Also worth testing: **intensifiers in formal vs. free verse** — do metered poems show lower intensifier density than free verse? Fixed form might substitute the meter itself as the expectation-setter.

---

## Suggested Next Steps
1. Run the "sponge-then-spring" tri-gram analysis on the full corpus
2. Compare intensifier density in prose poetry vs. free verse vs. formal verse
3. Track "even" specifically — it has the most poetic significance among presupposition triggers (climax particle, "even death")
4. Look at intensifier avoidance as a style marker: poets who write the least intensifier-heavy verse
