# Onomatopoeia and S₂: Sound-Imitating Words as Straussian Choices

**Date:** 2026-10-28  
**Experiment:** `experiments/onomatopoeia_s2.py` → `results/onomatopoeia_s2.json`  
**Corpus:** 361 English poems; 46 onomatopoeic tokens across 32 poems  
**Lexicon:** 80+ onomatopoeic lemmas with inflected forms (buzz, hiss, crack, murmur, sigh, etc.)

---

## Research Question

Onomatopoeic words — words that sound like what they mean (buzz, hiss, crack, murmur) — are
supposed to be "natural" fits for their referents. But GPT-2 knows only text, not sound.
At positions where a poet deploys onomatopoeia, is the choice predictable or surprising?
And what was the model expecting instead?

**Two competing hypotheses:**

- **Hypothesis A (Iconicity Advantage):** Even in text, readers and LLMs have absorbed
  the association between sound-words and their acoustic context. Prediction: lower-than-average S₂.
- **Hypothesis B (Straussian Oddity):** Onomatopoeic words are rare and concrete when
  the context could be satisfied by something vaguer. Prediction: higher-than-average S₂.

---

## Key Numbers

| Metric | Onomatopoeia (n=46) | Control (n=46,961) | Δ |
|--------|--------------------|--------------------|---|
| Mean S₂ | **2.749** | -0.426 | **+3.175** |
| Median S₂ | **2.269** | -1.193 | **+3.462** |
| % Tokens with Positive S₂ | **65.2%** | 33.5% | **+31.7pp** |
| Mean Rank | **899.8** | 304.6 | **+595** |
| Median Rank | **130.0** | 4.0 | **+126** |

**Result: Hypothesis B is confirmed.** Onomatopoeic tokens are dramatically more surprising
than the corpus baseline. Mean S₂ is 3.2 points higher — a very large effect. The poet's
sonic specificity is, from GPT-2's perspective, a Straussian choice.

---

## Per-Word Breakdown (≥3 occurrences)

| Word | N | Mean S₂ | Mean Rank | Interpretation |
|------|---|---------|-----------|----------------|
| hum | 4 | 10.292 | 1775.2 | Extremely unexpected; context offers no sonic cue |
| tap | 3 | 8.248 | 2142.0 | Precise, unexpected motion-sound |
| thunder | 3 | 2.052 | 809.7 | Contextually motivated but still surprising |
| sigh | 9 | 1.008 | 256.8 | Bimodal: sometimes expected, sometimes not |
| whisper | 3 | 0.306 | 465.3 | Near-zero: accepted by context |
| tapping | 4 | 0.041 | 93.0 | Nearly predicted (repetition context?) |
| boom | 3 | **-4.260** | 1.3 | **Expected: Vachel Lindsay's incantatory repetition** |

The `boom` case is revelatory. In Vachel Lindsay's "The Congo," "boom" is used in
incantatory repetition — and GPT-2, having seen this pattern, ranks "boom" as its
#1 prediction (rank=1, S₂ = -6.11 then -4.02 then -2.65). The onomatopoeic word
has become **habituated** by its context.

---

## What Was GPT-2 Expecting Instead?

At onomatopoeic positions, GPT-2's top alternatives are predominantly **non-sonic**:

| GPT-2's Top Predictions | Count |
|-------------------------|-------|
| [NEWLINE] | 15x |
| , (comma) | 13x |
| the | 9x |
| and | 9x |
| a | 6x |
| **voice** | 5x |
| . (period) | 5x |
| **boom** | 4x |
| are | 4x |
| tears | 3x |

The dominant expectation is **structural** (punctuation, conjunctions) — the model
expects the line to continue grammatically, not acoustically. The poet insists on
the sound word when the grammar expects a pause or a connector.

Notably, "voice" appears 5x — GPT-2 does reach for the semantic field of sound, but
it prefers the abstract noun over the concrete onomatopoeia.

---

## Cross-Onomatopoeia Prediction: 28.3%

At 28.3% of onomatopoeic positions, GPT-2's top-10 alternatives included at least one
other onomatopoeic word. This means GPT-2 has **partial semantic awareness** of the
sound-word category — it knows that a sonic context calls for a sonic word, but it
often gets the specific word wrong (predicting "boom" when the poet writes "crack").

This 28.3% figure suggests onomatopoeia is not a random insertion — it appears in
**sonic contexts** that GPT-2 recognizes as calling for sound vocabulary. Yet even within
that recognized frame, the specific onomatopoeic choice is often surprising.

---

## The "Habituated vs. Virgin" Onomatopoeia Distinction

The most interesting finding is the **bimodal distribution** within onomatopoeia:

**High-S₂ (Virgin) Onomatopoeia** — the word surprises the model:
- `'hum'` (S₂=25.65) by Kamau Brathwaite — dropped into a context where GPT-2 had no sonic expectation
- `'Buzz'` (S₂=15.23) by Emily Dickinson — placed exactly where GPT-2 expected a dash
- `'twitter'` (S₂=8.49) by Keats — GPT-2 expected punctuation; Keats gives a bird-sound

**Low-S₂ (Habituated) Onomatopoeia** — the word is expected:
- `'boom'` (S₂=-6.11) by Vachel Lindsay — the incantation has trained the local context
- `'whisper'` (S₂=-3.39) by Tennyson — in pastoral elegy, "whisper" follows naturally
- `'sigh'` (S₂=-3.27) by Frost — in lyric contexts, "sigh" is the conventional choice

The distinction: **virgin onomatopoeia** exploits its phonetic texture to surprise; **habituated
onomatopoeia** has become a genre convention, predictable by context. Vachel Lindsay's
"Congo" is the extreme case — repeated sonic incantation explicitly trains the model to expect itself.

---

## Era Breakdown

| Era | N | Mean S₂ |
|-----|---|---------|
| 19th_century | 11 | 2.659 |
| romantic | 4 | 2.611 |
| victorian | 4 | 1.214 |
| early_modern | 3 | 0.687 |
| modernist | 5 | **-3.098** |

19th-century and Romantic poets use onomatopoeia more surprisingly. Modernist poets
(largely due to Vachel Lindsay's habituated repetition) show negative mean S₂.
This may reflect Romantic investment in "natural" language reaching beyond convention
into precise sonic specificity.

---

## Most Surprising Onomatopoeic Moments

| Token | S₂ | GPT-2 Expected | Poet | Era |
|-------|-----|----------------|------|-----|
| hum | 25.65 | [NEWLINE] | Kamau Brathwaite | postcolonial |
| Buzz | 15.23 | — | Emily Dickinson | 19th_century |
| tap | 14.05 | dawn | Anonymous | found_poetry |
| Hum | 9.68 | " | Traditional | nursery_rhyme |
| crack | 8.80 | and | Walt Whitman | 19th_century |
| twitter | 8.49 | , | John Keats | romantic |
| buzz | 8.30 | er | Emily Dickinson | 19th_century |
| sigh | 7.78 | be | George Herbert | metaphysical |

Dickinson's two "Buzz" instances (S₂=15.23 and 8.30) are particularly striking —
in "I heard a Fly buzz — when I died," GPT-2 expects structural punctuation at positions
where Dickinson gives the sonic intrusion of the fly. The Straussian gap here is the gap
between death's grammar (dashes, endings) and the fly's insistence.

---

## Theoretical Implications

1. **Onomatopoeia as defiance, not fit**: Against the naive view that onomatopoeic words
   "naturally" belong to their acoustic contexts, the data shows they are Straussian choices.
   The poet's sonic precision surprises a model trained on the same literary corpus.

2. **The iconicity paradox**: Onomatopoeia claims to be the most "natural" language — words
   sounding like reality. But their naturalness lives in the sound-sense relationship, not
   in contextual predictability. GPT-2 knows the context but not the sound, so it cannot
   appreciate the "fit" — and registers only the statistical oddity.

3. **Habituation erases surprise**: When onomatopoeia becomes convention (Tennyson's
   pastoral "whisper," Lindsay's repeated "boom"), it loses its Straussian charge. Genre
   expectation absorbs the sonic specificity.

4. **The 'voice' substitution**: GPT-2 prefers "voice" over specific onomatopoeia 5x —
   the abstract sonic noun over the concrete sound-event. Poetry reverses this preference,
   insisting on the specific over the generic.

---

## Limitations

- Small sample (n=46 onomatopoeic tokens). A larger lexicon or more corpus texts would
  improve reliability of per-word and per-era estimates.
- GPT-2 may have learned some onomatopoeia as multi-word units ("buzz buzz," "boom boom")
  that single-token analysis misses.
- Context window matters: short poems may give onomatopoeia less "priming" than long ones.

---

## Suggested Next Steps

1. **Expand lexicon** — include less canonical sound-words (crinkle, squelch, plop, thwack)
2. **Onomatopoeia clustering** — do multiple onomatopoeic words in the same poem lower each
   other's S₂? (Habituation within a poem)
3. **Compare to other concrete vocabulary** — are non-sonic concrete nouns (stone, blood, eye)
   equally surprising, or is the effect specific to sound-vocabulary?
4. **Phonaesthetic analysis** — within the high-S₂ onomatopoeic positions, do the GPT-2
   alternatives share phonemes with the chosen word? (Would GPT-2 have found "hiss" less
   surprising than "buzz" at the same position?)
5. **Line-position interaction** — do onomatopoeic words at line-final positions have higher
   or lower S₂ than those mid-line? (Rhyme vs. interior deployment)
