# MT Occam2D — MTpy v2 Pipeline

**Author:** Oseni Olaonipekun  
**Contact:** oddbrushstudio@gmail.com

A portable, reusable pipeline for Magnetotelluric data loading and exploration using **MTpy v2** (`MTCollection` / `MTData` API).

---

## Setup

### 1. Install the MTpy v2 environment
```bash
conda env create -f mt_v2.yml
conda activate mt_v2
```
Or with pip:
```bash
pip install mtpy-v2
```

### 2. Edit `config.py`
Open `config.py` and set the two path variables:

```python
EDI_PATH  = Path(r"C:\path\to\your\edi_files")
SAVE_PATH = Path(r"C:\path\to\your\output_folder")
```

Review the strike angle after running `01_explore.py` and update:
```python
GEOELECTRIC_STRIKE = 30  # degrees from North
```

---

## Workflow

| Script | What it does | Run? |
|--------|-------------|------|
| `00_load_edi.py` | Reads `.edi` files → saves `mt_collection.h5` | **Once** |
| `01_explore.py` | Station map, MT response curves, strike analysis | Each session |

---

## Output files

After running both scripts your `SAVE_PATH` folder will contain:

| File | Description |
|------|-------------|
| `mt_collection.h5` | Consolidated MTH5 collection |
| `stations_map.png` | Station location map |
| `response_<station>.png` | MT response curve per station |
| `strike_analysis.png` | Geoelectric strike rose diagram |

---

## File structure
```
mt_occam2d_v2/
├── config.py          ← EDIT THIS FIRST
├── 00_load_edi.py
├── 01_explore.py
├── README.md
└── mt_v2.yml
```
