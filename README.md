# MT Occam2D Processing Pipeline

**Author:** Oseni Olaonipekun  
**Contact:** oddbrushstudio@gmail.com

A portable, config-driven pipeline for Magnetotelluric (MT) data processing and 2D inversion, built on MTpy and Occam2D. The repository is organized into two pipelines that work together — V2 for data loading and exploration, V1 for inversion.

---

## Repository Structure

```
mt-occam-processing-pipeline/
├── README.md                  ← you are here
├── mt_occam2d_v2/             ← data loading & exploration (MTpy v2)
│   ├── config.py
│   ├── 00_load_edi.py
│   ├── 01_explore.py
│   ├── README.md
│   └── mt_v2.yml
└── mt_occam2d_v1/             ← inversion pipeline (MTpy v1)
    ├── config.py
    ├── 01_write_data.py
    ├── 02_build_mesh.py
    ├── 03_trim_data.py
    ├── 04_verify_trim.py
    ├── 05_plot_results.py
    ├── README.md
    └── mt_v1.yml
```

---

## How V1 and V2 Relate

| Pipeline | Purpose | MTpy Version |
|----------|---------|--------------|
| **V2** | Load EDI files, inspect station map, plot MT response curves, determine geoelectric strike | MTpy v2 |
| **V1** | Write inversion input files, build mesh, trim data, run inversion, plot results | MTpy v1 |

Start with V2 to explore your data and confirm the geoelectric strike angle, then use V1 to prepare input files and run the inversion.

---

## Requirements

### 1. Occam2D Binary

This pipeline requires the **Occam2D binary** — a separate executable not included in this repository. Download and compile it from the official source:

> Scripps Institution of Oceanography — Marine EM Lab  
> https://marineemlab.ucsd.edu/Projects/Occam/2DMT/index.html

Follow the compilation instructions on that page. Once compiled, place the binary somewhere accessible and note its path — you will call it manually after running `02_build_mesh.py`.

### 2. Python Environments

Two separate conda environments are required — one for each pipeline.

**V2 environment:**
```bash
conda env create -f mt_occam2d_v2/mt_v2.yml
conda activate mt_v2
```

**V1 environment:**
```bash
conda env create -f mt_occam2d_v1/mt_v1.yml
conda activate mt_v1
```

---

## Full Workflow

### Step 1 — Explore your data (V2)
```bash
conda activate mt_v2
cd mt_occam2d_v2
```
Edit `config.py` with your EDI path and output folder, then:
```bash
python 00_load_edi.py
python 01_explore.py
```
Review the output plots and note the geoelectric strike angle from `strike_analysis.png`.

---

### Step 2 — Prepare inversion files (V1)
```bash
conda activate mt_v1
cd mt_occam2d_v1
```
Edit `config.py` with your paths and set `GEOELECTRIC_STRIKE` from Step 1, then:
```bash
python 01_write_data.py
python 02_build_mesh.py
```

---

### Step 3 — Run the Occam2D binary
Navigate to your output folder and run:
```bash
occam2d.exe Occam2DStartup
```
This produces `ITER` and `RESP` files for each iteration.

---

### Step 4 — Trim noisy data (optional)
If initial RMS is high, inspect your response curves and set per-station period cutoffs in `config.py`, then:
```bash
python 03_trim_data.py
python 04_verify_trim.py
```
Update `Occam2DStartup` to point to `OccamDataFile_trimmed.dat` and re-run the binary.

---

### Step 5 — Plot results (V1)
Set `ITER_NUMBER` in `05_plot_results.py` to your target iteration, then:
```bash
python 05_plot_results.py
```

---

## Notes

- Each pipeline has its own `config.py` — all parameters for that pipeline live there. You only ever need to edit `config.py`.
- The V2 inversion API is still under active development. V1 is used for all inversion input file preparation and result plotting.
- See the README inside each folder for pipeline-specific instructions.
