"""
Experiment: Technical/Scientific Vocabulary and S₂

Tests whether technical, scientific, or specialized vocabulary appears at systematically
higher S₂ positions in poetry. When poets borrow from chemistry, biology, medicine,
law, mathematics, or technology, they are crossing registers — importing words that
GPT-2 associates with non-literary contexts.

Hypothesis: Technical vocabulary constitutes a form of Straussian register-crossing:
the model is conditioned on lyric context and assigns low probability to specialized
terminology, generating high S₂ at those positions.

Sub-hypotheses:
  H1: Technical tokens have higher S₂ than non-technical tokens on average.
  H2: Technical tokens have higher ENTROPY preceding them (the model is uncertain).
  H3: The effect is stronger in modernist/contemporary poetry than in romantic.
  H4: Some poets use technical vocabulary systematically as an aesthetic strategy.
"""

import json
import os
import statistics
from collections import defaultdict

RESULTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "results")
FINDINGS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "findings")

# Technical/scientific vocabulary by domain
TECHNICAL_LEXICONS = {
    "chemistry": {
        "atom", "atoms", "atomic", "molecule", "molecules", "molecular",
        "element", "elements", "compound", "compounds", "ion", "ions",
        "electron", "electrons", "proton", "protons", "neutron", "neutrons",
        "nucleus", "oxide", "carbon", "hydrogen", "nitrogen", "oxygen",
        "chlorine", "sodium", "calcium", "iron", "magnesium", "phosphorus",
        "sulfur", "sulphur", "nitrogen", "periodic", "valence", "covalent",
        "catalyst", "enzyme", "protein", "proteins", "amino", "acid", "acids",
        "alkali", "alkaline", "acidic", "reaction", "reactant", "solvent",
        "solution", "precipitate", "oxidize", "reduce", "oxidation", "reduction",
        "plasma", "isotope", "isotopes", "radioactive", "radiation",
    },
    "biology": {
        "cell", "cells", "cellular", "gene", "genes", "genetic", "genetics",
        "chromosome", "chromosomes", "dna", "rna", "protein", "proteins",
        "membrane", "nucleus", "cytoplasm", "mitosis", "meiosis",
        "evolution", "evolved", "evolving", "species", "genus",
        "organism", "organisms", "bacteria", "virus", "viruses", "viral",
        "neural", "neuron", "neurons", "synapse", "synaptic", "cortex",
        "cerebral", "cerebrum", "cortical", "axon", "dendrite",
        "photosynthesis", "chlorophyll", "enzyme", "metabolism",
        "carnivore", "herbivore", "omnivore", "predator", "prey",
        "ecosystem", "habitat", "symbiosis", "parasite", "host",
        "mitochondria", "ribosome", "vacuole", "osmosis", "diffusion",
    },
    "physics": {
        "quantum", "quanta", "wave", "particle", "particles",
        "gravity", "gravitational", "mass", "velocity", "acceleration",
        "momentum", "force", "energy", "kinetic", "potential",
        "electromagnetic", "photon", "photons", "electron", "electrons",
        "neutron", "proton", "nucleus", "fission", "fusion",
        "entropy", "thermodynamic", "thermodynamics", "entropy",
        "oscillation", "frequency", "amplitude", "wavelength", "spectrum",
        "refraction", "diffraction", "interference", "resonance",
        "magnetic", "electric", "current", "voltage", "resistance",
        "relativity", "relativistic", "spacetime", "curvature",
        "subatomic", "antimatter", "neutrino", "quark", "boson",
        "trajectory", "parabola", "vector", "scalar", "tensor",
    },
    "medicine_anatomy": {
        "vein", "veins", "artery", "arteries", "capillary", "capillaries",
        "nerve", "nerves", "tendon", "tendons", "ligament", "ligaments",
        "muscle", "muscles", "muscular", "skeletal", "cartilage",
        "trachea", "esophagus", "tonsils", "larynx", "pharynx",
        "intestine", "intestines", "colon", "duodenum", "pancreas",
        "spleen", "thyroid", "adrenal", "pituitary", "hypothalamus",
        "retina", "cornea", "iris", "pupil", "cochlea", "tympanum",
        "diagnosis", "prognosis", "symptom", "symptoms", "pathology",
        "pathological", "hemorrhage", "fracture", "trauma",
        "anesthesia", "anesthetic", "scalpel", "suture", "incision",
        "viral", "bacterial", "infection", "infected", "contagion",
        "immune", "immunity", "antibody", "antibodies", "vaccine",
    },
    "mathematics": {
        "theorem", "theorems", "proof", "proofs", "axiom", "axioms",
        "equation", "equations", "variable", "variables", "coefficient",
        "integer", "integers", "rational", "irrational", "prime",
        "factorial", "exponent", "logarithm", "logarithms",
        "derivative", "derivatives", "integral", "integrals",
        "differential", "calculus", "algebra", "algebraic",
        "geometry", "geometric", "trigonometry", "trigonometric",
        "sine", "cosine", "tangent", "hypotenuse", "radius",
        "diameter", "circumference", "perpendicular", "parallel",
        "bisect", "vector", "matrix", "matrices", "dimension",
        "infinite", "infinity", "finite", "convergent", "divergent",
        "probability", "statistic", "statistics", "median", "mean",
        "standard", "deviation", "variance", "hypothesis",
    },
    "technology": {
        "mechanism", "mechanical", "hydraulic", "pneumatic",
        "electric", "electrical", "circuit", "circuits", "voltage",
        "current", "ampere", "watt", "transistor", "diode", "capacitor",
        "algorithm", "algorithms", "digital", "binary", "analog",
        "frequency", "bandwidth", "signal", "noise", "transmission",
        "combustion", "turbine", "piston", "cylinder", "gear", "gears",
        "valve", "valves", "pump", "pumps", "dynamo", "generator",
        "hydraulic", "pneumatic", "centrifuge", "centrifugal",
    },
    "geology_cosmology": {
        "tectonic", "geological", "sediment", "sediments", "sedimentary",
        "igneous", "metamorphic", "stratum", "strata", "fossil", "fossils",
        "seismic", "volcanic", "tectonic", "erosion", "erosive",
        "galaxy", "galaxies", "nebula", "nebulae", "constellation",
        "asteroid", "comet", "meteor", "meteorite", "orbit", "orbital",
        "equinox", "solstice", "perihelion", "aphelion",
        "gravitational", "stellar", "solar", "lunar", "planetary",
        "atmosphere", "stratosphere", "ionosphere", "troposphere",
    },
}

# All technical words flattened
ALL_TECHNICAL = set()
WORD_TO_DOMAIN = {}
for domain, words in TECHNICAL_LEXICONS.items():
    for w in words:
        wl = w.lower()
        ALL_TECHNICAL.add(wl)
        WORD_TO_DOMAIN[wl] = domain


def classify_token(token_str):
    """Return the technical domain of a token, or None."""
    clean = token_str.strip().lower().strip("'\".,;:!?-()[]")
    # Also try removing leading space (GPT-2 tokenizer often adds Ġ)
    clean2 = clean.lstrip("ġ Ġ")
    for candidate in [clean, clean2]:
        if candidate in WORD_TO_DOMAIN:
            return WORD_TO_DOMAIN[candidate]
    return None


def run_experiment(results_path="corpus_results.json"):
    with open(os.path.join(RESULTS_DIR, results_path)) as f:
        results = json.load(f)

    baseline_s2 = []
    baseline_h = []
    technical_s2 = defaultdict(list)   # domain → [s2]
    technical_h = defaultdict(list)    # domain → [h]
    all_technical_tokens = []          # list of dicts for detailed analysis
    era_technical = defaultdict(list)  # era → [s2]
    era_baseline = defaultdict(list)   # era → [s2]
    poet_technical = defaultdict(list) # poet → [s2]
    poet_baseline = defaultdict(list)  # poet → [s2]
    top_moments = []                   # (s2, token, context, poem, poet, domain)

    NEWLINE_THRESH = 0.9
    MIN_S2 = -30

    for poem_result in results:
        meta = poem_result.get("metadata", {})
        title = meta.get("title", "Unknown")
        author = meta.get("author", "Unknown")
        era = meta.get("era", "unknown")
        tokens = poem_result.get("tokens", [])
        lang = meta.get("language", "en")

        if lang != "en":
            continue

        if era in ("control", "cliche_control"):
            continue

        token_strs = [t.get("token", "") for t in tokens]

        for i, tok in enumerate(tokens):
            s2 = tok.get("s2")
            h = tok.get("entropy")
            p_nl = tok.get("p_newline", 0.0)

            if s2 is None or h is None:
                continue
            if p_nl >= NEWLINE_THRESH:
                continue
            if s2 < MIN_S2:
                continue

            domain = classify_token(tok.get("token", ""))

            if domain is None:
                baseline_s2.append(s2)
                baseline_h.append(h)
                era_baseline[era].append(s2)
                poet_baseline[author].append(s2)
            else:
                technical_s2[domain].append(s2)
                technical_h[domain].append(h)
                era_technical[era].append(s2)
                poet_technical[author].append(s2)
                all_technical_tokens.append({
                    "s2": s2, "h": h, "domain": domain,
                    "token": tok.get("token", ""),
                    "title": title, "author": author, "era": era,
                    "position": i,
                    "context": "".join(token_strs[max(0, i-5):i]),
                })

                if s2 > 2.0:
                    top_moments.append((s2, tok.get("token", ""), title, author, domain,
                                        "".join(token_strs[max(0, i-8):i])))

    # Sort top moments
    top_moments.sort(reverse=True, key=lambda x: x[0])

    # Per-domain summary
    domain_summary = {}
    for domain in TECHNICAL_LEXICONS:
        s2_vals = technical_s2[domain]
        h_vals = technical_h[domain]
        if len(s2_vals) < 3:
            domain_summary[domain] = None
            continue
        domain_summary[domain] = {
            "n": len(s2_vals),
            "mean_s2": statistics.mean(s2_vals),
            "mean_h": statistics.mean(h_vals),
            "pct_positive": sum(1 for x in s2_vals if x > 0) / len(s2_vals),
        }

    # Overall technical vs non-technical
    all_tech_s2 = [x for vals in technical_s2.values() for x in vals]
    all_tech_h = [x for vals in technical_h.values() for x in vals]

    # Poet-level analysis: poets with most technical vocabulary
    poet_counts = {p: len(v) for p, v in poet_technical.items()}
    top_poets = sorted(poet_counts.items(), key=lambda x: x[1], reverse=True)[:12]

    # Era-level: compare technical vs baseline S2 lift per era
    era_lift = {}
    for era in set(list(era_technical.keys()) + list(era_baseline.keys())):
        t_vals = era_technical.get(era, [])
        b_vals = era_baseline.get(era, [])
        if len(t_vals) >= 3 and len(b_vals) >= 5:
            era_lift[era] = {
                "n_tech": len(t_vals),
                "tech_mean": statistics.mean(t_vals),
                "baseline_mean": statistics.mean(b_vals),
                "lift": statistics.mean(t_vals) - statistics.mean(b_vals),
            }

    return {
        "baseline": {
            "n": len(baseline_s2),
            "mean_s2": statistics.mean(baseline_s2) if baseline_s2 else 0,
            "mean_h": statistics.mean(baseline_h) if baseline_h else 0,
        },
        "all_technical": {
            "n": len(all_tech_s2),
            "mean_s2": statistics.mean(all_tech_s2) if all_tech_s2 else 0,
            "mean_h": statistics.mean(all_tech_h) if all_tech_h else 0,
            "pct_positive": sum(1 for x in all_tech_s2 if x > 0) / len(all_tech_s2) if all_tech_s2 else 0,
        },
        "domain_summary": domain_summary,
        "top_moments": top_moments[:20],
        "top_poets": top_poets,
        "era_lift": dict(sorted(era_lift.items(), key=lambda x: x[1]["lift"], reverse=True)),
        "total_technical_tokens": len(all_tech_s2),
    }


def write_findings(data):
    from datetime import datetime
    date_str = datetime.now().strftime("%Y-%m-%d")

    baseline = data["baseline"]
    at = data["all_technical"]
    ds = data["domain_summary"]
    top = data["top_moments"]

    lines = [
        "# Technical/Scientific Vocabulary and S₂: Register-Crossing in Poetry",
        "",
        f"**Date:** {date_str}",
        "**Experiment:** `experiments/technical_vocabulary_s2.py`",
        f"**Corpus:** {baseline['n']:,} baseline tokens + {at['n']} technical tokens analyzed",
        "**Related:** `sensory_color_s2.md`, `latinate_germanic_diction_s2.md`, `straussian_gap_taxonomy.md`",
        "",
        "---",
        "",
        "## Research Question",
        "",
        "When poets borrow vocabulary from chemistry, biology, physics, medicine, or mathematics, they are",
        "crossing registers — importing words that GPT-2 associates with technical prose rather than lyric poetry.",
        "Does this register-crossing produce measurable S₂ elevation?",
        "",
        "**Hypothesis:** Technical vocabulary is a form of Straussian deviation — the model, conditioned on",
        "lyric context, assigns low probability to specialized terminology, generating high S₂.",
        "",
        "---",
        "",
        "## Main Result",
        "",
        f"| Category | N tokens | Mean S₂ | Mean H (bits) | % Positive S₂ |",
        f"|---|---|---|---|---|",
        f"| Baseline (all non-technical) | {baseline['n']:,} | {baseline['mean_s2']:.3f} | {baseline['mean_h']:.3f} | — |",
        f"| **Technical vocabulary** | {at['n']} | **{at['mean_s2']:.3f}** | {at['mean_h']:.3f} | {at['pct_positive']:.1%} |",
        "",
    ]

    if at['n'] > 0:
        lift = at['mean_s2'] - baseline['mean_s2']
        direction = "HIGHER" if lift > 0 else "LOWER"
        lines.append(f"**S₂ lift for technical vocabulary:** {lift:+.3f} bits ({direction} than baseline)")
        lines.append("")
        lines.append("---")
        lines.append("")

    lines += [
        "## By Domain",
        "",
        "| Domain | N | Mean S₂ | Mean H | % Positive S₂ | S₂ lift |",
        "|---|---|---|---|---|---|",
    ]
    for domain, info in sorted(ds.items(), key=lambda x: (x[1] or {}).get("mean_s2", -99), reverse=True):
        if info is None:
            lines.append(f"| {domain} | < 3 | — | — | — | — |")
        else:
            lift = info['mean_s2'] - baseline['mean_s2']
            lines.append(f"| {domain} | {info['n']} | {info['mean_s2']:.3f} | {info['mean_h']:.3f} | {info['pct_positive']:.1%} | {lift:+.3f} |")

    lines += [
        "",
        "---",
        "",
        "## Poets Using Technical Vocabulary Most",
        "",
        "| Poet | # Technical tokens |",
        "|---|---|",
    ]
    for poet, count in data["top_poets"]:
        lines.append(f"| {poet} | {count} |")

    lines += [
        "",
        "---",
        "",
        "## S₂ Lift by Era",
        "",
        "The 'lift' = mean S₂ of technical tokens − mean S₂ of non-technical tokens in the same era.",
        "Positive lift means technical vocabulary is MORE surprising than the era's baseline.",
        "",
        "| Era | N tech | Tech S₂ | Baseline S₂ | Lift |",
        "|---|---|---|---|---|",
    ]
    for era, info in list(data["era_lift"].items())[:15]:
        lines.append(f"| {era} | {info['n_tech']} | {info['tech_mean']:.3f} | {info['baseline_mean']:.3f} | {info['lift']:+.3f} |")

    lines += [
        "",
        "---",
        "",
        "## Top High-S₂ Moments Involving Technical Vocabulary",
        "",
        "The 'unsaid' reveals what GPT-2 expected at these register-crossing moments.",
        "",
        "| S₂ | Token | Poem | Poet | Domain | Context |",
        "|---|---|---|---|---|---|",
    ]
    for s2, token, title, author, domain, context in top[:15]:
        ctx = context.replace("\n", "↵").replace("|", "│")[:50]
        tok_clean = token.replace("|", "│").strip()
        lines.append(f"| {s2:.2f} | `{tok_clean}` | {title[:30]} | {author[:20]} | {domain} | `…{ctx}` |")

    lines += [
        "",
        "---",
        "",
        "## Finding",
        "",
    ]

    if at['n'] == 0:
        lines.append("No technical tokens found in the corpus — the lexicon may need expansion or case adjustment.")
    else:
        lift = at['mean_s2'] - baseline['mean_s2']
        if lift > 0.3:
            finding = (
                f"Technical vocabulary has **S₂ lift of {lift:+.3f} bits** over baseline. "
                "Register-crossing from technical domains IS a form of Straussian deviation: "
                "GPT-2, conditioned on lyric context, is surprised by borrowed scientific terminology. "
                "This confirms the hypothesis that poets exploit register-crossing as an information-theoretic strategy."
            )
        elif lift > 0:
            finding = (
                f"Technical vocabulary shows a modest **S₂ lift of {lift:+.3f} bits** over baseline. "
                "There is a weak register-crossing effect, suggesting technical terms are slightly more surprising "
                "in poetic context — but the effect is smaller than expected, possibly because many technical "
                "terms (e.g., 'atom', 'cell', 'force') have been absorbed into common vocabulary."
            )
        else:
            finding = (
                f"Technical vocabulary shows **no S₂ lift** (lift = {lift:+.3f} bits). "
                "Counterintuitively, technical terms in poetry are NOT more surprising than baseline. "
                "Possible explanations: (1) Technical terms may have been filtered by what poets actually use — "
                "poets self-select terms that fit their context; (2) GPT-2 may assign similar probability to "
                "technical terms because they appear in its prose training data in predictable positions."
            )
        lines.append(finding)
        lines.append("")
        lines.append("### Suggested Next Steps")
        lines.append("")
        lines.append("1. **Cluster by rarity**: Separate common technical terms ('atom', 'cell') from rare ones ('perihelion', 'ribosome') — the rarity effect may be hidden by common terms.")
        lines.append("2. **Semantic field analysis**: Do technical terms cluster with other technical terms in the same poem, or are they isolated intrusions?")
        lines.append("3. **Intentional vs incidental**: Some poets (Marianne Moore, William Carlos Williams) use technical vocabulary deliberately. Others have it appear as coincidence (e.g., 'cell' as prison cell).")
        lines.append("4. **Controlled study**: Substitute non-technical near-synonyms and compare S₂ — e.g., 'cell' vs 'room', 'atom' vs 'particle'.")

    return "\n".join(lines)


if __name__ == "__main__":
    import sys
    results_path = sys.argv[1] if len(sys.argv) > 1 else "corpus_results.json"
    print(f"Running technical vocabulary S₂ experiment on {results_path}...")
    data = run_experiment(results_path)
    print(f"Baseline: n={data['baseline']['n']:,}, mean_s2={data['baseline']['mean_s2']:.3f}")
    print(f"Technical: n={data['all_technical']['n']}, mean_s2={data['all_technical']['mean_s2']:.3f}")
    print(f"S₂ lift: {data['all_technical']['mean_s2'] - data['baseline']['mean_s2']:+.3f}")
    print(f"\nDomain breakdown:")
    for domain, info in sorted((data['domain_summary'] or {}).items(),
                                key=lambda x: (x[1] or {}).get('mean_s2', -99), reverse=True):
        if info:
            print(f"  {domain:25s}: n={info['n']:3d}, mean_s2={info['mean_s2']:.3f}")
    findings_text = write_findings(data)
    out_path = os.path.join(FINDINGS_DIR, "technical_vocabulary_s2.md")
    with open(out_path, "w") as f:
        f.write(findings_text)
    print(f"\nFindings written to {out_path}")
