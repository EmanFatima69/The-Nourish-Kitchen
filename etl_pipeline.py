"""Run the complete Extract-Transform-Validate-Load process."""
import os
import time
from typing import Any

from dotenv import load_dotenv

from database import initialize_database, save_recipe
from extraction import fetch_spoonacular_recipe
from validation import recipe_to_model


def run_etl(dish_name: str) -> dict[str, Any]:
    load_dotenv()
    api_key = os.getenv("SPOONACULAR_API_KEY")
    if not api_key:
        raise ValueError("SPOONACULAR_API_KEY is missing from your .env file.")

    start_time = time.time()
    initialize_database()
    raw_data = fetch_spoonacular_recipe(dish_name, api_key)
    if raw_data is None:
        return {"status": "not_found", "message": "No matching recipe was found."}

    recipe = recipe_to_model(raw_data)
    database_id, inserted = save_recipe(recipe)
    elapsed_time = round(time.time() - start_time, 2)

    return {
        "status": "success",
        "recipe": recipe,
        "database_id": database_id,
        "inserted": inserted,
        "elapsed_seconds": elapsed_time,
    }
