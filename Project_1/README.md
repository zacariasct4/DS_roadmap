# Superhero Portfolio — API + Local JSON + Visuals

A small Python project that:

* Loads superheroes from a **local JSON** file.
* Fetches additional heroes from the **SuperHero API**.
* Builds a small “portfolio” of characters with selected power stats.
* Shows **charts** (bar + radar) for a chosen hero.
* Optionally generates and downloads an **AI image** for that hero.

---

## Data sources

* Local file: `superheros.json`

  * Contains a list of heroes with fields like `id`, `name`, and `powerstats`.
* API: SuperHero API (`https://www.superheroapi.com/api.php`)

  * Used to fetch hero data by ID.

---

## Requirements

* Python 3.x
* Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Environment variables

This project loads environment variables from a **`.env` file in the project root**.

Create a `.env` file next to `requirements.txt` with:

```env
SUPERHERO_API_TOKEN=your_token_here
OPENAI_API_KEY=your_openai_key_here
endpoint_IEBS=your_dalle_endpoint_here
```

Notes:

* `SUPERHERO_API_TOKEN` is required to call the SuperHero API.
* `OPENAI_API_KEY` and `endpoint_IEBS` are required only if you want to generate images.

---

## How it works (high level)

* Reads heroes from `superheros.json`.
* Fetches heroes from the API (by ID).
* Removes duplicates by `id`.
* Builds a filtered list with:

  * `id`, `name`, `intelligence`, `strength`, `speed`
* Asks you to type a hero name and then:

  * Plots stats (bar + radar)
  * Generates an image and downloads it as `<hero_name>.png`

---

## Run

From the project root:

```bash
python src/main.py
```

What you’ll see:

* A printed list of available heroes in the portfolio.
* A prompt asking for the hero name.
* Charts opened in a window/browser.
* If image generation is enabled, a downloaded PNG in the current directory.

---

## Project structure

* `src/main.py` — main script (load data, fetch API, charts, optional image generation)
* `superheros.json` — local hero dataset
* `requirements.txt` — dependencies

---

## Troubleshooting

* **Missing tokens / endpoint**

  * Make sure `.env` is in the project root and variables are correctly named.
* **Hero not found**

  * The search expects an exact match with the printed hero names.
* **Image generation fails**

  * Check `OPENAI_API_KEY` and `endpoint_IEBS` and confirm the endpoint accepts the payload.
