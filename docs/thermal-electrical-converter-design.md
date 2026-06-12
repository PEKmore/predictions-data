# A Cascaded Regenerative Electrochemical Heat Engine

## Goal

Design a thermal-to-electrical energy converter that is rigorously grounded in
thermodynamics, with an explicit efficiency budget and a concrete test plan,
rather than a claim that bypasses the Carnot limit.

## Governing constraints

Every conversion scheme is bound by two rules:

1. **A temperature difference is the fuel.** No device extracts net work from
   a single reservoir at uniform temperature (Kelvin-Planck statement). This
   also means such a device can never cool something below ambient — that
   direction requires work input, not output.
2. **Carnot caps the fraction.** `η ≤ 1 − T_c / T_h`. Power roughly scales as
   ΔT², since both flux and efficiency scale with ΔT. The
   Curzon-Ahlborn efficiency at maximum power, `1 − sqrt(T_c / T_h)`, is a more
   honest target for anything power-dense.

Calibration (T_c = 20 °C / 293 K):

| T_h    | Carnot ceiling | Curzon-Ahlborn (power-optimal) |
|--------|----------------|---------------------------------|
| 60 °C  | ~12%           | ~6%                              |
| 95 °C  | ~20%           | ~11%                             |
| 150 °C | ~30%           | ~16%                             |
| Flame  | >80%           | >55%                             |

"Highly efficient" therefore means *a high fraction of Carnot at the
available temperature band* — the band picks the mechanism.

## Survey of mechanisms (real-world efficiency)

| Mechanism                          | Typical efficiency | Notes |
|-------------------------------------|---------------------|-------|
| Combined-cycle turbines              | ~63%               | Needs flame-grade heat, power-station scale |
| Stirling engine                      | 30–40%             | Regenerator approaches Carnot ideally; seals/lifetime limit practice |
| Organic Rankine cycle (ORC)          | 5–15%              | Industrial default for 80–300 °C waste heat |
| Thermoelectric (Seebeck)             | 5–8%               | Wiedemann-Franz: same carriers conduct heat and charge |
| Thermophotovoltaic (TPV)             | 41%+ demonstrated  | Photon recycling via emitter + rear-mirror PV cell |
| Thermionics                          | 10–15%             | Space-charge limited vacuum-gap emission |
| Electrochemical (thermogalvanic, JTEC) | up to ~38% of Carnot | dV/dT = ΔS / nF; charge cold, discharge hot |
| Phase-transition harvesters           | Variable, hysteresis-limited | Nitinol engines, thermomagnetic (Curie-point), pyroelectric Olsen cycles |

## Four recurring tricks, and a fifth for direct electrical output

1. **Isothermal exchange at a phase transition** — concentrates a large
   entropy change into a narrow temperature window (the nitinol latent-heat
   intuition).
2. **Regeneration** — recycle the sensible heat spent conditioning the
   working medium each cycle; this is why an idealised Stirling engine
   approaches Carnot.
3. **Cascading** — stage multiple converters, each tuned to a narrow slice of
   the overall gradient (cf. multi-junction solar cells).
4. **Carrier filtering** — only let energy of the "right size" cross (TPV's
   rear mirror returns sub-bandgap photons to the emitter).
5. **Native electrical output** — make the converter itself an
   electrochemical store, eliminating a separate generator stage.

## Proposed design: cascaded regenerative electrochemical heat engine

A "battery charged by temperature." Each cell exploits the
temperature-dependence of its electrode reaction's entropy:

```
dV/dT = ΔS / (nF)
```

**Cycle:**

1. Charge the cell while cold (low voltage, low energy cost).
2. Move the cell to the hot reservoir via a thermal switch.
3. Discharge at the higher voltage produced by the temperature-shifted
   reaction potential, αΔT, where α = dV/dT.
4. Return the cell to cold, regenerating its sensible heat through a
   counter-flow / thermal-switch regenerator before it re-enters the cycle.

**Efficiency budget:**

```
η ≈ η_Carnot × (regeneration effectiveness) × (voltage efficiency)
```

In the limit of perfect regeneration (effectiveness → 1) and zero internal
resistance (voltage efficiency → 1), η → η_Carnot. Every loss term has a
named, attributable cause:

- **Low regeneration effectiveness** — sensible heat lost moving the cell
  between reservoirs each cycle. Mitigated with snap-action thermal switches
  (low-hysteresis shape-memory alloys, powered parasitically by the gradient
  itself — repurposing the nitinol concept as a *switch*, not an *engine*,
  since hysteresis in an engine directly dissipates the work loop).
- **Low voltage efficiency** — IR drop from internal resistance at the
  chosen current density; αΔT margin is consumed directly by I·R losses.
  Mitigated by large electrode area, modest current density, and
  low-resistance electrolytes.
- **Small α (dV/dT)** — maximised by choosing electrode couples with a
  first-order phase transition, which piles entropy into the reaction (the
  electrochemical analogue of nitinol's latent heat).

**Cascading:** stack several banks of cells with staggered chemistries (each
tuned to a different temperature sub-range) down the full gradient, so each
stage operates near its own efficiency optimum.

### Realistic targets

- Bench-scale demonstrator (ferri/ferrocyanide thermogalvanic cell,
  α ≈ 1.4 mV/K): kettle-vs-ice gradient → ~100 mV per cell, milliwatts when
  stacked. This is the "entropy tax made visible on a multimeter" — a
  reproducible bench demonstration, not yet an optimised converter.
- Engineered cell with phase-transition electrodes + regenerative thermal
  switching, 95 °C source / 20 °C sink: target 40–50% of Carnot
  (≈ 8–10% absolute), comparable to or better than an ORC plant (5–8%) at
  the same grade, without turbomachinery.

### Flame-grade alternative

If the source is flame-grade rather than low-grade waste heat, the answer
changes: heat a graphite emitter to incandescence and harvest the glow with
a photon-recycling TPV cell (rear mirror returns sub-bandgap photons to the
emitter). 41%+ has been demonstrated; this is the architecture behind current
"thermal battery" ventures. The unifying principle is the same — match the
converter to the temperature band, and cascade across bands.

## Test plan

### Phase 1 — Bench demonstrator (low risk, low cost)

**Goal:** verify the basic thermogalvanic voltage-vs-temperature relationship
and establish a measured α.

1. Prepare two identical ferri/ferrocyanide (K₃Fe(CN)₆ / K₄Fe(CN)₆)
   electrolyte cells with inert electrodes (e.g. graphite or platinum).
2. Place one cell's electrode pair in a hot bath (e.g. 60–95 °C) and the
   other in an ice bath (~0 °C), connected via a salt bridge or shared
   electrolyte reservoir.
3. Measure open-circuit voltage (OCV) vs. ΔT across a range of gradients;
   fit to confirm α ≈ dV/dT (expect ~1.4 mV/K for this couple).
4. Measure short-circuit current and internal resistance (via
   current-interrupt or impedance spectroscopy) to characterise voltage
   efficiency at varying current draw.
5. Stack N cells in series; confirm voltage scales linearly with N and power
   scales as expected with stacking.

**Success criteria:** measured α within ~20% of literature value; power
output in the milliwatt range for a small stack; internal resistance
characterised well enough to predict voltage efficiency at a target current.

### Phase 2 — Regenerative cycling (moderate complexity)

**Goal:** quantify regeneration effectiveness and its impact on net cycle
efficiency.

1. Build a single-cell cycler: charge cold → thermal switch to hot →
   discharge hot → thermal switch to cold → repeat.
2. Instrument heat flow into/out of the cell (calorimetry) and electrical
   energy in/out (charge/discharge integration).
3. Compare cycle efficiency with and without a regenerator (e.g. a
   counter-flow heat exchanger or low-hysteresis SMA thermal switch that
   pre-conditions the cell before it crosses reservoirs).
4. Vary cycle frequency to find the point where thermal switching losses
   start to dominate IR losses — this identifies the practical
   power/efficiency operating point.

**Success criteria:** measured regeneration effectiveness > 0.7; net cycle
efficiency tracks the predicted `η_Carnot × regen × voltage_eff` formula
within measurement uncertainty.

### Phase 3 — Phase-transition electrode evaluation (higher risk)

**Goal:** evaluate candidate electrode couples with first-order phase
transitions for larger α.

1. Screen candidate redox couples (e.g. Prussian-blue analogues,
   spin-crossover complexes, or other systems with documented
   reaction-entropy anomalies near a transition temperature) for ΔS and
   reversibility over many cycles.
2. Measure α for each candidate across the target ΔT band; reject
   candidates with excessive hysteresis (hysteresis loop area directly
   subtracts from net work, mirroring the nitinol-engine failure mode).
3. Select the couple with the best α × cyclability product for the target
   band.

**Success criteria:** at least one candidate with α > 3× the
ferri/ferrocyanide baseline and < 10% capacity/voltage degradation over
1,000 thermal cycles.

### Phase 4 — Cascaded multi-bank prototype

**Goal:** demonstrate a cascaded system spanning the full source-to-ambient
gradient (e.g. 95 °C → 20 °C) using staged chemistries selected in Phase 3.

1. Partition the gradient into 2–3 sub-bands; assign each band the
   electrode couple with the best α for that range.
2. Build a multi-bank prototype with shared thermal-switch regenerators
   between adjacent banks.
3. Measure overall electrical output vs. heat input at the hot reservoir;
   compute overall η and compare against the 8–10% absolute target
   (40–50% of Carnot) at 95 °C / 20 °C.
4. Compare against an off-the-shelf TEG or small ORC unit at the same
   source temperature as a benchmark.

**Success criteria:** overall system efficiency ≥ 8% absolute at 95 °C
source / 20 °C sink, with a full energy balance (heat in, heat rejected,
electrical out) closing to within measurement error — i.e. no violation of
the first law, and entropy production consistent with
`Q_c/T_c − Q_h/T_h ≥ 0`.

## Summary

The achievable target is **fraction of Carnot and cost per watt**, not escape
from Carnot. The design above is an integration of existing, individually
demonstrated components (thermogalvanic cells, regenerative cycling,
low-hysteresis thermal switches, phase-transition electrodes) into a
cascaded system with no moving parts beyond optional switchgear, aimed at
8–10% absolute efficiency from a 95 °C source — competitive with turbine-based
ORC systems at the same grade. For flame-grade heat, photon-recycling TPV
remains the better-suited architecture.
