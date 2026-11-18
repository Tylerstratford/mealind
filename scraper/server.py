"""
MealMind — Local Scraper API Server
Lets the Vue app fetch and parse a recipe from any URL.

Run: python3 server.py
Then the app can POST to http://localhost:8742/scrape
"""
import asyncio
import json
import re
import uuid
from contextlib import asynccontextmanager
from typing import List

try:
    import anthropic
except ImportError:  # allow server to start without anthropic installed
    anthropic = None

import uvicorn
from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

from utils import find_jsonld_recipe, find_microdata_recipe, extract_jsonld_recipe, parse_ingredients

# Shared browser instance (created on startup, reused per request)
_browser = None
_playwright = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global _browser, _playwright
    print("🚀 Starting browser…")
    _playwright = await async_playwright().start()
    _browser = await _playwright.chromium.launch(headless=True)
    print("✅ Browser ready. Server listening on http://localhost:8742")
    yield
    await _browser.close()
    await _playwright.stop()
    print("🛑 Browser closed.")


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)


class ScrapeRequest(BaseModel):
    url: str


class Ingredient(BaseModel):
    name: str
    quantity: str = ""
    unit: str = ""


class NormalizeRequest(BaseModel):
    ingredients: List[Ingredient]


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/scrape")
async def scrape(req: ScrapeRequest):
    url = req.url.strip()
    if not url.startswith("http"):
        raise HTTPException(status_code=400, detail="Invalid URL")

    context = await _browser.new_context(
        user_agent=(
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/121.0.0.0 Safari/537.36"
        ),
        locale="sv-SE"
    )
    page = await context.new_page()

    try:
        await page.goto(url, wait_until="networkidle", timeout=30000)
        await page.wait_for_timeout(1500)
        html = await page.content()
        soup = BeautifulSoup(html, "lxml")

        from urllib.parse import urlparse
        domain = urlparse(url).netloc
        source = "ica" if "ica.se" in domain else \
                 "coop" if "coop.se" in domain else \
                 "mathem" if "mathem.se" in domain else "other"

        # 1. JSON-LD structured data (covers ~70% of recipe sites)
        data = find_jsonld_recipe(soup)

        # 2. Microdata fallback (itemscope/itemtype, covers most of the rest)
        if not data:
            data = find_microdata_recipe(soup)

        if data:
            recipe = extract_jsonld_recipe(data, url, source)
            return {"success": True, "recipe": recipe}

        # 3. HTML heuristics — handles blogs that use plain <p>/<li> without schema markup
        from utils import extract_ingredients_from_paragraphs

        name_el = soup.select_one("h1")
        name = name_el.get_text(strip=True) if name_el else ""

        og_image = soup.select_one("meta[property='og:image']")
        if og_image:
            image = og_image.get("content", "")
        else:
            image_el = soup.select_one(
                "img[class*='recipe'], img[class*='hero'], article img, "
                ".recipe img, [class*='Recipe'] img"
            )
            image = image_el.get("src", "") if image_el else ""

        # Try <li> elements first, then fall back to paragraph scanning
        ingredient_els = (
            soup.select(".ingredients li") or
            soup.select("[class*='ingredient'] li") or
            soup.select("[class*='Ingredient'] li") or
            soup.select("[class*='recipe'] li") or
            []
        )
        if ingredient_els:
            ingredients = [
                {"name": li.get_text(strip=True), "quantity": "", "unit": ""}
                for li in ingredient_els
                if li.get_text(strip=True)
            ]
        else:
            # Scan <p> tags for lines that start with quantities — works for plain blog posts
            ingredients = extract_ingredients_from_paragraphs(soup)

        time_el = soup.select_one("[class*='time'], [class*='Time'], time")
        time_str = time_el.get_text(strip=True) if time_el else ""

        desc_el = soup.select_one(
            "meta[name='description'], meta[property='og:description']"
        )
        description = desc_el.get("content", "") if desc_el else ""

        if not name:
            raise HTTPException(
                status_code=422,
                detail="Could not extract recipe from this page. It may not contain recognisable recipe data."
            )

        recipe = {
            "id": str(uuid.uuid4()),
            "source": source,
            "name": name,
            "url": url,
            "image": image,
            "time": time_str,
            "servings": "",
            "ingredients": ingredients,
            "tags": [],
            "description": description
        }
        return {"success": True, "recipe": recipe, "partial": True}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await page.close()
        await context.close()


@app.post("/normalize")
async def normalize(req: NormalizeRequest, x_api_key: str = Header(None)):
    if anthropic is None:
        raise HTTPException(
            status_code=503,
            detail="Anthropic SDK not installed. Run 'pip install anthropic' to enable normalization."
        )

    if not x_api_key:
        raise HTTPException(status_code=401, detail="Anthropic API key required. Pass it as the X-Api-Key header.")

    items_text = "\n".join([
        f"- {item.name}: {item.quantity} {item.unit}".rstrip()
        for item in req.ingredients
    ])

    prompt = f"""You are a shopping list assistant. Normalize this ingredient list by:
1. Merging duplicate or similar items (e.g. "potatoe", "Potatoes", "potato" all become "Potatoes")
2. Summing quantities of merged items when they share the same unit (e.g. 200g + 300g = 500g)
3. Fixing spelling mistakes and capitalizing ingredient names properly
4. Keeping items that cannot be summed (different units or no quantity) as separate entries if they are genuinely different ingredients

Return ONLY a valid JSON array with no other text, markdown, or explanation.
Format: [{{"name": "string", "quantity": "string", "unit": "string"}}]

Ingredients:
{items_text}"""

    try:
        client = anthropic.Anthropic(api_key=x_api_key)
        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt}]
        )
        result_text = message.content[0].text.strip()

        # Extract JSON array from response
        match = re.search(r'\[.*\]', result_text, re.DOTALL)
        if not match:
            raise HTTPException(status_code=500, detail="AI response did not contain a valid JSON array.")
        normalized = json.loads(match.group())
    except anthropic.AuthenticationError:
        raise HTTPException(status_code=401, detail="Invalid Anthropic API key.")
    except anthropic.APIError as e:
        raise HTTPException(status_code=502, detail=f"Anthropic API error: {e}")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Failed to parse the AI response as JSON.")

    return {"normalized": normalized}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8742, log_level="warning")
