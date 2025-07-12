"""
Pagina Balanță Stocuri pentru aplicația Brenado For House
Conține 2 subcategorii: La Dată și În Perioadă
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils.data_loaders import load_balanta_la_data, load_balanta_perioada

# Titlu pagină
st.markdown("### 📦 Balanță Stocuri")

# Tabs pentru subcategoriile Balanță Stocuri
tab1, tab2 = st.tabs(["📅 La Data", "📊 Perioadă"])

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
        st.metric("Total Valoare Stoc", f"{total_valoare_stoc_final:,.2f} RON")
    with col2:
        st.metric("Total Valoare Vânzare", f"{total_valoare_vanzare:,.2f} RON")
    
    st.markdown("---")
    
    # Filtrare date - INTERDEPENDENTE
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if 'DenumireGest' in balanta_df.columns:
            gestiune_filter = st.multiselect(
                "Filtrează după gestiune:",
                options=balanta_df['DenumireGest'].unique(),
                default=[],
                key="gestiune_filter_tab1"
            )
    
    # Filtrare pentru grupa bazată pe gestiunea selectată
    df_for_grupa = balanta_df.copy()
    if 'DenumireGest' in balanta_df.columns and gestiune_filter:
        df_for_grupa = df_for_grupa[df_for_grupa['DenumireGest'].isin(gestiune_filter)]
    
    with col2:
        if 'Grupa' in balanta_df.columns:
            # Afișează doar grupele din gestiunile selectate
            grupa_options = df_for_grupa['Grupa'].unique() if not df_for_grupa.empty else []
            grupa_filter = st.multiselect(
                "Filtrează după grupă:",
                options=grupa_options,
                default=[],
                key="grupa_filter_tab1"
            )
    
    # Filtrare pentru produs bazată pe gestiunea și grupa selectate
    df_for_produs = df_for_grupa.copy()
    if 'Grupa' in balanta_df.columns and grupa_filter:
        df_for_produs = df_for_produs[df_for_produs['Grupa'].isin(grupa_filter)]
    
    with col3:
        if 'Denumire' in balanta_df.columns:
            # Afișează doar produsele din gestiunile și grupele selectate
            produs_options = df_for_produs['Denumire'].unique() if not df_for_produs.empty else []
            produs_filter = st.multiselect(
                "Filtrează după produs:",
                options=produs_options,
                default=[],
                key="produs_filter_tab1"
            )
    
    # Aplicare filtre
    filtered_balanta = balanta_df.copy()
    if 'DenumireGest' in balanta_df.columns and gestiune_filter:
        filtered_balanta = filtered_balanta[filtered_balanta['DenumireGest'].isin(gestiune_filter)]
    
    if 'Grupa' in balanta_df.columns and grupa_filter:
        filtered_balanta = filtered_balanta[filtered_balanta['Grupa'].isin(grupa_filter)]
    
    if 'Denumire' in balanta_df.columns and produs_filter:
        filtered_balanta = filtered_balanta[filtered_balanta['Denumire'].isin(produs_filter)]
    
    # Tabel cu date
    st.dataframe(filtered_balanta, use_container_width=True)
    
    # Statistici pentru datele filtrate (doar când s-au aplicat filtre)
    if not filtered_balanta.empty and (gestiune_filter or grupa_filter or produs_filter):
        st.markdown("#### 📊 Statistici Date Filtrate")
        col1, col2 = st.columns(2)
        
        with col1:
            valoare_stoc_filtrata = filtered_balanta['ValoareStocFinal'].sum() if 'ValoareStocFinal' in filtered_balanta.columns else 0
            st.metric("Total Valoare Stoc", f"{valoare_stoc_filtrata:,.2f} RON")
        with col2:
            valoare_vanzare_filtrata = filtered_balanta['ValoareVanzare'].sum() if 'ValoareVanzare' in filtered_balanta.columns else 0
            st.metric("Total Valoare Vânzare", f"{valoare_vanzare_filtrata:,.2f} RON")
    
    # Donut Chart pentru stocuri pe gestiuni (doar când se filtrează după produs)
    if produs_filter and 'Stoc final' in filtered_balanta.columns and 'DenumireGest' in filtered_balanta.columns:
        st.markdown("#### 📊 Distribuția Stocului pe Gestiuni")
        
        # Grupare după gestiune și sumarea stocurilor
        stoc_pe_gestiune = filtered_balanta.groupby('DenumireGest')['Stoc final'].sum().reset_index()
        stoc_pe_gestiune = stoc_pe_gestiune[stoc_pe_gestiune['Stoc final'] > 0]  # Doar gestiunile cu stoc
        
        if not stoc_pe_gestiune.empty:
            # Calculare total pentru centru
            total_stoc = stoc_pe_gestiune['Stoc final'].sum()
            
            # Crearea donut chart-ului
            fig = go.Figure(data=[go.Pie(
                labels=stoc_pe_gestiune['DenumireGest'],
                values=stoc_pe_gestiune['Stoc final'],
                hole=0.4,  # Crează gaura din mijloc pentru donut
                textinfo='label+value',
                texttemplate='%{label}<br>%{value} buc',
                textposition='outside',
                hovertemplate='<b>%{label}</b><br>Stoc: %{value} buc<extra></extra>'
            )])
            
            # Adăugare text în centru cu totalul
            fig.add_annotation(
                text=f"<b>Total Stoc<br>{total_stoc:,.2f} buc</b>",
                x=0.5, y=0.5,
                font_size=16,
                showarrow=False
            )
            
            # Configurare layout
            fig.update_layout(
                title="Distribuția Stocului Final pe Gestiuni",
                title_x=0.5,
                height=500,
                showlegend=True,
                legend=dict(
                    orientation="v",
                    yanchor="middle",
                    y=0.5,
                    xanchor="left",
                    x=1.05
                )
            )
            
            # Afișare grafic
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Nu există date de stoc pentru produsele filtrate.")

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
