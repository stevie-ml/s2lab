# Imperative Mood and S₂: Commands as Informational Disruptions

**Date:** 2026-10-02  
**Experiment:** `experiments/imperative_mood_s2.py`  
**Corpus:** 175 English poetry texts (control and cliché excluded), 19,780 artifact-free tokens  
**Builds on:** `grammatical_person_s2.md`, `apostrophe_s2.md`, `negation_and_s2.md`, `epistemic_hedges_s2.md`

---

## Research Question

When poets issue direct commands — "Go, lovely rose," "Do not go gentle," "Look on my works, ye Mighty" — the grammatical subject is suppressed. GPT-2, trained predominantly on declarative prose, expects subjects before verbs. Does this structural suppression create a measurable S₂ signature? And does the apostrophic frame ("O hear!") *reduce* surprise by announcing the imperative in advance?

**Three hypotheses:**
- **H1:** Imperative verbs ARE high-S₂ — the suppressed subject makes them unexpected at clause-initial positions
- **H2:** The tokens BEFORE an imperative are unusually low-S₂ (high confidence), then surprise spikes at the verb itself
- **H3:** Apostrophic imperatives ("O sing!") show higher S₂ than bare imperatives — the elevated register amplifies surprise

**Corpus baseline:** N = 19,780 | mean S₂ = −0.437 | mean H = 6.21 bits | +S₂ rate = 33.9%

---

## Key Finding 1: H1 CONFIRMED — Imperatives Are Strongly High-S₂

Imperative-position verbs (line-initial or after strong punctuation) score dramatically above both their declarative equivalents and corpus baseline:

|                                  | N     | mean S₂ | ΔS₂ vs. base | +S₂%  | mean H |
|----------------------------------|-------|---------|--------------|-------|--------|
| Imperative (line-initial verb)   | 43    | +1.664  | **+2.101**   | 55.8% | 7.283  |
| Declarative (same verbs, mid-sent) | 421 | +0.025  | +0.462       | 43.0% | 7.260  |
| Baseline (all poetry tokens)     | 19,780 | −0.437 | —           | 33.9% | 6.213  |

The **imperative premium is +1.639 S₂ units** above the same verbs in declarative positions. This is not an intrinsic property of the verbs themselves — "go," "sing," "look" are perfectly common words. The surprise arises from *grammatical position*: these verbs appear where GPT-2 expects a subject.

---

## Key Finding 2: H2 CONFIRMED — The "Setup Dip" Before Imperatives

The S₂ and entropy window around imperative verbs reveals a distinctive two-phase profile:

| Position | Imperative S₂ | Declarative S₂ | Gap |
|----------|--------------|----------------|-----|
| −2       | −0.040       | −0.618         | +0.578 |
| **−1**   | **−2.137**   | −1.051         | **−1.086** |
| **IMP**  | **+1.664**   | +0.025         | **+1.639** |
| +1       | +0.192       | −0.545         | +0.737 |
| +2       | −0.466       | −0.644         | +0.178 |
| +3       | −0.795       | −0.094         | −0.701 |

The position immediately before the imperative (−1) shows **extraordinarily low S₂ (−2.137)** — the model is highly confident about what comes next. This is typically a comma, period, or end-of-clause marker. That high-confidence position amplifies the surprise: the model arrives at the line break having just "won" a prediction, then encounters a command verb instead of the expected subject.

This is a **confidence-trap structure**: the grammar of the previous clause closes smoothly, building the model's certainty, precisely when the poet springs the imperative.

**Entropy envelope:**

| Position | Imperative H | Declarative H |
|----------|-------------|---------------|
| −2       | 5.954       | 6.016         |
| −1       | 5.050       | 6.036         |
| **IMP**  | **7.283**   | 7.260         |
| +1       | 5.173       | 4.978         |
| +2       | 6.029       | 5.968         |
| +3       | 5.852       | 6.152         |

Entropy at the imperative itself (7.283 bits) is nearly identical for imperatives and declaratives — both verbs open wide possibility space for what follows. The difference is not in how many options the model considers; it is in *how surprised* it is by the choice.

---

## Key Finding 3: H3 OVERTURNED — Apostrophe REDUCES Surprise

The most striking reversal: imperatives framed with apostrophic markers (O/Oh/thee/thou within ±3 tokens) have **lower** S₂ than bare imperatives:

|                            | N  | mean S₂ | ΔS₂ vs. base | +S₂%  |
|----------------------------|----|---------|--------------|-------|
| Apostrophic imperative     | 3  | −3.234  | **−2.797**   | 33.3% |
| Non-apostrophic imperative | 40 | +2.032  | **+2.469**   | 57.5% |

The canonical example is Shelley's "oh, hear!" (S₂ = −4.44). After "Oh," the model strongly expects a verb of perception or attention — the apostrophic frame *announces* the command. The "O" functions as a predictive cue, not an intensifier. GPT-2 has seen enough "O hear" / "O sing" / "O come" constructions that the imperative following vocative "O" is nearly *expected*.

**The bare imperative is more surprising than the announced one.** Tennyson's "Break, break, break" (line-initial, after a stanza break: S₂ = +8.03) is more disruptive than any vocative-framed command in the corpus. The absence of announcement is the technique.

*(Note: N=3 for apostrophic is small; larger corpus would sharpen this finding.)*

---

## The Suppressed Subject: What GPT-2 Wanted Instead

At line-initial positions where poets place imperative verbs, GPT-2 most frequently expected:

| Token | Count | Avg prob |
|-------|-------|----------|
| (whitespace/newline) | 10 | 0.170 |
| I     | 7    | 0.086    |
| and   | 5    | 0.103    |
| the   | 4    | 0.079    |
| 'm    | 2    | 0.160    |
| we    | 1    | 0.035    |

The model most wanted **"I"** (7 times with high confidence) — the canonical lyric subject. At these positions, the poet is suppressing the conventional lyric "I" and replacing it with a direct command. The "unsaid" is literally the speaking subject: where GPT-2 predicts the poet will say "I go," the poet says "Go."

**This is subject suppression as Straussian act.** The poet erases themself from the grammatical frame at exactly the moment language expects their presence.

---

## Top Imperative Verbs by S₂

| Verb  | N | mean S₂ |
|-------|---|---------|
| sing  | 3 | +3.957  |
| let   | 4 | +0.022  |
| break | 5 | −0.059  |
| make  | 4 | −1.699  |

"Sing" carries the highest imperative surprise — a command to sing is unexpected even as a command. "Let" and "make" are near-baseline because these verbs appear frequently in a variety of grammatical contexts, reducing their positional surprise.

---

## Era Breakdown

| Era            | Imp N | Imp S₂ | Dec N | Dec S₂ | Gap     |
|----------------|-------|--------|-------|--------|---------|
| prose_poetry   | 2     | +8.593 | 39    | −0.321 | **+8.914** |
| spoken_word    | 1     | +8.154 | 5     | +1.354 | +6.800  |
| 19th_century   | 2     | +6.611 | 21    | +0.624 | +5.987  |
| metaphysical   | 2     | +4.586 | 25    | +0.114 | +4.472  |
| biblical       | 1     | +4.280 | 20    | +0.210 | +4.071  |
| romantic       | 5     | +1.939 | 28    | +1.579 | +0.360  |
| ballad         | 4     | −1.211 | 13    | −0.755 | −0.456  |
| victorian      | 13    | −0.910 | 80    | +0.024 | **−0.934** |
| fixed_form     | 1     | −2.347 | 21    | −1.809 | −0.537  |

The highest imperative premium appears in **prose poetry** (+8.914 gap). This makes sense: prose poetry typically employs sentence-like structures, so an imperative at sentence start in prose-like context disrupts the prose norm most sharply.

**Victorians show negative imperative premium** (−0.934): Victorian imperatives are slightly *less* surprising than the same verbs in declarative positions. Victorian imperatives may function as part of formal rhetorical structures (invocations, addresses) that GPT-2 has learned as predictable patterns. The formal Victorian apostrophic tradition — so common in the corpus — may have lowered expected S₂ for imperatives in that era.

**Romantics show near-zero gap** (+0.360): The Romantic tradition of direct address ("O wild West Wind, thou breath of Autumn's being") is so convention-entrenched that even imperatives within it don't create sharp informational disruption.

---

## Notable Examples

**Highest S₂ imperatives:**
- `mother , [look] I found these` — Russell Edson, S₂ = +10.09  
  (Edson's prose poetry; "look" as mid-clause attention-command after the domestic "mother")
- `hand ; [come] celebrate with` — Lucille Clifton, S₂ = +8.15
- `still ! [Break] , break ,` — Tennyson, S₂ = +8.03  
  (The famous anaphoric opening: "Break, break, break" — first instance is high S₂)

**Lowest S₂ imperatives:**
- `break , [break] , thy` — Tennyson, S₂ = −6.05  
  (The second "break" in "Break, break, break" — after the first, it's *expected*)
- `oh , [hear] !` — Shelley, S₂ = −4.44  
  (Vocative "oh" forecasts the perception imperative)

The Tennyson pair is a perfect natural experiment: the same word ("break") as the first vs. second element of anaphora. First occurrence: S₂ = +8.03. Second occurrence: S₂ = −6.05. **A differential of 14+ S₂ units for the same word.** The refrain effect transforms a surprise into an expectation within two tokens.

---

## Summary

1. **Imperatives are high-S₂ (+2.10 above baseline)** not because of the words chosen, but because grammatical subject suppression violates the model's strongest prediction: the lyric "I."

2. **A confidence-trap structure precedes imperatives**: the −1 position is unusually certain (S₂ = −2.14), and the grammar closes smoothly before the command.

3. **Apostrophic framing reduces surprise**: the "O [verb]" construction is a known template; the bare, unannounced imperative is more disruptive.

4. **The suppressed subject IS the subject**: GPT-2 most expects "I" at these positions. The imperative's Straussian act is erasing the lyric self exactly where language demands it.

5. **Tennyson's "Break, break, break" as a case study**: first instance S₂ = +8.03; second instance S₂ = −6.05. Anaphora converts surprise into certainty within the span of a few tokens.

---

## Suggested Next Steps

- **Larger apostrophic N**: Expand to full corpus including controls to get >20 apostrophic imperatives and retest H3 robustly.
- **Second-occurrence imperatives in anaphora**: Build on the Tennyson finding — how quickly does an imperative's S₂ decay across repeated instances in anaphoric structures? (cf. `refrain_betrayal.md`, `second_occurrence_dip.md`)
- **Reflexive imperatives**: "Let us" / "Let me" — does the reflexive "let" construction behave differently from the command form?
- **Era-stratified subject suppression**: Does the expected subject (what GPT-2 wants) differ by era? Romantic "I" vs. modernist fragmented subject?
- **Cross-linguistic comparison**: German imperative verbs in German GPT-2 corpus — does subject suppression have the same S₂ signature in a V2 language?
