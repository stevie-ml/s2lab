# Syntactic Prediction Diversity and Poetic Surprise

**Date:** 2026-11-04  
**Experiment:** `experiments/prediction_diversity_s2.py` → `results/prediction_diversity_s2.json`  
**Corpus:** 403 English poems, 51,940 artifact-free tokens  
**Research question:** Does the syntactic diversity of GPT-2's prediction space predict when poets make surprising choices?

---

## Background

Previous work established *what* poets choose at high-S2 moments (semantic fields, POS, rank distance) and *when* those moments tend to come (pre-peak setup, stanza structure). This experiment asks something different: **does the shape of the possibility space matter?**

For each artifact-free token, we classified GPT-2's top-10 alternatives by broad syntactic category (punct, func, num, noun_like, verb_like, adj_like, adv_like). "Diversity" = count of distinct syntactic categories present among the top-10 alternatives.

- **Diversity 1** = syntactically narrow: all alternatives are the same type (e.g., all punctuation, or all nouns)
- **Diversity 2–3** = mixed: alternatives span a couple of types (most common)
- **Diversity 4+** = syntactically wide: alternatives span four or more types

---

## Finding 1: The Null — Poetic Surprise Is Syntactically Agnostic

| S2 Bin | n | Mean Diversity | Median | 1-category% | 4+category% |
|---|---|---|---|---|---|
| Very low (<-3) | 12,210 | 2.246 | 2.0 | 16.8% | 4.0% |
| Low (-3 to -1) | 15,119 | 2.273 | 2.0 | 13.7% | 3.7% |
| Neutral (-1 to 1) | 10,847 | 2.233 | 2.0 | 16.5% | 4.6% |
| High (1 to 3) | 5,597 | 2.226 | 2.0 | 17.6% | 4.0% |
| **Very high (>3)** | 8,167 | **2.257** | **2.0** | **15.6%** | **4.3%** |

**The mean diversity is essentially flat across all S2 bins** (range: 2.226–2.273, a spread of 0.047 across the entire S2 spectrum). Whether a poet makes a low, moderate, or extreme surprise is completely uncorrelated with whether the prediction space was syntactically narrow or wide.

This is a **null finding with theoretical significance**: poetic surprise is not a byproduct of syntactic ambiguity. Poets do not mainly surprise us by being in contexts where "anything could come next." They impose surprise from within contexts that are just as constrained as ordinary conformist positions.

---

## Finding 2: Two Types of Surprise, Correlated with Era

While the aggregate null holds, era-level variation reveals two distinct "surprise architectures":

### Eras Surprising in Syntactically WIDER Contexts (high-S2 div > baseline div)

| Era | Baseline Div | High-S2 Div | Δ | Interpretation |
|---|---|---|---|---|
| ballad | 2.266 | 2.414 | **+0.149** | Formulaic contexts open lexical choices; bards exploit open slots |
| haiku | 2.328 | 2.475 | **+0.148** | Compression creates maximal semantic openness |
| beat | 2.169 | 2.315 | **+0.146** | Improvisational style picks freely from open syntactic positions |
| clerihew | 2.388 | 2.542 | **+0.154** | Humorous non sequitur fills syntactically open positions |
| mid_century | 2.273 | 2.404 | **+0.132** | Deep image poetics exploits syntactic freedom |

### Eras Surprising in Syntactically NARROWER Contexts (high-S2 div < baseline div)

| Era | Baseline Div | High-S2 Div | Δ | Interpretation |
|---|---|---|---|---|
| pantoum | 2.157 | 1.875 | **−0.282** | Repetition locks in syntactic expectations; surprise = structural violation |
| triolet | 2.223 | 2.100 | **−0.123** | Tight refrain structure; deviations must fight syntactic constraint |
| black_arts | 2.089 | 1.971 | **−0.119** | High-intensity rhetoric; surprise arrives against syntactic inevitability |
| old_english | 2.243 | 2.151 | **−0.092** | Alliterative half-line structure creates narrow syntactic slots |
| nursery_rhyme | 2.252 | 2.161 | **−0.091** | Fixed rhythmic template; content varies within narrow form |

---

## Interpretive Framework: Two Architectures of Poetic Surprise

The era variation suggests two fundamentally different modes of creating poetic surprise:

**Type A — Lexical-freedom surprise** (Δ > 0 eras: ballad, haiku, beat):  
The poet is in a syntactically *open* position (many word types could plausibly follow) but makes an unexpectedly specific, concrete, or anomalous choice within that freedom. The surprise comes from WHICH word within the available field.

**Type B — Structural-violation surprise** (Δ < 0 eras: pantoum, triolet, black_arts):  
The poet is in a syntactically *constrained* position (the prediction space is narrow — only one type of word is expected) but writes something from a different category entirely. The surprise comes from BREAKING the structural expectation rather than from unusual selection within it.

The null finding at the aggregate level reflects that these two types of surprise approximately cancel out when averaged across the full corpus.

---

## Finding 3: What High-S2 Tokens Look Like in Each Context

**Narrow-context surprises (div=1, S2>6)** — structural violations:  
`'riot'`, `'torches'`, `'Wan'`, `'Jesus'`, `'Fun'`, `'ashes'`, `'arm'`, `'Broken'`, `'jaws'`

Characteristic: concrete, specific, often embodied nouns arriving where the model expected continuation of an already-dominant category (usually punctuation or function words). These are the "hard breaks" in the fabric of linguistic expectation.

**Wide-context surprises (div≥4)** — lexical-freedom choices:  
`'badly'`, `'stacked'`, `'yellow'`, `'worms'`, `'revive'`, `'ruin'`, `'Nobody'`

Characteristic: diverse POS, more varied semantic domains. The poet picks from a large menu but chooses the most unexpected item on it.

---

## Finding 4: The Distribution of Prediction Diversity

Across the whole corpus, most token positions are **syntactically moderately constrained**:

| Diversity | Count | % |
|---|---|---|
| 1 (narrowest) | 8,171 | 15.7% |
| 2 | 24,871 | 47.9% |
| 3 | 16,773 | 32.3% |
| 4 | 1,960 | 3.8% |
| 5 | 160 | 0.3% |
| 6 (widest) | 5 | 0.0% |

The median prediction space spans exactly 2 syntactic categories. Poetry lives almost entirely in the 2–3 category zone — not the anarchically open multi-category space one might associate with "poetic freedom," and not the locked-down single-category space of purely formulaic expression.

---

## Theoretical Implications

1. **Poetic surprise is not exploiting syntactic ambiguity.** The flatness of diversity across S2 bins refutes the hypothesis that poets mainly surprise by inserting unexpected content into inherently ambiguous positions.

2. **Form constrains the type of surprise.** Highly repetitive forms (pantoum, triolet, refrain structures) force structural-violation surprise; more improvisational forms (beat, prose poetry) favor lexical-freedom surprise.

3. **The two-type model of surprise** may have implications for readerly processing. Structural-violation surprise arrives against strong prediction; lexical-freedom surprise arrives in an already open field. The phenomenology of these may differ — one feels like a jolt, the other like an unexpected selection from a menu.

---

## Next Steps

- Formally separate "structural violation" vs "lexical freedom" surprises using the div threshold (1 vs 4+) and test whether reader comprehension difficulty differs between types
- Compare the semantic domains of structural-violation surprises vs lexical-freedom surprises
- Test whether the two types are more prevalent in earlier stanzas (structural) vs later stanzas (lexical) within individual poems
- Apply to individual poets: does Dickinson's dash-heavy style generate more structural violations? Does Whitman's catalog generate more lexical-freedom surprises?
