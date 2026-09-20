"""
trend_analysis.py
Feature: Trend Analysis
Computes period-over-period growth, moving averages, and
simple trend direction (up/down/flat) for a chosen metric.
"""
import pandas as pd
import numpy as np
import plotly.graph_objects as go


def analyze_trend(df: pd.DataFrame, date_col: str, value_col: str, freq: str = "M") -> dict:
    """
    Resample the value column by the given frequency and compute
    growth rate + moving average trend.

    freq: 'D' daily, 'W' weekly, 'M' monthly
    """
    data = df[[date_col, value_col]].dropna().copy()
    data[date_col] = pd.to_datetime(data[date_col], errors="coerce")
    data = data.dropna(subset=[date_col]).sort_values(date_col)

    series = data.set_index(date_col)[value_col].resample(freq).sum()

    growth = series.pct_change().fillna(0) * 100
    moving_avg = series.rolling(window=3, min_periods=1).mean()

    if len(series) >= 2:
        overall_change = ((series.iloc[-1] - series.iloc[0]) / (abs(series.iloc[0]) + 1e-9)) * 100
        direction = "upward" if overall_change > 2 else ("downward" if overall_change < -2 else "flat")
    else:
        overall_change = 0
        direction = "insufficient data"

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=series.index, y=series.values, mode="lines+markers", name=value_col))
    fig.add_trace(go.Scatter(x=moving_avg.index, y=moving_avg.values, mode="lines", name="Moving Avg (3)"))
    fig.update_layout(title=f"Trend Analysis: {value_col}", xaxis_title="Period", yaxis_title=value_col)

    return {
        "series": series,
        "growth_pct": growth,
        "moving_avg": moving_avg,
        "overall_change_pct": round(float(overall_change), 2),
        "direction": direction,
        "figure": fig,
    }
