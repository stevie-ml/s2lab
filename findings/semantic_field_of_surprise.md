# The Semantic Field of Poetic Surprise

**Date:** 2026-09-22  
**Experiment:** `experiments/semantic_field_of_surprise.py`  
**Corpus:** 174 texts (169 poetry, 5 prose controls)  
**Clean high-S2 tokens (S2 ≥ 1.5, stanza-break artifact removed):** 3,402

---

## Research Question

When poets deviate from GPT-2's statistical predictions, what **kinds of words** do they reach for? Previous analyses have shown *that* poets deviate and *how much*, but not *what semantic category* of word tends to appear at moments of maximum surprise.

This experiment filters out the stanza-break artifact (tokens where GPT-2's top prediction was a newline — 16.1% of raw high-S2 tokens) and classifies the remaining 3,402 genuine deviations into semantic fields.

---

## Central Finding: Show Don't Tell, in Information Theory

| Semantic Field | Baseline% | High-S2% | Lift |
|---|---|---|---|
| **COLOR** | 0.66% | 1.12% | **1.69x** ◄ OVER |
| **SOUND_MUSIC** | 0.42% | 0.68% | **1.60x** ◄ OVER |
| MOTION | 0.53% | 0.71% | 1.32x |
| NATURE | 1.30% | 1.41% | 1.08x |
| LIGHT_SACRED | 0.98% | 1.06% | 1.08x |
| DEATH_DARK | 1.42% | 1.47% | 1.03x |
| NUMBER_QUANTITY | 2.25% | 2.18% | 0.97x |
| ABSTRACT_TIME | 2.05% | 1.85% | 0.90x |
| BODY | 1.18% | 1.00% | 0.85x |
| **EMOTION** | 0.64% | 0.50% | **0.78x** ▼ UNDER |

*"Lift" = rate at high-S2 positions / baseline rate across all poetry tokens.*

**COLOR and SOUND words are systematically over-represented at moments of maximum surprise. EMOTION words are systematically under-represented.**

This is the information-theoretic signature of the "show don't tell" principle: when poets are most surprising, they tend to reach for **perceptual** words (what you see and hear) rather than **emotional** labels (what you feel). The surprise is in the sensory — not the sentimental.

---

## What GPT-2 Expected Instead

At the 3,402 clean high-S2 moments, the most commonly suppressed alternatives (what the model predicted but the poet refused) were:

| Token | Count | Category |
|---|---|---|
| 'the' | 338 | function word |
| ',' | 332 | punctuation |
| '.' | 112 | punctuation |
| 'I' | 98 | function word |
| 'of' | 90 | function word |
| 'and' | 86 | function word |
| 'to' | 74 | function word |
| 'a' | 70 | function word |
| 'is' | 61 | function word |
| 'man' | 26 | content word |

**The model almost always expected grammatical infrastructure** — articles, conjunctions, prepositions, punctuation. Poets instead provided sensory content, especially color and sound. The Straussian gap is therefore often a **grammar-vs.-image** gap: where language statistics demand structural scaffolding, poets install a perceptual datum.

The one genuine content word in the top 20 suppressed alternatives is 'man' (26 times). When GPT-2 expected the generic human subject, poets chose something else. This is worth further investigation.

---

## Striking Individual Examples

### COLOR Surprises (lift 1.69x)
- **Sir Patrick Spens** (ballad): `...Sir Patrick'` → chose **'red'** (expected 'Sp', S2=17.95)
- **Lyn Hejinian** (*My Life*): `...'\nA moment'` → chose **'yellow'** (expected ',', S2=14.52)
- **Robert Frost**: poem-opening → chose **'black'** (expected ',', S2=11.55)
- **Philip Larkin**: `...to soundless'` → chose **'dark'** (expected ',', S2=8.40)

At these moments, GPT-2 predicted structural tokens; the poet delivered a color. The color *is* the surprise — not as decoration, but as the one specific sensory datum placed where grammar would install scaffolding.

### SOUND_MUSIC Surprises (lift 1.60x)
- **John Ashbery**: `'...Is merely'` → chose **'silence'** (expected 'a', S2=10.01)
- **Percy Shelley**: `...and soaring ever'` → chose **'sing'** (expected '.', S2=8.73)
- **Philip Larkin**: `...at four to'` → chose **'sound'** (expected 'five', S2=9.38)

The Larkin example is notable: the model expected a number completing "four to five," but Larkin chose "sound" — converting a temporal sequence into a sonic experience.

### EMOTION Surprises (under-represented at 0.78x)
When emotion words *do* appear at high-S2 moments, they tend to be the sharpest, most specific ones:
- **William Blake**: `'Shame is'` → chose **'Pride'** (expected 'the', S2=10.52) — an antonym of Shame where grammar expected the article
- **John Ashbery**: `'...And'` → chose **'envy'** (expected 'I', S2=8.68)
- **Traditional (American)**: `'...ah, I'` → chose **'love'** (expected 'long', S2=10.39)

The under-representation of emotion at high-S2 positions does *not* mean poetry lacks emotion — it means that **naming emotion directly is statistically expected behavior**. The model, trained on text that routinely names feelings, predicts emotional vocabulary. A poem that writes "I love" or "I fear" at the moment where GPT-2 would predict those words isn't surprising; it's confirming the model's expectation. What surprises the model is the perceptual world it didn't see coming.

---

## Era-Level Semantic Field Profiles

*Top fields at high-S2 positions (% of high-S2 tokens classified in each field):*

| Era | COLOR | SOUND | MOTION | NATURE | LIGHT_SACRED | DEATH |
|---|---|---|---|---|---|---|
| **language poetry** | **10.7%** | 0.0% | 3.6% | 0.0% | 7.1% | 3.6% |
| haiku | 0.0% | 0.0% | 0.0% | **5.1%** | 0.0% | **12.8%** |
| confessional | 2.2% | 0.0% | 1.1% | 2.2% | 0.0% | 1.1% |
| beat | 0.0% | 0.0% | 2.1% | 0.0% | 0.0% | 2.1% |
| romantic | 1.6% | 1.3% | 0.5% | 1.8% | **2.3%** | 1.3% |
| surrealist | 0.0% | 0.0% | 0.0% | 0.0% | **10.0%** | 0.0% |
| ancient | 0.0% | **7.1%** | 0.0% | 0.0% | 0.0% | 0.0% |

Notable patterns:
- **Language poetry** (Hejinian, Silliman, Andrews): dominant use of COLOR at high-S2 positions (10.7%). Language poetry's surprise strategy is distinctively *chromatic*.
- **Haiku** emphasizes DEATH at surprise moments (12.8%) — the sudden mortality pivot is information-theoretically encoded.
- **Ancient text** surprises with SOUND (7.1%) — oral/aural surprise in a written tradition.
- **Surrealism** surprises with LIGHT_SACRED (10.0%) — the numinous as the unexpected.

---

## Poet Semantic Surprise Profiles

Selected poets with notable patterns:

| Poet | Top Field | Interpretation |
|---|---|---|
| **William Blake** | COLOR + BODY | Visionary: both what the eye sees and what the body feels |
| **Emily Dickinson** | DEATH_DARK + COLOR | Her famous "slant": the deathward turn with vivid chromatics |
| **Sylvia Plath** | COLOR + BODY | Confessional precision: color before body, sensation before abstraction |
| **Percy Shelley** | ABSTRACT_TIME + NATURE | The abstraction-into-nature trajectory of Romanticism |
| **Walt Whitman** | MOTION + BODY | The democratic body in motion — his catalogues are kinetic |
| **Gerard Manley Hopkins** | ABSTRACT_TIME + LIGHT_SACRED | The theological abstraction behind his sensory violence |
| **Georg Trakl** | LIGHT_SACRED | German Expressionism's luminous violence |
| **Rainer Maria Rilke** | — (no field hits) | His most surprising tokens resist standard semantic categorization — a finding in itself |
| **John Ashbery** | DEATH_DARK + ABSTRACT_TIME | Abstract difficulty with a thematic core of mortality |
| **Thomas Hardy** | NUMBER_QUANTITY + DEATH_DARK | Hardy counts his losses; the mortality arithmetic |

**Rilke's absence from all fields** (73 high-S2 tokens, none matching semantic field lexicons) deserves attention. This likely indicates that Rilke's most surprising tokens are *hapax legomena* or coinages that evade standard word lists — the German-to-English translation challenge creating novel tokens. But it may also suggest a semantic strategy that operates in "the gaps between categories."

---

## Theoretical Implications

### 1. The Sensory Asymmetry Principle
The over-representation of COLOR (1.69x) and SOUND (1.60x) at moments of maximum surprise, combined with the under-representation of EMOTION (0.78x), suggests a fundamental **sensory asymmetry** in how poetic surprise works:

- **Sensory-perceptual language** (color, sound) surprises because it is *specific* — a color names one datum in a space of many possible colors, and that specificity is inherently less predictable than generic structure.
- **Emotional language** (love, fear, grief) does *not* surprise because it is *expected*: emotional naming is the default mode of textual self-expression that GPT-2 has seen often enough to predict routinely.

### 2. The Grammar-Image Gap
The dominant pattern in suppressed alternatives (function words and punctuation) vs. chosen tokens (color, sound, nature) is the grammar-image gap: **at moments where the statistical structure of language calls for grammar, poets deliver image**. This is not merely a stylistic flourish — it is an information-theoretic strategy for maximizing surprise at structural pivot points.

### 3. Sensory Specificity as Surprise Strategy
The color words that appear at high-S2 positions are not generic ("colorful") but specific ("red," "yellow," "black," "dark," "golden"). Specificity, not category, generates surprise. A poem that wrote "the poet used a color word" would not be surprising; the model could predict generic descriptors. What it cannot predict is *which* color, *which* specific sensation.

---

## Next Steps

1. **Extend the lexicon**: Rilke's absence from all categories suggests the need for richer, more fine-grained semantic categorization — perhaps using word embeddings to cluster high-S2 tokens without prespecified categories.
2. **Contrast with prose**: Run the same analysis on the 5 prose controls to see if prose high-S2 moments (fewer and more clustered) show different semantic profiles.
3. **The 'man' puzzle**: GPT-2 expected 'man' 26 times — what did poets choose instead, and what does that tell us about how poetry reimagines the default subject?
4. **Cross-linguistic check**: Do German poems (Rilke, Trakl, George) show the same sensory-surprise asymmetry in German embedding space?
5. **Temporal trajectory**: Does the COLOR lift increase in more recent periods? (Language poetry's 10.7% suggests it might.)
