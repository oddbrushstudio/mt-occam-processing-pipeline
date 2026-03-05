"""
================================================================================
Author  : Oseni Olaonipekun
Contact : oddbrushstudio@gmail.com
================================================================================

MT Occam2D — Shared Configuration
==================================
Edit the paths and parameters below, then run any script in this folder.
All scripts import from here so you only need to change things in one place.
"""

import os
from pathlib import Path

# ── PATHS ──────────────────────────────────────────────────────────────────
# Folder containing your .edi files
EDI_PATH = Path(r"C:\path\to\your\edi_files")

# Folder where all outputs will be saved (created automatically if missing)
SAVE_PATH  = Path(r"C:\path\to\your\output_folder")

# Folder where OCCAM2D binary results are stored (ITER/RESP files)
OCCAM_RESULTS_PATH  = Path(r"C:\path\to\your\occam2d_results")

# ── DATA PARAMETERS ────────────────────────────────────────────────────────
GEOELECTRIC_STRIKE = 30       # Strike angle in degrees
RES_TE_ERR         = 10       # TE resistivity error floor (%)
RES_TM_ERR         = 10       # TM resistivity error floor (%)
PHASE_TE_ERR       = 5        # TE phase error floor (degrees)
PHASE_TM_ERR       = 5        # TM phase error floor (degrees)
MODEL_MODE         = '1'      # '1' = TE+TM, '2' = TE only, '3' = TM only
FREQ_MIN           = 1e-3     # Minimum frequency (Hz)
FREQ_MAX           = 1e3      # Maximum frequency (Hz)
FREQ_COUNT         = 37       # Number of log-spaced frequencies

# ── MESH PARAMETERS ────────────────────────────────────────────────────────
N_LAYERS           = 30       # Number of vertical layers
Z1_LAYER           = 10       # Thickness of first layer (m)
Z_TARGET_DEPTH     = 50000    # Target depth of inversion (m)
X_PAD_MULTIPLIER   = 1.5      # Horizontal padding multiplier
NUM_X_PAD_CELLS    = 7        # Number of horizontal padding cells

# ── INVERSION PARAMETERS ───────────────────────────────────────────────────
RESISTIVITY_START  = 2        # Starting resistivity in log10 (2 = 100 ohm-m)
ITERATIONS_TO_RUN  = 30       # Maximum number of iterations
TARGET_MISFIT      = 1.0      # Target RMS misfit

# ── TRIMMING — Period cutoffs per station (seconds) ────────────────────────
# Data with period > cutoff will be removed for that station.
# Use float('inf') to keep all periods for a station.
# Keys are 1-based station indices as they appear in OccamDataFile.dat.
# Example: {1: float('inf'), 2: 0.5, 3: 500.0}
TRIM_CUTOFFS = {
    1: float('inf'),
    2: float('inf'),
    3: float('inf'),
    4: float('inf'),
    5: float('inf'),
}

# Station index → name mapping (used in trim reports and verification plots)
STATION_NAMES = {}   # e.g. {1: 'SG2201', 2: 'SG2203'} — auto-filled if left empty

# ── PLOT PARAMETERS ────────────────────────────────────────────────────────
PLOT_DEPTH_SCALE   = 'km'     # 'km' or 'm'
PLOT_CLIMITS       = (0, 4)   # Colour limits for resistivity model (log10)
PLOT_CMAP          = 'jet_r'  # Matplotlib colormap name

# ── DERIVED PATHS (do not edit) ────────────────────────────────────────────
Path(SAVE_PATH).mkdir(parents=True, exist_ok=True)

DATA_FILE         = os.path.join(SAVE_PATH, "OccamDataFile.dat")
TRIMMED_DATA_FILE = os.path.join(SAVE_PATH, "OccamDataFile_trimmed.dat")
TRIM_VERIFY_PLOT  = os.path.join(SAVE_PATH, "trim_verification.png")
