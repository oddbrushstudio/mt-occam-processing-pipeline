"""
STEP 0 — Load EDI Files into MTH5 Collection
==============================================
Reads all .edi files in EDI_PATH and saves them into a single
mt_collection.h5 file. Only needs to be run ONCE per dataset.

After this, all other scripts load from the .h5 file instead of
re-reading the EDI files every time.

Usage:
    python 00_load_edi.py
"""

from pathlib import Path
from mtpy import MTCollection
from config import EDI_PATH, COLLECTION_H5

print("=" * 60)
print("STEP 0: Loading EDI files into MTH5 collection")
print("=" * 60)
print(f"EDI folder:     {EDI_PATH}")
print(f"Collection file: {COLLECTION_H5}")

# Collect EDI file paths
edi_files = list(EDI_PATH.glob("*.edi"))
if not edi_files:
    raise FileNotFoundError(f"No .edi files found in:\n  {EDI_PATH}")
print(f"\nFound {len(edi_files)} EDI file(s):")
for f in sorted(edi_files):
    print(f"  {f.name}")

# Load into collection
with MTCollection() as mc:
    mc.open_collection(COLLECTION_H5)
    mc.add_tf(
        mc.make_file_list(EDI_PATH, file_types=["edi"])
    )

print(f"\n✓ Collection saved: {COLLECTION_H5}")
print("\nNext → run  01_explore.py")
