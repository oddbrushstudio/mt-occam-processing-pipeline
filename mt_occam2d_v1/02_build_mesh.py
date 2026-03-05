"""
================================================================================
Author  : Oseni Olaonipekun
Contact : oddbrushstudio@gmail.com
================================================================================

STEP 2 — Build Mesh, Regularization & Startup File
====================================================
Reads the data file written in Step 1 and produces:
  • MESH file
  • Regularization file
  • Occam2DStartup file

Run AFTER 01_write_data.py.

Usage:
    python 02_build_mesh.py
"""

import mtpy.modeling.occam2d_rewrite as occam2d
from config import (
    SAVE_PATH, DATA_FILE,
    N_LAYERS, Z1_LAYER, Z_TARGET_DEPTH,
    X_PAD_MULTIPLIER, NUM_X_PAD_CELLS,
    RESISTIVITY_START, ITERATIONS_TO_RUN, TARGET_MISFIT,
)

print("=" * 60)
print("STEP 2: Building mesh, regularization & startup")
print("=" * 60)

# ── Read the data file to get station locations ────────────────────────────
ocd = occam2d.Data()
ocd.read_data_file(DATA_FILE)
print(f"Read data file: {DATA_FILE}")
print(f"Stations: {len(ocd.station_locations)}")

# ── Build mesh & regularization ────────────────────────────────────────────
ocm = occam2d.Regularization(ocd.station_locations)
ocm.n_layers         = N_LAYERS
ocm.z1_layer         = Z1_LAYER
ocm.z_target_depth   = Z_TARGET_DEPTH
ocm.x_pad_multiplier = X_PAD_MULTIPLIER
ocm.num_x_pad_cells  = NUM_X_PAD_CELLS
ocm.save_path        = SAVE_PATH

ocm.build_mesh()
ocm.build_regularization()
ocm.write_mesh_file()
ocm.write_regularization_file()
print(f"\n✓ Mesh file:          {ocm.mesh_fn}")
print(f"✓ Regularization:     {ocm.reg_fn}")
print(f"  Free parameters:    {ocm.num_free_param}")

# ── Write startup file ─────────────────────────────────────────────────────
ocs = occam2d.Startup()
ocs.data_fn           = DATA_FILE
ocs.model_fn          = ocm.reg_fn
ocs.param_count       = ocm.num_free_param
ocs.save_path         = SAVE_PATH
ocs.resistivity_start = RESISTIVITY_START
ocs.iterations_to_run = ITERATIONS_TO_RUN
ocs.target_misfit     = TARGET_MISFIT
ocs.write_startup_file()

print(f"✓ Startup file:       {ocs.startup_fn}")
print("\n" + "=" * 60)
print("ALL INPUT FILES READY — now run OCCAM2D binary.")
print("  e.g.  occam2d.exe Occam2DStartup")
print("=" * 60)
print("\nNext → run  03_trim_data.py  (if you need to remove bad periods)")
print("       or   05_plot_results.py  (after inversion is complete)")
