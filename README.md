# GUE Gas Planning

This repository provides tools and a Jupyter notebook for GUE-style gas planning calculations.

Quick links:

- Notebook: `GUE Calculations.ipynb`
- Library: `gue_calc_lib.py`

CI status
---------

The repository includes a simple GitHub Actions workflow at `.github/workflows/ci.yml` that runs the pytest suite. Replace the badge below with the workflow run badge if you want to display status in the repo:

![CI status](https://github.com/<YOUR-ORG>/<YOUR-REPO>/actions/workflows/ci.yml/badge.svg)

Running locally
---------------

1. Create a virtualenv and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Run tests:

```bash
pytest -q
```

3. Open the notebook in Jupyter Lab/Notebook to interact with it:

```bash
jupyter lab
```

Removing CI
-----------

To remove CI, delete `.github/workflows/ci.yml` or remove the `.github/workflows` folder entirely.
