"""Validate and transform raw Spoonacular recipe data with Pydantic."""
import re
from typing import Any, Optional

from pydantic import BaseModel, Field, field_validator

from extraction import clean_html_text


class RecipeModel(BaseModel):
    spoonacular_id: Optional[int] = None
    title: str = Field(min_length=1, max_length=300)
    ready_in_minutes: Optional[int] = Field(default=None, ge=0)
    servings: Optional[int] = Field(default=None, ge=1)
    calories: Optional[float] = Field(default=None, ge=0)
    protein: Optional[float] = Field(default=None, ge=0)
    fat: Optional[float] = Field(default=None, ge=0)
    carbs: Optional[float] = Field(default=None, ge=0)
    cuisines: str = ""
    ingredients: str = ""
    instructions: str = ""
    image_url: str = ""

    @field_validator("calories", "protein", "fat", "carbs", mode="before")
    @classmethod
    def convert_nutrients(cls, value: Any) -> Optional[float]:
        if value is None or value == "":
            return None
        if isinstance(value, (int, float)):
            return float(value)
        match = re.search(r"-?\d+(?:\.\d+)?", str(value))
        return float(match.group()) if match else None


def recipe_to_model(data: dict[str, Any]) -> RecipeModel:
    """Map the nested API response into a validated, flat recipe record."""
    nutrient_values = {
        item.get("name"): item.get("amount")
        for item in data.get("nutrition", {}).get("nutrients", [])
        if item.get("name")
    }
    ingredient_names = [
        item.get("original") or item.get("name", "")
        for item in data.get("extendedIngredients", [])
    ]

    return RecipeModel(
        spoonacular_id=data.get("id"),
        title=data.get("title") or "Untitled recipe",
        ready_in_minutes=data.get("readyInMinutes"),
        servings=data.get("servings"),
        calories=nutrient_values.get("Calories"),
        protein=nutrient_values.get("Protein"),
        fat=nutrient_values.get("Fat"),
        carbs=nutrient_values.get("Carbohydrates"),
        cuisines=", ".join(data.get("cuisines") or []),
        ingredients="\n".join(name for name in ingredient_names if name),
        instructions=clean_html_text(data.get("instructions")),
        image_url=data.get("image") or "",
    )
