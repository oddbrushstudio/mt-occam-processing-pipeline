"""
================================================================================
Author  : Oseni Olaonipekun
Contact : oddbrushstudio@gmail.com
================================================================================

STEP 1 — Write Occam2D Data File
=================================
Reads all .edi files in EDI_PATH and writes OccamDataFile.dat to SAVE_PATH.

Usage:
    python 01_write_data.py
"""

import os
import numpy as np
import mtpy.modeling.occam2d_rewrite as occam2d
from config import (
    EDI_PATH, SAVE_PATH,
    GEOELECTRIC_STRIKE,
    RES_TE_ERR, RES_TM_ERR,
    PHASE_TE_ERR, PHASE_TM_ERR,
    MODEL_MODE,
    FREQ_MIN, FREQ_MAX, FREQ_COUNT,
    DATA_FILE,
)

print("=" * 60)
print("STEP 1: Writing Occam2D data file")
print("=" * 60)

station_list = [f[:-4] for f in os.listdir(EDI_PATH) if f.endswith('.edi')]
if not station_list:
    raise FileNotFoundError(f"No .edi files found in:\n  {EDI_PATH}")
print(f"Found {len(station_list)} station(s): {station_list}")

ocd = occam2d.Data(
    edi_path         = EDI_PATH,
    station_list     = station_list,
    interpolate_freq = True,
    freq             = np.logspace(
                           np.log10(FREQ_MIN),
                           np.log10(FREQ_MAX),
                           FREQ_COUNT
                       ),
)

ocd.save_path          = SAVE_PATH
ocd.geoelectric_strike = GEOELECTRIC_STRIKE
ocd.res_te_err         = RES_TE_ERR
ocd.res_tm_err         = RES_TM_ERR
ocd.phase_te_err       = PHASE_TE_ERR
ocd.phase_tm_err       = PHASE_TM_ERR
ocd.model_mode         = MODEL_MODE

ocd.write_data_file()
print(f"\n✓ Data file written: {DATA_FILE}")
print("\nNext → run  02_build_mesh.py")
