"""
MT Occam2D v2 — Shared Configuration
======================================
Edit the paths and parameters in this file only.
All scripts in this folder import from here.

MTpy v2 workflow summary:
  00_load_edi.py      → reads EDIs, saves mt_collection.h5  (run once)
  01_explore.py       → plot stations, responses, strike
  02_write_occam.py   → interpolate, rotate, write Occam2D input files
  03_trim_data.py     → remove noisy periods per station (optional)
  04_verify_trim.py   → visual check of trim (optional)
  05_plot_results.py  → plot model & data fit after inversion
"""

from pathlib import Path

# ── PATHS ──────────────────────────────────────────────────────────────────

# Folder containing your .edi files
EDI_PATH = Path(r"C:\path\to\your\edi_files")

# Where the MTH5 collection file will be saved (created once by 00_load_edi.py)
COLLECTION_H5 = EDI_PATH / "mt_collection.h5"

# Where all Occam2D input/output files will be saved
SAVE_PATH = Path(r"C:\path\to\your\output_folder")

# Folder where OCCAM2D binary results are stored (ITER / RESP files)
OCCAM_RESULTS_PATH = Path(r"C:\path\to\your\occam2d_results")

# ── DATA / INTERPOLATION ───────────────────────────────────────────────────

# Frequency range and count for interpolation (log-spaced)
FREQ_MIN   = 1e-3    # Hz
FREQ_MAX   = 1e3     # Hz
FREQ_COUNT = 37      # number of log-spaced frequencies

# ── OCCAM2D INVERSION PARAMETERS ──────────────────────────────────────────

# Geoelectric strike angle in degrees (measured from North, clockwise)
# Set to None to let mtpy estimate it from the data
GEOELECTRIC_STRIKE = 30

# Model mode — what components to invert
# Common choices:
#   'log_te_tm'  (4)  → log TE + TM              ← recommended default
#   'log_all'    (1)  → log TE + TM + Tipper
#   'log_te'     (5)  → TE only
#   'log_tm'     (6)  → TM only
MODEL_MODE = 'log_te_tm'

# Error floors — resistivity errors as fraction (not %), phase in degrees
# e.g. 0.05 = 5%
RES_XY_ERROR   = 0.20          # TE resistivity (20%)
RES_YX_ERROR   = 0.20          # TM resistivity (20%)
PHASE_XY_ERROR = 0.025 * 57.   # TE phase  (2.5% of 57°)
PHASE_YX_ERROR = 0.025 * 57.   # TM phase  (2.5% of 57°)

# Starting model resistivity (log10 ohm-m), e.g. 2 = 100 ohm-m
RESISTIVITY_START  = 2
ITERATIONS_TO_RUN  = 30
TARGET_MISFIT      = 1.0

# ── TRIMMING — period cutoffs per station (seconds) ────────────────────────
# Periods greater than the cutoff will be removed for that station.
# Keys are 1-based station indices as they appear in OccamDataFile.dat.
# Use float('inf') to keep all data for a station.
TRIM_CUTOFFS = {
    1: float('inf'),
    2: float('inf'),
    3: float('inf'),
    4: float('inf'),
    5: float('inf'),
}

# Station index → name mapping for trim reports (auto-detected if left empty)
STATION_NAMES = {}   # e.g. {1: 'SG2201', 2: 'SG2203'}

# ── PLOT PARAMETERS ────────────────────────────────────────────────────────
PLOT_DEPTH_SCALE = 'km'    # 'km' or 'm'
PLOT_CLIMITS     = (0, 4)  # log10 resistivity colour limits
PLOT_CMAP        = 'jet_r'

# ── DERIVED PATHS (do not edit) ────────────────────────────────────────────
SAVE_PATH.mkdir(parents=True, exist_ok=True)

DATA_FILE         = SAVE_PATH / "OccamDataFile.dat"
TRIMMED_DATA_FILE = SAVE_PATH / "OccamDataFile_trimmed.dat"
TRIM_VERIFY_PLOT  = SAVE_PATH / "trim_verification.png"
