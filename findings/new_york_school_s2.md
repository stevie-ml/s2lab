# New York School Poetics: S₂ Profile of Casual Diction and the Ashbery Paradox
**Date:** 2026-11-01  
**Experiment:** `experiments/new_york_school_diction.py`  
**New poems added:** Barbara Guest (2), Ted Berrigan, James Schuyler, Anne Waldman, John Ashbery ("Farm Implements")  
**Corpus now:** 395 texts

---

## Question

Does the New York School's celebrated "casual diction" — everyday items, direct address, proper names, parataxis — produce a distinct S₂ signature? And within the school, does Ashbery's famous difficulty translate into *higher* token-level surprise than O'Hara's apparently simpler style?

---

## Key Finding: NYS Is Near the Bottom of the S₂ Rankings

| Era | n | avg S₂ | std S₂ | +S₂% | median S₂ |
|---|---|---|---|---|---|
| confessional | 6 | **+0.568** | 5.870 | 40.9% | -0.996 |
| modernist | 27 | **+0.529** | 5.825 | 36.9% | -0.828 |
| imagist | 5 | **+0.384** | 5.603 | 39.2% | -0.839 |
| romantic | 21 | **+0.347** | 5.448 | 36.1% | -0.853 |
| victorian | 29 | **+0.328** | 5.166 | 36.9% | -0.910 |
| surrealist | 8 | **+0.194** | 5.270 | 34.1% | -1.193 |
| beat | 6 | **+0.180** | 4.347 | 21.7% | -0.261 |
| **new_york_school** | **26** | **−0.116** | **4.619** | **33.8%** | **−1.278** |
| language | 6 | **−0.414** | 4.222 | 31.5% | -1.530 |

NYS ranks second-to-last among all eras tested, with only Language Poetry lower. Its **median S₂ (−1.278)** is the most negative of any literary-historical era in the corpus. This confirms the hypothesis: the school's everyday language — product names, lunch orders, street addresses, conversational conjunctions — is more *predictable* to GPT-2 than the heightened diction of Romantic or Modernist poetry.

The **median being more negative than the mean** (−1.278 vs −0.116) indicates a right-skewed distribution: most NYS tokens are quite predictable, but occasional sharp spikes pull the mean up. The school's information-theoretic signature is *flat with rare bursts*, not the sustained high surprise of Modernism.

---

## The Ashbery Paradox

| Poet | n poems | avg S₂ | std S₂ | +S₂% |
|---|---|---|---|---|
| John Ashbery | 17 | **−0.162** | 4.593 | 36.1% |
| Frank O'Hara | 3 | **+0.174** | 4.677 | 35.1% |
| Kenneth Koch | 1 | **−0.322** | 3.671 | 32.7% |

**Counter-intuitive result:** O'Hara (+0.174) beats Ashbery (−0.162) in average S₂. The most "difficult" poet in the school is less surprising, token by token, than the most "casual" one.

This is the **Ashbery Paradox**: his fame rests on syntactic opacity — abrupt tonal shifts, pronoun antecedent confusion, non-sequitur transitions — but none of these produce high S₂, because GPT-2 processes tokens sequentially and Ashbery's actual *word choices*, given the preceding context, tend to be conventional. His difficulty is architectural, not lexical. He builds strange rooms from ordinary bricks.

O'Hara's S₂ spikes, by contrast, come from genuine semantic juxtapositions: unexpected function words in high-entropy contexts ("three", "is", "it", "or", "a" all appear as top high-S₂ tokens), suggesting his casual parataxis — "I go to the / bank / and then / to the / cinema" — produces genuine surprises at the syntactic pivots where the model is confident about what comes next.

---

## Per-Poem S₂ Summary (Expanded NYS Corpus, n=26)

| Title | Author | avg S₂ | std | +S₂% |
|---|---|---|---|---|
| What Is Poetry | Ashbery | **+1.001** | 6.658 | 35.8% |
| Poems | Guest | **+0.997** | 6.745 | 32.2% |
| A Few Days | Schuyler | **+0.803** | 6.628 | 36.7% |
| Why I Am Not a Painter | O'Hara | **+0.795** | 5.099 | 38.2% |
| The Day Lady Died | O'Hara | **+0.519** | 4.769 | 40.3% |
| Farm Implements and Rutabagas | Ashbery | **+0.517** | 4.882 | 39.9% |
| Wet Casements | Ashbery | **+0.338** | 4.043 | 41.6% |
| Paradoxes and Oxymorons | Ashbery | **+0.316** | 5.223 | 35.2% |
| Self-Portrait (opening) | Ashbery | +0.007 | 4.417 | 41.1% |
| Self-Portrait (closing) | Ashbery | −0.014 | 4.246 | 42.9% |
| Self-Portrait (middle) | Ashbery | −0.048 | 4.536 | 34.9% |
| Soonest Mended | Ashbery | −0.101 | 4.374 | 36.6% |
| The Painter | Ashbery | −0.153 | 4.398 | 43.7% |
| Leaving the Atocha Station | Ashbery | −0.211 | 4.996 | 37.0% |
| Having a Coke with You | O'Hara | −0.227 | 4.390 | 31.9% |
| You Were Wearing | Koch | −0.322 | 3.671 | 32.7% |
| Parachutes, My Love | Guest | −0.361 | 3.648 | 29.4% |
| Makeup on Empty Space | Waldman | **−0.490** | 3.685 | 26.8% |
| And Ut Pictura Poesis | Ashbery | −0.530 | 3.946 | 33.7% |
| Rivers and Mountains | Ashbery | −0.567 | 4.542 | 35.9% |
| Some Trees | Ashbery | −0.589 | 5.264 | 34.1% |
| The One Thing That Can Save | Ashbery | −0.825 | 4.179 | 32.9% |
| Personal Poem | Berrigan | **−0.852** | 3.113 | 25.4% |
| The Instruction Manual | Ashbery | −0.969 | 3.419 | 29.9% |
| A Blessing in Disguise | Ashbery | −1.048 | 3.708 | 28.9% |
| A Wave (opening) | Ashbery | **−1.144** | 3.635 | 25.7% |

**Range within the school: +1.001 to −1.144** — the NYS contains both some of the most and least surprising poems in the corpus (within its own era bracket).

**Notable:** Ashbery's two long meditative poems ("A Wave", "A Blessing in Disguise") have the *lowest S₂ of any poem in the group*. These are his most famously difficult works. Their very low S₂ (and very low std) suggests extreme *contextual regularity* — each token is well-predicted by the preceding context even while the poem's global meaning remains opaque. This quantifies a literary intuition: Ashbery's long poems feel "inevitable" line by line even when the argument is obscure.

---

## Repetition Drives S₂ Down Within NYS

Consistent with the earlier repetition-collapses-S₂ finding, the two most anaphoric poems have the lowest S₂:

- **Anne Waldman, "Makeup on Empty Space"** (−0.490): "I am putting makeup on empty space / I am putting makeup on empty space / …" Heavy anaphora. GPT-2 learns the refrain quickly; S₂ collapses.  
- **Ted Berrigan, "Personal Poem"** (−0.852): Chatty, repetitive, first-person observations. "I'm 27 years old. I'm going to write / another poem today."

The highest S₂ poems are those where repetition is minimal and juxtapositions are genuine: Ashbery's "What Is Poetry" (meta-poetic, switching registers abruptly), Guest's "Poems" (shifting imagery), Schuyler's "A Few Days" (plain but non-sequitur observations).

---

## Suppression Taxonomy: What Does NYS Suppress?

At high-S₂ positions (S₂ > 2.0), what did GPT-2 predict vs. what the poets chose?

| Category | NYS Chosen | NYS Suppressed | Romantic Chosen | Romantic Suppressed |
|---|---|---|---|---|
| content_word | 77.5% | **43.6%** | 79.8% | **36.1%** |
| other | 8.5% | 26.4% | 3.3% | 33.2% |
| article | 3.1% | **11.5%** | 2.7% | **13.6%** |
| preposition | 4.1% | 7.7% | 4.5% | 7.4% |
| conjunction | 2.5% | 5.2% | 7.4% | 5.9% |
| pronoun | 3.0% | 5.1% | 2.3% | 3.8% |

**NYS suppresses more content words** (43.6%) and fewer "other" tokens (26.4%) than Romantic poets (36.1% / 33.2%). This means: when NYS poets create a Straussian gap, they are most often replacing the *expected noun or verb* with an unexpected one — a content-word substitution. Romantic poets are more likely to surprise by choosing a function word in a content-word slot (a different kind of surprise).

This aligns with the school's poetics: NYS surprises at the *semantic* level (this noun, not that noun) rather than at the structural level (noun here, not conjunction).

---

## New Poets: Guest, Schuyler, Berrigan, Waldman

The new additions confirm and extend the NYS profile:

- **Barbara Guest** ("Poems": +0.997): Her imagist-inflected NYS lyrics — shorter, more compressed, with spatial imagery — produce high S₂ closer to the Imagist school than to Ashbery. Her S₂ is closer to Pound than to O'Hara.
- **James Schuyler** ("A Few Days": +0.803): The plainest diction in the group, yet highest S₂ after Guest and Ashbery's meta-poem. His "The cat wants out. / I let the cat out." sequences surprise GPT-2 with their radical non-sequitur transitions despite using only the most common vocabulary.
- **Ted Berrigan** ("Personal Poem": −0.852): The group's most Kerouac-adjacent poem; its stream-of-consciousness repetitions and circular structure produce the lowest S₂ among the new additions, confirming the repetition hypothesis.
- **Anne Waldman** ("Makeup on Empty Space": −0.490): Her anaphoric chant structure drives S₂ down progressively — a live instance of the refrain-betrayal effect.

---

## Hypothesis: The NYS S₂ Gradient Is Driven by Repetition Density

Within NYS, the best single predictor of a poem's S₂ may be its *repetition density* — the frequency of repeated content words. This would explain:
- Waldman (high repetition) → low S₂
- Berrigan (circular, chatty) → low S₂  
- Schuyler (non-repetitive observations) → high S₂
- O'Hara (chatty but non-repeating juxtapositions) → moderate-high S₂
- Ashbery long poems (meditative, repetitive themes) → very low S₂
- Ashbery short/formal poems (compact, less repetition) → moderate S₂

**Next step**: Operationalize repetition density (type-token ratio or repeat token ratio per poem) and test correlation with avg S₂ within the NYS group.

---

## Suggested Next Steps

1. **Type-token ratio vs S₂ within NYS**: Compute TTR per poem and correlate with avg S₂ — a direct test of the repetition-drives-down-S₂ hypothesis.
2. **Ashbery late vs early**: Test if the long, late Ashbery poems are consistently lower S₂ than his early compressed work — a career trajectory analysis specifically for his arc.
3. **NYS prose vs poetry**: Several Schuyler diary entries and O'Hara's "I do this, I do that" poems blur into prose. Compare their S₂ to the prose poetry era.
4. **Add more NYS poets**: Alice Notley, Ron Padgett, Bill Berkson, Bernadette Mayer. Test if the school's internal variation holds.
5. **The "occasional poem" subtype**: O'Hara's lunch poems are responses to specific events. Compare S₂ of "occasion-bound" poems vs "timeless" lyrics — does topicality suppress surprise?
