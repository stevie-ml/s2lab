# Within-Line Gradient: Where Does Conformity Kick In?

**Date:** 2026-09-27  
**Experiment:** `experiments/within_line_gradient.py`  
**Builds on:** `alternative_landscape_conformity.md`

---

## Research Question

The alternative landscape analysis showed that line-final tokens are highly conformist (82.6% from top-10 alternatives) while line-initial tokens are strongly non-conformist (41.4%). This experiment asks: **is this gradient smooth or does conformity kick in abruptly near line endings?**

Two hypotheses:
- **Smooth gradient**: conformity rises linearly from position 0 to end
- **Threshold effect**: conformity is flat for most of the line, then jumps sharply at the last 2–3 positions when rhyme/meter pressure is felt

---

## From-Start Positions (position 0 = line-initial)

| From-start | n | Avg S₂ | Avg H | % top-10 | Avg rank |
|---|---|---|---|---|---|
| 0 | 1,252 | -0.403 | 7.384 | 47.4% | 469.39 |
| 1 | 1,898 | -0.315 | 7.186 | 48.9% | 408.70 |
| 2 | 1,871 | -0.335 | 6.570 | 57.0% | 350.63 |
| 3 | 1,829 | -0.150 | 6.655 | 53.8% | 378.23 |
| 4 | 1,735 | -0.225 | 6.375 | 56.4% | 304.20 |
| 5 | 1,618 | -0.357 | 6.319 | 59.8% | 295.32 |
| 6 | 1,427 | -0.340 | 6.372 | 58.3% | 250.23 |
| 7 | 1,209 | -0.174 | 6.303 | 59.5% | 307.07 |
| 8 | 945 | -0.150 | 6.043 | 61.4% | 329.07 |

## From-End Positions (position 0 = line-final)

| From-end | n | Avg S₂ | Avg H | % top-10 | Avg rank |
|---|---|---|---|---|---|
| 0 | 1,853 | -0.881 | 5.323 | 76.3% | 124.35 |
| 1 | 1,863 | 0.063 | 6.503 | 53.0% | 330.99 |
| 2 | 1,845 | -0.246 | 6.269 | 58.4% | 363.74 |
| 3 | 1,805 | -0.132 | 6.595 | 54.0% | 341.93 |
| 4 | 1,703 | -0.272 | 6.566 | 56.2% | 353.10 |
| 5 | 1,558 | -0.166 | 6.768 | 53.1% | 392.79 |
| 6 | 1,352 | -0.296 | 6.798 | 52.5% | 375.34 |
| 7 | 1,128 | -0.379 | 6.853 | 52.6% | 351.14 |
| 8 | 874 | -0.442 | 6.975 | 52.4% | 338.34 |

## Relative Position (0.0 = line-start, 1.0 = line-end)

| Rel pos | n | Avg S₂ | % top-10 |
|---|---|---|---|
| 0.0 | 1,252 | -0.403 | 47.4% |
| 0.1 | 1,258 | -0.487 | 48.5% |
| 0.2 | 1,608 | -0.271 | 55.9% |
| 0.3 | 1,270 | -0.320 | 53.8% |
| 0.4 | 1,437 | -0.139 | 53.4% |
| 0.5 | 1,305 | -0.333 | 57.3% |
| 0.6 | 1,427 | -0.279 | 57.9% |
| 0.7 | 1,264 | -0.049 | 54.6% |
| 0.8 | 1,597 | -0.033 | 57.1% |
| 0.9 | 1,241 | -0.068 | 53.6% |
| 1.0 | 1,853 | -0.881 | 76.3% |

## Conformity Jumps (step-by-step from far to near line-end)

Positive = conformity increases as we get closer to the end.

| Step | Δ% top-10 |
|---|---|
| 1->0 (from_end 1->0) | +23.3pp |
| 2->1 (from_end 2->1) | -5.4pp |
| 3->2 (from_end 3->2) | +4.4pp |
| 4->3 (from_end 4->3) | -2.2pp |
| 5->4 (from_end 5->4) | +3.1pp |
| 6->5 (from_end 6->5) | +0.6pp |
| 7->6 (from_end 7->6) | -0.1pp |
| 8->7 (from_end 8->7) | +0.2pp |

## Era Breakdown: % Top-10 by From-End Position

| Era | FE=3 | FE=2 | FE=1 | FE=0 (final) | Δ(0−3) |
|---|---|---|---|---|---|
| 18th_century | 28.6% | 71.4% | 35.7% | 85.7% | +57.1pp |
| german_modernist | 19.0% | 66.7% | 50.0% | 65.0% | +46.0pp |
| early_modern | 35.3% | 41.2% | 33.3% | 78.0% | +42.7pp |
| cliche_control | 60.0% | 72.2% | 77.8% | 100.0% | +40.0pp |
| metaphysical | 44.0% | 56.0% | 38.0% | 82.4% | +38.4pp |
| mid_century | 41.7% | 46.2% | 67.9% | 78.6% | +36.9pp |
| romantic | 45.6% | 56.6% | 45.5% | 81.0% | +35.4pp |
| song_lyrics | 68.3% | 70.7% | 73.2% | 97.6% | +29.3pp |
| ballad | 60.5% | 61.4% | 51.1% | 88.2% | +27.8pp |
| 19th_century | 53.7% | 58.5% | 56.6% | 81.1% | +27.4pp |
| nursery_rhyme | 68.8% | 68.8% | 56.2% | 93.8% | +25.0pp |
| german_symbolist | 26.5% | 38.7% | 47.1% | 50.0% | +23.5pp |
| victorian | 52.3% | 57.9% | 45.1% | 74.6% | +22.3pp |
| german_expressionist | 37.0% | 46.4% | 53.8% | 57.1% | +20.1pp |
| fixed_form | 56.7% | 58.2% | 59.2% | 75.0% | +18.3pp |
| harlem_renaissance | 63.2% | 55.2% | 35.6% | 81.0% | +17.9pp |
| found_poetry | 66.9% | 71.8% | 78.5% | 84.6% | +17.7pp |
| confessional | 53.5% | 46.7% | 53.3% | 68.9% | +15.4pp |
| modernist | 53.1% | 58.2% | 52.4% | 67.3% | +14.2pp |
| spoken_word | 60.7% | 58.6% | 44.4% | 71.4% | +10.7pp |
| haiku | 48.8% | 50.0% | 39.6% | 57.7% | +8.9pp |
| contemporary | 65.8% | 56.1% | 60.5% | 74.4% | +8.6pp |
| language | 66.7% | 50.0% | 56.2% | 75.0% | +8.3pp |
| prose_poetry | 67.4% | 64.0% | 56.1% | 75.4% | +8.0pp |
| new_york_school | 60.0% | 58.1% | 57.1% | 65.9% | +5.9pp |

## Analysis

**Verdict: THRESHOLD EFFECT** (max jump = 23.3pp, mean jump = 4.9pp, ratio = 4.8x)

The largest single conformity increase occurs at step **1->0** (+23.3pp). The total conformity range across the line is 23.9pp.

### The Cliff-Edge: Conformity Is a Single-Token Phenomenon

The gradient is not a gradient at all. Positions from_end=1 through from_end=8 all cluster tightly between 52–59% top-10 conformity. Then, at from_end=0 (the very last token of the line), conformity jumps to 76.3% — a **23.3pp cliff** occurring in a single step.

This means: **the poet's freedom to surprise ends precisely at the line's last word, not the last few words.** There is no multi-token "build-up" toward the ending. Positions from_end=5 through from_end=1 are informationally equivalent — all treated as medial territory where the poet exercises similar discretion.

### The Penultimate Surprise

The second-to-last position (from_end=1, 53.0%) is actually *lower* than from_end=2 (58.4%) and from_end=3 (54.0%). The penultimate token may be where poets "spend" a last deviation budget before the forced conformist ending — a final surprise before submission. Its avg S₂ (+0.063) is the highest of any from-end position, compared to −0.881 at the final token. This asymmetry is striking: the last-but-one position is the most exploratory in the line.

### Why from_end=0 Has Lower Entropy

The avg entropy at from_end=0 (H=5.32) is ~1.5 bits lower than from_end=1 (H=6.50). By the time GPT-2 has read the full line content, it becomes more confident about possible line endings — a natural context-narrowing. Yet the **alternative_landscape** experiment showed that the *dispersion* of GPT-2's predictions at line-final positions is actually *higher*. The lower H here reflects GPT-2's own certainty about the next token, not a constrained alternative space. The poet is conforming into a wide but low-surprisal field.

### Era Variation Confirms "Active Conformity"

The threshold effect size varies dramatically by tradition, strongly correlated with formal constraint:

- **18th century** (+57.1pp): highest threshold, reflecting strict couplet and heroic verse conventions where the final word is essentially forced
- **Early modern / Metaphysical** (+42.7pp, +38.4pp): formal traditions with strong closure norms
- **Language poetry** (+8.3pp), **New York School** (+5.9pp): weakest thresholds — these traditions actively resist conventional endings, treating line-breaks as syntactic disruptions rather than semantic resolutions
- **Haiku** (+8.9pp): the kireji occupies a near-final position and is often itself unexpected; the line's "ending" is semantically open

The avant-garde eras show a threshold of ~8–9pp, still positive — even Language poets conform somewhat at line ends — but the traditional eras show a 5–7× stronger effect. The cliff-edge is a choice encoded in tradition, not in language itself.

---

## Suggested Next Steps

1. **Rhymed vs. free verse split**: Does the threshold position differ between rhymed poems (where end-pressure is phonetic) and free verse (where it may be purely syntactic)?
2. **Line-length interaction**: Does the threshold position scale with line length or stay fixed (e.g., always at from_end=1 regardless of line length)?
3. **Token type at threshold**: What kinds of tokens occupy the threshold position? Are they adjectives (pre-nominal) or prepositions (pre-object)?
4. **The penultimate surprise**: Is from_end=1's elevated S₂ (+0.063, highest in the line) consistent across eras, or specific to traditions where the penultimate carries special semantic weight (e.g., the turn before the closing couplet)?
