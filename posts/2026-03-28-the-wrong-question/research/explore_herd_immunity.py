"""
Exploratory script: herd immunity dynamics for four disease archetypes.

Models the non-linear relationship between vaccination coverage and disease burden.
Key insight: near the herd immunity threshold, small changes in coverage produce
dramatic changes in disease burden (the "S-curve" effect).

Usage:
    uv run --with numpy --with matplotlib posts/2026-03-28-the-wrong-question/research/explore_herd_immunity.py
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from pathlib import Path

# ---------------------------------------------------------------------------
# Disease archetypes
# ---------------------------------------------------------------------------

archetypes = [
    {
        "name": "Measles-like",
        "R0": 15,
        "CFR": 0.002,
        "vaccine_efficacy": 0.97,
        "adverse_rate": 1e-6,
        # Herd threshold in a perfectly-efficacious world: 1 - 1/R0
        # With vaccine efficacy e, coverage needed: (1 - 1/R0) / e
        "color": "#e63946",  # vivid red
        "linestyle": "-",
    },
    {
        "name": "Smallpox-like",
        "R0": 6,
        "CFR": 0.30,
        "vaccine_efficacy": 0.95,
        "adverse_rate": 1e-5,
        "color": "#e76f51",  # orange-red
        "linestyle": "--",
    },
    {
        "name": "Gray Threat",
        "R0": 4,
        "CFR": 0.02,
        "vaccine_efficacy": 0.75,
        "adverse_rate": 1e-4,
        "color": "#457b9d",  # steel blue
        "linestyle": "-.",
    },
    {
        "name": "Black Swan Pandemic",
        "R0": 3,          # point estimate; uncertain (range 2–6)
        "CFR": 0.05,      # point estimate; uncertain (range 0.01–0.15)
        "vaccine_efficacy": 0.60,
        "adverse_rate": 5e-5,
        "color": "#2d6a4f",  # dark green
        "linestyle": ":",
    },
]

# ---------------------------------------------------------------------------
# Core model functions
# ---------------------------------------------------------------------------

def effective_reproduction_number(R0: float, v: np.ndarray, efficacy: float) -> np.ndarray:
    """
    Re(v) = R0 * (1 - v * e)

    v        : vaccination coverage, 0–1
    efficacy : vaccine efficacy (fraction of vaccinated who are fully protected)
    """
    return R0 * (1.0 - v * efficacy)


def disease_burden_per_1000(Re: np.ndarray, smooth_width: float = 0.05) -> np.ndarray:
    """
    Simplified SIR steady-state fraction infected as a function of Re.

    If Re <= 1  : epidemic cannot sustain; fraction infected ≈ 0
    If Re >  1  : SIR final-size approximation, fraction ≈ 1 - 1/Re

    A smooth sigmoid transition is applied around Re=1 to avoid a hard kink
    and to reflect the real-world uncertainty near the threshold.

    Returns expected infections per 1000 population.
    """
    # Raw SIR fraction infected when Re > 1
    raw = np.where(Re > 1.0, 1.0 - 1.0 / np.maximum(Re, 1e-9), 0.0)

    # Smooth transition: weight = sigmoid((Re - 1) / smooth_width)
    weight = 1.0 / (1.0 + np.exp(-(Re - 1.0) / smooth_width))

    return raw * weight * 1000.0


def herd_immunity_coverage(R0: float, efficacy: float) -> float:
    """
    Minimum coverage v* such that Re(v*) = 1:
        R0 * (1 - v* * e) = 1
        v* = (1 - 1/R0) / e

    If v* > 1, herd immunity is unachievable with this vaccine alone.
    """
    return (1.0 - 1.0 / R0) / efficacy


# ---------------------------------------------------------------------------
# Plotting
# ---------------------------------------------------------------------------

def build_figure(archetypes: list) -> plt.Figure:
    fig, axes = plt.subplots(2, 2, figsize=(12, 9), sharey=False)
    axes = axes.flatten()

    v = np.linspace(0.0, 1.0, 500)

    for ax, arch in zip(axes, archetypes):
        R0 = arch["R0"]
        e = arch["vaccine_efficacy"]
        color = arch["color"]

        Re = effective_reproduction_number(R0, v, e)
        burden = disease_burden_per_1000(Re)

        v_threshold = herd_immunity_coverage(R0, e)
        threshold_achievable = v_threshold <= 1.0

        ax.plot(v * 100, burden, color=color, linewidth=2.5, zorder=3)

        if threshold_achievable:
            ax.axvline(
                x=v_threshold * 100,
                color=color,
                linewidth=1.2,
                linestyle="--",
                alpha=0.7,
                zorder=2,
                label=f"Herd threshold ≈ {v_threshold*100:.0f}%",
            )
            # Shade the "safe zone" past the threshold
            ax.axvspan(v_threshold * 100, 100, alpha=0.07, color=color, zorder=1)
        else:
            ax.text(
                0.97, 0.95,
                f"Herd immunity\nnot achievable\n(need {v_threshold*100:.0f}% coverage)",
                transform=ax.transAxes,
                ha="right", va="top",
                fontsize=8.5,
                color=color,
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=color, alpha=0.8),
            )

        # Annotate Re=1 crossing with a dot on the curve
        if threshold_achievable:
            burden_at_threshold = disease_burden_per_1000(
                np.array([effective_reproduction_number(R0, v_threshold, e)])
            )[0]
            ax.plot(
                v_threshold * 100, burden_at_threshold,
                "o", color=color, markersize=7, zorder=4,
            )

        # Panel decoration
        ax.set_title(
            f"{arch['name']}\nR₀ = {R0}, CFR = {arch['CFR']*100:.1f}%, "
            f"efficacy = {e*100:.0f}%",
            fontsize=10, fontweight="bold", pad=8,
        )
        ax.set_xlabel("Vaccination coverage (%)", fontsize=9)
        ax.set_ylabel("Expected infections per 1 000", fontsize=9)
        ax.set_xlim(0, 100)
        ax.set_ylim(bottom=0)
        ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:.0f}%"))
        ax.grid(True, linestyle=":", linewidth=0.6, alpha=0.5)
        ax.spines[["top", "right"]].set_visible(False)

        if threshold_achievable:
            ax.legend(fontsize=8.5, loc="upper right", framealpha=0.9)

    fig.suptitle(
        "Herd Immunity Dynamics: Disease Burden vs. Vaccination Coverage\n"
        "(simplified SIR steady-state model)",
        fontsize=13, fontweight="bold", y=1.01,
    )
    fig.tight_layout()
    return fig


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    # Print threshold summary
    print("=" * 62)
    print(f"{'Archetype':<25} {'R0':>4} {'Efficacy':>9} {'Threshold':>10}")
    print("-" * 62)
    for arch in archetypes:
        vt = herd_immunity_coverage(arch["R0"], arch["vaccine_efficacy"])
        achievable = "achievable" if vt <= 1.0 else "NOT achievable (>100%)"
        thresh_str = f"{vt*100:.1f}%" if vt <= 1.0 else f"{vt*100:.0f}%"
        print(
            f"{arch['name']:<25} {arch['R0']:>4} "
            f"{arch['vaccine_efficacy']*100:>8.0f}% "
            f"{thresh_str:>10}  {achievable}"
        )
    print("=" * 62)

    fig = build_figure(archetypes)

    out_path = (
        Path(__file__).parent / "herd_immunity_curves.png"
    )
    fig.savefig(out_path, dpi=150, bbox_inches="tight", facecolor="white")
    print(f"\nFigure saved to: {out_path}")

    plt.show()


if __name__ == "__main__":
    main()
