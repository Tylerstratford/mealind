"""
Arla.se Recipe Scraper — async, parallel workers
Run: python3 scrape_arla.py [--limit 100] [--workers 5]
"""
import asyncio
import json
import re
import argparse
import uuid
from pathlib import Path
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from utils import is_valid_recipe, extract_jsonld_recipe, find_jsonld_recipe

BASE_URL = "https://www.arla.se"
RECIPE_LIST_URL = "https://www.arla.se/recept/"
OUTPUT_FILE = Path(__file__).parent.parent / "data" / "recipes_arla.json"
SOURCE = "arla"


async def get_recipe_urls(page, limit):
    urls = set()
    current_page = 1

    while len(urls) < limit:
        url = f"{RECIPE_LIST_URL}?page={current_page}"
        print(f"  Listing page {current_page}…")
        await page.goto(url, wait_until="networkidle", timeout=30000)
        await page.wait_for_timeout(1000)

        soup = BeautifulSoup(await page.content(), "lxml")
        found_before = len(urls)

        for a in soup.select("a[href]"):
            href = a.get("href", "")
            if re.match(r"^/recept/[a-z0-9\-]+/?$", href) and href != "/recept/":
                urls.add(BASE_URL + href)

        if len(urls) == found_before:
            print(f"  No new recipes on page {current_page}, stopping.")
            break

        print(f"  Page {current_page}: {len(urls)} URLs so far")
        current_page += 1

    return list(urls)[:limit]


async def parse_recipe(context, url, semaphore):
    async with semaphore:
        page = await context.new_page()
        try:
            await page.goto(url, wait_until="networkidle", timeout=30000)
            await page.wait_for_timeout(500)
            soup = BeautifulSoup(await page.content(), "lxml")

            data = find_jsonld_recipe(soup)
            if data:
                return extract_jsonld_recipe(data, url, SOURCE)

            # HTML fallback
            name = (soup.select_one("h1") or soup.new_tag("x")).get_text(strip=True)
            image_el = soup.select_one("img[class*='recipe'], .recipe img, article img")
            ingredients = [
                {"name": li.get_text(strip=True), "quantity": "", "unit": ""}
                for li in soup.select("[class*='ingredient'] li, .ingredients li")
                if li.get_text(strip=True)
            ]
            return {
                "id": str(uuid.uuid4()), "source": SOURCE, "name": name, "url": url,
                "image": image_el.get("src", "") if image_el else "",
                "time": "", "servings": "", "ingredients": ingredients,
                "tags": [], "description": ""
            }
        except Exception as e:
            print(f"    x {url}: {e}")
            return None
        finally:
            await page.close()


async def main_async(limit, workers, append):
    print(f"Scraping up to {limit} Arla recipes with {workers} parallel workers…\n")

    existing_recipes = []
    existing_urls = set()
    existing_images = set()
    if append and OUTPUT_FILE.exists():
        with open(OUTPUT_FILE, encoding="utf-8") as f:
            existing_recipes = json.load(f)
        existing_urls = {r["url"] for r in existing_recipes}
        existing_images = {r.get("image", "") for r in existing_recipes}
        print(f"Loaded {len(existing_recipes)} existing recipes, will skip already-scraped URLs\n")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/121.0 Safari/537.36",
            locale="sv-SE"
        )

        nav_page = await context.new_page()
        print("Collecting recipe URLs…")
        all_urls = await get_recipe_urls(nav_page, limit)
        await nav_page.close()

        urls = [u for u in all_urls if u not in existing_urls]
        print(f"  {len(all_urls)} found, {len(all_urls) - len(urls)} already scraped, {len(urls)} new\n")

        semaphore = asyncio.Semaphore(workers)
        tasks = [parse_recipe(context, url, semaphore) for url in urls]

        new_recipes = []
        seen_images = existing_images.copy()
        results = await asyncio.gather(*tasks)

        for recipe in results:
            valid, reason = is_valid_recipe(recipe, seen_images)
            if valid:
                new_recipes.append(recipe)
                print(f"  + {recipe['name']}")
            else:
                name = recipe["name"] if recipe and recipe.get("name") else "unknown"
                print(f"  - Skipped ({reason}): {name}")

        await browser.close()

    all_recipes = existing_recipes + new_recipes
    OUTPUT_FILE.parent.mkdir(exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_recipes, f, ensure_ascii=False, indent=2)

    print(f"\nSaved {len(all_recipes)} Arla recipes ({len(new_recipes)} new) -> {OUTPUT_FILE}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=100)
    parser.add_argument("--workers", type=int, default=5,
                        help="Number of parallel browser pages (default: 5)")
    parser.add_argument("--append", action="store_true",
                        help="Add new recipes to existing file instead of overwriting")
    args = parser.parse_args()
    asyncio.run(main_async(args.limit, args.workers, args.append))


if __name__ == "__main__":
    main()
