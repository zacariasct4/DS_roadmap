# DS_roadmap
# Superhero Stats Explorer 🦸‍♂️🦸‍♀️  
**Local JSON + SuperHero API + Interactive Visualisations + AI Image Generation**

A small Python project for the community that combines:
- **Local data** (a JSON file with superheroes),
- **Live API data** (SuperHero API),
- **Data cleaning/deduplication**,
- **Quick visual analytics** (Matplotlib + Plotly),
- And an **optional image generation** step (if you have an OpenAI-compatible image endpoint configured).

The goal is to showcase a clean, beginner-friendly pipeline: **load → fetch → merge → filter → visualise → interact**.

---

## ✨ Features

- Loads **5 superheroes from a local JSON** (`superheros.json`)
- Fetches **5 superheroes from the SuperHero API** (by ID)
- Merges both sources and **removes duplicates** by `id`
- Extracts and works with a subset of stats:
  - `intelligence`, `strength`, `speed`
- Builds visualisations:
  - **Matplotlib** bar chart + pie chart
  - **Plotly** radar chart (polar)
- CLI interaction:
  - You type a superhero name and get their charts
- AI interaction:
  - Generates an AI image of a character inspired by the hero name (requires your own configured endpoint)
