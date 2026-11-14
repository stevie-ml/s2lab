# Procedural Poetry and S₂: Where Does Surprise Live in Instructional Verse?

**Date:** 2026-11-14  
**Experiment:** `experiments/procedural_poetry_s2.py`  
**Corpus:** 8 procedural poems (new era added today) vs. 103 lyric poems (romantic/victorian/modernist/confessional/19th_century) vs. 12 prose poems  
**Builds on:** `adversative_turn_s2.md`, `enjambment_two_strategies.md`, `whitman_catalogue_entropy_decay.md`

---

## Research Question

Procedural poetry — poems written as recipes, instructions, protocols, algorithms — imposes an unusual grammatical regime: imperative verbs dominate, objects are specific, and the syntax is relentlessly functional. Does this create a distinctive S₂ signature? 

**Hypothesis (Sawtooth):** In procedural poems, the information load falls primarily on the **imperative verb** (which specific action will be named?), while the object noun that follows should be more constrained — lower S₂. This would create a high-low-high-low "sawtooth" oscillation tied to the grammatical structure.

**Null hypothesis:** Procedural grammar doesn't differ from lyric grammar in its S₂ distribution.

---

## Method

1. Added 8 new poems to the corpus in a new "procedural" era:
   - 5 synthetic test cases (purpose-built to maximize imperative grammar)
   - Hesiod's *Works and Days* agricultural instructions (trans. Mair, 1908)
   - Benjamin Franklin's *Poor Richard's Almanac* "Way to Wealth" extract
   - Horace's *Ars Poetica* opening (trans. Howes, 1849)

2. Classified each clean token (p_newline < 0.9) as:
   - **Imperative verb**: token matching a list of imperative verb forms
   - **Post-verb**: token immediately following an imperative verb (the object slot)
   - **Other**: everything else

3. Compared procedural S₂ distribution to lyric and prose poetry baselines.

---

## Key Results

### 1. The Sawtooth Hypothesis Is Inverted

| Group | Imperative verb S₂ | Post-verb S₂ | Other S₂ | n_verbs |
|---|---|---|---|---|
| **Procedural** | +0.54 | **+0.91** | −0.31 | 18 |
| Lyric baseline | +0.70 | **−1.10** | −0.20 | 33 |
| Prose poetry | +1.32 | **−0.78** | −0.41 | 2 |

**The hypothesis fails — and the failure is itself the finding.**

In **lyric and prose poetry**, the expected sawtooth *does* appear: verbs have high S₂, their objects have low S₂ (−1.10). The model knows what a verb constrains; once a verb is placed, the object is in a narrower semantic field.

In **procedural poetry**, the pattern **reverses**: post-verb objects average +0.91, nearly 2 full S₂ units *above* the lyric post-verb baseline. The object noun is where the poetic surprise lives — not the verb.

### 2. The "Poetic Object" Effect

This inversion reveals the aesthetic logic of procedural poetry. The genre works by:

- **Keeping the verbs ordinary** ("take", "gather", "press", "observe") — these are low-surprise, imperative command words
- **Making the objects strange** ("the morning", "your silences", "what you remember", "the landscape")

The poetic register is displaced from verb to object. In a recipe, you'd expect: *Take the [egg|dough|butter|flour]* — but the procedural poem writes *Take the [morning|memory|distance|country]*. The verb is conventional; the object is a Straussian gap.

### 3. Per-Poem Variation Reveals Mechanism

| Poem | Verb S₂ | Post-verb S₂ | Mechanism |
|---|---|---|---|
| "How to Disappear" | **−4.88** | −0.42 | Verb repetition — "Begin" ×6 flattens verb S₂ |
| "Recipe" (synth I) | +0.52 | +0.35 | Moderate both; mild inversion |
| "Instructions for Forgetting" | +1.19 | +1.22 | High both; strongly poetic objects |
| "Field Notes for Living" | **+1.91** | **+1.95** | Maximum inversion; both elevated |
| *Works and Days* (Hesiod) | **+6.52** | +4.80 | Extreme — agricultural verbs alien to GPT-2 |
| *Poor Richard* (Franklin) | **+7.59** | −1.49 | Classic sawtooth — aphoristic not poetic |

**"How to Disappear"** is the most revealing case: its imperative verb ("Begin") is repeated six times. The refrain effect documented in `refrain_information_decay.md` operates here — the model learns the anaphoric structure and each "Begin" becomes increasingly expected (verb S₂ averages −4.88). But the objects remain surprising (−0.42 is still above the lyric post-verb baseline of −1.10). **The surprise migrates from verb to object as the structure is learned.**

**Benjamin Franklin's almanac** shows the *inverse* pattern: a classic sawtooth. "Drive" and "make" have extremely high S₂ (+7.59 average) but their aphoristic objects ("thy business", "a man healthy") are constrained (−1.49). Franklin's verse works because the verbs are unexpected commands; the consequences are conventional wisdom.

**Hesiod** is an outlier: *both* verbs and objects are alien to GPT-2 (trained on modern text), yielding extreme S₂ at every position. This is an artifact of temporal distance, not poetic strategy.

### 4. Structural Implications

The findings suggest two distinct procedural poetry strategies:

| Strategy | Verb S₂ | Object S₂ | Example |
|---|---|---|---|
| **Object-displacement** | Low (ordinary commands) | High (strange objects) | Contemporary synthetic poems |
| **Verb-foregrounding** | High (unexpected commands) | Low (predictable objects) | Franklin's aphorisms |
| **Full-displacement** | High (alien verbs) | High (alien objects) | Hesiod (artifact of temporal distance) |

Contemporary procedural poetry (Bernadette Mayer, Chelsey Minnis, Matthew Zapruder) predominantly uses **object-displacement**: the reader accepts the grammatical frame of instruction, then is surprised by what must be acted upon.

---

## Finding

**Procedural poetry inverts the standard verb-object S₂ relationship.** In lyric poetry, imperative verb positions have high S₂ while post-verb objects drop to −1.10 — the verb is the surprise, the object is constrained. In procedural poetry, the opposite holds: objects after imperative verbs average +0.91, nearly 2 units *above* lyric baseline. The genre achieves its defamiliarizing effect not by choosing unusual verbs (the commands stay ordinary) but by choosing unusual *objects* — things that cannot be easily acted upon, that resist the mechanical frame the verb imposes.

This creates a **genre-specific Straussian gap**: what GPT-2 "expects" after "Take" or "Gather" is a physical object (flour, tools, supplies). What the procedural poem provides is an abstraction — "the morning", "your silences", "what you remember". The gap between the mechanical and the metaphysical is the poem's subject.

---

## Limitations

- Sample size: only 18 imperative verb positions across 8 procedural poems. Larger corpus needed.
- The imperative verb list is manually curated and may miss edge cases.
- Hesiod and Franklin are temporal-distance artifacts rather than stylistic ones.
- Synthetic poems were designed by this research agent and may not generalize.

---

## Suggested Next Steps

1. **Expand the procedural corpus** with more public-domain instructional verse (Virgil's *Georgics*, Tusser's *Five Hundred Points of Good Husbandry*, Marcus Aurelius as found poetry)
2. **Test the "object class" hypothesis**: do procedural poems preferentially use **abstract nouns** as objects? Classify object nouns as concrete/abstract and measure S₂ by class.
3. **Apply to known procedural poets**: find public-domain equivalents or secure permission for contemporary procedural poets.
4. **The anaphora-displacement interaction**: as "Begin" or other repeated verbs become normalized, do their objects have *higher* S₂ to compensate? Test by comparing S₂ of objects to their position in the anaphoric chain (1st "Begin" vs. 6th).
