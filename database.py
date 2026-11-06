"""SQLite database operations for recipe records."""
import sqlite3
from typing import Optional

import pandas as pd

from validation import RecipeModel

DATABASE_NAME = "recipes.db"


def get_connection(database_name: str = DATABASE_NAME) -> sqlite3.Connection:
    connection = sqlite3.connect(database_name)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database(database_name: str = DATABASE_NAME) -> None:
    query = """
    CREATE TABLE IF NOT EXISTS recipes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        spoonacular_id INTEGER UNIQUE,
        title TEXT NOT NULL,
        ready_in_minutes INTEGER,
        servings INTEGER,
        calories REAL,
        protein REAL,
        fat REAL,
        carbs REAL,
        cuisines TEXT,
        ingredients TEXT,
        instructions TEXT,
        image_url TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """
    with get_connection(database_name) as connection:
        connection.execute(query)


def save_recipe(recipe: RecipeModel, database_name: str = DATABASE_NAME) -> tuple[int, bool]:
    """Insert a new recipe; update it if the Spoonacular ID already exists."""
    values = recipe.model_dump()
    columns = ", ".join(values.keys())
    placeholders = ", ".join(["?"] * len(values))
    update_fields = ", ".join(
        f"{column}=excluded.{column}"
        for column in values.keys()
        if column != "spoonacular_id"
    )
    query = f"""
    INSERT INTO recipes ({columns}) VALUES ({placeholders})
    ON CONFLICT(spoonacular_id) DO UPDATE SET {update_fields}
    """
    with get_connection(database_name) as connection:
        existing = None
        if recipe.spoonacular_id is not None:
            existing = connection.execute(
                "SELECT id FROM recipes WHERE spoonacular_id = ?",
                (recipe.spoonacular_id,),
            ).fetchone()
        cursor = connection.execute(query, tuple(values.values()))
        if existing:
            return int(existing["id"]), False
        return int(cursor.lastrowid), True


def load_recipes(database_name: str = DATABASE_NAME) -> pd.DataFrame:
    with get_connection(database_name) as connection:
        return pd.read_sql_query(
            "SELECT * FROM recipes ORDER BY created_at DESC", connection
        )


def delete_recipe(recipe_id: int, database_name: str = DATABASE_NAME) -> None:
    with get_connection(database_name) as connection:
        connection.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
