"""
visualization.py
Feature: Automated Charts
Automatically picks sensible chart types based on column data types
and renders them with Plotly for the interactive dashboard.
"""
import pandas as pd
import plotly.express as px


def get_numeric_columns(df: pd.DataFrame) -> list:
    return df.select_dtypes(include="number").columns.tolist()


def get_categorical_columns(df: pd.DataFrame) -> list:
    return df.select_dtypes(include="object").columns.tolist()


def get_date_columns(df: pd.DataFrame) -> list:
    return df.select_dtypes(include="datetime").columns.tolist()


def auto_generate_charts(df: pd.DataFrame) -> list:
    """
    Inspect the DataFrame and automatically build a list of
    (title, plotly_figure) tuples for the most useful charts.
    """
    charts = []
    numeric_cols = get_numeric_columns(df)
    cat_cols = get_categorical_columns(df)
    date_cols = get_date_columns(df)

    # 1. Time series line chart (date + first numeric column)
    if date_cols and numeric_cols:
        date_col, num_col = date_cols[0], numeric_cols[0]
        ts = df.groupby(date_col)[num_col].sum().reset_index().sort_values(date_col)
        fig = px.line(ts, x=date_col, y=num_col, title=f"{num_col} Over Time")
        charts.append((f"{num_col} Trend", fig))

    # 2. Bar chart: top categories by first numeric column
    if cat_cols and numeric_cols:
        cat_col, num_col = cat_cols[0], numeric_cols[0]
        agg = df.groupby(cat_col)[num_col].sum().reset_index().sort_values(num_col, ascending=False).head(10)
        fig = px.bar(agg, x=cat_col, y=num_col, title=f"Top {cat_col} by {num_col}")
        charts.append((f"{num_col} by {cat_col}", fig))

    # 3. Distribution histogram of first numeric column
    if numeric_cols:
        num_col = numeric_cols[0]
        fig = px.histogram(df, x=num_col, title=f"Distribution of {num_col}")
        charts.append((f"{num_col} Distribution", fig))

    # 4. Correlation heatmap if 2+ numeric columns
    if len(numeric_cols) >= 2:
        corr = df[numeric_cols].corr()
        fig = px.imshow(corr, text_auto=".2f", title="Correlation Heatmap", color_continuous_scale="RdBu_r")
        charts.append(("Correlation Heatmap", fig))

    # 5. Pie chart for a low-cardinality categorical column
    for c in cat_cols:
        if df[c].nunique() <= 8 and numeric_cols:
            agg = df.groupby(c)[numeric_cols[0]].sum().reset_index()
            fig = px.pie(agg, names=c, values=numeric_cols[0], title=f"{numeric_cols[0]} Share by {c}")
            charts.append((f"{c} Breakdown", fig))
            break

    return charts
