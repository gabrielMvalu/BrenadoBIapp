"""
Pagina Vânzări pentru aplicația Brenado For House
Conține logica pentru afișarea și filtrarea datelor de vânzări
"""

import streamlit as st
import pandas as pd
from data.loaders import load_vanzari_zi_clienti, load_top_produse
from components.metrics import render_metrics_row, format_currency, format_number
from components.filters import render_multiselect_filter, render_date_filter, render_selectbox_filter
from components.tables import render_filtered_dataframe, render_statistics_for_filtered_data
from config.settings import SHOW_OPTIONS

def calculate_vanzari_metrics(vanzari_df, produse_df):
    """Calculează metricile pentru pagina de vânzări"""
    total_valoare = vanzari_df['Valoare'].sum() if 'Valoare' in vanzari_df.columns else 0
    numar_clienti = vanzari_df['Client'].nunique() if 'Client' in vanzari_df.columns else 0
    numar_produse = len(produse_df)
    valoare_medie = vanzari_df['Valoare'].mean() if 'Valoare' in vanzari_df.columns else 0
    
    return [
        {"label": "Vânzări Totale", "value": format_currency(total_valoare)},
        {"label": "Clienți Unici", "value": format_number(numar_clienti)},
        {"label": "Produse Active", "value": format_number(numar_produse)},
        {"label": "Valoare Medie", "value": format_currency(valoare_medie)}
    ]

def render_situatia_zi_clienti_tab(vanzari_df):
    """Renderează tab-ul cu situația vânzărilor pe zi și clienți"""
    st.subheader("📊 Situația Vânzărilor pe Zi și Clienți")
    
    # Filtrare date
    col1, col2 = st.columns(2)
    
    with col1:
        client_filter = []
        if 'Client' in vanzari_df.columns:
            client_filter = render_multiselect_filter(
                "Filtrează după client:",
                vanzari_df['Client'].unique(),
                "client_filter_vanzari"
            )
    
    with col2:
        date_filter = "Toate zilele"
        if 'Data' in vanzari_df.columns:
            vanzari_df['Data'] = pd.to_datetime(vanzari_df['Data'], errors='coerce')
            date_filter = render_date_filter(
                "Filtrează după zi:",
                vanzari_df['Data'],
                "date_filter_vanzari"
            )
    
    # Aplicare filtre
    filtered_df = apply_vanzari_filters(vanzari_df, client_filter, date_filter)
    
    # Afișare tabel filtrat
    render_filtered_dataframe(filtered_df)
    
    # Statistici pentru datele filtrate
    if not filtered_df.empty:
        columns_config = [
            {"column": "Pret Contabil", "label": "Total Preț Contabil", "format": "currency"},
            {"column": "Valoare", "label": "Total Valoare", "format": "currency"},
            {"column": "Adaos", "label": "Total Adaos", "format": "currency"},
            {"column": "Cost", "label": "Total Cost", "format": "currency"}
        ]
        render_statistics_for_filtered_data(filtered_df, columns_config)
        
        # Metric pentru numărul de înregistrări
        col_extra = st.columns(5)
        with col_extra[4]:
            st.metric("Înregistrări", len(filtered_df))

def render_top_produse_tab(produse_df):
    """Renderează tab-ul cu top produse"""
    st.subheader("🏆 Top Produse după Valoare")
    
    # Opțiuni de filtrare
    col1, col2 = st.columns(2)
    with col1:
        show_option = st.selectbox(
            "Afișează:",
            SHOW_OPTIONS,
            key="show_option_produse"
        )
    
    # Sortare și filtrare top produse
    if 'Valoare' in produse_df.columns:
        top_produse = produse_df.sort_values('Valoare', ascending=False)
        
        # Aplicare filtrare bazată pe selecție
        if show_option == "Top 10":
            top_produse = top_produse.head(10)
        elif show_option == "Top 20":
            top_produse = top_produse.head(20)
        elif show_option == "Top 50":
            top_produse = top_produse.head(50)
        elif show_option == "Top 100":
            top_produse = top_produse.head(100)
        
        # Afișare tabel
        render_filtered_dataframe(top_produse)
        
        # Statistici produse
        columns_config = [
            {"column": "Valoare", "label": "Top Produs Valoare", "format": "max_currency"},
            {"column": "Cantitate", "label": "Cantitate Totală", "format": "sum"},
            {"column": "Valoare", "label": "Valoare Totală", "format": "currency"},
            {"column": "Adaos", "label": "Adaos Total", "format": "currency"}
        ]
        
        # Statistici personalizate pentru produse
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Top Produs Valoare", format_currency(produse_df['Valoare'].max()))
        with col2:
            st.metric("Cantitate Totală", format_number(produse_df['Cantitate'].sum()))
        with col3:
            st.metric("Valoare Totală", format_currency(produse_df['Valoare'].sum()))
        with col4:
            st.metric("Adaos Total", format_currency(produse_df['Adaos'].sum()))
    else:
        st.error("Nu s-au putut încărca datele produselor")

def apply_vanzari_filters(df, client_filter, date_filter):
    """Aplică filtrele pentru datele de vânzări"""
    filtered_df = df.copy()
    
    # Aplicare filtru client
    if 'Client' in df.columns and client_filter:
        filtered_df = filtered_df[filtered_df['Client'].isin(client_filter)]
    
    # Aplicare filtru dată
    if 'Data' in df.columns and date_filter != "Toate zilele":
        selected_date = pd.to_datetime(date_filter).date()
        filtered_df = filtered_df[filtered_df['Data'].dt.date == selected_date]
    
    return filtered_df

def render_page():
    """Funcția principală pentru renderarea paginii Vânzări"""
    st.markdown("### 📊 Vânzări")
    
    # Încărcare date
    vanzari_df = load_vanzari_zi_clienti()
    produse_df = load_top_produse()
    
    # Calculare și afișare metrici principale
    metrics_data = calculate_vanzari_metrics(vanzari_df, produse_df)
    render_metrics_row(metrics_data)
    
    st.markdown("---")
    
    # Tabs pentru diferite secțiuni
    tab1, tab2 = st.tabs(["📊 Situația Zi și Clienți", "🏆 Top Produse"])
    
    with tab1:
        render_situatia_zi_clienti_tab(vanzari_df)
    
    with tab2:
        render_top_produse_tab(produse_df)
