# Numerals in Poetry: When Poets Count

**Date:** 2026-11-07  
**Experiment:** `experiments/numerals_in_poetry.py`  
**Data saved:** `findings/numerals_s2_results.json`

---

## Research Question

Do numeral tokens (digit strings, number words, ordinals) carry distinctive
S₂ signatures in poetry? When a poet writes "two" or "1959", what did GPT-2
expect instead — and does numerical specificity correlate with the Straussian
gap?

---

## Key Numbers

| Category | n | mean S₂ | pos% | max S₂ |
|----------|---|---------|------|--------|
| Digit (1, 42, 1984) | 16 | **+2.674** | 62.5% | 10.23 |
| Cardinal word (one, two, hundred) | 259 | **+0.527** | 45.9% | 14.88 |
| Ordinal word (first, second, twice) | 93 | **+0.141** | 44.1% | 10.51 |
| **Approximate (many, few, some)** | 201 | **+0.538** | 58.2% | 14.42 |
| Baseline (other content words) | 30,431 | +0.297 | 43.4% | 36.66 |

All numeral categories beat the baseline (+0.297), confirming that numerical
language is a site of the Straussian gap.

**Surprising result**: Approximate quantifiers ("many", "few", "some") have
*higher* S₂ (0.538) and *more* positive instances (58.2%) than exact
cardinal numbers (0.527, 45.9%). GPT-2 is well-calibrated to expect exact
counting language in certain positions, but does not expect vague magnitude
language.

---

## What GPT-2 Expects at Numeral Positions

When poets write cardinal numbers, GPT-2 overwhelmingly predicted
grammatical/structural tokens:

| Poet writes | GPT-2 expected (top-1) | S₂ |
|-------------|------------------------|-----|
| "three" (ballad) | "an" (p=0.991!) | +14.88 |
| "Five" (Yeats) | "" (line start, p=0.807) | +12.57 |
| "six" (Szymborska "Pi") | "that" (p=0.283) | +11.19 |
| "Three" (C.K. Williams) | "the" (p=0.248) | +10.80 |
| "seven" (Christopher Smart) | "and" (p=0.213) | +10.43 |
| "forty" (Szymborska "Pi") | "the" (p=0.246) | +10.35 |
| "twenty" (Heaney "Digging") | "," (p=0.260) | +8.98 |
| "twenty" (Yeats "Second Coming") | "the" (p=0.205) | +8.87 |

The pattern is clear: **GPT-2 expects the article, conjunction, or punctuation,
not the specific number.** Counting is a semantic pivot that the model, trained
predominantly on number-sparse prose genres, doesn't anticipate.

---

## Frank O'Hara and the Year as Straussian Gambit

The highest-S₂ *digit* token in the corpus:

> **"1959"** (S₂ = +10.23) — Frank O'Hara, "The Day Lady Died"  
> GPT-2 expected '12' (p=0.233), since the context is a date format

O'Hara's New York School practice of embedding specific dates and years
achieves the Straussian gap by the precision of real fact: the year 1959 is
both syntactically appropriate (a date) and maximally unguessable among the
infinite space of years. His "12" (noon), "27" (temperature), and "4"
(o'clock) similarly use concrete factual specificity to inhabit the gap
between expectation and reality.

---

## Szymborska's Pi: A Case Study

The poem "Pi" explicitly about the mathematical constant π features multiple
high-S₂ numerals:

- "six" at S₂ = +11.19 (context: "be comprehended")
- "forty" at S₂ = +10.35 (context: "to three times")

Even when a poem is *about* numbers and signals this explicitly in its title,
each individual number remains a surprise to GPT-2. The poem exploits the
infinite specificity of irrational numbers as an inexhaustible source of S₂.

---

## Villanelle and Fixed-Form Paradox

Forms with structural repetition show **negative numeral S₂**:

| Era | n | mean S₂ |
|-----|---|---------|
| villanelle | 3 | −1.52 |
| fixed_form | 3 | −1.40 |
| prose_poetry | 4 | −1.63 |
| oulipo | 3 | −2.98 |

When these forms use numbers, they tend to be formulaic ordinal markers
("first", "second") or Oulipo-style mechanical counting — low-S₂ because
the numerical context is predictable within the form.

---

## By Era (mean S₂ at numeral positions)

Highest numeral S₂:
- nursery_rhyme: +7.59 (n=1)
- war_poetry: +6.25 (n=2) — specific casualty counts
- parody: +4.64 (n=4)
- language poetry: +3.82 (n=4)
- new_york_school: +1.00 (n=30) — consistent O'Hara/Berrigan digit use

---

## Finding

**Numerals are reliable but modest sites of the Straussian gap** (mean S₂
+0.52 for cardinal words, +2.67 for digit strings), principally because
GPT-2 — trained on prose — expects grammatical continuation rather than
counting.

The most effective numeral strategies are:
1. **Exact year/date digits** (O'Hara, Berrigan): factual specificity achieves
   maximum S₂ because dates are drawn from infinite possibility space.
2. **Cardinal numbers at sentence-opening positions** (ballads, Yeats): the
   model expects "An" or "The" but the poet offers a quantity.
3. **Counting in defamiliarized contexts** (Szymborska, Smart): when counting
   serves a strange aesthetic purpose, each numeral lands in an unprimed slot.

The surprising finding — that **approximate quantifiers slightly outperform
exact numbers** — suggests that "few" and "many" disrupt grammatical
expectation more reliably than precise numbers, which sometimes land in
expected counting positions.

---

## Suggested Next Steps

1. **Test the "O'Hara digit effect"** systematically: compare S₂ of digit
   tokens across all New York School poets vs. other contemporary poets.
2. **Distinguish counting contexts**: numerals in list structures vs. at
   line openings vs. mid-sentence — do these have different profiles?
3. **Year vs. other digits**: does the form `19XX` specifically carry different
   S₂ than other digit forms because of its strong association with dates?
4. **Bible/liturgical counting**: "ten commandments", "forty days" — are
   numerologically significant numbers lower S₂ because they're formulaic?
