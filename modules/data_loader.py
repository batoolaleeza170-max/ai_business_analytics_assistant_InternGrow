"""
data_loader.py
Feature: CSV/Excel Upload
Handles reading uploaded CSV or Excel files into a pandas DataFrame.
"""
import pandas as pd
import streamlit as st


def load_data(uploaded_file):
    """
    Load a CSV or Excel file uploaded via Streamlit's file_uploader
    into a pandas DataFrame.

    Args:
        uploaded_file: Streamlit UploadedFile object

    Returns:
        pd.DataFrame or None
    """
    if uploaded_file is None:
        return None

    file_name = uploaded_file.name.lower()

    try:
        if file_name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        elif file_name.endswith((".xlsx", ".xls")):
            df = pd.read_excel(uploaded_file)
        else:
            st.error("Unsupported file type. Please upload a .csv or .xlsx file.")
            return None

        if df.empty:
            st.warning("The uploaded file appears to be empty.")
            return None

        return df

    except Exception as e:
        st.error(f"Error reading file: {e}")
        return None


def get_basic_info(df: pd.DataFrame) -> dict:
    """Return quick metadata about the loaded dataset."""
    return {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "column_names": list(df.columns),
        "dtypes": df.dtypes.astype(str).to_dict(),
        "missing_values": df.isnull().sum().to_dict(),
    }
