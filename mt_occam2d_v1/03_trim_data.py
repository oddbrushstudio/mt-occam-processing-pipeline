"""
================================================================================
Author  : Oseni Olaonipekun
Contact : oddbrushstudio@gmail.com
================================================================================

STEP 3 — Trim Bad Frequency Ranges from Data File
===================================================
Removes data points with periods exceeding per-station cutoffs
defined in config.py → TRIM_CUTOFFS.

Run this if visual inspection of your data shows noise or bad values
at certain period ranges. After trimming, re-run the OCCAM2D binary
pointing to the new trimmed data file.

Usage:
    python 03_trim_data.py
"""

import numpy as np
import re
from config import (
    DATA_FILE, TRIMMED_DATA_FILE,
    TRIM_CUTOFFS, STATION_NAMES,
)

print("=" * 60)
print("STEP 3: Trimming data file")
print("=" * 60)
print(f"Input:  {DATA_FILE}")
print(f"Output: {TRIMMED_DATA_FILE}")

# ── Read file ──────────────────────────────────────────────────────────────
with open(DATA_FILE, 'r') as f:
    lines = f.readlines()

# ── Parse frequency list ───────────────────────────────────────────────────
freq_list = []
i = 0
while i < len(lines):
    if re.match(r'\s*FREQUENCIES', lines[i], re.IGNORECASE):
        n_freq = int(re.findall(r'\d+', lines[i])[0])
        i += 1
        for _ in range(n_freq):
            freq_list.append(float(lines[i].strip()))
            i += 1
        break
    i += 1

if not freq_list:
    raise ValueError("Could not find FREQUENCIES block in data file.")

periods = [1.0 / f for f in freq_list]
print(f"\nFrequencies: {len(freq_list)}")
print(f"Period range: {min(periods):.5f}s → {max(periods):.1f}s")

# ── Locate data block ──────────────────────────────────────────────────────
data_block_idx = None
data_start_idx = None

for idx, line in enumerate(lines):
    if re.match(r'\s*DATA BLOCKS', line, re.IGNORECASE):
        data_block_idx = idx
        j = idx + 1
        while j < len(lines):
            stripped = lines[j].strip()
            if stripped and not stripped.startswith('!') and not stripped.startswith('#'):
                if re.match(r'^\s*\d', lines[j]):
                    data_start_idx = j
                    break
            j += 1
        break

if data_start_idx is None:
    raise ValueError("Could not find data lines in file.")

# ── Filter ─────────────────────────────────────────────────────────────────
kept = []
removal_summary = {}

for line in lines[data_start_idx:]:
    stripped = line.strip()
    if not stripped or stripped.startswith('!') or stripped.startswith('#'):
        continue
    parts = stripped.split()
    if len(parts) < 4:
        continue
    try:
        site_idx = int(parts[0])
        freq_idx = int(parts[1]) - 1  # 1-based → 0-based
    except ValueError:
        kept.append(line)
        continue

    if freq_idx < 0 or freq_idx >= len(periods):
        kept.append(line)
        continue

    period = periods[freq_idx]
    cutoff = TRIM_CUTOFFS.get(site_idx, float('inf'))

    if period > cutoff:
        removal_summary[site_idx] = removal_summary.get(site_idx, 0) + 1
    else:
        kept.append(line)

# ── Report ─────────────────────────────────────────────────────────────────
total_removed = sum(removal_summary.values())
if total_removed == 0:
    print("\nNo data removed — all periods within cutoffs.")
    print("Tip: edit TRIM_CUTOFFS in config.py to remove noisy periods.")
else:
    print("\nRemoval summary:")
    for site_idx, count in sorted(removal_summary.items()):
        name = STATION_NAMES.get(site_idx, f"Station {site_idx}")
        cutoff = TRIM_CUTOFFS.get(site_idx, float('inf'))
        print(f"  {name}: removed {count} points  (cutoff = {cutoff}s)")
    print(f"\nTotal removed : {total_removed}")
    print(f"Total kept    : {len(kept)}")

# ── Write trimmed file ─────────────────────────────────────────────────────
with open(TRIMMED_DATA_FILE, 'w') as f:
    for idx in range(data_start_idx):
        line = lines[idx]
        if re.match(r'\s*DATA BLOCKS', line, re.IGNORECASE):
            f.write(f'DATA BLOCKS:      {len(kept)}\n')
        else:
            f.write(line)
    for line in kept:
        f.write(line)

print(f"\n✓ Trimmed file written: {TRIMMED_DATA_FILE}")
print("\nNext steps:")
print("  1. Run  04_verify_trim.py  to visually confirm what was removed")
print("  2. Update your Occam2DStartup to point to the trimmed data file")
print("  3. Re-run the OCCAM2D binary")
