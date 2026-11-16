"""
Dramatic Monologue and the Self-Betrayal Index

Research question: In dramatic monologue, do the moments where the speaker
unintentionally reveals their true character (self-betrayal moments) show
elevated S2? Can GPT-2's prediction surprise index detect dramatic irony —
the gap between what the speaker intends and what they disclose?

Distinct from irony_s2.py which studied verbal/rhetorical irony. This
examines structural/dramatic irony: the speaker is unaware of what they reveal.
"""

import json
import sys

# Load corpus
data = json.load(open('results/corpus_results.json'))

# -------------------------------------------------------------------------
# 1. Manual annotation of self-betrayal moments
#    For each dramatic monologue, we annotate:
#    - The token (or partial token) that marks a self-betrayal moment
#    - A brief description of the betrayal
# -------------------------------------------------------------------------

BETRAYAL_ANNOTATIONS = {
    'My Last Duchess (complete)': [
        # The murder admission - most famous line in the poem
        # "I gave commands; / Then all smiles stopped together."
        {'token_contains': 'commands', 'description': 'Murder admission: "I gave commands"'},
        # Jealousy over status - the real grievance
        # "ranked / My gift of a nine-hundred-years-old name / With anybody's gift"
        {'token_contains': 'ranked', 'description': 'Status obsession: "she ranked / My gift...with anybody\'s gift"'},
        # The controlling metaphor - Neptune taming a seahorse
        {'token_contains': 'Neptune', 'description': 'Control metaphor: Neptune "taming" = Duke\'s ideal self'},
        # Private contempt fantasized aloud
        {'token_contains': 'disgust', 'description': 'Contempt revealed: "that in you disgusts me"'},
        # Proprietary view of the Duchess as object
        {'token_contains': 'stoop', 'description': 'Pride in not explaining: "I choose Never to stoop"'},
    ],
    'Soliloquy of the Spanish Cloister': [
        # Brother Laurence (the speaker) is the actual villain, not the target
        {'token_contains': 'hate', 'description': 'Hatred revealed through "If hate killed men..."'},
        {'token_contains': 'Gr-r', 'description': 'Opening outburst reveals murderous obsession'},
        {'token_contains': 'Hell', 'description': 'Willingness to damn himself to spite Brother Lawrence'},
        {'token_contains': 'Plena', 'description': 'Fake piety: quoting Latin prayers while plotting'},
    ],
    'The Love Song of J. Alfred Prufrock (middle)': [
        # Prufrock's self-deprecation reveals his paralysis
        {'token_contains': 'Prince', 'description': 'Failed Hamlet identification: "I am not Prince Hamlet"'},
        {'token_contains': 'Hamlet', 'description': 'Explicit self-demotion: "not Prince Hamlet, nor was meant to be"'},
        {'token_contains': 'mermaids', 'description': 'Final abandonment of fantasy: "mermaids singing, each to each"'},
        {'token_contains': 'Lazarus', 'description': 'Grotesque self-image: "like John the Baptist\'s head"'},
        {'token_contains': 'peach', 'description': 'Trivial anxiety: "Do I dare to eat a peach?"'},
    ],
    'Gerontion': [
        # An old man's dissolution and self-knowledge
        {'token_contains': 'fear', 'description': 'Opening fear: "I have lost my passion: why should I need to keep it"'},
        {'token_contains': 'Christ', 'description': 'Failed religious redemption: "In the juvescence of the year / Came Christ the tiger"'},
        {'token_contains': 'whispering', 'description': 'Paranoid self-knowledge: "In depraved May... whispering ambitions"'},
        {'token_contains': 'unnatural', 'description': 'Explicit self-condemnation: "unnatural vices"'},
    ],
    'Tithonus': [
        # Tithonus asks to die — reveals the horror of immortality
        {'token_contains': 'die', 'description': 'Death-wish: central desire for death as release'},
        {'token_contains': 'cold', 'description': 'Aging imagery: "thy cold fingers" — beauty vs decay'},
        {'token_contains': 'Troy', 'description': 'Nostalgia as self-pity: Troy = glorious past vs current decay'},
        {'token_contains': 'whiten', 'description': 'Decay embodied: "I wither slowly in thine arms"'},
    ],
    'Andrea del Sarto': [
        # Andrea admits his technical perfection but moral/spiritual failure
        {'token_contains': 'faultless', 'description': 'The key paradox: "A faultless painter" — technical mastery covering spiritual emptiness'},
        {'token_contains': 'Lucrezia', 'description': 'The faithless wife named lovingly: Andrea\'s self-delusion'},
        {'token_contains': 'cousin', 'description': "The lover's signal: Lucrezia's cousin summons her away from Andrea"},
        {'token_contains': 'reach', 'description': 'The great betrayal: "a man\'s reach should exceed his grasp"'},
        {'token_contains': 'sold', 'description': 'Admission of prostituting art: sold the painting for the King'},
    ],
    'The Bishop Orders His Tomb at Saint Praxed\'s Church': [
        # The Bishop reveals worldly obsession at the moment of death
        {'token_contains': 'basalt', 'description': 'Material obsession at deathbed: marble, basalt, lapis lazuli'},
        {'token_contains': 'vanity', 'description': 'The old vanity unrelinquished: "And then how I shall lie through centuries"'},
        {'token_contains': 'porphyry', 'description': 'Competitive tombstone obsession: comparing with Gandolf'},
        {'token_contains': 'Gandolf', 'description': 'Deathbed rivalry with predecessor bishop'},
    ],
    # === NEW POEMS ADDED ===
    "Porphyria's Lover": [
        # The murderer speaker's narcissistic psychology
        {'token_contains': 'worshipped', 'description': 'Narcissistic revelation: "Porphyria worshipped me: surprise"'},
        {'token_contains': 'strangled', 'description': 'THE MURDER ACT: "And strangled her. No pain felt she"'},
        {'token_contains': 'Word', 'description': 'Final narcissistic certainty: "God has not said a word!"'},
        {'token_contains': 'mine', 'description': 'Possessive climax: "That moment she was mine, mine, fair"'},
        {'token_contains': 'unt', 'description': 'Post-murder eroticism: untightening the stranglehold'},
    ],
    'Ulysses': [
        # Aging hero's restlessness and contempt
        {'token_contains': 'idle', 'description': 'Opening contempt: "It little profits that an idle king"'},
        {'token_contains': 'aged', 'description': 'Dismissal of Penelope: "matched with an aged wife"'},
        {'token_contains': 'savage', 'description': 'Contempt for his people: "unto a savage race"'},
        {'token_contains': 'yield', 'description': 'The heroic refusal as self-delusion: "not to yield"'},
        {'token_contains': 'strove', 'description': 'Retrospective self-aggrandizement: "men that strove with gods"'},
    ],
}

# -------------------------------------------------------------------------
# 2. Extract S2 for annotated tokens
# -------------------------------------------------------------------------

def find_token_s2(poem_tokens, token_contains):
    """Find S2 of tokens that contain the given substring (case-insensitive)."""
    matches = []
    for t in poem_tokens:
        if token_contains.lower() in t['token'].lower():
            matches.append(t['s2'])
    return matches

results = {}
all_betrayal_s2 = []
all_baseline_s2 = []

print("Dramatic Monologue Self-Betrayal Index")
print("=" * 60)

for poem_title, betrayals in BETRAYAL_ANNOTATIONS.items():
    # Find the poem
    poem = next((p for p in data if p['metadata'].get('title') == poem_title), None)
    if poem is None:
        print(f"WARNING: Could not find '{poem_title}'")
        continue

    tokens = poem['tokens']
    all_s2 = [t['s2'] for t in tokens]
    poem_mean = sum(all_s2) / len(all_s2)
    poem_std = (sum((x - poem_mean)**2 for x in all_s2) / len(all_s2))**0.5

    print(f"\n{poem_title}")
    print(f"  Author: {poem['metadata']['author']} ({poem['metadata']['year']})")
    print(f"  Tokens: {len(tokens)}, Mean S2: {poem_mean:+.3f}, Std: {poem_std:.3f}")
    print(f"  Self-betrayal moments:")

    poem_betrayal_s2 = []
    betrayal_details = []

    for ann in betrayals:
        matched = find_token_s2(tokens, ann['token_contains'])
        if matched:
            s2 = matched[0]  # Take first match
            z = (s2 - poem_mean) / poem_std if poem_std > 0 else 0
            poem_betrayal_s2.append(s2)
            all_betrayal_s2.append(s2)
            betrayal_details.append({
                'token': ann['token_contains'],
                'description': ann['description'],
                's2': s2,
                'z_score': z,
            })
            print(f"    [{ann['token_contains']:12s}] S2={s2:+6.2f}  z={z:+5.2f}  — {ann['description']}")
        else:
            print(f"    [{ann['token_contains']:12s}] NOT FOUND")

    # Baseline: all poem S2 values
    all_baseline_s2.extend(all_s2)

    if poem_betrayal_s2:
        betrayal_mean = sum(poem_betrayal_s2) / len(poem_betrayal_s2)
        print(f"  → Betrayal mean S2: {betrayal_mean:+.3f} vs poem mean: {poem_mean:+.3f} (gap: {betrayal_mean - poem_mean:+.3f})")

    results[poem_title] = {
        'metadata': poem['metadata'],
        'summary': poem['summary'],
        'poem_mean_s2': poem_mean,
        'poem_std_s2': poem_std,
        'betrayal_moments': betrayal_details,
        'betrayal_mean_s2': sum(poem_betrayal_s2) / len(poem_betrayal_s2) if poem_betrayal_s2 else None,
    }

# -------------------------------------------------------------------------
# 3. Compare dramatic monologue vs lyric era statistics
# -------------------------------------------------------------------------

print("\n\n" + "=" * 60)
print("Era-Level S2 Statistics")
print("=" * 60)

era_stats = {}
for p in data:
    era = p['metadata'].get('era', 'unknown')
    if era not in era_stats:
        era_stats[era] = []
    era_stats[era].append(p['summary']['avg_s2'])

comparison_eras = ['dramatic_monologue', 'victorian', 'modernist', 'romantic',
                   'confessional', 'contemporary', 'beat', 'language', 'new_york_school']

for era in comparison_eras:
    if era in era_stats:
        vals = era_stats[era]
        mean = sum(vals) / len(vals)
        std = (sum((x - mean)**2 for x in vals) / len(vals))**0.5
        print(f"  {era:25s}: n={len(vals):3d}  mean={mean:+.3f}  std={std:.3f}")

# -------------------------------------------------------------------------
# 4. Grand summary
# -------------------------------------------------------------------------

print("\n\n" + "=" * 60)
print("Self-Betrayal S2 — Grand Summary")
print("=" * 60)

if all_betrayal_s2:
    betrayal_mean = sum(all_betrayal_s2) / len(all_betrayal_s2)
    baseline_mean = sum(all_baseline_s2) / len(all_baseline_s2)

    # Compare betrayal s2 to poem baseline
    print(f"  Annotated betrayal tokens: n={len(all_betrayal_s2)}")
    print(f"  Betrayal mean S2: {betrayal_mean:+.3f}")
    print(f"  All-poem baseline S2: {baseline_mean:+.3f}")
    print(f"  Betrayal vs baseline gap: {betrayal_mean - baseline_mean:+.3f}")

    # Distribution
    high = sum(1 for s in all_betrayal_s2 if s > 5)
    medium = sum(1 for s in all_betrayal_s2 if 1 <= s <= 5)
    low = sum(1 for s in all_betrayal_s2 if s < 1)
    print(f"\n  Betrayal moment distribution:")
    print(f"    High S2 (>5):    {high}/{len(all_betrayal_s2)} = {100*high/len(all_betrayal_s2):.0f}%")
    print(f"    Medium S2 (1-5): {medium}/{len(all_betrayal_s2)} = {100*medium/len(all_betrayal_s2):.0f}%")
    print(f"    Low S2 (<1):     {low}/{len(all_betrayal_s2)} = {100*low/len(all_betrayal_s2):.0f}%")

# Save results
output = {
    'experiment': 'dramatic_monologue_betrayal',
    'poems_analyzed': len(results),
    'betrayal_tokens_total': len(all_betrayal_s2),
    'betrayal_mean_s2': sum(all_betrayal_s2) / len(all_betrayal_s2) if all_betrayal_s2 else None,
    'baseline_mean_s2': sum(all_baseline_s2) / len(all_baseline_s2),
    'era_stats': {era: {'n': len(v), 'mean': sum(v)/len(v)} for era, v in era_stats.items()},
    'poems': results,
}

json.dump(output, open('results/dramatic_monologue_betrayal.json', 'w'), indent=2)
print("\nResults saved to results/dramatic_monologue_betrayal.json")
