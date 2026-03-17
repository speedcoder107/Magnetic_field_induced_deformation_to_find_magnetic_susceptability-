# Magnetic Field Induced Deformation to Find Magnetic Susceptibility

This repository contains an experimental + computational workflow for estimating magnetic susceptibility of liquids from magnetic-field-induced surface deformation ("Moses effect") measured via laser reflection.

## Project Context (from PDFs + code)

### 1) Reference paper: `095112_1_online.pdf`
The paper title text extracted from the PDF indicates it is a Review of Scientific Instruments article on a *simple technique to measure magnetic susceptibility of liquids* using modest applied fields and optical readout.

From extracted content, the approach is:
- apply a magnetic field to a liquid surface,
- measure deformation through laser-bounce/deflection,
- balance magnetic, gravitational, and surface-energy terms,
- estimate susceptibility for diamagnetic/paramagnetic liquids.

Extracted text also references DOI `10.1063/1.4749847` and mentions NdFeB magnets, low-cost setup, and copper sulfate as an example liquid.

### 2) Project report: `Final_Report.pdf`
The report text extraction indicates the project is titled approximately:
- *Exploring Magnetic Field-Induced Deformations in Fluids to Find Susceptibility*

The report describes:
- measuring deformation of liquid surface under magnetic field,
- detecting displacement via an optical laser-reflection method,
- processing measurements for water and 1M copper sulfate,
- comparing measured values against expected susceptibility with reported deviations around ~10%.

Note: PDF extraction on this machine was partially garbled (missing PDF text tooling), so exact mathematical notation/significant figures in the report could not be reconstructed perfectly from raw text streams.

## Repository Workflow

### Data and image processing
1. Capture images of laser spot while stepping magnet position.
2. Convert images if needed:
   - `jpg_to_png.py` converts `.JPG` files to `.png`.
3. Optional pixel filtering:
   - `process_image.py` applies threshold-based red-pixel cleanup.
4. Extract spot geometry and distance:
   - `my_module.py` (`find_red_circle_diameters_and_distances`) scans each image for red spot boundaries and computes:
     - spot diameter (px)
     - center distance from image bottom (px)
5. Convert pixel units and write CSV:
   - `my_module.py` has conversion and CSV helpers.
   - `convert_csv_from_image.py` shows a usage pattern and post-adjusts `copper_sulphate.csv`.

### Analysis notebooks
- `data_analysis water.ipynb`
- `data_analysis copper sulphate.ipynb`

Both notebooks:
- load CSV trajectories,
- average repeated measurements,
- compute angular deflection from geometry,
- integrate deflection (trapezoidal integration) to estimate displacement profile,
- visualize angle/displacement/height curves (outputs in `all_images/...`).

### Utility notebook
- `compression.ipynb`: scans for large files and compresses them to `.zip`.

## Key Files
- `my_module.py`: reusable image + averaging utilities.
- `process_image.py`: threshold filter for image cleanup.
- `jpg_to_png.py`: batch conversion utility.
- `convert_csv_from_image.py`: CSV generation/adjustment script.
- `magnet.py`: small curve-fit sandbox (`y = k/x^2`).
- `water.csv`, `copper_sulphate.csv`: processed measurement data.

## Install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Typical usage

```bash
# 1) Convert source images (if required)
python jpg_to_png.py

# 2) Process images (optional thresholding)
python process_image.py

# 3) Run notebook analysis
# Open Jupyter and run:
# - data_analysis water.ipynb
# - data_analysis copper sulphate.ipynb
```

## Output artifacts
- CSV data tables (`water.csv`, `copper_sulphate.csv`)
- Plot files under `all_images/water/` and `all_images/copper_sulphate/`
- (after running compression utility) zipped large files

