# Module 2 Project — House Price Prediction (Linear Regression)

Predict house **prices** using a **Linear Regression** model and the Kaggle dataset: [https://www.kaggle.com/shree1992/housedata](https://www.kaggle.com/shree1992/housedata)

## What this project does

* Loads and explores a housing dataset.
* Cleans a small number of extreme / under-represented cases to reduce outlier impact.
* Trains and compares **three feature/encoding hypotheses**.
* Evaluates with **RMSE** and **R²**, plus simple prediction plots.

## Dataset

* Source: Kaggle (House Data)
* Local file expected at: `datasets/data.csv`
* Target column: `price`

## Approach (high level)

### Data preparation

* Removed a few rare extremes (very high `price`, very high `bedrooms`/`bathrooms`) and `condition == 1`.
* Dropped redundant / unhelpful columns:

  * `sqft_above` (highly correlated with `sqft_living`)
  * `country` (single value)
  * `street` (very high cardinality; location already covered by `city` and `statezip`)

### Modelling hypotheses

* **H1 — Numeric-only:** drop `object` columns; one-hot encode `waterfront`.
* **H2 — Target Encoding:** target-encode `date`, `city`, `statezip` (manual and smoothed variants); one-hot encode `waterfront`.
* **H3 — Feature reduction:** starting from H2 (manual), drop features with `|corr(price, feature)| < 0.1`.

## Results summary

* Linear Regression shows **large errors overall** (the relationship is not fully linear).
* Best performance was obtained with **H2 (manual target encoding)**, but differences vs other hypotheses were **very small**.
* Removing `price == 0` cases provided a **small improvement**.

## How to run

### 1) Create environment and install dependencies

```bash
pip install -r requirements.txt
```

### 2) Ensure dataset path

* Place the file at: `datasets/data.csv`

### 3) Run

* Execute the notebook/script that contains the pipeline (EDA → training → evaluation).

## Repo structure (suggested)

* `datasets/`

  * `data.csv`
* `notebooks/`

  * `module2_house_price_regression.ipynb`
* `requirements.txt`
* `README.md`

## Tech stack

* Python, pandas, numpy
* scikit-learn
* matplotlib, seaborn
* category_encoders

## Next steps (optional)

* Try non-linear models (Random Forest, Gradient Boosting, XGBoost/LightGBM).
* Consider transforming the target (e.g., `log(price)`) to reduce skew.
