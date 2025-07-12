"""
Pagina Balanță Stocuri pentru aplicația Brenado For House
Conține 2 subcategorii: La Dată și În Perioadă
"""

import streamlit as st
from utils.data_loaders import load_balanta_la_data, load_balanta_perioada

# Titlu pagină
st.markdown("### 📦 Balanță Stocuri")

# Tabs pentru subcategoriile Balanță Stocuri
tab1, tab2 = st.tabs(["📅 În Data", "📊 Perioadă"])

with tab1:
    st.markdown("#### 📅 Balanță Stocuri la Data")
    
    # Încărcare date
    balanta_df = load_balanta_la_data()
    
    # Calculare metrici
    total_valoare_vanzare = balanta_df['ValoareVanzare'].sum() if 'ValoareVanzare' in balanta_df.columns else 0
    total_valoare_stoc_final = balanta_df['ValoareStocFinal'].sum() if 'ValoareStocFinal' in balanta_df.columns else 0
    
    # Metrici principale
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Total Valoare Vânzare", f"{total_valoare_vanzare:,.0f} RON")
    with col2:
        st.metric("Total Valoare Stoc Final", f"{total_valoare_stoc_final:,.0f} RON")
    
    st.markdown("---")
    
    # Filtrare date
    col1, col2 = st.columns(2)
    with col1:
        if 'DenumireGest' in balanta_df.columns:
            gestiune_filter = st.multiselect(
                "Filtrează după gestiune:",
                options=balanta_df['DenumireGest'].unique(),
                default=[],
                key="gestiune_filter_tab1"
            )
    
    with col2:
        if 'Denumire' in balanta_df.columns:
            produs_filter = st.multiselect(
                "Filtrează după produs:",
                options=balanta_df['Denumire'].unique(),
                default=[],
                key="produs_filter_tab1"
            )
    
    # Aplicare filtre
    filtered_balanta = balanta_df.copy()
    if 'DenumireGest' in balanta_df.columns and gestiune_filter:
        filtered_balanta = filtered_balanta[filtered_balanta['DenumireGest'].isin(gestiune_filter)]
    
    if 'Denumire' in balanta_df.columns and produs_filter:
        filtered_balanta = filtered_balanta[filtered_balanta['Denumire'].isin(produs_filter)]
    
    # Tabel cu date
    st.dataframe(filtered_balanta, use_container_width=True)
    
    # Statistici pentru datele filtrate
    if not filtered_balanta.empty:
        st.markdown("#### 📊 Statistici Date Filtrate")
        col1, col2 = st.columns(2)
        
        with col1:
            valoare_vanzare_filtrata = filtered_balanta['ValoareVanzare'].sum() if 'ValoareVanzare' in filtered_balanta.columns else 0
            st.metric("Total Valoare Vânzare Filtrată", f"{valoare_vanzare_filtrata:,.0f} RON")
        with col2:
            valoare_stoc_filtrata = filtered_balanta['ValoareStocFinal'].sum() if 'ValoareStocFinal' in filtered_balanta.columns else 0
            st.metric("Total Valoare Stoc Final Filtrată", f"{valoare_stoc_filtrata:,.0f} RON")

with tab2:
    st.markdown("#### 📊 Balanță Stocuri pe Perioadă")
    
    # Încărcare date
    perioada_df = load_balanta_perioada()
    
    # Calculare metrici
    total_stoc = perioada_df['Stoc final'].sum() if 'Stoc final' in perioada_df.columns else 0
    valoare_intrare = perioada_df['Valoare intrare'].sum() if 'Valoare intrare' in perioada_df.columns else 0
    numar_produse = len(perioada_df)
    vechime_medie = perioada_df['ZileVechime'].mean() if 'ZileVechime' in perioada_df.columns else 0
    
    # Metrici principale
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Stoc Total", f"{total_stoc:,.0f} buc")
    with col2:
        st.metric("Valoare Intrare", f"{valoare_intrare:,.0f} RON")
    with col3:
        st.metric("Produse", f"{numar_produse:,}")
    with col4:
        st.metric("Vechime Medie", f"{vechime_medie:.0f} zile")
    
    st.markdown("---")
    
    # Filtrare date
    col1, col2 = st.columns(2)
    with col1:
        if 'Denumire gestiune' in perioada_df.columns:
            gestiune_filter = st.multiselect(
                "Filtrează după gestiune:",
                options=perioada_df['Denumire gestiune'].unique(),
                default=[],
                key="gestiune_filter_tab2"
            )
    
    with col2:
        if 'Denumire' in perioada_df.columns:
            produs_filter = st.multiselect(
                "Filtrează după produs:",
                options=perioada_df['Denumire'].unique(),
                default=[],
                key="produs_filter_tab2"
            )
    
    # Aplicare filtre
    filtered_perioada = perioada_df.copy()
    if 'Denumire gestiune' in perioada_df.columns and gestiune_filter:
        filtered_perioada = filtered_perioada[filtered_perioada['Denumire gestiune'].isin(gestiune_filter)]
    
    if 'Denumire' in perioada_df.columns and produs_filter:
        filtered_perioada = filtered_perioada[filtered_perioada['Denumire'].isin(produs_filter)]
    
    # Tabel cu date
    st.dataframe(filtered_perioada, use_container_width=True)
    
    # Statistici pentru datele filtrate
    if not filtered_perioada.empty:
        st.markdown("#### 📊 Statistici Date Filtrate")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            stoc_filtrat = filtered_perioada['Stoc final'].sum() if 'Stoc final' in filtered_perioada.columns else 0
            st.metric("Stoc Filtrat", f"{stoc_filtrat:,.0f} buc")
        with col2:
            valoare_filtrata = filtered_perioada['Valoare intrare'].sum() if 'Valoare intrare' in filtered_perioada.columns else 0
            st.metric("Valoare Filtrată", f"{valoare_filtrata:,.0f} RON")
        with col3:
            produse_filtrate = len(filtered_perioada)
            st.metric("Produse Filtrate", f"{produse_filtrate:,}")
        with col4:
            vechime_filtrata = filtered_perioada['ZileVechime'].mean() if 'ZileVechime' in filtered_perioada.columns else 0
            st.metric("Vechime Medie", f"{vechime_filtrata:.0f} zile")
