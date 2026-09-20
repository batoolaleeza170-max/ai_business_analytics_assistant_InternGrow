"""
prediction.py
Feature: Sales Prediction
Uses a simple, dependency-light regression approach (Linear Regression
on time index, with optional polynomial features) to forecast future
values of a chosen numeric column (e.g. sales) based on a date column.
"""
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_absolute_error, r2_score
import plotly.graph_objects as go


def predict_sales(df: pd.DataFrame, date_col: str, value_col: str,
                   periods_ahead: int = 6, freq: str = "M", degree: int = 2) -> dict:
    """
    Fit a polynomial regression on (time_index -> value) and forecast
    `periods_ahead` future periods.

    Returns dict with historical + forecast data and an interactive figure.
    """
    data = df[[date_col, value_col]].dropna().copy()
    data[date_col] = pd.to_datetime(data[date_col], errors="coerce")
    data = data.dropna(subset=[date_col]).sort_values(date_col)

    series = data.set_index(date_col)[value_col].resample(freq).sum()
    series = series[series.index.notna()]

    if len(series) < 3:
        return {"error": "Not enough time-series data points to build a reliable forecast (need at least 3)."}

    X = np.arange(len(series)).reshape(-1, 1)
    y = series.values

    poly = PolynomialFeatures(degree=degree)
    X_poly = poly.fit_transform(X)

    model = LinearRegression()
    model.fit(X_poly, y)

    y_pred_hist = model.predict(X_poly)
    mae = mean_absolute_error(y, y_pred_hist)
    r2 = r2_score(y, y_pred_hist)

    future_X = np.arange(len(series), len(series) + periods_ahead).reshape(-1, 1)
    future_X_poly = poly.transform(future_X)
    forecast = model.predict(future_X_poly)
    forecast = np.maximum(forecast, 0)  # sales shouldn't be negative

    future_dates = pd.date_range(series.index[-1], periods=periods_ahead + 1, freq=freq)[1:]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=series.index, y=series.values, mode="lines+markers", name="Historical"))
    fig.add_trace(go.Scatter(x=future_dates, y=forecast, mode="lines+markers",
                              name="Forecast", line=dict(dash="dash")))
    fig.update_layout(title=f"Sales Forecast: {value_col}", xaxis_title="Period", yaxis_title=value_col)

    return {
        "historical_dates": series.index,
        "historical_values": series.values,
        "forecast_dates": future_dates,
        "forecast_values": forecast,
        "mae": round(float(mae), 2),
        "r2_score": round(float(r2), 3),
        "figure": fig,
    }
