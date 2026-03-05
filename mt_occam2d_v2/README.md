# MT Occam2D — MTpy v2 Pipeline

A portable, reusable pipeline for 2D Magnetotelluric inversion using **MTpy v2** (`MTCollection` / `MTData` API) and Occam2D.

---

## Setup

### 1. Install the MTpy v2 environment
```bash
conda env create -f mtpy_env.yml
conda activate mtpy
```

### 2. Edit `config.py`
Open `config.py` and set the **three path variables** at the top:

```python
EDI_PATH            = Path(r"C:\path\to\your\edi_files")
SAVE_PATH           = Path(r"C:\path\to\your\output_folder")
OCCAM_RESULTS_PATH  = Path(r"C:\path\to\your\occam2d_results")
```

Everything else — error floors, model mode, mesh parameters, trim cutoffs — is also in `config.py`. You only ever need to edit this one file.

---

## Workflow

| Script | What it does | Run? |
|--------|-------------|------|
| `00_load_edi.py` | Reads `.edi` files → saves `mt_collection.h5` | **Once** |
| `01_explore.py` | Station map, MT responses, strike analysis | Optional but recommended |
| `02_write_occam.py` | Interpolate → set errors → write data/mesh/startup files | Every inversion |
| *(run OCCAM2D binary)* | `occam2d.exe Occam2DStartup` | — |
| `03_trim_data.py` | Remove noisy periods per station | Optional |
| `04_verify_trim.py` | Visual check: kept vs removed data | Optional |
| `05_plot_results.py` | Resistivity model + data fit plots | After inversion |

---

## Key differences from MTpy v1

| v1 | v2 |
|----|----|
| `import mtpy.modeling.occam2d_rewrite as occam2d` | `from mtpy import MTCollection, MTData` |
| EDIs read every run | EDIs loaded **once** into `mt_collection.h5` |
| `occam2d.Data(edi_path=...)` | `md.interpolate(freqs).to_occam2d(...)` |
| Error floors set as `ocd.res_te_err = 10` (%) | Set on `occam2d_obj.dataframe["res_xy_model_error"]` as fraction |
| Model modes as integers `'1'`, `'2'`... | Named strings: `'log_te_tm'`, `'log_all'`, etc. |

---

## Model modes (set `MODEL_MODE` in `config.py`)

| Key | Meaning |
|-----|---------|
| `'log_te_tm'` | Log TE + TM ← recommended default |
| `'log_all'` | Log TE + TM + Tipper |
| `'log_te'` | TE only |
| `'log_tm'` | TM only |
| `'log_te_tip'` | Log TE + Tipper |
| `'log_tm_tip'` | Log TM + Tipper |

---

## Trimming noisy data (optional)

Edit `TRIM_CUTOFFS` in `config.py` — data with period > cutoff will be removed for that station:

```python
TRIM_CUTOFFS = {
    1: float('inf'),  # keep all for station 1
    2: 0.5,           # remove periods > 0.5s for station 2
    3: 500.0,         # remove periods > 500s for station 3
}
```

Add `STATION_NAMES` so reports show real names:
```python
STATION_NAMES = {1: 'SG2201', 2: 'SG2203'}
```

Then run `03_trim_data.py` → `04_verify_trim.py`, update your Occam2DStartup, and re-run the binary.

---

## File structure
```
mt_occam2d_v2/
├── config.py             ← EDIT THIS FIRST
├── 00_load_edi.py
├── 01_explore.py
├── 02_write_occam.py
├── 03_trim_data.py
├── 04_verify_trim.py
├── 05_plot_results.py
└── README.md
```
