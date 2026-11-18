"""
Shared utilities for MealMind scrapers.
"""
import re
import uuid
import json
from html import unescape


def is_valid_recipe(recipe, seen_images):
    if not recipe or not recipe["name"]:
        return False, "no name"
    if not recipe["ingredients"]:
        return False, "no ingredients"
    img = recipe.get("image", "").strip()
    if not img:
        return False, "no image"
    if img in seen_images:
        return False, "reused placeholder image"
    seen_images.add(img)
    return True, "ok"


def parse_duration(s):
    if not s:
        return ""
    h = re.search(r"(\d+)H", s)
    m = re.search(r"(\d+)M", s)
    parts = []
    if h:
        parts.append(f"{h.group(1)}h")
    if m:
        parts.append(f"{m.group(1)} min")
    return " ".join(parts)


def normalize_tags(tags):
    if isinstance(tags, str):
        return [tags] if tags else []
    return [t for t in tags if t]


def parse_image(image):
    if isinstance(image, list):
        raw = image[0].get("url", "") if image and isinstance(image[0], dict) else (image[0] if image else "")
    elif isinstance(image, dict):
        raw = image.get("url", "")
    else:
        raw = image or ""
    return unescape(raw)


def parse_ingredients(raw_list):
    ingredients = []
    for raw in raw_list:
        raw = raw.strip()
        match = re.match(r"^([\d.,½¼¾/]+)\s*([a-zA-ZåäöÅÄÖ]+)?\s+(.+)$", raw)
        if match:
            ingredients.append({
                "name": match.group(3).strip(),
                "quantity": match.group(1),
                "unit": match.group(2) or ""
            })
        else:
            ingredients.append({"name": raw, "quantity": "", "unit": ""})
    return ingredients


def extract_ingredients_from_paragraphs(soup):
    """Scan <p> tags for ingredient-like lines (quantity + optional unit + name).

    Used as a fallback for blogs that write recipe ingredients as plain paragraphs
    rather than <li> elements or structured data (e.g. 56kilo.se, older Swedish blogs).
    Collects lines from any paragraph where at least 2 lines look like ingredients.
    """
    # Matches lines starting with a number/fraction optionally followed by a known unit
    INGREDIENT_RE = re.compile(
        r"^[\d.,\-–½¼¾⅓⅔⅛⅜⅝⅞/]+\s*"
        r"(?:dl|msk|tsk|g|gr|gram|kg|ml|l|liter|st|krm|cl|port|tbsp|tsp|cup|cups|oz|lb|pinch)?"
        r"\s*\S",
        re.IGNORECASE,
    )

    candidate_lines = []
    for p in soup.find_all("p"):
        lines = [ln.strip() for ln in p.get_text(separator="\n").split("\n") if ln.strip()]
        matched = [ln for ln in lines if INGREDIENT_RE.match(ln)]
        # Only treat this paragraph as an ingredient block if ≥2 lines look like ingredients
        if len(matched) >= 2:
            candidate_lines.extend(lines)

    return parse_ingredients(candidate_lines)


def extract_jsonld_recipe(data, url, source):
    return {
        "id": str(uuid.uuid4()),
        "source": source,
        "name": data.get("name", "").strip(),
        "url": url,
        "image": parse_image(data.get("image", "")),
        "time": parse_duration(data.get("totalTime", "")),
        "servings": str(data.get("recipeYield", "")),
        "ingredients": parse_ingredients(data.get("recipeIngredient", [])),
        "tags": normalize_tags(data.get("recipeCategory", [])),
        "description": data.get("description", "")
    }


def find_jsonld_recipe(soup):
    """Find and parse Recipe JSON-LD from a BeautifulSoup page.

    Handles three common shapes:
      - {"@type": "Recipe", ...}
      - [{"@type": "Recipe", ...}, ...]
      - {"@graph": [{"@type": "Recipe", ...}, ...]}   ← Yoast SEO / WordPress
    """
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(script.string or "")
            # Unwrap @graph (Yoast SEO, RankMath, many WordPress themes)
            if isinstance(data, dict) and "@graph" in data:
                data = next(
                    (d for d in data["@graph"] if d.get("@type") == "Recipe"), None
                )
            elif isinstance(data, list):
                data = next((d for d in data if d.get("@type") == "Recipe"), None)
            if data and data.get("@type") == "Recipe":
                return data
        except Exception:
            continue
    return None


def find_microdata_recipe(soup):
    """Extract recipe from HTML microdata (itemscope / itemtype).

    Used by sites that don't embed JSON-LD but annotate HTML directly, e.g.:
      <div itemscope itemtype="https://schema.org/Recipe">
    Returns a dict shaped like a JSON-LD Recipe object, or None.
    """
    recipe_el = soup.find(attrs={"itemtype": re.compile(r"schema\.org/Recipe", re.I)})
    if not recipe_el:
        return None

    def get_prop(name):
        el = recipe_el.find(attrs={"itemprop": name})
        if not el:
            return ""
        return el.get("content") or el.get_text(strip=True)

    def get_props(name):
        els = recipe_el.find_all(attrs={"itemprop": name})
        return [
            el.get("content") or el.get_text(strip=True)
            for el in els
            if el.get("content") or el.get_text(strip=True)
        ]

    name = get_prop("name")
    if not name:
        return None

    img_el = recipe_el.find(attrs={"itemprop": "image"})
    image = ""
    if img_el:
        image = img_el.get("src") or img_el.get("content") or ""

    return {
        "@type": "Recipe",
        "name": name,
        "image": image,
        "totalTime": get_prop("totalTime") or get_prop("cookTime"),
        "recipeYield": get_prop("recipeYield"),
        "recipeIngredient": get_props("recipeIngredient"),
        "description": get_prop("description"),
        "recipeCategory": get_props("recipeCategory"),
    }
