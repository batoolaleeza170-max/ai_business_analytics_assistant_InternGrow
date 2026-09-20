"""
data_cleaning.py
Feature: Data Cleaning
Automated cleaning: handles missing values, duplicates, type fixes,
whitespace, and date parsing so downstream modules get a clean DataFrame.
"""
import pandas as pd
import numpy as np


def clean_data(df: pd.DataFrame, fill_strategy: str = "auto") -> tuple[pd.DataFrame, dict]:
    """
    Clean a raw DataFrame.

    Args:
        df: raw DataFrame
        fill_strategy: "auto" (mean for numeric, mode for categorical),
                        "drop" (drop rows with any NaN), or "zero"

    Returns:
        (cleaned_df, report) where report is a dict summarizing changes made.
    """
    report = {}
    df = df.copy()

    # 1. Strip whitespace from string/object columns and column names
    df.columns = [str(c).strip() for c in df.columns]
    obj_cols = df.select_dtypes(include="object").columns
    for col in obj_cols:
        df[col] = df[col].astype(str).str.strip().replace({"nan": np.nan, "None": np.nan, "": np.nan})

    # 2. Remove exact duplicate rows
    before = len(df)
    df = df.drop_duplicates()
    report["duplicates_removed"] = before - len(df)

    # 3. Try to auto-detect and parse date columns
    date_like_cols = []
    for col in df.columns:
        if df[col].dtype == object:
            sample = df[col].dropna().head(20)
            if len(sample) == 0:
                continue
            parsed = pd.to_datetime(sample, errors="coerce", infer_datetime_format=True)
            if parsed.notna().mean() > 0.8:
                df[col] = pd.to_datetime(df[col], errors="coerce", infer_datetime_format=True)
                date_like_cols.append(col)
    report["date_columns_detected"] = date_like_cols

    # 4. Handle missing values
    missing_before = int(df.isnull().sum().sum())
    if fill_strategy == "drop":
        df = df.dropna()
    else:
        for col in df.columns:
            if df[col].isnull().sum() == 0:
                continue
            if pd.api.types.is_numeric_dtype(df[col]):
                fill_val = 0 if fill_strategy == "zero" else df[col].mean()
                df[col] = df[col].fillna(fill_val)
            elif pd.api.types.is_datetime64_any_dtype(df[col]):
                df[col] = df[col].fillna(method="ffill")
            else:
                mode = df[col].mode()
                fill_val = mode.iloc[0] if not mode.empty else "Unknown"
                df[col] = df[col].fillna(fill_val)
    missing_after = int(df.isnull().sum().sum())
    report["missing_values_before"] = missing_before
    report["missing_values_after"] = missing_after

    # 5. Try converting numeric-looking object columns to numeric
    for col in df.select_dtypes(include="object").columns:
        converted = pd.to_numeric(df[col].str.replace(",", "", regex=False), errors="coerce")
        if converted.notna().mean() > 0.9:
            df[col] = converted

    report["final_shape"] = df.shape
    return df, report
