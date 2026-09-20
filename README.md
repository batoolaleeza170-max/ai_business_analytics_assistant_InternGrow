# AI Business Analytics Assistant (Task 5 — Week 5)

Ek AI-powered analytics assistant jo CSV/Excel data upload karke automatically
data clean karta hai, charts banata hai, trends dikhata hai, sales predict karta
hai, aur AI se business insights generate karta hai. Upgrade features me natural
language queries, interactive dashboard, aur PDF report generation shamil hain.

## Project Structure
```
ai_business_analytics_assistant/
├── app.py                     # Main Streamlit app (interactive dashboard)
├── requirements.txt           # All required libraries
├── .env.example                # API key template
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
| Feature (from task list)     | File |
|---|---|
| CSV/Excel Upload             | `modules/data_loader.py` |
| Data Cleaning                | `modules/data_cleaning.py` |
| Automated Charts             | `modules/visualization.py` |
| Trend Analysis               | `modules/trend_analysis.py` |
| Sales Prediction              | `modules/prediction.py` |
| AI-Generated Insights         | `modules/ai_insights.py` (`generate_insights`) |
| Natural Language Queries (Upgrade) | `modules/ai_insights.py` (`answer_nl_query`) |
| Interactive Dashboard (Upgrade)    | `app.py` (Streamlit tabs) |
| PDF Report Generation (Upgrade)    | `modules/report_generator.py` |

## Installation (sab libraries yahan install hongi)

1. Python 3.10+ install hona chahiye.
2. Virtual environment banayein (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   ```
3. Saari required libraries ek sath install karein:
   ```bash
   pip install -r requirements.txt
   ```
   Ye libraries install hongi:
   - `streamlit` — web dashboard / UI
   - `pandas`, `numpy` — data handling
   - `openpyxl` — Excel file support
   - `plotly` — interactive charts
   - `scikit-learn` — sales prediction model (Linear/Polynomial Regression)
   - `statsmodels` — extra time-series utilities
   - `fpdf2` — PDF report generation
   - `anthropic` — Claude AI API (insights + natural language queries)
   - `python-dotenv` — load API key from `.env` file
   - `kaleido` — export Plotly charts as images (used internally by some export paths)

4. API key set karein (AI Insights aur NL Queries ke liye zaroori hai):
   - `.env.example` ko `.env` me copy karein aur apni Anthropic API key dalein, YA
   - App chalane ke baad sidebar me directly API key paste kar dein.

5. App run karein:
   ```bash
   streamlit run app.py
   ```
   Browser me `http://localhost:8501` par app khul jayega.

## Usage
1. Sidebar se CSV/Excel file upload karein.
2. "Overview" tab me raw data dekhein.
3. "Data Cleaning" tab automatically missing values, duplicates, aur date columns
   handle karke cleaned data dikhata hai — CSV download bhi kar sakte hain.
4. "Auto Charts" tab data ke column types ke hisaab se khud charts bana deta hai.
5. "Trend Analysis" tab me date + numeric column select karke growth trend dekhein.
6. "Sales Prediction" tab future periods ke liye forecast deta hai (Polynomial
   Regression, scikit-learn se).
7. "AI Insights" tab Claude API se plain-English business insights generate
   karta hai.
8. "Ask a Question" tab me apni data ke baare me normal English/Urdu me sawal
   puchein — AI pandas code khud likh kar answer nikalta hai.
9. "PDF Report" tab sab kuch (stats + trend + forecast + AI insights) ek PDF
   report me combine karke download karne deta hai.

## Notes
- Agar API key nahi di, to sirf "AI Insights" aur "Ask a Question" features
  kaam nahi karenge — baki sab (upload, cleaning, charts, trend, prediction,
  PDF) bina API key ke bhi chalte hain.
- Deployment ke liye Streamlit Community Cloud, Render, ya koi bhi Python-
  supporting host use kar sakte hain.
