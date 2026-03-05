"""
================================================================================
Author  : Oseni Olaonipekun
Contact : oddbrushstudio@gmail.com
================================================================================

MT Occam2D — Shared Configuration
==================================
Edit the paths and parameters below, then run any script in this folder.
All scripts import from here so you only need to change things in one place.

PATH SETUP:
  EDI_PATH    — folder containing your .edi files
  SAVE_PATH   — folder where your occam2d binary is located.
                Input files (OccamDataFile.dat, mesh, startup) are written
                here so the binary can find them. Place occam2d.exe here
                and run it from this folder.
  OUTPUT_PATH — folder where all plots, maps and result images are saved.
"""

import os
from pathlib import Path

# ── PATHS ──────────────────────────────────────────────────────────────────

# Folder containing your .edi files
EDI_PATH = Path(r"C:\path\to\your\edi_files")

# Folder where your occam2d binary is located — input files are written here
SAVE_PATH = Path(r"C:\path\to\your\occam2d_binary_folder")

# Folder where all output plots and maps are saved
OUTPUT_PATH = Path(r"C:\path\to\your\output_folder")

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
TRIM_CUTOFFS = {
    1: float('inf'),
    2: float('inf'),
    3: float('inf'),
    4: float('inf'),
    5: float('inf'),
}

# Station index → name mapping (used in trim reports and verification plots)
STATION_NAMES = {}   # e.g. {1: 'SG2201', 2: 'SG2203'}

# ── PLOT PARAMETERS ────────────────────────────────────────────────────────
PLOT_DEPTH_SCALE   = 'km'     # 'km' or 'm'
PLOT_CLIMITS       = (0, 4)   # Colour limits for resistivity model (log10)
PLOT_CMAP          = 'jet_r'  # Matplotlib colormap name

# ── DERIVED PATHS (do not edit) ────────────────────────────────────────────
SAVE_PATH.mkdir(parents=True, exist_ok=True)
OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

OCCAM_RESULTS_PATH = SAVE_PATH
DATA_FILE          = os.path.join(SAVE_PATH, "OccamDataFile.dat")
TRIMMED_DATA_FILE  = os.path.join(SAVE_PATH, "OccamDataFile_trimmed.dat")
TRIM_VERIFY_PLOT   = os.path.join(OUTPUT_PATH, "trim_verification.png")
