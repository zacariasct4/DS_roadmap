# Project 2 — House Price Prediction (Linear Regression)

A notebook-based project that builds a **Linear Regression** model to predict **house prices** from housing features.

* Dataset (Kaggle): [https://www.kaggle.com/shree1992/housedata](https://www.kaggle.com/shree1992/housedata)
* Main notebook: `Proyecto_mod2.ipynb`
* Local dataset path used by the notebook: `datasets/data.csv`

---

## What’s inside

* **Phase 1:** Dataset import
* **Phase 2:** Exploratory Data Analysis (EDA)

  * Basic checks (shape, types, nulls)
  * Distribution plots and outlier inspection
  * Correlation analysis + feature pruning
  * Handling categorical columns (`waterfront`, `city`, `statezip`, `date`, etc.)
* **Phase 3:** Training (3 hypotheses)

  * H1: numeric-only + one-hot for `waterfront`
  * H2: target encoding for `date/city/statezip` (manual + smoothed variant)
  * H3: remove low-correlation features (|corr| < 0.1)
* **Phase 4:** Evaluation

  * Metrics: **RMSE** and **R²**
  * Plots: predicted vs actual comparisons

---

## Quick start

### 1) Create an environment (recommended)

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

### 2) Install dependencies

```bash
pip install -r requirements.txt
```

> Note: `requirements.txt` was exported from a notebook environment and may contain many Jupyter-related packages.

### 3) Run the notebook

```bash
jupyter lab
```

* Open: `Proyecto_mod2.ipynb`
* Make sure the dataset exists at: `datasets/data.csv`

---

## Data prep decisions (brief)

To reduce the sensitivity of linear regression to rare extremes, the notebook removes a small number of:

* very high-price houses
* extreme `bedrooms`/`bathrooms`
* under-represented `condition` category

Also drops:

* `sqft_above` (highly redundant with `sqft_living`)
* `country` (single unique value)
* `street` (too high-cardinality; location already covered by `city`/`statezip`)

---

## Outputs you should expect

* Correlation heatmaps
* Distribution plots (histograms/boxplots)
* Predicted vs actual scatter plots
* Printed RMSE/R² comparisons across hypotheses

---

## Repository structure

* `Proyecto_mod2.ipynb` — full workflow (EDA → training → evaluation)
* `datasets/`

  * `data.csv` — dataset file
* `requirements.txt` — dependencies

---

## Next steps (optional)

If you want better predictive performance than linear regression:

* Try non-linear models (Random Forest, Gradient Boosting, XGBoost/LightGBM)
* Consider `log(price)` to reduce skew
* Revisit outlier strategy (robust methods or segmented modelling)
