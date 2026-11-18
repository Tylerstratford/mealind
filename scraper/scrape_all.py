"""
MealMind — Master Scraper
Runs all site scrapers and merges results into a single recipes.json
Run: python scrape_all.py [--limit 100]
"""
import subprocess
import json
import argparse
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
OUTPUT_FILE = DATA_DIR / "recipes.json"
# Also copy to Vue app's public folder so Vite can serve it
APP_PUBLIC = Path(__file__).parent.parent / "app" / "public" / "data"


def merge_recipes():
    all_recipes = []
    seen_ids = set()

    for fname in ["recipes_ica.json", "recipes_coop.json", "recipes_mathem.json", "recipes_arla.json", "recipes_koket.json"]:
        fpath = DATA_DIR / fname
        if fpath.exists():
            with open(fpath, encoding="utf-8") as f:
                recipes = json.load(f)
            for r in recipes:
                if r["id"] not in seen_ids and r.get("name"):
                    all_recipes.append(r)
                    seen_ids.add(r["id"])
            print(f"  ✓ {fname}: {len(recipes)} recipes")
        else:
            print(f"  ⚠ {fname} not found (run individual scraper first)")

    return all_recipes


def main():
    parser = argparse.ArgumentParser(description="Run all scrapers and merge results")
    parser.add_argument("--limit", type=int, default=100,
                        help="Max recipes per site (default: 100)")
    parser.add_argument("--skip-scraping", action="store_true",
                        help="Skip scraping, just merge existing JSON files")
    parser.add_argument("--append", action="store_true",
                        help="Add new recipes to existing files instead of overwriting")
    args = parser.parse_args()

    if not args.skip_scraping:
        scrapers = [
            ("ICA.se",    "scrape_ica.py"),
            ("Coop.se",   "scrape_coop.py"),
            ("Mathem.se", "scrape_mathem.py"),
            ("Arla.se",   "scrape_arla.py"),
            ("Koket.se",  "scrape_koket.py"),
        ]
        for name, script in scrapers:
            print(f"\n{'='*50}")
            print(f"  Scraping {name}…")
            print(f"{'='*50}")
            cmd = ["python3", script, "--limit", str(args.limit)]
            if args.append:
                cmd.append("--append")
            subprocess.run(cmd, cwd=Path(__file__).parent)

    print(f"\n{'='*50}")
    print("  Merging all recipes…")
    print(f"{'='*50}")

    recipes = merge_recipes()

    # Save to data/
    DATA_DIR.mkdir(exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(recipes, f, ensure_ascii=False, indent=2)
    print(f"\n✅ Merged {len(recipes)} total recipes → {OUTPUT_FILE}")

    # Copy to Vue public folder so app can load it
    APP_PUBLIC.mkdir(parents=True, exist_ok=True)
    app_output = APP_PUBLIC / "recipes.json"
    with open(app_output, "w", encoding="utf-8") as f:
        json.dump(recipes, f, ensure_ascii=False, indent=2)
    print(f"✅ Also copied to Vue public folder → {app_output}")
    print("\n🚀 Ready! Start the app with: cd app && npm install && npm run dev")


if __name__ == "__main__":
    main()
