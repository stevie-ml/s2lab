# Whitman's Catalogue: Template Learning and the Paradox of the List

**Date:** 2026-10-28  
**Experiment:** `experiments/whitman_catalogue_s2.py`  
**Corpus poem:** Song of Myself (section 15, catalogue) — 640 tokens, 26 catalogue items  
**Builds on:** `catalog_decay_s2.md` (lexical anaphora), `entropy_conditioned_deviation.md`, `confidence_trap_analysis.md`

---

## Research Question

`catalog_decay_s2.md` showed that lexical anaphora (repeated anchor words like "being...") causes
both entropy and S2 to decay as GPT-2 adapts to the template. But Whitman's catalogues work
differently: Section 15 of *Song of Myself* enumerates ~87 American occupations using **syntactic**
parallelism without a fixed lexical anchor. Each line begins "The [occupation]..." but the
occupation word is always new.

Question: Does GPT-2 learn the *syntactic* template even without lexical repetition? And if entropy
decays, does Whitman compensate by escalating his lexical surprise?

---

## The Poem's Structure

Section 15 is one of the longest catalogues in English poetry. Each item follows the pattern:

> The carpenter dresses his plank...  
> The married and unmarried children ride home...  
> The pilot seizes the king-pin...  
> The quadroon girl is sold at the auction-stand...  
> The Wolverine sets traps on the creek...

There is no repeated anchor word — only a repeated *grammar* (The + NP + VP). This tests whether
GPT-2's context model abstracts syntactic templates, not just lexical patterns.

---

## Key Finding 1: Entropy Decays (r = −0.50)

**r(catalogue position, mean entropy) = −0.501 — a strong negative correlation.**

| Section | Items | Mean Entropy | Mean S₂ | First-Noun S₂ |
|---------|-------|-------------|---------|----------------|
| First third | 1–8 | **7.647** | −0.229 | +0.729 |
| Middle third | 9–17 | 7.325 | −0.258 | +1.235 |
| Final third | 18–26 | **6.859** | −0.136 | +0.392 |

Entropy drops by 0.79 nats across the catalogue — a meaningful decline. GPT-2 progressively
learns to expect the "The [X] [verb]s..." template, narrowing its prediction distribution even
before it knows what occupation will appear.

This confirms: **syntactic templates are learned by GPT-2's context window even without lexical
repetition.** The model generalizes from "The carpenter... The pilot... The spinning-girl..." to
expect the pattern.

---

## Key Finding 2: S₂ Does NOT Decay (r = −0.04)

**r(catalogue position, mean S₂) = −0.039 — essentially flat.**

Despite entropy dropping, Whitman's S₂ values remain roughly constant. In the final third,
mean S₂ is actually *higher* (−0.136) than in the first third (−0.229).

**This is the paradox of the list:** As GPT-2 becomes more confident about the syntactic frame
(lower entropy), the model's predictions about *which specific noun* will fill the slot become
more focused. A lower-entropy context makes each actual choice more visible — more countable
against what the model expected. Whitman maintains his surprise level by filling predictable
syntactic slots with increasingly specific, archaic, or peripheral occupation names.

In other words: **the catalogue template doesn't exhaust surprise — it redirects it.**
From structural surprise to lexical surprise.

---

## Finding 3: The 'The' Article Becomes More Predicted

The definite article 'The' that opens each line:

| Section | Mean S₂ of 'The' | Mean Entropy at 'The' |
|---------|-----------------|----------------------|
| Early (items 1–13) | **−1.982** | 4.122 |
| Late (items 14–26) | **−3.592** | 4.506 |

'The' becomes *less* surprising as the catalogue progresses (-1.98 → -3.59), even as the entropy
at that position *rises* slightly. GPT-2 learns to strongly expect a line to open with 'The'
after encountering this pattern many times. The article becomes structurally invisible — a
mere template marker — freeing the occupation noun to do all the work.

---

## Finding 4: High-S₂ Occupations Are Peripheral; Low-S₂ Are Generic

### Most Informationally Surprising Occupation Nouns

| Rank | Item # | S₂ | Line |
|------|--------|-----|------|
| 1 | 20 | **+8.92** | The Wolverine sets traps on the creek... |
| 2 | 26 | +4.08 | The paving-man leans on his two-handed rammer... |
| 3 | 17 | +3.85 | The groups of newly-come immigrants cover the wharf... |
| 4 | 9 | +3.26 | The lunatic is carried at last to the asylum... |
| 5 | 16 | +3.26 | The western turkey-shooting draws old and young... |
| 6 | 7 | +3.19 | The spinning-girl retreats and advances... |
| 7 | 10 | +2.88 | The jour printer with gray head and gaunt jaws... |

"Wolverine" (S₂=+8.92) is the most informationally startling entry — in 1855, it would refer
to an Ojibwe person from the Great Lakes region. GPT-2, trained on modern text, has no model of
this usage and spikes violently.

The archaic "jour printer" (*jour* from French *journalier*, a day-laborer typesetter) also spikes
dramatically — the line reaches max S₂ = **+20.64** at some token, the highest in the catalogue —
because GPT-2 cannot predict this pre-industrial occupational slang.

"Lunatic," "immigrants," "turkey-shooting" — these are the marginal, the stigmatized, the
vernacular. Whitman's most informationally surprising entries are *the excluded* of 1855 America.

### Least Surprising (Most GPT-2-Expected) Occupation Nouns

| Rank | Item # | S₂ | Line |
|------|--------|-----|------|
| Last | 23 | **−5.72** | The young sister holds out the skein... |
| 2nd last | 14 | −4.05 | The young fellow drives the express-wagon... |
| 3rd last | 8 | −2.53 | The farmer stops by the bars... |
| 4th last | 19 | −2.12 | The youth lies awake... |
| 5th last | 15 | −1.74 | The half-breed straps on his light boots... |

Generic domestic figures — sister, farmer, youth — are fully expected by GPT-2. After a sequence
of "The [occupational noun]..." lines, these are exactly what the model anticipates.

Interestingly, "half-breed" scores low despite being socially marked. GPT-2's training data
evidently contains enough of this archaic term for it not to register as surprising.

---

## Finding 5: Position of Peak S₂ Within Each Item

The occupation noun (first content token after 'The') is NOT always the highest-S₂ token in each
line. The highest S₂ often comes later, in the activity phrase:

| Item | Max S₂ token | Max S₂ value | Location in line |
|------|-------------|-------------|-----------------|
| "jour printer" | "jour" | +20.64 | position 2 (the occupation itself) |
| "carpenter" | "foreplane" | +11.47 | position 7 (activity noun) |
| "connoisseur" | "exhibition-gallery" | +10.47 | position 6 (location compound) |
| "one-year wife" | "borne" | +9.54 | position 9 (past participle — ambiguous) |
| "Wolverine" | "Wolverine" | +8.92 | position 1 |

So peak surprise comes either at the occupation name (exotic/archaic nouns) or at **specific
activity vocabulary** — the distinctive tools, actions, or locations that individualize each
worker. Whitman's catalogue works by "showing the work" — the concrete implements of labor are
as informationally rich as the workers themselves.

---

## Comparison: Lexical vs Syntactic Anaphora

| Feature | Lexical anaphora (being...) | Syntactic parallel (The + NP + VP) |
|---------|---------------------------|-----------------------------------|
| Entropy trend | Strong decay | Strong decay (r = −0.50) |
| S₂ trend | Decays | Flat (r = −0.04) |
| Template-learning | Fast (anchor learned immediately) | Slower (pattern abstracted across items) |
| Poet's strategy | Escalate content surprise; insert epistemic disruptions | Escalate occupational specificity; use archaic/peripheral nouns |

**Whitman's catalogue maintains surprise better than lexical anaphora catalogues.** The absence
of a repeated anchor word keeps the model's residual uncertainty higher across positions, giving
Whitman more room to work.

---

## The "Confidence Trap" Mechanism (Revised)

The standard confidence trap: GPT-2 becomes confident, so the poet's choice becomes more
visible against the narrow prediction set. In Whitman, the trap operates differently:

1. **Frame confidence rises**: GPT-2 learns "The [something] [verbs]..." and expects this structure.
2. **Slot entropy drops**: The model narrows its slot predictions but still can't predict *which*
   occupation noun appears (there are too many possibilities).
3. **Lexical specificity escalates**: Whitman uses increasingly archaic ("jour printer"),
   culturally specific ("Wolverine"), or compound ("paving-man") terms to defeat the narrowed
   prediction space.
4. **Result**: Entropy drops but S₂ stays level — the catalogue form *enables* sustained surprise
   by making the structural choices irrelevant (they're already predicted) and concentrating
   reader attention on lexical choices.

This suggests a general principle: **catalogues trade structural surprise for lexical surprise.**
Once the template is established, every deviation at the content level registers more loudly.

---

## New Poems Added to Corpus

Seven catalogue/list poems added to test these patterns across a broader range:

| Title | Author | Year | Era | Rationale |
|-------|--------|------|-----|-----------|
| I Hear America Singing | Walt Whitman | 1860 | 19th_century | Shorter Whitman catalogue; pure "singing" anaphora |
| For I Will Consider My Cat Jeoffry (excerpt) | Christopher Smart | 1763 | 18th_century | "For..." lexical anaphora; 18 items |
| We Real Cool | Gwendolyn Brooks | 1959 | mid_century | Ultra-short "We" anaphora; 8 items |
| This Is Just to Say | William Carlos Williams | 1934 | modernist | Implicit list structure; no anaphora |
| Song of Myself (section 33, excerpt) | Walt Whitman | 1855 | 19th_century | Different Whitman catalogue: identification not enumeration |
| Ode to My Socks | Pablo Neruda | 1956 | latin_american | Simile catalogue; object poem |
| The Red Wheelbarrow | William Carlos Williams | 1923 | modernist | Anti-catalogue: single object, maximal focus |

---

## Suggested Next Steps

1. **Run the catalogue analysis on "I Hear America Singing"** once the corpus is updated — it
   should show even stronger entropy decay since it IS lexically anchored ("singing"). Compare
   decay rate to section 15.

2. **Smart's "Jeoffry" catalogue** uses "For..." prefix — unlike Whitman's "The", "For" carries
   a liturgical expectation (biblical parallelism). Does entropy decay faster with a religiously
   marked anchor?

3. **Test the claim**: Brooks's "We Real Cool" has 8 items, each ending "We / [verb]." Does the
   extreme shortness of each item (2-4 tokens) affect entropy decay rate?

4. **Straussian gap in the catalogue**: Build a taxonomy of the *kinds* of things Whitman chose
   NOT to write at each slot (GPT-2's top-5 alternatives). How do actual occupation names differ
   from GPT-2's predictions? Are GPT-2's predictions more abstract, more common, more domestic?
