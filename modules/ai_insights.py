"""
ai_insights.py
Feature: AI-Generated Insights (+ Upgrade: Natural Language Queries)
Uses the Anthropic Claude API to turn dataset statistics into
plain-English business insights, and to answer free-text questions
about the data by generating + running safe pandas code.
"""
import os
import json
import pandas as pd
import streamlit as st
from anthropic import Anthropic

MODEL = "claude-sonnet-4-5"  # update to the latest available model string as needed


def get_client() -> Anthropic | None:
    api_key = os.getenv("ANTHROPIC_API_KEY") or st.session_state.get("api_key")
    if not api_key:
        return None
    return Anthropic(api_key=api_key)


def generate_insights(df: pd.DataFrame, business_context: str = "") -> str:
    """
    Summarize key stats and ask Claude to produce business insights.
    """
    client = get_client()
    if client is None:
        return "⚠️ No API key set. Add ANTHROPIC_API_KEY to use AI-generated insights."

    summary = {
        "shape": df.shape,
        "columns": list(df.columns),
        "numeric_summary": json.loads(df.describe(include="number").round(2).to_json()),
        "sample_rows": df.head(5).to_dict(orient="records"),
    }

    prompt = f"""You are a business data analyst. Given this dataset summary, write a concise,
plain-English report (use headers and bullet points) covering:
1. Key trends and patterns
2. Notable anomalies or outliers
3. 3-5 actionable business recommendations

Business context: {business_context or "General business dataset"}

Dataset summary (JSON):
{json.dumps(summary, default=str)[:6000]}
"""

    response = client.messages.create(
        model=MODEL,
        max_tokens=1200,
        messages=[{"role": "user", "content": prompt}],
    )
    return "".join(block.text for block in response.content if block.type == "text")


def answer_nl_query(df: pd.DataFrame, question: str):
    """
    Upgrade Feature: Natural Language Queries.
    Ask Claude to write a small pandas snippet that answers `question`
    using a DataFrame called `df`, then execute it in a restricted scope.

    Returns (answer_text, result_value_or_None, generated_code)
    """
    client = get_client()
    if client is None:
        return "⚠️ No API key set. Add ANTHROPIC_API_KEY to use natural language queries.", None, None

    schema = {"columns": list(df.columns), "dtypes": df.dtypes.astype(str).to_dict()}

    prompt = f"""You are a pandas expert. A DataFrame named `df` has this schema:
{json.dumps(schema, default=str)}

Write ONLY a single Python expression (no imports, no print, no assignment,
no explanation) using `df` that answers this question:
"{question}"

Respond with ONLY the code, nothing else."""

    response = client.messages.create(
        model=MODEL,
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
    )
    code = "".join(block.text for block in response.content if block.type == "text").strip()
    code = code.strip("`").replace("python\n", "").strip()

    # Restricted execution: only pandas/numpy + the dataframe are exposed
    safe_globals = {"pd": pd, "df": df}
    try:
        result = eval(code, {"__builtins__": {}}, safe_globals)
    except Exception as e:
        return f"Could not compute an answer ({e}).", None, code

    explain_prompt = f"""The question was: "{question}"
The computed pandas result is: {str(result)[:2000]}
Write one short, friendly sentence answering the question using this result."""
    explain_resp = client.messages.create(
        model=MODEL,
        max_tokens=200,
        messages=[{"role": "user", "content": explain_prompt}],
    )
    answer_text = "".join(block.text for block in explain_resp.content if block.type == "text")

    return answer_text, result, code
