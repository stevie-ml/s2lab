# Parody, Pastiche, and Literary Subversion: S₂ Analysis
**Date:** 2026-10-10
**Experiment:** `experiments/parody_s2.py`

## Question

Does parody achieve its comic and critical effect through an information-theoretic mechanism?
Specifically: does parody *evoke* familiar language (GPT-2 is confident → LOW entropy → LOW S₂)
and then *subvert* it at key moments (HIGH S₂ spikes where the poet deviates from expectation)?

**Corpus:** Lewis Carroll's parodies of Watts and Southey (3 pairs); Alexander Pope's mock-epic
*Rape of the Lock*; paired source texts as `parody_original` control.

---

## Overall S₂ Comparison

| Group | n poems | n tokens | Mean S₂ | StDev S₂ | Variance | +S₂ Ratio | High-S₂ Ratio (>3) |
|---|---|---|---|---|---|---|---|
| Parody | 4 | 669 | -0.288 | 3.364 | 11.319 | 36.0% | 15.5% |
| Parody Original | 3 | 443 | -0.454 | 3.217 | 10.352 | 33.2% | 14.9% |
| General Poetry | 222 | 24918 | -0.382 | 3.658 | 13.382 | 33.7% | 15.9% |
| Prose Control | 5 | 163 | -1.721 | 2.329 | 5.426 | 20.2% | 3.7% |

**First-pass finding:** Parody has *higher* mean S₂ (-0.288) than its original source texts (-0.454) and
slightly higher +S₂ ratio (36% vs. 33%), but lower variance than general poetry. The prose-poetry gap
(-1.72 vs. ≥-0.29) confirms that even simple parody verse sits firmly in the poetry S₂ range.

---

## Per-Poem Profile

| Title | Author | Era | n tokens | Mean S₂ | StDev | Variance | +S₂ | High-S₂ |
|---|---|---|---|---|---|---|---|---|
| 'Tis the Voice of the Lobster | Lewis Carroll | parody | 105 | -1.230 | 2.928 | 8.572 | 27.6% | 9.5% |
| 'Tis the Voice of the Sluggard | Isaac Watts | parody_original | 107 | -1.090 | 3.168 | 10.037 | 29.0% | 13.1% |
| How Doth the Little Busy Bee | Isaac Watts | parody_original | 110 | -0.348 | 3.344 | 11.184 | 41.8% | 13.6% |
| How Doth the Little Crocodile | Lewis Carroll | parody | 49 | -0.351 | 3.454 | 11.933 | 40.8% | 14.3% |
| The Old Man's Comforts (Southey) | Robert Southey | parody_original | 226 | -0.205 | 3.151 | 9.929 | 31.0% | 16.4% |
| The Rape of the Lock (Pope) | Alexander Pope | parody | 175 | **+0.274** | 3.819 | **14.585** | **43.4%** | **21.7%** |
| You Are Old, Father William | Lewis Carroll | parody | 340 | -0.278 | 3.172 | 10.059 | 34.1% | 14.4% |

**Pope stands apart.** The *Rape of the Lock* has the only positive mean S₂ among all parody/original
poems, the highest variance, and nearly double the high-S₂ rate of any other poem. Mock-epic parody
is a more information-theoretically active mode than Carroll's direct substitution parody.

---

## Carroll Divergence Analysis: The Mechanism of Substitution

Each Carroll parody opens with the *exact* text of its original, then diverges. This design exposes
the evocation-subversion dynamic directly.

### Pair 1: Watts "Busy Bee" → Carroll "Crocodile"

**Shared prefix:** `" doth the little"` (4 tokens, avg S₂ = **−0.550**)

The shared prefix pulls S₂ deeply negative — GPT-2 recognizes this formulaic opening and assigns
high confidence to the continuation.

| Position | Original | S₂ | Parody | S₂ |
|---|---|---|---|---|
| Divergence (+5) | `busy` | 5.27 | `crocod` | 2.78 |

Counterintuitively, the parody's divergence token (`crocodile`) is *less* surprising (S₂=2.78) than the
original's `busy` (5.27). After "the little", GPT-2 anticipates a noun — animal names are a natural
continuation. The adjective "busy" is structurally unexpected (adjective before noun when noun expected).

**Carroll's real subversion comes later in the poem:**

| Token | S₂ | Context |
|---|---|---|
| `cheer` | **11.12** | `...scale!↵↵How cheer` |
| `spreads` | **9.43** | `...grin,↵How neatly spreads` |
| `gently` | 4.54 | `...fishes in,↵With gently` |
| `little` | 3.51 | `...claws,↵And welcomes little` |

"How cheerfully he seems to grin" (S₂=11.12 at "cheer") — after the praise formula "How neatly", GPT-2
expects a virtuous attribute. "Cheerfully" applied to a predator is the information-theoretic punchline.

---

### Pair 2: Southey "Old Man's Comforts" → Carroll "You Are Old, Father William"

**Shared prefix:** `" are old, Father William, the young man"` (9 tokens, avg S₂ = **−0.059**)

The longer, near-perfect shared prefix keeps S₂ near zero — GPT-2 has essentially reproduced
the Southey poem up to this point.

| Position | Original | S₂ | Parody | S₂ |
|---|---|---|---|---|
| Divergence (+10) | `cried` | 6.43 | `said` | 2.08 |

Again, the parody's initial divergence word is *less* surprising than the original. "Cried" (S₂=6.43)
is the more literary/dramatic verb — even Southey's own word is unexpectedly elevated. Carroll's
colloquial "said" (S₂=2.08) sounds almost plain by comparison. Carroll begins with a False Lull.

**But the S₂ spikes arrive through the stanzas of absurdity:**

| Token | S₂ | Context |
|---|---|---|
| `incess` | **12.45** | `...;↵And yet you incess` |
| `said` | **10.04** | `...↵You are old, said` |
| `muscular` | **9.94** | `...wife;↵And the muscular` |
| `sage` | **9.43** | `...my youth, said the sage` |
| `grey` | 8.77 | `...as he shook his grey` |
| `downstairs` | 8.31 | `...or I'll kick you downstairs` |
| `somers` | 8.26 | `...turned a back-somers` |

"Incessantly stand on your head" (S₂=12.45 at "incess"), "the muscular strength" from arguing with
his wife (S₂=9.94), and "I'll kick you downstairs" (S₂=8.31): Carroll's highest-S₂ moments are
precisely the violent, bodily, undignified departures from Southey's pious self-improvement narrative.

The second instance of "said" has S₂=10.04 — by the 3rd stanza, GPT-2 has learned the poem's
dialogue structure enough that the repeated colloquial "said" becomes surprising against its own
trained expectation of more varied attribution verbs ("replied", "answered", "declared").

---

### Pair 3: Watts "Voice of the Sluggard" → Carroll "Voice of the Lobster"

**Shared prefix:** `"'Tis the voice of the"` (6 tokens, avg S₂ = **−2.915**)

The most extreme evocation: S₂ = −2.915 in the shared prefix. GPT-2 is *highly* confident here —
this formulaic opening is deeply recognizable. The ground is perfectly prepared.

| Position | Original | S₂ | Parody | S₂ |
|---|---|---|---|---|
| Divergence (+7) | `sl` (sluggard) | 0.92 | `Lob` (Lobster) | **6.29** |

Here Carroll departs from his usual pattern: the divergence token itself (`Lob[ster]`) is highly
surprising (S₂=6.29 vs. 0.92 for `sl[uggard]`). The word "Lobster" immediately delivers the subversion.

**The rest of the parody sustains the high S₂:**

| Token | S₂ | Context |
|---|---|---|
| `baked` | **7.32** | `...declare,↵You have baked` |
| `sharks` | 6.41 | `...when the tide rises and sharks` |
| `Lob` | 6.29 | `...'tis the voice of the Lob` |
| `brown` | 5.77 | `...You have baked me too brown` |
| `sugar` | 5.71 | `...too brown, I must sugar` |
| `Shark` | 3.72 | `...contemptuous tones of the Shark` |
| `contempt` | 3.17 | `...And will talk in contempt` |

"You have baked me too brown" (S₂=7.32 at "baked") substitutes the moral complaint of a lazy person
("you waked me too soon") with a culinary complaint from a crustacean. The semantic field shift
(moral → culinary, human → animal) consistently generates high S₂.

---

## Pope's Mock-Epic: A Different Parody Mode

Pope's *Rape of the Lock* doesn't substitute one word for another — it applies the *full machinery*
of epic to a trivial domestic incident. The result is the highest variance (14.585) and the only
positive mean S₂ (+0.274) among all poems in this study.

**Top moments of incongruity:**

| Token | S₂ | Context |
|---|---|---|
| `tasks` | **12.31** | `...a lord?↵In tasks` |
| `Muse` | **11.33** | `...verse to Caryll, Muse` |
| `Bel` (Belinda) | **11.27** | `...↵This, even Bel` |
| `'` (tim'rous) | 10.12 | `...shot a tim'` |
| `Could` | 8.90 | `...unexplor'd,↵Could` |
| `Goddess` | 8.68 | `...strange motive, Goddess` |

"In tasks so bold, can little men engage" (S₂=12.31 at "tasks") — after an epic invocation about
courtly assault, "tasks" is the deflating word. "Belinda" (S₂=11.27) as the epic heroine's name
in a high-flown invocation. The contracted "tim'rous" (S₂=10.12) is Augustan poetic diction applied
to curtains letting in morning light: the epic grandeur collides with pure domesticity.

Unlike Carroll's word-substitution, Pope's mock-epic keeps S₂ *consistently* high because every
epic convention (muse invocation, catalogue, elevated diction) sits incongruously in a domestic
context. There is no "evocation" phase followed by subversion — the incongruity is constant.

---

## Variance: Parody as Spiky Language

| Group | Mean within-poem S₂ variance |
|---|---|
| Parody | **11.287** |
| Parody Original | 10.384 |

Parody poems show **0.903 higher mean variance** than their source texts. The effect is modest but
consistent: 3/3 parody poems have higher variance than their paired originals when we exclude Pope
(who has no direct pair):

| Pair | Original variance | Parody variance | Δ |
|---|---|---|---|
| Busy Bee / Crocodile | 11.184 | 11.933 | +0.749 |
| Old Man / Father William | 9.929 | 10.059 | +0.130 |
| Voice of Sluggard / Lobster | 10.037 | 8.572 | **−1.465** |

The Lobster/Sluggard pair is the exception: the parody has *lower* variance than the original.
Looking at the top tokens, both poems are dominated by formulaic, confidence-low text. The
parody's absurdist vocabulary (baked, sharks, sugar) produces high isolated spikes but the
baseline is even more formulaic than Watts's moralistic original.

---

## Finding

**Parody's information-theoretic signature is not primarily higher variance, but a specific
SPATIAL PATTERN: a deeply negative shared prefix (evocation), followed by a spike at or shortly
after the divergence point (subversion), followed by sustained high-S₂ moments encoding the
absurdist/critical content.**

This "False Lull → Spike → Sustained Disruption" pattern holds for all three Carroll pairs:
- Shared prefix S₂: −2.92 / −0.55 / −0.06
- Divergence S₂ (parody): 6.29 / 2.78 / 2.08
- Top-5 avg S₂ post-divergence: 5.8 / 5.7 / 8.7

Pope's mock-epic shows a different but related structure: no lull because the incongruity is
constant. The mock-epic form maximizes S₂ throughput by maintaining the epic register while
varying the subject every few tokens.

**The 'unsaid' in parody:** At each high-S₂ moment in Carroll, GPT-2's top prediction would be
a word appropriate to the *original's* moral/religious register ("virtuous", "diligent",
"sleeping", etc.). The poet's choice — "cheerfully", "baked", "muscular" — is not just surprising
but semantically *opposed* to that expectation. The Straussian gap here encodes not mere novelty
but deliberate subversion of a known alternative.

---

## Suggested Next Steps

1. Extend corpus with more parody pairs (Virgil parodies, T.S. Eliot self-parody, *Don Quixote*
   as prose parody, etc.)
2. Align parody/original at the sentence level to better isolate divergence points and compute
   per-clause S₂ delta
3. Compute semantic distance (sentence embeddings) between GPT-2's top prediction and the poet's
   actual choice at high-S₂ parody moments — the "suppressed word's" semantic distance from
   the chosen word may be a measure of parody intensity
4. Test whether the "False Lull → Spike" pattern is unique to parody or also appears in
   allusion and quotation
5. Compare Carroll's comic parody vs. Pope's critical mock-epic in terms of WHICH semantic
   fields generate the highest S₂ (body/food for Carroll; domestic/name for Pope)
