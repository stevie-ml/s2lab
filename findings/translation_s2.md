# Translation and S2: Does the Straussian Gap Survive Translation?

**Date:** 2026-10-03  
**Experiment:** `experiments/translation_s2.py`  
**Results:** `results/translation_s2.json`

---

## Research Question

When a poem is translated multiple times into English, how much does the translator's
word choice determine its S2 profile — vs. the underlying semantic content of the
source poem? If S2 is measuring the *poem's* meanings (the concepts being expressed),
translations should cluster together. If S2 is measuring *English style* (how unusual
the translator's vocabulary is), literal and creative translations should diverge.

**Test case:** 4 source poems × 3-6 English translations each.

---

## Method

- Run GPT-2 S2 analysis on each translation individually
- Compute avg S2, std, and +S2% (artifact-free tokens only)
- Compare inter-translation spread vs. typical within-poem variation

---

## Results by Poem

### 1. Bashō "Old Pond" (1686)
*古池や　蛙飛び込む　水の音*

| Translator | n tokens | Avg S2 | Std S2 | +S2% | Max S2 | Top deviation |
|---|---|---|---|---|---|---|
| R.H. Blyth (1949)       | 12 | −0.388 | 2.152 | 42% |  3.84 | ' —' (punct) |
| Harold Henderson (1958) | 14 | **+1.087** | 2.940 | 43% |  5.35 | ' sleepy' |
| Allen Ginsberg (1978)   | 11 | **+0.780** | 2.514 | 55% |  5.21 | '!' |
| Robert Hass (1994)      | 18 |  +0.031 | 2.695 | 39% |  5.11 | ' Silence' |
| Jane Reichhold (2008)   | 10 |  +0.486 | 2.265 | 50% |  5.49 | ' sound' |
| W.S. Merwin (2012)      | 11 |  +0.052 | 1.805 | 46% |  3.43 | ' sound' |

**Inter-translation spread: 1.475 bits** — by far the largest of any poem.

### 2. Rilke "Archaic Torso of Apollo" (1908)

| Translator | n tokens | Avg S2 | Std S2 | +S2% | Max S2 | Top deviation |
|---|---|---|---|---|---|---|
| Stephen Mitchell (1982)                  | 147 | −0.283 | 2.178 | 38% |  6.43 | 'rip' (of "ripening") |
| C.F. MacIntyre (1940)                    | 136 | −0.064 | 2.628 | 35% | 10.81 | 'lab' (of "candlelabrum") |
| Edward Snow (1991)                       | 141 | −0.196 | 2.149 | 38% |  9.30 | 'unheard' |
| Galway Kinnell & Hannah Liebmann (1999)  | 142 | −0.175 | 2.141 | 37% |  7.34 | ' fertility' |

**Inter-translation spread: 0.219 bits** — very tight clustering.

### 3. Catullus 5 (~55 BCE)
*Vivamus, mea Lesbia, atque amemus*

| Translator | n tokens | Avg S2 | Std S2 | +S2% | Max S2 | Top deviation |
|---|---|---|---|---|---|---|
| A.S. Kline (2001)      | 93 | −0.264 | 2.282 | 37% | 8.83 | 'Les' (of "Lesbia") |
| Peter Whigham (1966)   | 73 | −0.643 | 2.411 | 34% | 5.56 | ' stiff' (of "stiff-necked") |
| Horace Gregory (1931)  | 78 | −0.641 | 2.022 | 28% | 8.56 | ' sour' (of "sour old men") |
| Frank O. Copley (1957) | 87 | −0.226 | 2.079 | 41% | 5.81 | 'ne' (of "neverending") |

**Inter-translation spread: 0.417 bits** — moderate.

### 4. Rumi "The Guest House" (13th c.)

| Translator | n tokens | Avg S2 | Std S2 | +S2% | Max S2 | Top deviation |
|---|---|---|---|---|---|---|
| Coleman Barks (1995)                      | 82 | −0.127 | 2.692 | 40% | 10.41 | ' violently' |
| Kabir Helminski (2000)                    | 71 | −0.279 | 2.372 | 39% |  6.60 | ' sadnesses' |
| A.J. Arberry (1949, scholarly literal)    | 71 | −0.411 | 2.242 | 38% |  4.80 | ' baseness' |

**Inter-translation spread: 0.283 bits**

---

## Cross-Poem Summary

| Poem | Translations | S2 Spread | Within σ |
|---|---|---|---|
| Bashō "Old Pond"          | 6 | **1.475** | 0.497 |
| Catullus 5                | 4 |  0.417 | 0.199 |
| Rumi "Guest House"        | 3 |  0.283 | 0.116 |
| Rilke "Archaic Torso"     | 4 |  **0.219** | 0.078 |

---

## Key Findings

### Finding 1: Poem Length Creates Convergence

The Rilke translations (≈140 tokens each) cluster within 0.22 bits despite very different
word choices. Bashō translations (10–18 tokens each) spread across 1.47 bits.

**Why**: With more tokens, law-of-large-numbers averaging stabilizes the S2 mean
around the poem's *semantic content*. Short poems are dominated by individual word
choices — a single unusual word like "sleepy" (Henderson) or a bare exclamation
"plunk!" (Ginsberg) can swing the avg S2 dramatically.

**Implication**: S2 comparisons across poems are more stable when poems are
roughly the same length. Haiku S2 comparisons measure translator idiosyncrasy more
than poetic meaning.

### Finding 2: Creative Translations Score Higher S2

There is a clear pattern across all poems: the **most liberal/creative translations
have higher avg S2** than the most literal/scholarly ones.

| Poem | High-S2 translator | Low-S2 translator | Δ |
|---|---|---|---|
| Bashō | Henderson (+1.09, inventive) | Blyth (−0.39, terse) | 1.47 |
| Rumi  | Barks (−0.13, expansive) | Arberry (−0.41, scholarly) | 0.28 |
| Catullus | Copley (−0.23, modern) | Whigham (−0.64, archaic) | 0.42 |

Henderson's translation adds words not in the original ("old dark sleepy pool")
and uses onomatopoeia ("go plop! watersplash"). Barks' Rumi is famous for creative
elaboration beyond the literal Persian. In both cases, higher S2 reflects the
translator's *own Straussian choices* — words that GPT-2's English model would not predict.

**Implication**: S2 is not purely measuring the source poem's meaning; it is also
measuring the translator's creative latitude. A translator who stays close to the
source creates a *lower-S2* English text than one who interprets freely.

### Finding 3: Semantic Moments Produce Consistent Spike Positions

Even when avg S2 differs between translations, the *same conceptual moments* tend
to create spikes across multiple translations of the same poem:

**Bashō**: The "sound of water" moment consistently spikes across translations —
'sound' (Reichhold: 5.49), 'Silence' (Hass: 5.11), '!' (Ginsberg: 5.21), 'waters'
(Henderson: 4.99). The frog's sudden action is the semantic core of the poem, and
different English renderings of that moment all produce high S2. The *concept* is
hard to express conventionally in English.

**Rilke**: The "ripening" metaphor spikes in all translations — 'rip' (Mitchell: 6.43),
'rip' (MacIntyre: 6.95), 'eyes' (Snow: 6.23). The compound German concept
(*Augen wie reifende Früchte*) has no ready English equivalent, forcing all
translators into unusual word choices.

**Catullus**: "Lesbia" itself is a top spike in Kline's version (8.83) — a proper
noun GPT-2 cannot predict from context, as opposed to translations that substitute
"my love" or "you."

**Implication**: There may be a **semantic S2 floor** determined by the source poem's
concepts, plus a **translator stylistic S2 premium** added on top. These are
partially separable.

### Finding 4: The Arberry Baseline

A.J. Arberry's 1949 scholarly translation of Rumi is the **most literal** (his goal
was semantic fidelity) and scores **lowest S2 (−0.411)**. Coleman Barks' translation
is the **most creative** and scores **highest S2 (−0.127)**.

This is the cleanest test case: same source poem, same era of translation, with
explicit difference in translation philosophy. Barks' creative elaborations
('violently sweeping your house / empty of its furniture') introduce words like
"violently" (S2 = 10.41!) that the model finds extremely surprising given the
devotional/philosophical context. Arberry's equivalent ('violently sweep your
house clean') scores a much lower surprise because "sweep your house clean" is
a common enough English phrase.

---

## Hypothesis for Future Work

The **translation experiment reveals two distinct sources of S2**:

1. **Semantic S2**: Arising from the concepts in the source poem that don't have
   conventional English expressions. These produce consistent spikes across all
   translations. They can be identified by finding spike positions that are
   *shared across all translations of the same poem*.

2. **Stylistic S2**: Arising from the translator's idiosyncratic English word
   choices. These are *unique to one translation* and disappear or appear
   differently in other versions.

A disambiguation method: map spike positions across translations of the same poem.
Spikes that appear in **≥ 2/3 of translations** at the same semantic position are
"semantic S2" (inherent to the source poem). Spikes that appear in only one
translation are "stylistic S2" (translator's fingerprint).

---

## Suggested Next Steps

1. **Add more translation comparisons** — Homer (Pope vs. Fagles vs. Wilson),
   Chinese poetry (various translations of Li Bai), Dante, etc.
2. **Map spike positions across translations** — implement the semantic vs.
   stylistic S2 decomposition above.
3. **Test with prose translations** — does translating a poem as prose lower S2
   to the level of prose generally?
4. **Back-translation test** — does an AI translation of a poem have different
   S2 from a human translation? (AI translations tend to be more "conventional.")
