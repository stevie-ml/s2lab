"""
Translation and S2: Does the Straussian Gap survive translation?

Compare multiple English translations of the same source poem.
If S2 is capturing something real about the poem's semantic content,
translations should cluster together. If it's measuring English style
choices, translators should diverge.

Test cases:
1. Bashō's "Old Pond" haiku — 6 famous English translations
2. Rilke's "Archaic Torso of Apollo" — 4 translations
3. Catullus 5 ("Vivamus mea Lesbia") — 4 translations
4. Rumi's "The Guest House" — 3 translations
"""

import sys
import os
import json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import torch
from transformers import GPT2LMHeadModel, GPT2TokenizerFast
import numpy as np

# Load model
tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")
model.eval()

TRANSLATIONS = {
    "basho_old_pond": {
        "source": "Matsuo Bashō (松尾芭蕉), 1686 — 古池や kawazu tobikomu mizu no oto",
        "variants": [
            {
                "translator": "R.H. Blyth (1949)",
                "text": "The old pond;\nA frog jumps in —\nSound of water."
            },
            {
                "translator": "Harold Henderson (1958)",
                "text": "Old dark sleepy pool\nquick unexpected frog\ngo plop! watersplash"
            },
            {
                "translator": "Allen Ginsberg (1978)",
                "text": "The old pond—\na frog jumps in,\nplunk!"
            },
            {
                "translator": "Robert Hass (1994)",
                "text": "An old silent pond...\nA frog jumps into the pond.\nSplash! Silence again."
            },
            {
                "translator": "Jane Reichhold (2008)",
                "text": "old pond\na frog jumps in\nthe sound of water"
            },
            {
                "translator": "W.S. Merwin (2012)",
                "text": "the old pond\na frog jumps in\nthe sound of water"
            },
        ]
    },
    "rilke_archaic_torso": {
        "source": "Rainer Maria Rilke, 'Archaïscher Torso Apollos' (1908)",
        "variants": [
            {
                "translator": "Stephen Mitchell (1982)",
                "text": """We cannot know his legendary head
with eyes like ripening fruit. And yet his torso
is still suffused with brilliance from inside,
like a lamp, in which his gaze, now turned to low,

gleams in all its power. Otherwise
the curved breast could not dazzle you so, nor could
a smile run through the placid hips and thighs
to that dark center where procreation flared.

Otherwise this stone would seem defaced
beneath the translucent cascade of the shoulders
and would not glisten like a wild beast's fur:

would not, from all the borders of itself,
burst like a star: for here there is no place
that does not see you. You must change your life."""
            },
            {
                "translator": "C.F. MacIntyre (1940)",
                "text": """We never knew his head and all the light
that ripened in his fabled eyes. But
his torso still glows like a candlelabrum
in which his gaze, turned low, holds fast and bright.

Otherwise the curved breast could not blind you,
nor through the soft turn of the loins could glide
a smile seeking the center where seeds abide.
Otherwise this stone would stand defaced and squat

under the shoulders' diaphanous fall,
and would not shimmer so like the wild beast's fell,
and would not break out of its borders, a star:

for there's no spot that does not see you. You
must alter your life."""
            },
            {
                "translator": "Edward Snow (1991)",
                "text": """We did not know his unheard-of head
where eyes like apples ripened. Yet
his torso's glow persists—like candelabra
where his sight, turned low, still holds its brightness

and steadies. Otherwise the curving breast
would not dazzle you so, nor would a smile
pass through the soft fall of the loins
toward that center where procreation thrived.

Otherwise this stone would stand deformed
beneath the shoulders' diaphanous slope
and not glisten just like wild beasts' fur,

and not break from every edge
of itself like a star: for there is no place
that does not see you. You must change your life."""
            },
            {
                "translator": "Galway Kinnell & Hannah Liebmann (1999)",
                "text": """We did not know his legendary head,
in which the eyeballs ripened. Yet his torso
glows still as a candelabra, in which his gaze,
though turned down low, holds itself and gleams.

Otherwise the curve of his breast wouldn't blind you,
and in the soft turn of the loin a smile
wouldn't seek the center where fertility lay.
Otherwise this stone would stand short and disfigured

under the transparent plunge of the shoulders
and not glisten like the skin of a beast of prey;
and not burst out from every edge of itself

like a star—for here there's no place
that doesn't see you. You must change your life."""
            },
        ]
    },
    "catullus_5": {
        "source": "Gaius Valerius Catullus, Carmina 5 (~55 BCE) — Vivamus, mea Lesbia",
        "variants": [
            {
                "translator": "A.S. Kline (2001)",
                "text": """Let us live, my Lesbia, and let us love,
and let us judge all the rumors of the old men
to be worth just one penny!
The suns are able to fall and rise:
When that brief light has fallen for us,
we must sleep a never ending night.
Give me a thousand kisses, then another hundred,
then another thousand, then a second hundred,
then yet another thousand more, then another hundred."""
            },
            {
                "translator": "Peter Whigham (1966)",
                "text": """Live with me & love me, Lesbia,
& all the loose talk
of stiff-necked elders
— worth not one dried pea!
Suns can set & rise again:
we, when our brief light has set,
sleep one unending night.
Give me a thousand kisses,
a hundred more, another thousand,
another hundred then."""
            },
            {
                "translator": "Horace Gregory (1931)",
                "text": """Come, Lesbia, let us live and love,
nor give a damn what sour old men say.
The sun that sets may rise again
but when our light has sunk into the earth,
it is gone forever.
Give me a thousand kisses,
then another hundred,
then another thousand,
then a second hundred,
then yet another thousand more,
then another hundred."""
            },
            {
                "translator": "Frank O. Copley (1957)",
                "text": """My Lesbia, let's live and love!
The nagging of old-fashioned folk
let's count it all a penny!
Suns can set and suns can rise:
we, when our brief light fades,
must sleep one neverending night.
Give me a thousand kisses, then a hundred,
then another thousand, then a second hundred,
then yet a thousand more, then a hundred."""
            },
        ]
    },
    "rumi_guest_house": {
        "source": "Jalal ad-Din Muhammad Rumi (جلال‌الدین محمد رومی), 13th century — Masnavi",
        "variants": [
            {
                "translator": "Coleman Barks (1995)",
                "text": """This human being is a guest house.
Every morning a new arrival.

A joy, a depression, a meanness,
some momentary awareness comes
as an unexpected visitor.

Welcome and entertain them all!
Even if they're a crowd of sorrows,
who violently sweep your house
empty of its furniture,
still, treat each guest honorably.
He may be clearing you out
for some new delight."""
            },
            {
                "translator": "Kabir Helminski (2000)",
                "text": """The human body is like a guest house:
every morning someone new arrives.

Grief and depression and meanness—
they're all visiting strangers.
Welcome them all in!
Even if they're a group of sadnesses
who violently ransack your house,
still be a kind host to each.
Maybe they're clearing you out
for some new joy."""
            },
            {
                "translator": "A.J. Arberry (1949, scholarly literal)",
                "text": """The human being is a guest-house:
every morning a new guest comes.

Joy and sorrow, and baseness
arrive as unexpected visitors.
Welcome all of them!
Even if they are a troop of sorrows,
violently sweeping your house clean—
yet treat each guest with honor.
Perhaps he is making your house ready
for a fresh delight."""
            },
        ]
    }
}


def compute_s2_tokens(text):
    """Return per-token surprisal, entropy, and s2 values."""
    tokens = tokenizer.encode(text, return_tensors="pt")
    if tokens.shape[1] < 3:
        return []

    with torch.no_grad():
        outputs = model(tokens)
        logits = outputs.logits  # (1, seq_len, vocab)

    results = []
    seq_len = tokens.shape[1]
    for i in range(1, seq_len):
        log_probs = torch.nn.functional.log_softmax(logits[0, i - 1, :], dim=-1)
        probs = torch.exp(log_probs)

        token_id = tokens[0, i].item()
        surprisal = -log_probs[token_id].item()
        entropy = -torch.sum(probs * log_probs).item()
        s2 = surprisal - entropy

        token_str = tokenizer.decode([token_id])
        top_pred_id = torch.argmax(probs).item()
        top_pred_str = tokenizer.decode([top_pred_id])
        top_pred_prob = probs[top_pred_id].item()

        # Skip stanza-break artifacts
        is_artifact = (top_pred_id == tokenizer.encode("\n")[0] and top_pred_prob > 0.9)

        results.append({
            "token": token_str,
            "surprisal": surprisal,
            "entropy": entropy,
            "s2": s2,
            "is_artifact": is_artifact,
            "top_pred": top_pred_str,
            "top_pred_prob": top_pred_prob,
        })

    return results


def analyze_translation_group(group_name, group_data):
    print(f"\n{'='*70}")
    print(f"SOURCE: {group_data['source']}")
    print(f"{'='*70}")

    summary_rows = []
    for variant in group_data["variants"]:
        tokens = compute_s2_tokens(variant["text"])
        clean = [t for t in tokens if not t["is_artifact"]]
        if not clean:
            continue

        s2_vals = [t["s2"] for t in clean]
        avg_s2 = np.mean(s2_vals)
        std_s2 = np.std(s2_vals)
        pct_pos = sum(1 for s in s2_vals if s > 0) / len(s2_vals)
        max_s2 = max(s2_vals)
        max_token = clean[np.argmax(s2_vals)]["token"]
        max_context = "..." + variant["text"][:200]

        # Find the top 3 S2 tokens
        sorted_tokens = sorted(clean, key=lambda x: x["s2"], reverse=True)[:3]

        summary_rows.append({
            "translator": variant["translator"],
            "n_tokens": len(clean),
            "avg_s2": avg_s2,
            "std_s2": std_s2,
            "pct_pos": pct_pos,
            "max_s2": max_s2,
            "max_token": max_token,
            "top3": [(t["token"].strip(), round(t["s2"], 2), t["top_pred"].strip()) for t in sorted_tokens],
        })

    # Print table
    print(f"\n{'Translator':<35} {'n':>4} {'Avg S2':>8} {'Std S2':>7} {'+S2%':>6} {'Max S2':>7} {'Max Token'}")
    print("-" * 85)
    for r in summary_rows:
        print(f"{r['translator']:<35} {r['n_tokens']:>4} {r['avg_s2']:>8.3f} {r['std_s2']:>7.3f} {r['pct_pos']:>5.1%} {r['max_s2']:>7.2f}  {repr(r['max_token'])}")

    print(f"\nTop S2 tokens per translation:")
    for r in summary_rows:
        top3_str = "  ".join(f"'{tok}'({s2}, expected '{exp}')" for tok, s2, exp in r["top3"])
        print(f"  {r['translator'][:30]}: {top3_str}")

    # Compute inter-translation variance in avg S2
    avg_s2_vals = [r["avg_s2"] for r in summary_rows]
    spread = max(avg_s2_vals) - min(avg_s2_vals)
    within_group_std = np.std(avg_s2_vals)

    print(f"\nInter-translation spread in avg S2: {spread:.3f} bits")
    print(f"Std of translation means: {within_group_std:.3f} bits")

    return summary_rows


def main():
    all_results = {}

    for group_name, group_data in TRANSLATIONS.items():
        rows = analyze_translation_group(group_name, group_data)
        all_results[group_name] = {
            "source": group_data["source"],
            "rows": rows
        }

    # Summary: how much do translations vary vs. typical within-poem variation?
    print("\n\n" + "="*70)
    print("CROSS-POEM SUMMARY")
    print("="*70)
    print(f"\n{'Poem':<30} {'Translations':>12} {'Spread':>8} {'Within σ':>10}")
    print("-" * 65)
    for group_name, data in all_results.items():
        rows = data["rows"]
        if len(rows) < 2:
            continue
        avg_s2_vals = [r["avg_s2"] for r in rows]
        spread = max(avg_s2_vals) - min(avg_s2_vals)
        within_std = np.std(avg_s2_vals)
        print(f"{group_name:<30} {len(rows):>12} {spread:>8.3f} {within_std:>10.3f}")

    # Save results
    output_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                               "results", "translation_s2.json")
    # Convert for JSON serialization
    for gn, gd in all_results.items():
        for r in gd["rows"]:
            r.pop("top3", None)  # not JSON-serializable as-is
    with open(output_path, "w") as f:
        json.dump(all_results, f, indent=2)
    print(f"\nResults saved to {output_path}")


if __name__ == "__main__":
    main()
