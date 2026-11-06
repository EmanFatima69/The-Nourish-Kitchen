"""Extract recipe data from the Spoonacular API."""
import re
import time
from typing import Any, Optional

import requests


def clean_html_text(raw_text: Optional[str]) -> str:
    """Remove HTML tags and normalize whitespace in recipe instructions."""
    if not raw_text:
        return ""
    text = re.sub(r"<[^>]*>", " ", str(raw_text))
    return re.sub(r"\s+", " ", text).strip()


def fetch_spoonacular_recipe(dish_name: str, api_key: str, retries: int = 3) -> Optional[dict[str, Any]]:
    """Search for a recipe and fetch its detailed information and nutrition."""
    if not dish_name or not dish_name.strip():
        raise ValueError("Please enter a recipe name.")
    if not api_key:
        raise ValueError("SPOONACULAR_API_KEY is missing. Add it to your .env file.")

    search_url = "https://api.spoonacular.com/recipes/complexSearch"
    search_params = {"query": dish_name.strip(), "apiKey": api_key, "number": 1}

    for attempt in range(retries):
        try:
            response = requests.get(search_url, params=search_params, timeout=20)
            if response.status_code in (401, 402):
                raise ValueError("API key is invalid or the Spoonacular request quota has been reached.")
            response.raise_for_status()
            results = response.json().get("results", [])
            if not results:
                return None

            recipe_id = results[0].get("id")
            if not recipe_id:
                return None

            details_url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"
            details_params = {"includeNutrition": "true", "apiKey": api_key}
            details_response = requests.get(details_url, params=details_params, timeout=20)
            if details_response.status_code in (401, 402):
                raise ValueError("API key is invalid or the Spoonacular request quota has been reached.")
            details_response.raise_for_status()
            return details_response.json()

        except ValueError:
            raise
        except requests.exceptions.RequestException:
            if attempt == retries - 1:
                raise
            time.sleep(attempt + 1)
    return None
