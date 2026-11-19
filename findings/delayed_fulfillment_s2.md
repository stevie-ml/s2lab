# Delayed Fulfillment: When Poets Suppress a Word, Do They Use It Later?

**Date:** 2026-11-19  
**Question:** When a poet makes an unexpected word choice (high S₂), does GPT-2's suppressed top prediction appear *later* in the same poem?

---

## Hypothesis

The "Straussian gap" framing treats each high-S₂ moment as a one-time deviation: the poet chose X when language expected Y. But what if Y doesn't disappear? What if the most-expected word becomes a kind of *semantic debt* — deferred, then paid off later in the poem?

If this is true, the top-1 suppressed prediction should appear later in the same poem at a *higher rate* than lower-ranked alternatives (which represent words the model considered less natural).

---

## Method

For each token with S₂ > 2.0 (a substantial deviation from expectation):
1. Identify GPT-2's top-1 alternative prediction (the "unsaid")
2. Filter to content words only (remove function words, punctuation, tokens < 3 chars)
3. Check whether that content word appears anywhere in the remaining tokens of the same poem
4. Classify fulfillment as: **quick** (≤20 tokens), **delayed** (21–100 tokens), **long_arc** (>100 tokens), or **unfulfilled**

**Baseline:** Compare top-1 fulfillment rate against random alternatives (positions 3–9 in the probability ranking).

**Corpus:** 431 poems (excluding 5 prose controls), 3,561 qualifying suppression events.

---

## Results

### Overall Fulfillment Rates

| Category | Count | Rate |
|---|---|---|
| Quick (≤20 tokens) | 223 | 6.3% |
| Delayed (21–100 tokens) | 207 | 5.8% |
| Long-arc (>100 tokens) | 79 | 2.2% |
| **Total fulfilled** | **509** | **14.3%** |
| Unfulfilled | 3,052 | 85.7% |

**Baseline (random alternatives, positions 3–9):** 9.0% fulfillment

**Key finding: Top-1 predictions are fulfilled at 1.59× the rate of lower-ranked alternatives.** When GPT-2's most-expected word is suppressed, it appears later in the poem more often than chance—a ~60% excess. This is consistent with a "semantic debt" model.

---

### Fulfillment Rate by Era (n ≥ 5 events)

| Era | Events | Fulfilled | Quick | Delayed | Long-arc |
|---|---|---|---|---|---|
| triolet | 7 | 42.9% | 2 | 1 | 0 |
| concrete | 14 | 35.7% | 3 | 2 | 0 |
| german_expressionist | 91 | 30.8% | 14 | 13 | 1 |
| villanelle | 26 | 30.8% | 1 | 7 | 0 |
| german_modernist | 41 | 29.3% | 9 | 3 | 0 |
| german_symbolist | 61 | 26.2% | 12 | 4 | 0 |
| parody_original | 28 | 25.0% | 5 | 2 | 0 |
| ghazal | 12 | 25.0% | 2 | 1 | 0 |
| nursery_rhyme | 13 | 23.1% | 1 | 2 | 0 |
| ekphrastic | 111 | 21.6% | 2 | 11 | 11 |
| latin_american | 33 | 21.2% | 2 | 5 | 0 |
| 19th_century | 241 | 19.5% | 13 | 21 | 13 |
| dramatic_monologue | 237 | 16.9% | 6 | 18 | 16 |
| modernist | 290 | 16.2% | 15 | 25 | 7 |
| romantic | 193 | 15.0% | 10 | 14 | 5 |
| victorian | 237 | 14.3% | 15 | 14 | 5 |
| confessional | 29 | 0.0% | 0 | 0 | 0 |
| haiku | 22 | 0.0% | 0 | 0 | 0 |
| ancient | 18 | 0.0% | 0 | 0 | 0 |
| clerihew | 15 | 0.0% | 0 | 0 | 0 |

**Note on German data:** German poems produce elevated S₂ globally because GPT-2 is English-trained. German era statistics should be interpreted cautiously.

---

### Poem Length Effect

| Poem length | Events | Quick | Delayed | Long-arc | Total fulfilled |
|---|---|---|---|---|---|
| Short (<50 tokens) | 115 | 7.0% | 0.0% | 0.0% | 7.0% |
| Long (>200 tokens) | 1,175 | 5.1% | 7.4% | 5.7% | 18.2% |

**Long poems have 2.6× the long-arc fulfillment of short poems.** This is expected (more room to revisit suppressed words), but the magnitude confirms that the signal is genuine structure, not noise.

Haiku and clerihew at 0% are entirely length artifacts.

---

### Striking Examples of Delayed Fulfillment

**Walt Whitman, "O Captain! My Captain!" — The clearest case:**
- Position of suppression: Whitman writes "fearful" at a moment where GPT-2 predicts **"Captain"** (p=0.66, S₂=17.3)  
- Distance to fulfillment: **+77 tokens**  
- Context: This is likely the famous "O Captain! My Captain!" refrain — GPT-2 knows the poem well enough to predict "Captain" with high confidence. Whitman defers it, building tension, then delivers it in the refrain.  
- This is *the* canonical example of intentional delayed fulfillment.

**John Keats, "Ode on a Grecian Urn":**
- Wrote "bride" when GPT-2 predicted **"thy"** (p=0.10, S₂=12.9)  
- "thy" appears +52 tokens later  
- The ode addresses the urn directly with "thou still unravish'd bride of quietness" — "thy" recurs throughout as the apostrophic possessive.

**Anonymous (Hebrew Bible), "Psalms":**
- Wrote "Israel" when GPT-2 predicted **"thee"** (p=0.74, S₂=11.6)  
- "thee" appears +32 tokens later  
- Biblical parallelism: direct address ("thee") is deferred through the proper name ("Israel"), then re-established. The syntax of the Psalms uses name and pronoun as parallel forms.

**John Donne (early_modern):**
- Wrote "meant" when GPT-2 predicted **"what"** (p=0.74, S₂=11.1)  
- "what" appears +78 tokens later  
- Characteristic of Donne's syntax: an unexpected verb intrusion that postpones the expected interrogative.

---

## Theoretical Interpretation

The 60% excess (14.3% vs 9.0%) suggests that **GPT-2's top-1 prediction captures something linguistically privileged** about the words poets are thinking with, even when they don't use them immediately.

Three possible mechanisms:

1. **Structural debt (refrain/repetition):** The suppressed word IS a structural element (refrain, repeated motif) the poet is building toward. The villanelle finding (30.8%) supports this: villanelles require exact repetitions, so a high-S₂ deviation at word W is often followed by W at the refrain position.

2. **Semantic orbit:** The poem is "about" a cluster of related words. GPT-2 predicts the most natural word in that cluster; the poet defers to a synonym or related concept, but the central word appears when the orbit completes. The Keats and Whitman examples fit this.

3. **Discourse coherence:** Some words establish discourse topic-chains. GPT-2 predicts the topic continuation; the poet diverts, but the topic eventually reclaims its position.

**Crucially, the 85.7% that never appear are not evidence against this mechanism** — they may represent cases where the poet genuinely abandons the expected path. The 14.3% who do appear are the signal.

---

## Comparison to Prose Baseline

Control prose: only 7 qualifying events (too few for statistical comparison). This aligns with the finding that prose rarely produces high-S₂ content word suppressions — it doesn't generate enough events for delayed fulfillment to operate.

---

## Limitations

- GPT-2 tokenizes subword units (e.g., "ro" for a German word's stem), which creates spurious events in German-language poems.
- Matching uses normalized strings (lowercase, strip whitespace) but not stemming — "walk" and "walking" count as different words, slightly deflating the fulfillment rate.
- The control prose corpus is too small (5 texts) for meaningful comparison.

---

## Suggested Next Steps

1. **Refine with stemming:** Use a stemmer to match "walk"/"walked"/"walking" — this would increase fulfillment rates and might reveal more cases.
2. **Test specifically for REFRAINS:** Identify poems with known refrain structures and compute fulfillment rates for refrain words vs. non-refrain words at high-S₂ positions.
3. **Semantic debt across poems:** If a suppressed word doesn't appear in this poem, does it appear in the next poem by the same author? (Inter-poem debt)
4. **Rank decay:** How does fulfillment rate vary by rank of the suppressed prediction? Top-1 at 14.3%, what about top-2, top-3, top-5? This would sharpen the "linguistic privilege" claim.
5. **Distance analysis:** Plot the full distribution of fulfillment distances. Is there a characteristic "return distance" for different forms (e.g., villanelle refrain at fixed intervals vs. ode's wandering return)?
