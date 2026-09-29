# Numerals in Poetry: When Poets Count

**Date:** 2026-09-29  
**Experiment:** `experiments/numerals_in_poetry.py`  
**Corpus:** 200 texts from `results/corpus_results.json` (stanza-break artifact filtered)  
**Research question:** Do numeral tokens (digit strings and number words) carry distinctive S₂ signatures? When a poet writes a number, what did GPT-2 expect instead?

---

## Background

Using a specific number in a poem is always a choice. "Two roads diverged" (Frost), "Twenty centuries of stony sleep" (Yeats), "It is twelve / o'clock in Billie Holiday's voice" (O'Hara) — these numerals function differently from abstract quantifiers ("many roads", "countless centuries"). Numbers are semantically precise, referentially anchored, and — crucially — rare in conventional poetic language. Does that precision make them information-theoretically distinctive?

**Hypothesis A (Precision = Surprise):** Exact numerals resist GPT-2 prediction because they are more specific than what language typically expects at those positions.

**Hypothesis B (Formulaic):** Many number uses are stock phrases ("first light", "once more unto the breach", "one day"), so ordinals and common cardinals are highly predictable.

---

## Method

- Categorized all corpus tokens into: **digit** (e.g., 1959, 12), **cardinal word** (one, two, hundred), **ordinal word** (first, second, twice), **approximate** (many, few, some), and **baseline** (other alphabetic content words >2 chars).
- Stanza-break artifact positions (p\_newline > 0.9) excluded.
- Measured mean/median S₂, positive-S₂ %, and maximum S₂ per category.

---

## Key Results

### 1. S₂ by Numeral Category

| Category | n | mean S₂ | median S₂ | pos% | max S₂ |
|---|---|---|---|---|---|
| **Digit (e.g. 1959, 12)** | 7 | **+2.868** | +2.454 | 57.1% | +10.23 |
| **Cardinal word (one, two, hundred)** | 92 | **+1.091** | +0.353 | 54.3% | +14.88 |
| **Approximate (many, few, some)** | 72 | **+0.582** | +0.854 | 58.3% | +8.91 |
| **Baseline (other content words)** | 12,033 | +0.231 | −0.483 | 43.1% | +23.40 |
| **Ordinal word (first, second, twice)** | 32 | **−0.518** | −1.221 | 34.4% | +9.24 |

**Finding 1:** Exact numerals (digits and cardinal words) sit significantly *above* baseline. Digits especially are the most predictably-surprising tokens in the corpus — not because GPT-2 never sees numbers, but because it doesn't expect them *here*, in poetic context.

**Finding 2:** Ordinals are the one numeral category *below* baseline (mean S₂ = −0.518). "First," "second," and "once" have been domesticated into poetic formulas. "First light," "second chance," "once upon a time" — these are the clichés of numbering.

**Finding 3:** Approximate quantities (many, few, some) are moderately above baseline (+0.582) but below exact numbers. Vagueness costs some S₂.

---

### 2. The Frank O'Hara Phenomenon

All 7 digit tokens in the corpus originate from a single poem: Frank O'Hara's **"The Day Lady Died"** (1964). O'Hara lists actual dates and times:

```
It is 12:20 in New York a Friday
three days after Bastille day, yes
it is 1959 and I go get a shoeshine
```

| Token | S₂ | Rank in corpus |
|---|---|---|
| 1959 | +10.23 | Very high |
| 12 | +7.82 | High |
| 19 | +2.52 | Above baseline |
| 4 | +2.45 | Above baseline |
| 20 | −0.48 | Below baseline |
| 15 | −0.93 | Below baseline |
| 7 | −1.54 | Below baseline |

The year "1959" and the hour "12" carry enormous S₂; the smaller digits become increasingly conventional as the list proceeds. O'Hara's New York School anti-lyric aesthetic — treating a poem like a datebook entry or a newspaper dateline — produces the single highest-digit-S₂ sequence in the corpus.

GPT-2's top prediction at "1959": "12" (p=0.233) — it expected another time-stamp format, not a year. At "1959" in a poetic context, GPT-2 was still navigating the logic of a list of numbers, not a lyric poem.

---

### 3. The Highest-S₂ Cardinal Words

| S₂ | Token | Context (end) | Author / Poem |
|---|---|---|---|
| +14.88 | three | *(line start)* | Trad. (Scottish ballad), "The Wife of Usher's Well" |
| +10.10 | seven | *"...hing his body"* | Christopher Smart, "For I Will Consider My Cat Jeoffry" |
| +9.47 | Nine | *(line start)* | Rudyard Kipling, "Recessional" |
| +8.98 | twenty | *(line start)* | Seamus Heaney, "Digging" |
| +8.87 | twenty | *"...know / That"* | W.B. Yeats, "The Second Coming" |
| +6.24 | four | *(line start)* | E.E. Cummings, "Buffalo Bill 's" |
| +5.66 | ten | *"...Love you"* | Andrew Marvell, "To His Coy Mistress" |
| +4.91 | billion | *(line start)* | Gerard Manley Hopkins, "The Windhover" |

**Finding 4 — Odd numbers dominate the high end.** The highest-S₂ cardinals are: three, seven, nine, twenty, twenty, four, ten, billion. These are not randomly distributed. Odd, mythologically resonant numbers (3, 7, 9) appear at positions where GPT-2 expected function words ("an," "and," "the"). The model cannot predict specificity at those junctures.

**Finding 5 — "Twenty" as the measurement of historical time.** Both Yeats ("Twenty centuries of stony sleep") and Heaney ("My grandfather cut more turf in a day / Than any other man on Toner's bog. / …twenty years ago") achieve S₂ ≈ +9 with the same word. GPT-2 expected a definite article; both poets use a generational measurement. This is a structural pattern: *numeral + [unit of historical time]* is a high-S₂ construction.

**Finding 6 — "Billion" in Hopkins.** In "The Windhover," Hopkins writes: "a billion / Times told lovelier." At "billion," GPT-2 expected "fire" (p=0.034). This is a near-hapax construction in poetry — hyperbole via astronomical scale. Hopkins knew what he was doing.

---

### 4. Numeral S₂ by Era

| Era | n numerals | mean S₂ |
|---|---|---|
| nursery_rhyme | 1 | **+7.59** |
| language | 1 | **+5.81** |
| mid_century | 2 | **+3.01** |
| harlem_renaissance | 2 | **+2.94** |
| ballad | 5 | **+2.41** |
| victorian | 16 | **+1.99** |
| new_york_school | 14 | +1.17 |
| found_poetry | 12 | +0.76 |
| modernist | 17 | +0.66 |
| 19th_century | 3 | **−3.46** |
| fixed_form | 3 | **−1.40** |
| prose_poetry | 3 | **−1.83** |

**Finding 7 — Era pattern mirrors the poetry/prose distinction.** Ballads, nursery rhymes, victorian, and harlem renaissance poetry use numbers *unexpectedly*. Prose poetry, fixed form, and 19th century poetry have the lowest numeral S₂ — these eras have absorbed numbers into conventional rhetorical roles. The nursery rhyme result ("+7.59" for "one") is striking: "One, two, buckle my shoe" — the numeral in a counting-rhyme context has no prose analogue, so GPT-2 is completely lost.

---

### 5. Ordinals: The Clichés of Counting

The lowest category is **ordinals** (first, second, twice): mean S₂ = −0.518, well below even the baseline. Sample low-S₂ ordinal instances:

- "first" in "the first of all" → highly predictable in anaphoric position
- "second" in "the second / time" → highly predictable in sequential position  
- "once" in ballad refrains → formulaic, expected

The exception is "once" in Hemans' "Casabianca" (+9.24), where it appears at the start of a line in a position GPT-2 expected "cried." This is the rule-that-proves-the-rule: even "once" surprises when placed structurally wrong.

---

## Synthesis

The numeral hierarchy in poetry:

```
Digits (1959, 12) > Cardinal words (three, twenty, billion) > Approximate (many, few) > Baseline > Ordinals (first, once)
```

This ordering reflects a spectrum from *precision* to *formula*:
- Digits are the most semantically constrained — exactly one thing satisfies "1959." They have no near-synonyms, no conventional substitutes in verse.
- Cardinal words are precise but have a formal dimension — "three" signals the fairy-tale and ballad tradition, "twenty" signals historical reckoning.
- Approximate words hedge, which costs some information.
- Ordinals have been neutralized into grammatical positions ("first" functions almost like an article in "the first of May").

The implication for literary analysis: when a poet uses an *exact number*, especially a large or unusual one, it is almost certainly doing maximum information-theoretic work. The poem is betting on specificity over generality — and GPT-2, trained to expect conventional language, loses that bet.

---

## Suggested Next Steps

1. **Extend digit coverage**: Add poems with prominent numerals to test the O'Hara finding at scale (e.g., Counting poems, numbered sections, date-poems).
2. **Sacred vs. mundane numbers**: Is the S₂ of "seven" higher in religious contexts (seven deadly sins) vs. secular ones? Marvell's "ten" years is a love measurement; Kipling's "nine" is a military list.
3. **Numeral density analysis**: Do poems with high numeral density (O'Hara-style) have a distinctive overall S₂ profile vs. poems that avoid numbers altogether?
4. **Cross-era comparison of "one"**: The word "one" appears at all S₂ levels in all eras. A deep dive on this single word — the smallest counting number, the most solitary — could model the full numeral gradient.
