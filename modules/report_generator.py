"""
report_generator.py
Upgrade Feature: PDF Report Generation
Builds a downloadable PDF summarizing dataset stats, trend/prediction
results, and AI-generated insights.
"""
import io
from datetime import datetime
import pandas as pd
from fpdf import FPDF


class ReportPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(30, 30, 90)
        self.cell(0, 12, "AI Business Analytics Report", ln=True, align="C")
        self.set_font("Helvetica", "", 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 8, datetime.now().strftime("Generated on %Y-%m-%d %H:%M"), ln=True, align="C")
        self.ln(4)

    def section_title(self, title):
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(20, 20, 20)
        self.cell(0, 10, title, ln=True)
        self.set_draw_color(180, 180, 180)
        self.line(self.get_x(), self.get_y(), self.get_x() + 190, self.get_y())
        self.ln(3)

    def body_text(self, text):
        self.set_font("Helvetica", "", 11)
        self.set_text_color(40, 40, 40)
        self.multi_cell(0, 6, text)
        self.ln(2)


def build_pdf_report(df: pd.DataFrame, insights_text: str = "",
                      trend_summary: str = "", forecast_summary: str = "") -> bytes:
    """
    Assemble a PDF report from dataset stats + optional AI insight text.
    Returns raw PDF bytes suitable for st.download_button.
    """
    pdf = ReportPDF()
    pdf.add_page()

    # Dataset overview
    pdf.section_title("1. Dataset Overview")
    pdf.body_text(
        f"Rows: {df.shape[0]}   |   Columns: {df.shape[1]}\n"
        f"Columns: {', '.join(map(str, df.columns))}"
    )

    # Numeric summary table
    numeric_df = df.select_dtypes(include="number")
    if not numeric_df.empty:
        pdf.section_title("2. Key Statistics")
        desc = numeric_df.describe().round(2)
        pdf.set_font("Courier", "", 8)
        pdf.multi_cell(0, 4.5, desc.to_string())
        pdf.ln(2)

    # Trend section
    if trend_summary:
        pdf.section_title("3. Trend Analysis")
        pdf.body_text(trend_summary)

    # Forecast section
    if forecast_summary:
        pdf.section_title("4. Sales Prediction")
        pdf.body_text(forecast_summary)

    # AI insights
    if insights_text:
        pdf.section_title("5. AI-Generated Insights & Recommendations")
        pdf.body_text(insights_text)

    return bytes(pdf.output(dest="S"))
