"""
STEP 1 — Explore Data (Stations, Responses, Strike)
=====================================================
Loads the MTH5 collection and produces:
  • Station location map
  • MT response curves (ρ & φ) for each station
  • Strike analysis plot

Use this to inspect your data and confirm the geoelectric strike
before setting GEOELECTRIC_STRIKE in config.py.

Usage:
    python 01_explore.py
"""

import matplotlib
matplotlib.use("Agg")  # non-interactive backend — safe for scripting
import matplotlib.pyplot as plt
from mtpy import MTCollection
from config import COLLECTION_H5, SAVE_PATH

print("=" * 60)
print("STEP 1: Exploring data")
print("=" * 60)

mc = MTCollection()
mc.open_collection(COLLECTION_H5)
md = mc.to_mt_data()
mc.close_collection()

print(f"Loaded {md.n_stations} station(s)")
print("\nStation locations:")
print(md.station_locations.to_string())

# ── Station map ────────────────────────────────────────────────────────────
print("\nPlotting station map...")
md.plot_stations()
plt.savefig(SAVE_PATH / "stations_map.png", dpi=150, bbox_inches="tight")
plt.close("all")
print(f"✓ Station map saved: {SAVE_PATH / 'stations_map.png'}")

# ── MT responses ───────────────────────────────────────────────────────────
print("\nPlotting MT responses...")
for station_key in md.keys():
    mt_obj = md[station_key]
    mt_obj.plot_mt_response()
    out = SAVE_PATH / f"response_{station_key.replace('.', '_')}.png"
    plt.savefig(str(out), dpi=150, bbox_inches="tight")
    plt.close("all")
    print(f"  ✓ {station_key}")
print(f"✓ Response plots saved to: {SAVE_PATH}")

# ── Strike analysis ────────────────────────────────────────────────────────
print("\nPlotting strike analysis...")
md.plot_strike(period_limits=(1e-3, 100))
plt.savefig(SAVE_PATH / "strike_analysis.png", dpi=150, bbox_inches="tight")
plt.close("all")
print(f"✓ Strike plot saved: {SAVE_PATH / 'strike_analysis.png'}")

print("\nReview plots, then set GEOELECTRIC_STRIKE in config.py")
print("Next → run  02_write_occam.py")
