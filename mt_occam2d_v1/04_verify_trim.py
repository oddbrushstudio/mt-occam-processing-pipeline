"""
================================================================================
Author  : Oseni Olaonipekun
Contact : oddbrushstudio@gmail.com
================================================================================

STEP 4 — Verify Trim (Visual Check)
=====================================
Plots kept (blue) vs removed (red) data points per station and per
data type. Run after 03_trim_data.py to confirm trimming looks correct.

Usage:
    python 04_verify_trim.py
"""

import numpy as np
import matplotlib.pyplot as plt
import re
from config import (
    DATA_FILE, TRIMMED_DATA_FILE,
    TRIM_CUTOFFS, STATION_NAMES, TRIM_VERIFY_PLOT,
)

print("=" * 60)
print("STEP 4: Verification plot (kept vs removed)")
print("=" * 60)

# Data types to plot: (type_index, column_label, y_axis_label)
PLOT_TYPES = [
    (1, 'log10 ρ TE',  'log10 App. Res. (Ω·m)'),
    (2, 'Phase TE',    'Phase TE (°)'),
    (5, 'log10 ρ TM',  'log10 App. Res. (Ω·m)'),
    (6, 'Phase TM',    'Phase TM (°)'),
]

# ── Parser ─────────────────────────────────────────────────────────────────
def parse_occam_file(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()

    freq_list = []
    data = {}

    i = 0
    while i < len(lines):
        line = lines[i]

        if re.match(r'\s*FREQUENCIES', line, re.IGNORECASE):
            n = int(re.findall(r'\d+', line)[0])
            i += 1
            for _ in range(n):
                freq_list.append(float(lines[i].strip()))
                i += 1
            continue

        if re.match(r'\s*DATA BLOCKS', line, re.IGNORECASE):
            i += 1
            while i < len(lines):
                dl = lines[i].strip()
                parts = dl.split()
                if (len(parts) >= 5 and parts[0].isdigit()
                        and not dl.startswith('!')
                        and not dl.startswith('SITE')):
                    try:
                        site  = int(parts[0])
                        freq  = int(parts[1]) - 1
                        dtype = int(parts[2])
                        value = float(parts[3])
                        if 0 <= freq < len(freq_list):
                            period = 1.0 / freq_list[freq]
                            data.setdefault((site, dtype), []).append((period, value))
                    except (ValueError, IndexError):
                        pass
                i += 1
            break
        i += 1

    return freq_list, data

# ── Parse ──────────────────────────────────────────────────────────────────
print("Parsing original file...")
orig_freqs, orig_data = parse_occam_file(DATA_FILE)
print("Parsing trimmed file...")
trim_freqs, trim_data = parse_occam_file(TRIMMED_DATA_FILE)

# Determine stations from the data
all_sites = sorted(set(k[0] for k in orig_data))
n_sites = len(all_sites)
n_types = len(PLOT_TYPES)

# ── Plot ───────────────────────────────────────────────────────────────────
fig, axes = plt.subplots(n_sites, n_types,
                         figsize=(4 * n_types, 4 * n_sites))

# Handle single-station edge case
if n_sites == 1:
    axes = [axes]

fig.suptitle('Trim Verification: Kept (blue) vs Removed (red)',
             fontsize=14, fontweight='bold', y=1.01)

for row, site_idx in enumerate(all_sites):
    site_name = STATION_NAMES.get(site_idx, f"Station {site_idx}")
    cutoff    = TRIM_CUTOFFS.get(site_idx, float('inf'))

    for col, (dtype, type_label, ylabel) in enumerate(PLOT_TYPES):
        ax  = axes[row][col] if n_sites > 1 else axes[col]
        key = (site_idx, dtype)

        orig_pts = orig_data.get(key, [])
        trim_pts = trim_data.get(key, [])

        if orig_pts:
            kept_set = set(round(p, 8) for p, v in trim_pts)
            kept_p, kept_v       = [], []
            removed_p, removed_v = [], []

            for p, v in orig_pts:
                if round(p, 8) in kept_set:
                    kept_p.append(p);    kept_v.append(v)
                else:
                    removed_p.append(p); removed_v.append(v)

            if kept_p:
                ax.semilogx(kept_p, kept_v, 'b.-', markersize=5,
                            linewidth=1.2, label='Kept', zorder=3)
            if removed_p:
                ax.semilogx(removed_p, removed_v, 'r.--', markersize=7,
                            linewidth=1, alpha=0.8, label='Removed', zorder=2)

            if cutoff != float('inf'):
                ax.axvline(x=cutoff, color='orange', linewidth=2,
                           linestyle='--', label=f'Cutoff {cutoff}s', zorder=4)
        else:
            ax.text(0.5, 0.5, 'No data', transform=ax.transAxes,
                    ha='center', va='center', color='gray', fontsize=9)

        ax.set_xscale('log')
        ax.set_xlabel('Period (s)', fontsize=8)
        ax.grid(True, alpha=0.3, which='both')
        ax.tick_params(labelsize=7)

        if row == 0:
            ax.set_title(type_label, fontsize=10, fontweight='bold')
        if col == 0:
            ax.set_ylabel(f'{site_name}\n{ylabel}', fontsize=8, fontweight='bold')
        else:
            ax.set_ylabel(ylabel, fontsize=8)
        if row == 0 and col == 0:
            ax.legend(fontsize=7)

plt.tight_layout()
plt.savefig(TRIM_VERIFY_PLOT, dpi=150, bbox_inches='tight')
plt.show()
print(f"\n✓ Verification plot saved: {TRIM_VERIFY_PLOT}")
print("\nNext → run OCCAM2D binary, then  05_plot_results.py")
