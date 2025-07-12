# src/components/sidebar.py
"""
Componenta sidebar pentru aplicația Brenado For House
"""

import streamlit as st

def render_sidebar():
    """Renderează sidebar-ul aplicației"""
    with st.sidebar:
        st.title("🏠 Brenado For House")
        st.caption("Segmentul rezidențial")

# src/components/metrics.py
"""
Componente pentru afișarea metricilor în aplicația Brenado For House
"""

import streamlit as st

def render_metrics_row(metrics_data):
    """
    Renderează o linie de metrici
    
    Args:
        metrics_data: Lista de dicționare cu structura [{"label": "...", "value": "...", "delta": "..."}, ...]
    """
    cols = st.columns(len(metrics_data))
    
    for i, metric in enumerate(metrics_data):
        with cols[i]:
            st.metric(
                metric["label"], 
                metric["value"], 
                delta=metric.get("delta", None)
            )

def format_currency(value, currency="RON"):
    """Formatează o valoare ca monedă"""
    return f"{value:,.0f} {currency}"

def format_number(value):
    """Formatează un număr cu separatori"""
    return f"{value:,.0f}"

# components/filters.py
"""
Componente pentru filtrele comune în aplicația Brenado For House
"""

import streamlit as st
import pandas as pd
from src.config.settings import FILTER_DEFAULTS

def render_multiselect_filter(label, options, key, default=None):
    """
    Renderează un filtru multiselect
    
    Args:
        label: Eticheta filtrului
        options: Lista de opțiuni
        key: Cheia unică pentru widget
        default: Valorile implicite
    
    Returns:
        Lista valorilor selectate
    """
    if default is None:
        default = []
    
    return st.multiselect(
        label,
        options=options,
        default=default,
        key=key
    )

def render_selectbox_filter(label, options, key, include_all=True):
    """
    Renderează un filtru selectbox cu opțiunea 'Toate'
    
    Args:
        label: Eticheta filtrului
        options: Lista de opțiuni
        key: Cheia unică pentru widget
        include_all: Dacă să includă opțiunea 'Toate'
    
    Returns:
        Valoarea selectată
    """
    if include_all:
        all_options = [FILTER_DEFAULTS['show_all_option']] + list(options)
    else:
        all_options = list(options)
    
    return st.selectbox(label, options=all_options, key=key)

def render_date_filter(label, date_series, key):
    """
    Renderează un filtru pentru date
    
    Args:
        label: Eticheta filtrului
        date_series: Seria pandas cu datele
        key: Cheia unică pentru widget
    
    Returns:
        Data selectată sau 'Toate zilele'
    """
    # Convertește la datetime și creează opțiuni
    date_series = pd.to_datetime(date_series, errors='coerce')
    date_options = ["Toate zilele"] + sorted([str(date.date()) for date in date_series.dropna().unique()])
    
    return st.selectbox(label, options=date_options, key=key)

def render_amount_filter(label, key, min_value=0, step=1000):
    """
    Renderează un filtru pentru sume
    
    Args:
        label: Eticheta filtrului
        key: Cheia unică pentru widget
        min_value: Valoarea minimă
        step: Pasul pentru incrementare
    
    Returns:
        Valoarea introdusă
    """
    return st.number_input(
        label,
        min_value=min_value,
        value=min_value,
        step=step,
        key=key
    )

# components/tables.py
"""
Componente pentru afișarea tabelelor în aplicația Brenado For House
"""

import streamlit as st

def render_filtered_dataframe(df, title=None):
    """
    Renderează un DataFrame cu titlu opțional
    
    Args:
        df: DataFrame-ul de afișat
        title: Titlul opțional
    """
    if title:
        st.subheader(f"📋 {title} ({len(df)} înregistrări)")
    
    st.dataframe(df, use_container_width=True)

def render_statistics_for_filtered_data(df, columns_config):
    """
    Renderează statistici pentru datele filtrate
    
    Args:
        df: DataFrame-ul filtrat
        columns_config: Configurarea coloanelor pentru statistici
                       [{"column": "col_name", "label": "Label", "format": "currency/number"}]
    """
    if not df.empty:
        st.markdown("#### 📊 Statistici Date Filtrate")
        
        cols = st.columns(len(columns_config))
        
        for i, config in enumerate(columns_config):
            with cols[i]:
                column_name = config["column"]
                label = config["label"]
                format_type = config.get("format", "number")
                
                if column_name in df.columns:
                    if format_type == "sum":
                        value = df[column_name].sum()
                        formatted_value = f"{value:,.0f}"
                    elif format_type == "mean":
                        value = df[column_name].mean()
                        formatted_value = f"{value:.0f}"
                    elif format_type == "count":
                        value = df[column_name].nunique()
                        formatted_value = f"{value}"
                    elif format_type == "currency":
                        value = df[column_name].sum()
                        formatted_value = f"{value:,.0f} RON"
                    else:  # number
                        value = len(df) if column_name == "count_rows" else df[column_name].sum()
                        formatted_value = f"{value:,.0f}"
                    
                    st.metric(label, formatted_value)
