"""Exploratory data analysis using Pandas, Matplotlib, and Seaborn."""
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


NUTRITION_COLUMNS = ["calories", "protein", "fat", "carbs"]


def prepare_eda_data(data: pd.DataFrame) -> pd.DataFrame:
    cleaned = data.copy()
    for column in NUTRITION_COLUMNS + ["ready_in_minutes", "servings"]:
        if column in cleaned.columns:
            cleaned[column] = pd.to_numeric(cleaned[column], errors="coerce")
    return cleaned


def get_eda_summary(data: pd.DataFrame) -> pd.DataFrame:
    cleaned = prepare_eda_data(data)
    available_columns = [
        column for column in NUTRITION_COLUMNS + ["ready_in_minutes", "servings"]
        if column in cleaned.columns
    ]
    if not available_columns:
        return pd.DataFrame()
    return cleaned[available_columns].describe().round(2)


def create_calorie_chart(data: pd.DataFrame):
    cleaned = prepare_eda_data(data).dropna(subset=["calories"])
    if cleaned.empty:
        return None
    cleaned = cleaned.sort_values("calories", ascending=False).head(15)
    figure, axis = plt.subplots(figsize=(10, 5))
    sns.barplot(data=cleaned, x="calories", y="title", hue="title", legend=False,
                palette="flare", ax=axis)
    axis.set_title("Calories by Recipe", fontsize=15, weight="bold")
    axis.set_xlabel("Calories (kcal)")
    axis.set_ylabel("Recipe")
    figure.tight_layout()
    return figure


def create_calorie_distribution(data: pd.DataFrame):
    cleaned = prepare_eda_data(data).dropna(subset=["calories"])
    if cleaned.empty:
        return None
    figure, axis = plt.subplots(figsize=(8, 4))
    sns.histplot(data=cleaned, x="calories", bins=10, kde=True,
                 color="#7A2336", ax=axis)
    axis.set_title("Distribution of Recipe Calories", fontsize=14, weight="bold")
    axis.set_xlabel("Calories (kcal)")
    figure.tight_layout()
    return figure





def create_correlation_heatmap(data: pd.DataFrame):
    cleaned = prepare_eda_data(data)
    available = [column for column in NUTRITION_COLUMNS + ["ready_in_minutes"]
                 if column in cleaned.columns]
    numeric_data = cleaned[available].dropna(axis=1, how="all")
    if numeric_data.shape[1] < 2 or len(numeric_data) < 2:
        return None
    figure, axis = plt.subplots(figsize=(7, 5))
    sns.heatmap(numeric_data.corr(), annot=True, cmap="RdYlBu_r", fmt=".2f",
                linewidths=0.5, ax=axis)
    axis.set_title("Correlation Between Recipe Attributes", fontsize=14, weight="bold")
    figure.tight_layout()
    return figure


def create_nutrition_doughnut(data: pd.DataFrame):
    """Show the average protein, fat, and carbohydrate amounts as a doughnut chart."""
    cleaned = prepare_eda_data(data)
    nutrients = [column for column in ["protein", "fat", "carbs"] if column in cleaned.columns]
    if not nutrients:
        return None
    averages = cleaned[nutrients].mean().dropna()
    averages = averages[averages > 0]
    if len(averages) < 2:
        return None
    labels = {"protein": "Protein", "fat": "Fat", "carbs": "Carbohydrates"}
    figure, axis = plt.subplots(figsize=(7, 4.5))
    wedges, _ = axis.pie(
        averages.values,
        startangle=90,
        wedgeprops={"width": 0.42, "edgecolor": "#FBF7F0", "linewidth": 2},
        colors=["#70283B", "#C58B75", "#D8B995"][:len(averages)],
    )
    legend_labels = [f"{labels.get(name, name.title())}: {value:.1f} g" for name, value in averages.items()]
    axis.legend(wedges, legend_labels, title="Average per recipe", loc="center left", bbox_to_anchor=(0.92, 0.5), frameon=False)
    axis.set_title("Average Macronutrient Composition", fontsize=14, weight="bold", color="#4E1929")
    figure.tight_layout()
    return figure
