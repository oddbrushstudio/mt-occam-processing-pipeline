"""
================================================================================
Author  : Oseni Olaonipekun
Contact : oddbrushstudio@gmail.com
================================================================================

STEP 5 — Plot Inversion Results
=================================
Plots the 2D resistivity model and data fit (observed vs predicted)
from completed OCCAM2D inversion results.

Run AFTER the OCCAM2D binary has finished.

Usage:
    python 05_plot_results.py

Required files in OCCAM_RESULTS_PATH (config.py):
    ITER<N>.iter   — iteration file (set ITER_NUMBER below)
    RESP<N>.resp   — response file  (set ITER_NUMBER below)
    OccamDataFile*.dat — data file used for the inversion
"""

import os
import matplotlib.pyplot as plt
import mtpy.modeling.occam2d_rewrite as occam2d
from config import (
    OCCAM_RESULTS_PATH, SAVE_PATH,
    TRIMMED_DATA_FILE, DATA_FILE,
    PLOT_DEPTH_SCALE, PLOT_CLIMITS, PLOT_CMAP,
)

# ── SET THIS to whichever iteration you want to plot ───────────────────────
ITER_NUMBER = 30

# ── PATHS ──────────────────────────────────────────────────────────────────
iter_file = os.path.join(OCCAM_RESULTS_PATH, f"ITER{ITER_NUMBER:02d}.iter")
resp_file = os.path.join(OCCAM_RESULTS_PATH, f"RESP{ITER_NUMBER:02d}.resp")

# Use trimmed data file if it exists, otherwise fall back to full data file
if os.path.exists(TRIMMED_DATA_FILE):
    data_file = TRIMMED_DATA_FILE
    print(f"Using trimmed data file: {TRIMMED_DATA_FILE}")
else:
    data_file = DATA_FILE
    print(f"Using data file: {DATA_FILE}")

for path, label in [(iter_file, "ITER file"), (resp_file, "RESP file"), (data_file, "Data file")]:
    if not os.path.exists(path):
        raise FileNotFoundError(f"{label} not found:\n  {path}\n"
                                f"Check OCCAM_RESULTS_PATH and ITER_NUMBER in config.py")

print("=" * 60)
print(f"STEP 5: Plotting iteration {ITER_NUMBER} results")
print("=" * 60)

# ── Resistivity model ──────────────────────────────────────────────────────
print("Plotting resistivity model...")
pm = occam2d.PlotModel(
    iter_fn    = iter_file,
    resp_fn    = resp_file,
    station_fn = data_file,
    depth_scale= PLOT_DEPTH_SCALE,
    fig_size   = (12, 6),
    dpi        = 150,
    climits    = PLOT_CLIMITS,
    map_scale  = PLOT_DEPTH_SCALE,
    cmap       = plt.get_cmap(PLOT_CMAP),
)
pm.plot()
model_out = os.path.join(SAVE_PATH, f'resistivity_model_iter{ITER_NUMBER:02d}.png')
pm.save_figure(model_out, fig_dpi=150)
print(f"✓ Resistivity model saved: {model_out}")

# ── Data fit ───────────────────────────────────────────────────────────────
print("\nPlotting data fit...")
pr = occam2d.PlotResponse(
    data_fn  = data_file,
    resp_fn  = resp_file,
    fig_size = (8, 10),
    dpi      = 150,
)
pr.plot()
pr.save_figures(SAVE_PATH, fig_dpi=150)
print(f"✓ Response plots saved to: {SAVE_PATH}")

print("\nDone! Check your output folder for plots.")
