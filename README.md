🍲 The Nourish Kitchen

Your Pocket Nutritionist

The Nourish Kitchen is a Smart Recipe and Calorie Analyzer developed using Python and Streamlit. It extracts recipe information from the Spoonacular API, validates and transforms the data, stores recipes in an SQLite database, and provides statistical analysis and interactive visualizations of nutritional information.

🌟 Project Overview

The main goal of this project is to provide users with an interactive platform to explore recipes and understand their nutritional values.

The application follows an ETL (Extract, Transform, Load) pipeline and performs Exploratory Data Analysis (EDA) on stored recipe data.

✨ Features

- Recipe Search: Search for recipes using the Spoonacular API.
- Nutritional Analysis: View calories, protein, fats, and carbohydrates.
- Recipe Details: Explore ingredients, cooking instructions, preparation time, and servings.
- Recipe Storage: Save and retrieve recipes using an SQLite database.
- Statistical Analysis: Generate descriptive statistics for nutritional data.
- Data Visualization: Explore nutritional information through interactive charts.
- Recipe Management: View and delete stored recipes.

🛠️ Technologies and Libraries

- Python – Core programming language
- Streamlit – Interactive web application
- Pandas – Data manipulation and analysis
- Pydantic – Data validation
- Requests – API communication
- SQLite3 – Database management
- Matplotlib – Data visualization
- Seaborn – Statistical visualization
- python-dotenv – Environment variable management

🔄 ETL Pipeline

The project follows three main ETL stages:

1. Extract

Recipe information is retrieved from the Spoonacular API using HTTP requests.

2. Transform

Extracted data is cleaned, transformed, and validated using Pandas and Pydantic.

3. Load

Validated recipe information is stored in an SQLite database for future retrieval and analysis.

📊 Exploratory Data Analysis (EDA)

The project performs statistical analysis and visualizes nutritional information using:

- Descriptive statistical summaries
- Nutritional composition doughnut chart
- Calories by recipe chart
- Calorie distribution chart
- Nutritional correlation heatmap


Application Screenshots

1. Recipe Search Page

"Recipe Search Page" (screenshots/01-recipe-search.png)

2. Recipe Search Results

"Recipe Search Results" (screenshots/02-recipe-results.png)

3. Statistical Analysis

"Statistical Analysis" (screenshots/03-statistical-analysis.png)

4. Macronutrient Distribution – Doughnut Chart

"Macronutrient Doughnut Chart" (screenshots/04-macronutrient-doughnut.png)

5. Calorie Distribution

"Calorie Distribution" (screenshots/05-calorie-distribution.png)

6. Calorie Distribution – Histogram with Distribution Curve

"Calorie Distribution Histogram" (screenshots/06-calorie-distribution-histogram.png)

7. Nutritional Correlation Heatmap

"Nutritional Correlation Heatmap" (screenshots/07-nutritional-correlation-heatmap.png)

📁 Project Structure
```text
The-Nourish-Kitchen/
│
├── app.py
├── extraction.py
├── validation.py
├── etl_pipeline.py
├── database.py
├── eda.py
│
├── requirements.txt
├── README.md
├── .gitignore
├── .env.example
│
└── recipes.db ```



⚙️ Installation and Setup

1. Clone the Repository

git clone https://github.com/EmanFatima69/The-Nourish-Kitchen.git

2. Navigate to the Project Directory

cd The-Nourish-Kitchen

3. Install Required Libraries

pip install -r requirements.txt

4. Configure the API Key

Create a ".env" file in the project directory and add your Spoonacular API key:

SPOONACULAR_API_KEY=your_api_key_here

You can obtain an API key from the "Spoonacular website" (https://spoonacular.com/food-api).



5. Run the Application

streamlit run app.py

The application will open in your web browser.

🗄️ Database

The project uses SQLite3 to store recipe information, including recipe names, preparation times, servings, nutritional values, ingredients, and instructions.

A sample database is included in the repository.

👩‍💻 Project Information

Project Name: The Nourish Kitchen – Smart Recipe & Calorie Analyzer

Project Type: Python Programming Course Project

Core Concepts: ETL Pipeline, Data Validation, SQLite Database, Exploratory Data Analysis, Data Visualization, API Integration.



Your Pocket Nutritionist – Making recipe exploration and nutritional analysis easier! 🍲



Spoonacular API – Free Tier Limitations

The Nourish Kitchen uses the Spoonacular Food API to retrieve recipe information.

API Plan: Free Tier

Daily Quota: 50 points per day.

Limitations:

- API usage is restricted by a daily points quota.
- Different API endpoints may consume different amounts of points.
- Recipe search requests generally consume 1 point plus 0.01 points per returned result.
- Once the daily quota is exhausted, further requests may return HTTP 402.
- The daily quota resets at midnight UTC.

API Configuration:
A valid Spoonacular API key is required. Users must provide their own API key through environment variables.

Note: API availability depends on the remaining daily quota and Spoonacular's service availability.