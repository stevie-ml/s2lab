"""
Experiment: Active vs Passive voice and S₂

Hypothesis: Passive voice should produce different entropy/S₂ profiles
because it suppresses the agent and reorders information flow.
GPT-2, trained on predominantly active constructions, should find
passive constructions more surprising — but in predictable ways.
"""

import sys
sys.path.insert(0, "/Users/steviemiller/s2lab")
from engine import analyze_poem

pairs = [
    # Active vs passive pairs
    ("The boy threw the ball across the field.", "The ball was thrown across the field."),
    ("Death kindly stopped for me.", "I was kindly stopped by Death."),
    ("The wind scattered the leaves across the yard.", "The leaves were scattered across the yard by the wind."),
    ("She broke the silence with a whisper.", "The silence was broken with a whisper."),
    ("The emperor rules the kingdom of ice-cream.", "The kingdom of ice-cream is ruled by the emperor."),
    ("Mourners treaded around my brain.", "My brain was treaded around by mourners."),
    ("The poet chose unexpected words.", "Unexpected words were chosen by the poet."),
    ("Lightning struck the ancient oak.", "The ancient oak was struck by lightning."),
]

print("=" * 90)
print("  ACTIVE vs PASSIVE VOICE: Information-Theoretic Comparison")
print("=" * 90)

active_s2s = []
passive_s2s = []
active_surps = []
passive_surps = []
active_ents = []
passive_ents = []

for i, (active, passive) in enumerate(pairs):
    a = analyze_poem(active)
    p = analyze_poem(passive)

    print(f"\n{'─' * 90}")
    print(f"  Pair {i+1}")
    print(f"  Active:  \"{active}\"")
    print(f"  Passive: \"{passive}\"")
    print(f"{'─' * 90}")
    print(f"  {'':30} {'Surprisal':>10} {'Entropy':>10} {'S₂':>10} {'+S₂%':>8}")
    print(f"  {'Active':<30} {a['summary']['avg_surprisal']:>10.2f} {a['summary']['avg_entropy']:>10.2f} {a['summary']['avg_s2']:>10.2f} {a['summary']['pos_s2_ratio']:>7.0%}")
    print(f"  {'Passive':<30} {p['summary']['avg_surprisal']:>10.2f} {p['summary']['avg_entropy']:>10.2f} {p['summary']['avg_s2']:>10.2f} {p['summary']['pos_s2_ratio']:>7.0%}")

    diff_s2 = p['summary']['avg_s2'] - a['summary']['avg_s2']
    diff_surp = p['summary']['avg_surprisal'] - a['summary']['avg_surprisal']
    print(f"  {'Δ (passive - active)':<30} {diff_surp:>+10.2f} {'':>10} {diff_s2:>+10.2f}")

    active_s2s.append(a['summary']['avg_s2'])
    passive_s2s.append(p['summary']['avg_s2'])
    active_surps.append(a['summary']['avg_surprisal'])
    passive_surps.append(p['summary']['avg_surprisal'])
    active_ents.append(a['summary']['avg_entropy'])
    passive_ents.append(p['summary']['avg_entropy'])

    # Show token-level for most interesting pair
    if i == 1:  # Death/Dickinson pair
        print(f"\n  Token-level detail:")
        for voice, result in [("ACTIVE", a), ("PASSIVE", p)]:
            print(f"\n  {voice}:")
            for t in result['tokens']:
                marker = " <<<" if t['s2'] > 3 else ""
                print(f"    {t['token']:<15} surp={t['surprisal']:>6.2f}  ent={t['entropy']:>6.2f}  S₂={t['s2']:>7.2f}  rank={t['rank']}{marker}")

# Summary
print(f"\n\n{'=' * 90}")
print(f"  SUMMARY ACROSS ALL {len(pairs)} PAIRS")
print(f"{'=' * 90}")

import statistics
avg_a_s2 = statistics.mean(active_s2s)
avg_p_s2 = statistics.mean(passive_s2s)
avg_a_surp = statistics.mean(active_surps)
avg_p_surp = statistics.mean(passive_surps)
avg_a_ent = statistics.mean(active_ents)
avg_p_ent = statistics.mean(passive_ents)

print(f"\n  {'':20} {'Avg Surprisal':>14} {'Avg Entropy':>14} {'Avg S₂':>14}")
print(f"  {'Active voice':<20} {avg_a_surp:>14.2f} {avg_a_ent:>14.2f} {avg_a_s2:>14.2f}")
print(f"  {'Passive voice':<20} {avg_p_surp:>14.2f} {avg_p_ent:>14.2f} {avg_p_s2:>14.2f}")
print(f"  {'Δ (passive-active)':<20} {avg_p_surp - avg_a_surp:>+14.2f} {avg_p_ent - avg_a_ent:>+14.2f} {avg_p_s2 - avg_a_s2:>+14.2f}")

# Count how many pairs have higher passive S₂
passive_higher = sum(1 for a, p in zip(active_s2s, passive_s2s) if p > a)
print(f"\n  Passive S₂ > Active S₂ in {passive_higher}/{len(pairs)} pairs")

print(f"\n  INTERPRETATION:")
if avg_p_s2 > avg_a_s2:
    print(f"  Passive voice has HIGHER S₂ ({avg_p_s2:.2f} vs {avg_a_s2:.2f}).")
    print(f"  This means passive constructions deviate MORE from what GPT-2 expects.")
    print(f"  The suppressed agent creates a Straussian gap — the 'who' is the unsaid.")
elif avg_p_s2 < avg_a_s2:
    print(f"  Passive voice has LOWER S₂ ({avg_p_s2:.2f} vs {avg_a_s2:.2f}).")
    print(f"  Passive constructions are MORE predictable once initiated.")
    print(f"  The 'was/were + past participle' pattern is highly formulaic —")
    print(f"  GPT-2 can predict it easily. But this predictability is itself revealing:")
    print(f"  passive voice TRADES surprisal for agent-suppression.")
    print(f"  The information cost is paid up front (surprising 'was'), then the")
    print(f"  construction becomes a low-entropy channel that hides the actor.")
else:
    print(f"  No significant difference detected.")
