import streamlit as st
import pandas as pd

from modules.data_loader import load_data, get_basic_info
from modules.data_cleaning import clean_data
from modules.visualization import auto_generate_charts, get_numeric_columns, get_date_columns, get_categorical_columns
from modules.trend_analysis import analyze_trend
from modules.prediction import predict_sales
from modules.ai_insights import generate_insights, answer_nl_query
from modules.report_generator import build_pdf_report

st.set_page_config(page_title="AI Business Analytics Assistant", layout="wide", page_icon="📊")

# ---------- Sidebar ----------
st.sidebar.title("📊 AI Business Analytics Assistant")
st.sidebar.markdown("Upload your business data and let AI find the insights.")

api_key_input = st.sidebar.text_input("Anthropic API Key (for AI features)", type="password")
if api_key_input:
    st.session_state["api_key"] = api_key_input

uploaded_file = st.sidebar.file_uploader("Upload CSV / Excel file", type=["csv", "xlsx", "xls"])

fill_strategy = st.sidebar.selectbox(
    "Missing value strategy", ["auto", "drop", "zero"],
    help="auto = mean/mode fill, drop = remove incomplete rows, zero = fill numerics with 0"
)

st.title("AI-Powered Business Analytics Assistant")

if uploaded_file is None:
    st.info("👈 Upload a CSV or Excel file from the sidebar to get started.")
    st.stop()

# ---------- Load & Clean ----------
raw_df = load_data(uploaded_file)
if raw_df is None:
    st.stop()

with st.spinner("Cleaning data..."):
    clean_df, clean_report = clean_data(raw_df, fill_strategy=fill_strategy)

tabs = st.tabs([
    "📁 Overview", "🧹 Data Cleaning", "📈 Auto Charts", "📉 Trend Analysis",
    "🔮 Sales Prediction", "🤖 AI Insights", "💬 Ask a Question", "📄 PDF Report",
])

# ---------- Tab 1: Overview ----------
with tabs[0]:
    st.subheader("Dataset Overview")
    info = get_basic_info(raw_df)
    c1, c2, c3 = st.columns(3)
    c1.metric("Rows", info["rows"])
    c2.metric("Columns", info["columns"])
    c3.metric("Missing values", sum(info["missing_values"].values()))
    st.dataframe(raw_df.head(20), use_container_width=True)

# ---------- Tab 2: Data Cleaning ----------
with tabs[1]:
    st.subheader("Data Cleaning Report")
    st.json(clean_report, expanded=False)
    st.write("Cleaned data preview:")
    st.dataframe(clean_df.head(20), use_container_width=True)
    st.download_button(
        "Download Cleaned CSV", clean_df.to_csv(index=False).encode("utf-8"),
        file_name="cleaned_data.csv", mime="text/csv"
    )

# ---------- Tab 3: Automated Charts ----------
with tabs[2]:
    st.subheader("Automated Charts")
    charts = auto_generate_charts(clean_df)
    if not charts:
        st.warning("Could not auto-detect chartable columns.")
    for title, fig in charts:
        st.plotly_chart(fig, use_container_width=True)

# ---------- Tab 4: Trend Analysis ----------
with tabs[3]:
    st.subheader("Trend Analysis")
    date_cols = get_date_columns(clean_df)
    numeric_cols = get_numeric_columns(clean_df)
    if not date_cols or not numeric_cols:
        st.warning("Trend analysis needs at least one date column and one numeric column.")
    else:
        col1, col2, col3 = st.columns(3)
        date_col = col1.selectbox("Date column", date_cols, key="trend_date")
        value_col = col2.selectbox("Value column", numeric_cols, key="trend_value")
        freq = col3.selectbox("Frequency", ["D", "W", "M"], index=2, key="trend_freq")

        trend = analyze_trend(clean_df, date_col, value_col, freq)
        st.plotly_chart(trend["figure"], use_container_width=True)
        st.metric("Overall change", f"{trend['overall_change_pct']}%", trend["direction"])
        st.session_state["trend_summary"] = (
            f"{value_col} shows a {trend['direction']} trend with an overall change of "
            f"{trend['overall_change_pct']}% over the analyzed period."
        )

# ---------- Tab 5: Sales Prediction ----------
with tabs[4]:
    st.subheader("Sales / Metric Prediction")
    date_cols = get_date_columns(clean_df)
    numeric_cols = get_numeric_columns(clean_df)
    if not date_cols or not numeric_cols:
        st.warning("Prediction needs at least one date column and one numeric column.")
    else:
        col1, col2, col3, col4 = st.columns(4)
        date_col = col1.selectbox("Date column", date_cols, key="pred_date")
        value_col = col2.selectbox("Value to predict", numeric_cols, key="pred_value")
        freq = col3.selectbox("Frequency", ["D", "W", "M"], index=2, key="pred_freq")
        periods = col4.number_input("Periods ahead", min_value=1, max_value=36, value=6)

        result = predict_sales(clean_df, date_col, value_col, periods_ahead=periods, freq=freq)
        if "error" in result:
            st.warning(result["error"])
        else:
            st.plotly_chart(result["figure"], use_container_width=True)
            c1, c2 = st.columns(2)
            c1.metric("Model R² score", result["r2_score"])
            c2.metric("Mean Absolute Error", result["mae"])
            forecast_df = pd.DataFrame({
                "period": result["forecast_dates"], "forecast": result["forecast_values"]
            })
            st.dataframe(forecast_df, use_container_width=True)
            st.session_state["forecast_summary"] = (
                f"Forecast for {value_col} over the next {periods} periods "
                f"(model R²={result['r2_score']}, MAE={result['mae']}): "
                + ", ".join(f"{d.date()}: {v:.2f}" for d, v in zip(result["forecast_dates"], result["forecast_values"]))
            )

# ---------- Tab 6: AI Insights ----------
with tabs[5]:
    st.subheader("AI-Generated Business Insights")
    context = st.text_input("Business context (optional)", placeholder="e.g. Monthly retail sales across 5 regions")
    if st.button("Generate Insights"):
        with st.spinner("Asking Claude for insights..."):
            insights = generate_insights(clean_df, business_context=context)
            st.session_state["insights_text"] = insights
    if "insights_text" in st.session_state:
        st.markdown(st.session_state["insights_text"])

# ---------- Tab 7: Natural Language Queries ----------
with tabs[6]:
    st.subheader("Ask a Question About Your Data")
    question = st.text_input("e.g. 'What was the total sales in March?' or 'Which region had the highest profit?'")
    if st.button("Ask"):
        with st.spinner("Thinking..."):
            answer, result, code = answer_nl_query(clean_df, question)
        st.write(answer)
        with st.expander("Show generated pandas code"):
            st.code(code or "N/A", language="python")

# ---------- Tab 8: PDF Report ----------
with tabs[7]:
    st.subheader("Generate PDF Report")
    st.write("Combines dataset stats, trend analysis, forecast, and AI insights into one PDF.")
    if st.button("Build PDF Report"):
        pdf_bytes = build_pdf_report(
            clean_df,
            insights_text=st.session_state.get("insights_text", ""),
            trend_summary=st.session_state.get("trend_summary", ""),
            forecast_summary=st.session_state.get("forecast_summary", ""),
        )
        st.download_button(
            "⬇️ Download PDF Report", data=pdf_bytes,
            file_name="business_analytics_report.pdf", mime="application/pdf"
        )
