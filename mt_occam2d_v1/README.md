# MT Occam2D — MTpy v1 Pipeline

A portable, reusable pipeline for 2D Magnetotelluric inversion using MTpy and Occam2D.

---

## Setup

### 1. Install the MTpy environment
Import the conda environment exported from the original machine:
```bash
conda env create -f mt_v1.yml
conda activate mt_v1
```
Or if you received a `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 2. Configure your paths and parameters
**Open `config.py` and edit the three path variables at the top:**

```python
EDI_PATH     = r"C:\path\to\your\edi_files"
SAVE_PATH    = r"C:\path\to\your\occam2d_binary_folder"
OUTPUT_PATH  = r"C:\path\to\your\output_folder"
```

- `EDI_PATH` — folder containing your `.edi` files
- `SAVE_PATH` — folder where your `occam2d.exe` binary is located. Input files are written here and the binary runs from here.
- `OUTPUT_PATH` — folder where all plots, maps and result images are saved.

Everything else (error floors, mesh parameters, inversion settings) can also be adjusted in `config.py`. You only ever need to edit this one file.

---

## Workflow

Run the scripts in order:

| Script | What it does |
|--------|-------------|
| `01_write_data.py` | Reads `.edi` files → writes `OccamDataFile.dat` |
| `02_build_mesh.py` | Builds mesh, regularization, and startup file |
| *(run OCCAM2D binary)* | `occam2d.exe Occam2DStartup` |
| `03_trim_data.py` | *(optional)* Removes noisy periods per station |
| `04_verify_trim.py` | *(optional)* Plots kept vs removed data points |
| `05_plot_results.py` | Plots resistivity model and data fit |

---

## Trimming noisy data (optional)

If some stations have bad data at long or short periods, edit `TRIM_CUTOFFS` in `config.py`:

```python
TRIM_CUTOFFS = {
    1: float('inf'),  # keep all periods for station 1
    2: 0.5,           # remove periods > 0.5s for station 2
    3: 500.0,         # remove periods > 500s for station 3
}
```

Also fill in `STATION_NAMES` so the trim report shows real names:
```python
STATION_NAMES = {1: 'SG2201', 2: 'SG2203', 3: 'SG2202'}
```

Then run `03_trim_data.py` → `04_verify_trim.py`. Update your Occam2DStartup to point to `OccamDataFile_trimmed.dat` and re-run the binary.

---

## Plotting results

Set `ITER_NUMBER` at the top of `05_plot_results.py` to whichever iteration you want to visualise, then run it.

---

## File structure
```
mt_occam2d_v1/
├── config.py            ← EDIT THIS FIRST
├── 01_write_data.py
├── 02_build_mesh.py
├── 03_trim_data.py
├── 04_verify_trim.py
├── 05_plot_results.py
├── README.md
└── mt_v1.yml
```
**Author:** Oseni Olaonipekun  
**Contact:** oddbrushstudio@gmail.com
