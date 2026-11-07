"""The Nourish Kitchen: Streamlit interface for the course-scope ETL + EDA project."""
import os

import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from EDA import (
    create_calorie_chart,
    create_calorie_distribution,
    create_correlation_heatmap,
    create_nutrition_doughnut,
    get_eda_summary,
)
from database import delete_recipe, initialize_database, load_recipes
from etl_pipeline import run_etl


# Load API key from local .env or Streamlit Cloud Secrets
load_dotenv()

API_KEY = os.getenv("SPOONACULAR_API_KEY")

if not API_KEY:
    try:
        API_KEY = st.secrets["SPOONACULAR_API_KEY"]
    except Exception:
        API_KEY = None

st.set_page_config(page_title="The Nourish Kitchen", page_icon="🍲", layout="centered")


st.markdown(r"""
<style>
:root {
    --maroon: #70283B;
    --maroon-dark: #4E1929;
    --beige: #F3E8D8;
    --cream: #FBF7F0;
    --sand: #D8B995;
    --ink: #3D2B28;
}
.stApp {
    background: radial-gradient(circle at 12% 10%, #fffaf2 0, transparent 30%),
                linear-gradient(135deg, #F3E8D8 0%, #EAD9C4 100%);
    color: var(--ink);
}
.block-container { max-width: 1080px; padding: 1.5rem 2rem 3rem; }
[data-testid="stHeader"] { background: transparent; }
[data-testid="stSidebar"] { background: #6B2639; border-right: 1px solid #D8B995; }
[data-testid="stSidebar"] * { color: #FFF8EE !important; }
/* Kitchen Hub navigation panel */
[data-testid="stSidebar"] [data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(255, 248, 238, 0.10);
    border: 1px solid rgba(255, 248, 238, 0.25);
    border-radius: 20px;
    padding: 14px 10px;
    box-shadow: 0 8px 22px rgba(30, 8, 15, 0.18);
}

/* Space between navigation items */
[data-testid="stSidebar"] [role="radiogroup"] {
    gap: 10px;
}

/* Normal navigation item */
[data-testid="stSidebar"] [role="radio"] {
    background: rgba(255, 248, 238, 0.08);
    border: 1px solid rgba(255, 248, 238, 0.18);
    border-radius: 13px;
    padding: 13px 12px;

    transform: scale(1);
    transform-origin: center;

    transition:
        background-color 0.35s ease,
        color 0.35s ease,
        transform 0.35s cubic-bezier(0.2, 0.8, 0.2, 1),
        box-shadow 0.35s ease,
        border-color 0.35s ease;

    cursor: pointer;
}

/* Smooth hover effect */
[data-testid="stSidebar"] [role="radio"]:hover {
    background-color: #A45D6A !important;
    border-color: #E8CBAA;
    transform: translateX(5px) scale(1.045);
    box-shadow: 0 6px 16px rgba(30, 8, 15, 0.25);
}

/* Selected navigation item */
[data-testid="stSidebar"] [role="radio"]:has(input:checked) {
    background-color: #F0DDC5 !important;
    border-color: #D8B995;
    transform: translateX(4px) scale(1.02);
    box-shadow: 0 4px 12px rgba(30, 8, 15, 0.15);
}

[data-testid="stSidebar"] [role="radio"]:has(input:checked) * {
    color: #572033 !important;
}
/* Navigation menu - smooth hover animation */

[data-testid="stSidebar"] [role="radio"] {
    background: rgba(255,248,238,0.08);
    border: 1px solid rgba(255,248,238,0.16);
    border-radius: 12px;
    padding: 12px 14px;

    transform: scale(1);
    transform-origin: left center;

    transition:
        background-color 0.35s ease,
        color 0.35s ease,
        transform 0.35s cubic-bezier(0.2, 0.8, 0.2, 1),
        box-shadow 0.35s ease,
        border-color 0.35s ease;

    cursor: pointer;
}

/* When cursor moves over a menu item */
[data-testid="stSidebar"] [role="radio"]:hover {
    background-color: #A45D6A !important;
    border-color: #D8B995;

    transform: translateX(6px) scale(1.06);

    box-shadow: 0 6px 16px rgba(30,8,15,0.25);
}

/* Selected menu item */
[data-testid="stSidebar"] [role="radio"]:has(input:checked) {
    background-color: #F0DDC5;
    color: #572033 !important;

    transform: translateX(4px) scale(1.02);
    border-color: #D8B995;
}

/* Selected menu text */
[data-testid="stSidebar"] [role="radio"]:has(input:checked) * {
    color: #572033 !important;
}
[data-testid="stSidebar"] [role="radio"]:has(input:checked) {
    background: #F0DDC5; color: #572033 !important; transform: translateX(4px);
}
[data-testid="stSidebar"] [role="radio"]:has(input:checked) * { color: #572033 !important; }
.hero {
    position: relative; overflow: hidden; text-align: center; padding: 2rem 1.2rem 1.7rem;
    margin: .2rem 0 1.6rem; border-radius: 24px;
    background: linear-gradient(125deg, #5B1E31, #82394B 62%, #A66A68);
    box-shadow: 0 14px 35px rgba(75,25,40,.20); color: #FFF5E8;
}
.hero h1 { color: #FFF5E8 !important; font-family: Georgia, 'Palatino Linotype', serif;
    font-size: clamp(2rem, 5vw, 3.25rem); letter-spacing: .02em; margin: 0; }
.hero .tagline { color: #F2D9B9; font-family: 'Trebuchet MS', sans-serif;
    font-size: 1.18rem; font-style: italic; letter-spacing: .09em; margin-top: .5rem; }
.hero .subline { color: #F9EBDD; font-size: .78rem; letter-spacing: .18em; margin-top: .7rem; }
.float-item { position: absolute; opacity: .20; font-size: 2.1rem; pointer-events: none;
    animation: drift 7s ease-in-out infinite alternate; }
.float-one { left: 5%; top: 17%; }
.float-two { right: 8%; top: 12%; animation-delay: -2s; }
.float-three { left: 15%; bottom: 8%; animation-delay: -4s; }
.float-four { right: 17%; bottom: 7%; animation-delay: -1s; }
@keyframes drift { from { transform: translate(0, 0) rotate(-8deg); }
    to { transform: translate(15px, -17px) rotate(9deg); } }
h1, h2, h3, h4 { color: var(--maroon-dark); }
.section-heading { color: var(--maroon); font-family: Georgia, serif; font-size: 1.55rem;
    font-weight: 700; margin: .5rem 0 1rem; }
div[data-testid="stMetric"] { background: var(--cream); border: 1px solid #E4D2BC;
    border-left: 4px solid var(--maroon); padding: 14px; border-radius: 13px;
    box-shadow: 0 5px 14px rgba(77,39,35,.06); }
.stButton > button, .stFormSubmitButton > button, .stDownloadButton > button {
    background: var(--maroon); color: #FFF8EF; border: 1px solid var(--maroon);
    border-radius: 11px; padding: .55rem 1rem; transition: all .25s ease; }
.stButton > button:hover, .stFormSubmitButton > button:hover, .stDownloadButton > button:hover {
    background: #9A5360; color: white; transform: translateY(-2px) scale(1.025);
    box-shadow: 0 7px 16px rgba(80,25,43,.18); border-color: #9A5360; }
.stTextInput input, .stSelectbox div[data-baseweb="select"] > div,
.stNumberInput input { background: #FFFDF9; border-radius: 10px; }
[data-testid="stDataFrame"] { border: 1px solid #E4D2BC; border-radius: 12px; }
hr { border-color: #D9C3A9; }
footer { visibility: hidden; }
@media (prefers-reduced-motion: reduce) { *, *::before, *::after { animation: none !important; transition: none !important; } }
/* Custom maroon table styling */
.nourish-table {
    width: 100%;
    border-collapse: collapse;
    background-color: #FBF7F0;
    border-radius: 12px;
    overflow: hidden;
    font-family: Arial, sans-serif;
    margin-bottom: 15px;
}

.nourish-table thead th {
    background-color: #70283B !important;
    color: #FFFFFF !important;
    font-weight: bold;
    text-align: center;
    padding: 13px 10px;
    border: 1px solid #70283B;
}

.nourish-table tbody td,
.nourish-table tbody th {
    color: #3D2B28;
    padding: 11px 10px;
    text-align: center;
    border: 1px solid #E4D2BC;
}

.nourish-table tbody tr:nth-child(even) {
    background-color: #F3E8D8;
}

.nourish-table tbody tr:hover {
    background-color: #EAD9C4;
    transition: background-color 0.25s ease;
}
</style>
<div class="hero">
  <span class="float-item float-one">👩‍🍳</span><span class="float-item float-two">🍳</span>
  <span class="float-item float-three">🥕</span><span class="float-item float-four">🍲</span>
  <h1>The Nourish Kitchen</h1>
  <div class="tagline">Your Pocket Nutritionist</div>
  <div class="subline">DISCOVER&nbsp; · &nbsp;ANALYZE&nbsp; · &nbsp;NOURISH</div>
</div>
""", unsafe_allow_html=True)

initialize_database()

with st.sidebar:

    with st.container(border=True):

        st.markdown(
            """
            <div style="text-align:center; padding: 8px 0 18px;">
                <div style="font-size:35px;">🍲</div>
                <h2 style="
                    font-family:Georgia,serif;
                    color:#FFF0DC;
                    margin:5px 0;
                    font-size:25px;">
                    Kitchen Hub
                </h2>
                <p style="
                    color:#E8CBAA;
                    font-size:12px;
                    letter-spacing:1px;
                    margin:0;">
                    YOUR FOOD JOURNEY
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        page = st.radio(
            "Explore",
            [
                "🔎  Recipe Search",
                "📚  Stored Recipes",
                "📊  Statistical Analysis",
                "🍩  Visual Charts"
            ],
            label_visibility="collapsed",
        )

    st.markdown("<br>", unsafe_allow_html=True)

    st.caption("✨  Fresh insights from your saved recipes")


def section_title(title: str, subtitle: str = "") -> None:
    st.markdown(f"<div class='section-heading'>{title}</div>", unsafe_allow_html=True)
    if subtitle:
        st.caption(subtitle)

def style_table(dataframe, hide_index=False):
    return dataframe.to_html(
        index=not hide_index,
        classes="nourish-table",
        border=0,
        escape=True
    )


if page == "🔎  Recipe Search":
    section_title(
        "Find something delicious",
        "Search a dish to collect its recipe and nutrition details."
    )

    with st.form("recipe_search_form"):

        user_api_key = st.text_input(
            "🔑 Enter Your Own Spoonacular API Key (Optional):",
            type="password",
            help="Sign up for a Spoonacular account to get your API key:" \
            "https://spoonacular.com/food-api/console/#Dashboard"
        )

        st.markdown(
            "Don't have an API Key? [Get one from " \
            "Spoonacular](https://spoonacular.com/food-api/console#Dashboard)"
        )

        if user_api_key.strip():
            active_api_key = user_api_key.strip()
        else:
            active_api_key = API_KEY

        dish_name = st.text_input(
            "What would you like to cook?",
            placeholder="e.g. chicken biryani"
        )

        submitted = st.form_submit_button("Find and save recipe")

    if submitted:
        if not dish_name.strip():
            st.error("Please enter a recipe name to get started.")

        elif not active_api_key:
            st.error("Your API key is missing. Please enter your own API key.")

        else:
            with st.spinner("Finding your recipe..."):
                try:
                    result = run_etl(dish_name, active_api_key)

                    if result["status"] == "not_found":
                        st.info(
                            "We couldn't find a matching recipe. Try another dish name."
                        )

                    else:
                        recipe = result["recipe"]

                        st.success("Your recipe is ready and saved!")
                        st.metric(
                            "ETL Execution Time",
                            f"{result['elapsed_seconds']} seconds"
                        )

                        left, right = st.columns([1, 2])

                        with left:
                            if recipe.image_url:
                                st.image(recipe.image_url, width="stretch")

                        with right:
                            st.subheader(recipe.title)

                            x, y, z = st.columns(3)

                            x.metric(
                                "Calories",
                                recipe.calories if recipe.calories is not None else "—"
                            )

                            y.metric(
                                "Ready in",
                                f"{recipe.ready_in_minutes} min"
                                if recipe.ready_in_minutes is not None else "—"
                            )

                            z.metric(
                                "Servings",
                                recipe.servings
                                if recipe.servings is not None else "—"
                            )

                            st.write(
                                f"**Protein:** {recipe.protein if recipe.protein is not None else '—'} g"
                            )
                            st.write(
                                f"**Fat:** {recipe.fat if recipe.fat is not None else '—'} g"
                            )
                            st.write(
                                f"**Carbohydrates:** {recipe.carbs if recipe.carbs is not None else '—'} g"
                            )

                        with st.expander("Ingredients"):
                            st.write(
                                recipe.ingredients or "Ingredient details are not available."
                            )

                        with st.expander("Cooking instructions"):
                            st.write(
                                recipe.instructions or "Instructions are not available."
                            )

                except Exception as error:
                    st.error(f"We couldn't process that recipe: {error}")

elif page == "📚  Stored Recipes":
    section_title("Your recipe collection", "Browse, search, download, or remove saved recipes.")
    data = load_recipes()
    if data.empty:
        st.info("Your collection is empty for now. Search for a recipe to add the first one.")
    else:
        c1, c2, c3 = st.columns(3)
        c1.metric("Recipes saved", len(data))
        c2.metric("Average calories", f"{data['calories'].mean():.1f}" if data["calories"].notna().any() else "—")
        c3.metric("Average prep time", f"{data['ready_in_minutes'].mean():.1f} min" if data["ready_in_minutes"].notna().any() else "—")
        search_text = st.text_input("Search by recipe name", placeholder="Start typing a recipe name...")
        filtered = data[data["title"].str.contains(search_text, case=False, na=False)] if search_text else data
      
        recipe_table = filtered[
            [
                "id", "title", "ready_in_minutes", "servings",
                "calories", "protein", "fat", "carbs", "cuisines"
            ]
        ]

        st.markdown(
            style_table(recipe_table, hide_index=True),
            unsafe_allow_html=True
        )
        st.download_button("Download recipes as CSV", data=filtered.to_csv(index=False).encode("utf-8"), file_name="my_recipes.csv", mime="text/csv")
        st.divider()
        options = {f"{row['title']} (#{row['id']})": int(row["id"]) for _, row in data.iterrows()}
        selected = st.selectbox("Choose a recipe to remove", list(options.keys()))
        if st.button("Remove selected recipe"):
            delete_recipe(options[selected])
            st.success("Recipe removed from your collection.")
            st.rerun()

elif page == "📊  Statistical Analysis":
    section_title("A closer look at nutrition")
    data = load_recipes()
    if data.empty:
        st.info("Save a few recipes to unlock your nutrition insights.")
    else:
        summary = get_eda_summary(data)
        st.markdown(
            style_table(summary),
            unsafe_allow_html=True
        )
        st.markdown("#### Collection snapshot")
        a, b, c, d = st.columns(4)
        a.metric("Recipes", len(data))
        b.metric("Average calories", f"{data['calories'].mean():.1f}" if data["calories"].notna().any() else "—")
        c.metric("Average protein", f"{data['protein'].mean():.1f} g" if data["protein"].notna().any() else "—")
        d.metric("Average carbs", f"{data['carbs'].mean():.1f} g" if data["carbs"].notna().any() else "—")
        
else:
    section_title("Food facts, made visual", "Choose a calorie range to explore your saved recipes.")
    data = load_recipes()
    if data.empty:
        st.info("Your charts will appear here once you save some recipes.")
    else:
        min_cal = int(data["calories"].min()) if data["calories"].notna().any() else 0
        max_cal = int(data["calories"].max()) if data["calories"].notna().any() else 0
        if max_cal > min_cal:
            selected_range = st.slider("Calorie range", min_cal, max_cal, (min_cal, max_cal))
            data = data[data["calories"].between(*selected_range)]
        if data.empty:
            st.warning("No saved recipes fall within that calorie range.")
        else:
            chart_items = [
                ("Nutrition mix", create_nutrition_doughnut(data)),
                ("Calories by recipe", create_calorie_chart(data)),
                ("Calorie distribution", create_calorie_distribution(data)),
                ("Nutrition correlations", create_correlation_heatmap(data)),
            ]
            for index in range(0, len(chart_items), 2):
                columns = st.columns(2)
                for column, (title, figure) in zip(columns, chart_items[index:index + 2]):
                    with column:
                        st.markdown(f"#### {title}")
                        if figure is not None:
                            st.pyplot(figure, width="stretch")
                            import matplotlib.pyplot as plt
                            plt.close(figure)
                        else:
                            st.caption("More recipe data is needed for this chart.")
            st.caption("Charts update automatically based on saved recipes and selected calorie range.")
