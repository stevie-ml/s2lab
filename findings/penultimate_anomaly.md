# The Penultimate Anomaly: The True Last Semantic Choice

**Date:** 2026-10-21  
**Experiment:** `experiments/penultimate_anomaly.py` → `results/penultimate_anomaly.json`  
**Corpus:** 289 English-language poems (≥30 artifact-free tokens)  
**Completes trilogy with:** `findings/opening_salvo.md`, `findings/closing_salvo.md`

---

## Research Question

`closing_salvo.md` (same date) documented the lag profile of the final 15 tokens of a poem and revealed a striking anomaly: lag −1 (the penultimate token) has **S₂ = +0.019** — near zero and dramatically higher than every neighboring position:

| Lag | Mean S₂ | Mean Entropy |
|:---:|:-------:|:------------:|
| 0 (last) | **−1.330** | 4.222 |
| **−1 (penultimate)** | **+0.019** | **6.195** |
| −2 | −1.013 | 6.023 |
| −3 | −0.402 | 6.079 |

The penultimate is the only near-positive position in the entire closing window. Its spike rate (S₂ ≥ 3.0) is 20.1% — higher than any other closing position and comparable to the opening window. Why?

---

## The Structural Explanation: Poems End With Punctuation

The answer is almost completely structural. Examining what types of tokens occupy each position:

### Last-Token Categories (lag 0)
| Category | n | % | Mean S₂ |
|----------|---|---|---------|
| **Punctuation** | 268 | **92.7%** | −1.587 |
| Content word | 16 | 5.5% | +0.867 |
| Empty/artifact | 3 | 1.0% | +10.062 |
| Function word | 2 | 0.7% | −1.584 |

### Penultimate-Token Categories (lag −1)
| Category | n | % | Mean S₂ |
|----------|---|---|---------|
| **Content word** | 254 | **87.9%** | **+0.207** |
| Function word | 30 | 10.4% | −1.760 |
| Punctuation | 3 | 1.0% | +1.973 |
| Capitalized | 1 | 0.3% | −0.186 |

**92.7% of English poems end their artifact-free token stream with punctuation** (period, exclamation point, question mark). GPT-2, having processed the full poem, confidently predicts terminal punctuation after the final content word — and is almost always right. The "last token" is not a semantic choice; it is a graphological convention.

The penultimate token, by contrast, is almost always a **content word** — the actual final semantic decision the poet makes. Content-word penultimate tokens average **S₂ = +0.207** (positive), while punctuation last-tokens average **−1.587**.

**The "penultimate anomaly" resolves: the graphological last token is not the true last token. The penultimate content word is.**

---

## Decomposition: Why Is Penultimate S₂ Higher?

The S₂ elevation at lag −1 is driven by BOTH components of S₂ = surprisal − entropy:

| Position | S₂ | Entropy (H) | Surprisal |
|----------|:--:|:-----------:|:---------:|
| lag 0 (last) | −1.330 | 4.222 | 2.892 |
| **lag −1 (penultimate)** | **+0.019** | **6.195** | **6.214** |
| lag −2 | −1.013 | 6.023 | 5.009 |

Going from last to penultimate:
- **Entropy rises +1.97 bits** — GPT-2 is genuinely less certain about what word precedes the final punctuation than it is about the final punctuation itself
- **Surprisal rises +3.32 bits** — the actual penultimate word is even more unexpected than the raw entropy rise predicts
- **Net S₂ gain: +1.35 units** — the penultimate is the only closing-window position where poet choice meaningfully outpaces model confidence

---

## Two Closing Strategies

The data reveals two distinct patterns for how poems use their final positions:

### Strategy A: Setup → Resolution (pen >> last)
The penultimate delivers a surprising content word; the last token is predictable punctuation. This is the dominant strategy (85%+ of poems).

| Title | Author | Era | Pen Token | Pen S₂ | Last Token | Last S₂ | Gap |
|-------|--------|-----|-----------|:------:|------------|:-------:|:---:|
| Remember | Joy Harjo | postcolonial | ' poems' | +18.06 | '.' | −1.86 | +19.92 |
| Caedmon's Hymn | Caedmon | old_english | ' Almighty' | +13.58 | '.' | −2.14 | +15.73 |
| Susie Asado | Gertrude Stein | modernist | ' jelly' | +8.96 | '.' | −5.37 | +14.32 |
| Dream Song 14 | John Berryman | confessional | ' bored' | +10.45 | '.' | −2.73 | +13.18 |
| Lady Lazarus | Sylvia Plath | confessional | ' linen' | +9.05 | '.' | −3.67 | +12.73 |
| Amoretti LXXV | Edmund Spenser | early_modern | ' likewise' | +10.42 | '.' | −2.23 | +12.65 |
| London | William Blake | romantic | ' Palace' | +10.52 | ' walls' | −2.02 | +12.54 |

**The Straussian gap at the penultimate position is the last moment of true poetic defiance.** The model expects continuations (',' ',' of', 'the') or terminal punctuation ('.'); the poet delivers a semantically dense content word that resolves the poem's meaning before the punctuation arrives.

Notable Straussian gaps:
- Harjo's ' **poems**' — model expected: ','
- Caedmon's ' **Almighty**' — model expected: ' of'
- Shelley's ' **begun**' — model expected: '.'
- Blake's ' **Palace**' — model expected: ' the'
- Berryman's ' **bored**' — model expected: '.'

The "unsaid" at the penultimate is typically grammatical filler or premature punctuation. The poet insists on one more unexpected word.

### Strategy B: Terminal Explosion (last > pen)
A minority of poems place the highest S₂ at the final token — usually because they close WITHOUT punctuation (the final word IS the final token).

| Title | Author | Era | Pen Token | Pen S₂ | Last Token | Last S₂ | Gap |
|-------|--------|-----|-----------|:------:|------------|:-------:|:---:|
| Calypso | Kamau Brathwaite | postcolonial | ' ' | −0.124 | ' **hum**' | +25.66 | −25.78 |
| Constantly Risking Absurdity | Ferlinghetti | beat | ' of' | −2.18 | ' **day**' | +10.69 | −12.86 |
| In After Days (rondeau) | Austin Dobson | fixed_form | ' days' | −3.13 | '!' | +8.41 | −11.54 |
| One Art | Elizabeth Bishop | mid_century | ' master' | −0.26 | '.' | +6.27 | −6.53 |
| Tell all the truth | Emily Dickinson | 19th_century | ' blind' | −4.39 | ' —' | +1.92 | −6.31 |

**Brathwaite's "Calypso"** is the extreme case: the poem ends on ' hum' (S₂ = +25.66) with no punctuation. The terminal explosion is absolute — the whole poem builds toward this single, maximally unexpected word.

**Bishop's "One Art"** is a subtler case: the poem ends on '.' but that period has S₂ = **+6.27** (the 7th percentile of all periods in the corpus). After "the art of losing's not too hard to master," GPT-2 apparently expected a comma or further clause — and the terminal period itself carries surprise.

**Dickinson's "Tell all the truth"** closes on ' —' (em-dash, S₂ = +1.92) rather than a period. For Dickinson, the "last punctuation" is itself unusual — the em-dash suspends resolution rather than providing it.

---

## Predictive Power: Endpoints Don't Define the Poem

| Predictor | r vs. overall S₂ |
|-----------|:----------------:|
| r(penultimate S₂, overall S₂) | 0.077 |
| r(last S₂, overall S₂) | 0.057 |
| r(closing zone S₂, overall S₂) | 0.317 (from closing_salvo.md) |
| r(middle S₂, overall S₂) | **0.907** (from closing_salvo.md) |

Neither endpoint carries significant information about a poem's overall character. The ending is where a poem *arrives*, not where it *lives*. The poem's middle (everything between opening and closing windows) is its true signature.

---

## Most Frequent Penultimate Tokens

The most common "true last semantic words" in the corpus:

| Token | Count |
|-------|:-----:|
| night | 6 |
| me | 5 |
| more | 4 |
| he | 4 |
| air | 2 |
| time | 2 |
| world | 2 |
| again | 2 |
| last | 2 |
| survey | 2 |

**Night, air, time, world** — the canon ends, characteristically, with late-romantic phenomenology: atmospheric nouns that open outward rather than resolve inward. "More" and "again" (cyclical motion words) recur. "Me" and "he" are final anchors of grammatical person.

Compare to last tokens (96%+ punctuation). The "true" last word list looks nothing like a list of periods.

---

## Full Closing Window Profile

Extended to 21 positions to show the penultimate standing alone:

| Lag | S₂ | Entropy | Spike Rate |
|:---:|:--:|:-------:|:----------:|
| 0 (last) | −1.330 | 4.222 | 3.8% |
| **−1 (penultimate)** | **+0.019** | **6.195** | **20.1%** |
| −2 | −1.013 | 6.023 | 10.7% |
| −3 | −0.402 | 6.079 | 12.8% |
| −4 | −0.564 | 6.329 | 15.2% |
| −5 | −0.429 | 6.000 | 14.5% |
| −6 | −0.705 | 5.839 | 12.8% |
| −7 to −20 | −0.33 to −0.92 | 5.9–6.4 | 10–15% |

Lag −1 is the singular anomaly in the closing window. At every other position, S₂ is negative and spike rates are typical or suppressed. The penultimate is the last place where the corpus averages *near-positive* S₂.

---

## Synthesis: The Three-Zone Model, Revised

From this trilogy of experiments (`opening_salvo`, `closing_salvo`, `penultimate_anomaly`), a revised picture of the poem's structural S₂ architecture emerges:

1. **Position 0 (first token)**: structurally incapable of Straussian surprise — entropy 11.14 bits, no model confidence to defeat
2. **Positions 1–8 (opening window)**: spike opportunity zone — GPT-2 forms first confident predictions which poets systematically violate; mean S₂ positive (+0.06 zone average)
3. **Positions 9+ (middle)**: the poem's true voice — settles to mean S₂ ≈ −0.34, but this is where character, style, and the vast majority of spikes live
4. **Lag −1 (penultimate = true last semantic token)**: the final spike opportunity — content word, 20.1% spike rate, mean S₂ ≈ 0
5. **Lag 0 (last = terminal punctuation)**: almost always a period, structurally incapable of surprise — entropy 4.22 bits, fully anticipated

**Poems have two non-surprising structural endpoints and one non-surprising structural terminal** (the last graphological token). Between these, the poet has from position 1 through lag −1 as their "live" surprise zone. The closing salvo finding that "the closing zone is most conformist" is partially an artifact of this terminal punctuation convention — the zone's S₂ average is dragged down by the near-inevitable period at the end.

---

## Suggested Next Steps

1. **Content-word closing study**: analyze only the last *content word* of each poem (not the graphological last token) — this is the true "last semantic position" and likely has a richer distribution than either the penultimate or last token as defined here
2. **Era breakdown of terminal explosion strategy**: which eras are more likely to close without punctuation (terminal explosion)?
3. **Punctuation semantics**: Bishop's period (+6.27), Dickinson's em-dash (+1.92), and Ferlinghetti's unpunctuated ending — a study of how punctuation choice in the final position carries or withholds surprise
4. **The opening/closing asymmetry**: opening exploits entropy rise (GPT-2 unsettled); closing exploits entropy drop (GPT-2 locked in). Does an era's opening advantage predict its closing strategy?
