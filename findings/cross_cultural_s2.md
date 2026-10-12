# Cross-Cultural Poetic Signatures: S2 in Non-Western Traditions

**Date:** 2026-10-12
**Experiment:** `experiments/cross_cultural_s2.py`
**New eras added:** classical_chinese (4 poems), persian (2 poems), japanese_classical (2 poems)

## Research Question

Do poems from Classical Chinese (Tang Dynasty, ~700-760 CE), Persian (Khayyam/Rumi, ~12th-13th c.), and Japanese classical (tanka, ~880-905 CE) traditions show distinctive information-theoretic profiles when analyzed in English translation, compared to Western poetry of similar periods?

Four hypotheses tested:

- **H1 (Terse Syntax):** Classical Chinese translations, characterized by ellipsis and parataxis, should produce higher artifact-free S2 because they violate English clause-structure expectations.
- **H2 (Sufi Paradox):** Persian Sufi poetry's mystical imagery should produce higher S2 than comparable Western court/lyric verse.
- **H3 (Tanka Arc):** Japanese tanka should have a different S2 distribution shape than haiku — the coda (7-7) resolves the opening image, potentially dropping S2 there.
- **H4 (Translation Flattening):** Alternatively, translators may normalize exotic syntax into conventional English, producing LOWER S2 than native English poems of comparable age.

## Individual Poem Results: New Eras

### classical_chinese (n=4)

| Poem | Author | Year | Avg S2 (clean) | +S2% | Max S2 | Avg H |
|---|---|---|---|---|---|---|
| Quiet Night Thoughts (literal trans.) | Li Bai | 726 | **-0.342** | 28% | 13.28 | 5.75 |
| On the Tower of Yellow Crane (literal trans.) | Cui Hao | 730 | **-0.512** | 37% | 14.49 | 6.87 |
| Spring View (literal trans.) | Du Fu | 757 | **-0.534** | 35% | 12.24 | 6.54 |
| Deer Park (literal trans.) | Wang Wei | 740 | **-0.986** | 31% | 6.62 | 7.30 |

### persian (n=2)

| Poem | Author | Year | Avg S2 (clean) | +S2% | Max S2 | Avg H |
|---|---|---|---|---|---|---|
| Rubaiyat of Omar Khayyam (stanzas 7–10) | Omar Khayyam (trans. FitzGeral | 1120 | **-0.186** | 39% | 13.69 | 6.65 |
| Rubaiyat of Omar Khayyam (stanzas 11–14) | Omar Khayyam (trans. FitzGeral | 1120 | **-0.285** | 38% | 12.76 | 6.97 |

### japanese_classical (n=2)

| Poem | Author | Year | Avg S2 (clean) | +S2% | Max S2 | Avg H |
|---|---|---|---|---|---|---|
| Tanka on cherry blossoms (Ariwara no Narihira, lit | Ariwara no Narihira | 880 | **-0.695** | 33% | 5.22 | 5.74 |
| Tanka on longing (Ki no Tsurayuki, literal trans.) | Ki no Tsurayuki | 905 | **-0.715** | 38% | 7.39 | 6.57 |

## Era Comparison: Focus Eras vs. Western Baselines

> Artifact-free S2 (p_newline < 0.9 tokens excluded)

| Era | n poems | Avg S2 | +S2% | Avg H | Max S2 |
|---|---|---|---|---|---|
| haiku | 14 | **0.033** | 37% | 7.07 | 16.65 |
| ancient | 3 | **-0.187** | 40% | 6.75 | 14.33 |
| persian ← **new** | 2 | **-0.235** | 38% | 6.81 | 13.69 |
| victorian | 21 | **-0.305** | 36% | 6.62 | 22.09 |
| imagist | 3 | **-0.403** | 37% | 6.43 | 15.90 |
| modernist | 24 | **-0.405** | 36% | 6.60 | 25.63 |
| romantic | 15 | **-0.470** | 36% | 6.84 | 16.72 |
| metaphysical | 4 | **-0.558** | 37% | 6.83 | 15.36 |
| classical_chinese ← **new** | 4 | **-0.594** | 33% | 6.62 | 14.49 |
| japanese_classical ← **new** | 2 | **-0.705** | 35% | 6.15 | 7.39 |
| control | 5 | **-1.736** | 20% | 5.59 | 7.19 |

## H1: Terse Syntax (Classical Chinese)

Classical Chinese avg S2: **-0.594**
vs. ancient+romantic avg: -0.423 → **LOWER**

**H1 NOT SUPPORTED**: Classical Chinese translations do not show elevated S2 compared to comparable Western poetry — translation flattening (H4) may dominate.

**Terse-syntax indicators:**
- Spring View (literal trans.): avg_s2=-0.534, avg_H=6.54
- Quiet Night Thoughts (literal trans.): avg_s2=-0.342, avg_H=5.75
- Deer Park (literal trans.): avg_s2=-0.986, avg_H=7.30
- On the Tower of Yellow Crane (literal trans.): avg_s2=-0.512, avg_H=6.87

## H2: Sufi Paradox (Persian Poetry)

Persian avg S2: **-0.235**
vs. metaphysical+victorian avg: -0.346 → **HIGHER**

| Poem | Avg S2 | Max S2 | +S2% |
|---|---|---|---|
| Rubaiyat of Omar Khayyam (stanzas 7–10) | -0.186 | 13.69 | 39% |
| Rubaiyat of Omar Khayyam (stanzas 11–14) | -0.285 | 12.76 | 38% |

## H3: Tanka Coda vs. Haiku (Japanese Classical)

| Form | n | Avg S2 | +S2% | Avg H |
|---|---|---|---|---|
| Tanka (5-7-5-7-7) | 2 | **-0.705** | 35% | 6.15 |
| Haiku (5-7-5) | 14 | **0.033** | 37% | 7.07 |

Tanka - Haiku avg S2 gap: **-0.738**

**H3 SUPPORTED**: Tanka shows lower avg S2 than haiku, consistent with the idea that the 7-7 coda provides conventional resolution after the 5-7-5 opening image.

## H4: Translation Flattening?

If translators normalize exotic syntax, all translated non-Western poems should cluster toward LOWER S2 than native English poems of comparable periods.

| Group | n eras | Grand avg S2 |
|---|---|---|
| Native English poetry | 4 | -0.434 |
| Translated non-Western poetry | 3 | -0.511 |

Translated poetry avg S2 is **LOWER** than native English. H4 (flattening) is consistent with this result.

## Notable High-S2 Tokens in New Traditions

| S2 | Token | GPT-2 expected | Prob | Poem |
|---|---|---|---|---|
| 14.49 | `' Par'` | ' the' | 64.0% | Cui Hao, "On the Tower of Yellow Crane (literal tr" |
| 13.69 | `'heed'` | '\n' | 22.3% | Omar Khayyam (trans. FitzGerald, 1859), "Rubaiyat of Omar Khayyam (stanzas 7–10)" |
| 13.28 | `' frost'` | "'s" | 41.2% | Li Bai, "Quiet Night Thoughts (literal trans.)" |
| 12.76 | `' '` | 'And' | 25.5% | Omar Khayyam (trans. FitzGerald, 1859), "Rubaiyat of Omar Khayyam (stanzas 11–14)" |
| 12.32 | `' drop'` | '\n' | 24.0% | Omar Khayyam (trans. FitzGerald, 1859), "Rubaiyat of Omar Khayyam (stanzas 7–10)" |
| 12.24 | `' shorter'` | ' so' | 69.1% | Du Fu, "Spring View (literal trans.)" |
| 11.53 | `' Yellow'` | '\n' | 18.2% | Cui Hao, "On the Tower of Yellow Crane (literal tr" |
| 10.94 | `'ás'` | 'á' | 97.4% | Omar Khayyam (trans. FitzGerald, 1859), "Rubaiyat of Omar Khayyam (stanzas 7–10)" |
| 10.81 | `' underneath'` | ' of' | 13.5% | Omar Khayyam (trans. FitzGerald, 1859), "Rubaiyat of Omar Khayyam (stanzas 11–14)" |
| 10.65 | `' throw'` | ' of' | 13.3% | Omar Khayyam (trans. FitzGerald, 1859), "Rubaiyat of Omar Khayyam (stanzas 11–14)" |
| 10.33 | `' Jam'` | ' the' | 9.0% | Omar Khayyam (trans. FitzGerald, 1859), "Rubaiyat of Omar Khayyam (stanzas 7–10)" |
| 10.25 | `' on'` | 'ed' | 88.0% | Li Bai, "Quiet Night Thoughts (literal trans.)" |
| 9.69 | `'án'` | 'ry' | 65.3% | Omar Khayyam (trans. FitzGerald, 1859), "Rubaiyat of Omar Khayyam (stanzas 11–14)" |
| 9.68 | `' Bes'` | ' ' | 58.3% | Omar Khayyam (trans. FitzGerald, 1859), "Rubaiyat of Omar Khayyam (stanzas 11–14)" |
| 9.42 | `'hm'` | 'r' | 28.7% | Omar Khayyam (trans. FitzGerald, 1859), "Rubaiyat of Omar Khayyam (stanzas 11–14)" |

## Summary and Interpretation

Results are mixed: translated non-Western poetry sits near the center of the native English S2 distribution. Neither strong flattening nor strong elevation is observed. This may mean the information-theoretic signature of these traditions is primarily determined by content (sparse imagery, mystical vocabulary) rather than syntactic structure.

**Next steps:**
1. Add more classical Chinese poems (especially Du Fu's longer regulated verse) to increase n
2. Compare Arabic poetry (pre-Islamic qasida) in translation
3. Test whether *different translators* of the same Chinese poem produce different S2 profiles (cf. `translation_s2.md` methodology applied to Chinese sources)
4. Add Sanskrit poetry (Kalidasa, Bhartrihari) as a test of highly inflected language in translation
