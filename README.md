# 🥗 MealMind

A Swedish meal planner app that scrapes recipes from ICA, Coop, and Mathem, helps you plan 7 days of meals, builds a shopping list, and exports it for ordering at Willys.se.

## Quick Start

### 1. Install Python dependencies (for scraper)
```bash
cd scraper
pip install -r requirements.txt
```

### 2. Scrape recipes
```bash
# Scrape ~100 recipes from all sites
python scrape_all.py --limit 100

# Or scrape individual sites
python scrape_ica.py --limit 100
python scrape_coop.py --limit 100
python scrape_mathem.py --limit 50
```

### 3. Start the local API server (optional — needed for URL import and AI normalization)
```bash
cd scraper
pip install anthropic  # only needed once, for AI normalization
python3 server.py
# or from the repo root
cd scraper && python3 server.py
```
Runs on http://localhost:8742. Keep this running in a separate terminal alongside the Vue app.

### 4. Start the Vue app
```bash
cd app
npm install
npm run dev
```
Open http://localhost:5173 in your browser.

---

## Project Structure

```
mealmind/
├── scraper/
│   ├── scrape_all.py       ← Run all scrapers + merge
│   ├── scrape_ica.py       ← ICA.se scraper
│   ├── scrape_coop.py      ← Coop.se scraper
│   ├── scrape_mathem.py    ← Mathem.se scraper
│   ├── scrape_arla.py      ← Arla.se scraper
│   ├── scrape_koket.py     ← Koket.se scraper
│   ├── server.py           ← Local API server (URL import + AI normalization)
│   └── requirements.txt
├── data/
│   ├── recipes.json        ← Merged recipe database
│   ├── recipes_ica.json
│   ├── recipes_coop.json
│   ├── recipes_mathem.json
│   ├── recipes_arla.json
│   └── recipes_koket.json
└── app/                    ← Vue 3 frontend
    ├── src/
    │   ├── views/
    │   │   ├── MealPlanner.vue   ← 7-day planner with lock/swap/save
    │   │   ├── ShoppingList.vue  ← Shopping list with AI normalization
    │   │   ├── Recipes.vue       ← Browse all recipes
    │   │   ├── MyRecipes.vue     ← Manage custom recipes
    │   │   └── AddRecipe.vue     ← Add/edit custom recipes
    │   └── stores/
    │       ├── recipes.js        ← Recipe data store (Pinia)
    │       └── mealplan.js       ← Meal plan + shopping list logic
    └── public/data/
        └── recipes.json          ← Served to the app (copy of data/recipes.json)
```

## Recipe Data Schema

```json
{
  "id": "unique-uuid",
  "source": "ica | coop | mathem",
  "name": "Recipe name",
  "url": "https://...",
  "image": "https://... (or empty)",
  "time": "30 min",
  "servings": "4",
  "ingredients": [
    { "name": "Pasta", "quantity": "400", "unit": "g" }
  ],
  "tags": ["pasta", "kött"],
  "description": "Short description"
}
```

## Workflow

1. **Planner** → Generate a 7-day meal plan → Lock meals you like → Regenerate the rest
2. **Shopping List** → Auto-generated from planned meals → Check off items you have → Add extras
3. **Export** → Copy list → Use with Willys.se ordering skill in Claude

## Adding More Recipes

Re-run the scraper with a higher limit at any time:
```bash
cd scraper && python scrape_all.py --limit 300
```
The `scrape_all.py` script automatically copies the merged `recipes.json` to the Vue app's public folder.
