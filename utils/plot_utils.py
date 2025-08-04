# utils/plot_utils.py
import pandas as pd
import streamlit as st

def plot_bar(bar: dict) -> None:
    """
    Plot a bar chart based on the LangChain output format.
    Supports both single-dimensional and multi-dimensional data.

    Args:
        bar (dict): Contains 'columns' (List[str]) and 'data' (List or List[List]).
    """
    cols = bar["columns"]
    data = bar["data"]
    # Handle multi-dimensional data
    if isinstance(data[0], list):
        df = pd.DataFrame(data, columns=cols).set_index(cols[0])
    else:
        # Handle single-dimensional data and ensure length matches the number of columns
        if len(data) != len(cols):
            data = data[:len(cols)]
        df = pd.DataFrame({"value": data}, index=cols)
    st.bar_chart(df)


def plot_line(line: dict) -> None:
    """
    Plot a line chart based on the LangChain output format.
    Supports both single-dimensional and multi-dimensional data.

    Args:
        line (dict): Contains 'columns' (List[str]) and 'data' (List or List[List]).
    """
    cols = line["columns"]
    data = line["data"]
    if isinstance(data[0], list):
        df = pd.DataFrame(data, columns=cols).set_index(cols[0])
    else:
        if len(data) != len(cols):
            data = data[:len(cols)]
        df = pd.DataFrame({"value": data}, index=cols)
    st.line_chart(df)


def plot_scatter(scatter: dict) -> None:
    """
    Plot a scatter chart based on the LangChain output format.

    Args:
        scatter (dict): Contains 'columns' (List[str]) and 'data' (List[List]).
    """
    cols = scatter["columns"]
    data = scatter["data"]
    df = pd.DataFrame(data, columns=cols)
    st.scatter_chart(df)
