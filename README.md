# AI Business Analytics Assistant (Task 5 — Week 5)

An AI-powered analytics assistant that lets you upload CSV/Excel data and
automatically cleans it, generates charts, shows trends, predicts sales, and
produces AI-generated business insights. Upgrade features include natural
language queries, an interactive dashboard, and PDF report generation.

## Project Structure
```
ai_business_analytics_assistant/
├── app.py                     # Main Streamlit app (interactive dashboard)
├── requirements.txt           # All required libraries
├── .env.example                # API key template
├── .gitignore                  # Files/folders excluded from Git
├── README.md
└── modules/
    ├── __init__.py
    ├── data_loader.py          # CSV / Excel Upload
    ├── data_cleaning.py        # Data Cleaning
    ├── visualization.py        # Automated Charts
    ├── trend_analysis.py       # Trend Analysis
    ├── prediction.py           # Sales Prediction
    ├── ai_insights.py          # AI-Generated Insights + Natural Language Queries
    └── report_generator.py     # PDF Report Generation
```

## Features Mapped to Files
| Feature (from task list)           | File |
|---|---|
| CSV/Excel Upload                   | `modules/data_loader.py` |
| Data Cleaning                      | `modules/data_cleaning.py` |
| Automated Charts                   | `modules/visualization.py` |
| Trend Analysis                     | `modules/trend_analysis.py` |
| Sales Prediction                    | `modules/prediction.py` |
| AI-Generated Insights               | `modules/ai_insights.py` (`generate_insights`) |
| Natural Language Queries (Upgrade)  | `modules/ai_insights.py` (`answer_nl_query`) |
| Interactive Dashboard (Upgrade)     | `app.py` (Streamlit tabs) |
| PDF Report Generation (Upgrade)     | `modules/report_generator.py` |

## Installation

1. Make sure Python 3.10+ is installed.
2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   ```
3. Install all required libraries in one go:
   ```bash
   pip install -r requirements.txt
   ```
   This installs:
   - `streamlit` — web dashboard / UI
   - `pandas`, `numpy` — data handling
   - `openpyxl` — Excel file support
   - `plotly` — interactive charts
   - `scikit-learn` — sales prediction model (Linear/Polynomial Regression)
   - `statsmodels` — extra time-series utilities
   - `fpdf2` — PDF report generation
   - `anthropic` — Claude AI API (insights + natural language queries)
   - `python-dotenv` — load API key from a `.env` file
   - `kaleido` — export Plotly charts as images (used internally by some export paths)

4. Set your API key (required for AI Insights and Natural Language Queries):
   - Copy `.env.example` to `.env` and add your Anthropic API key, OR
   - Paste the API key directly into the sidebar after launching the app.

5. Run the app:
   ```bash
   streamlit run app.py
   ```
   The app will open in your browser at `http://localhost:8501`.

## Usage
1. Upload a CSV or Excel file from the sidebar.
2. View the raw data on the **Overview** tab.
3. The **Data Cleaning** tab automatically handles missing values, duplicates,
   and date columns, showing the cleaned data — you can also download it as CSV.
4. The **Auto Charts** tab automatically generates charts based on your
   column types.
5. The **Trend Analysis** tab lets you pick a date + numeric column to view
   the growth trend.
6. The **Sales Prediction** tab forecasts future periods using Polynomial
   Regression (scikit-learn).
7. The **AI Insights** tab generates plain-English business insights via the
   Claude API.
8. The **Ask a Question** tab lets you ask normal questions about your data
   in plain English — the AI writes the pandas code itself and returns the answer.
9. The **PDF Report** tab combines everything (stats + trend + forecast + AI
   insights) into a single downloadable PDF report.

## Notes
- Without an API key, only the **AI Insights** and **Ask a Question** features
  will be unavailable — everything else (upload, cleaning, charts, trend,
  prediction, PDF) still works fine.
- For deployment, you can use Streamlit Community Cloud, Render, or any
  Python-supporting host.
