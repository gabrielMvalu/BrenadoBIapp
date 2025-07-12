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
tab1, tab2, tab3 = st.tabs(["📅 În Dată", "📊 Perioadă", "🔍 Analize Stocuri"])

with tab1:
    st.markdown("#### 📅 Balanță Stocuri la Dată")
    
    # Încărcare date
    balanta_df = load_balanta_la_data()
    
    # Calculare metrici
    total_valoare_vanzare = balanta_df['ValoareVanzare'].sum() if 'ValoareVanzare' in balanta_df.columns else 0
    total_valoare_stoc_final = balanta_df['ValoareStocFinal'].sum() if 'ValoareStocFinal' in balanta_df.columns else 0
    
    # Metrici principale
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Total Valoare Stoc Final", f"{total_valoare_stoc_final:,.0f} RON")
    with col2:
        st.metric("Total Valoare Vânzare", f"{total_valoare_vanzare:,.0f} RON")
    
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
            st.metric("Total Valoare Stoc Final Filtrată", f"{valoare_stoc_filtrata:,.0f} RON")
        with col2:
            valoare_vanzare_filtrata = filtered_balanta['ValoareVanzare'].sum() if 'ValoareVanzare' in filtered_balanta.columns else 0
            st.metric("Total Valoare Vânzare Filtrată", f"{valoare_vanzare_filtrata:,.0f} RON")
    
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
                text=f"<b>Total Stoc<br>{total_stoc:,.0f} buc</b>",
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

with tab3:
    st.markdown("#### 🔍 Analize Stocuri - Vizualizare Ierarhică")
    
    # Încărcare date pentru analize
    analiza_df = load_balanta_la_data()
    
    if not analiza_df.empty and all(col in analiza_df.columns for col in ['DenumireGest', 'Grupa', 'ValoareStocFinal', 'ValoareVanzare']):
        
        # Calculare totaluri generale
        total_valoare_stoc_general = analiza_df['ValoareStocFinal'].sum()
        total_valoare_vanzare_general = analiza_df['ValoareVanzare'].sum()
        
        # Metrici generale în partea de sus
        st.markdown("#### 📊 Totaluri Generale")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Valoare Stoc Final", f"{total_valoare_stoc_general:,.0f} RON")
        with col2:
            st.metric("Total Valoare Vânzare", f"{total_valoare_vanzare_general:,.0f} RON")
        with col3:
            profit_potential = total_valoare_vanzare_general - total_valoare_stoc_general
            st.metric("Profit Potențial", f"{profit_potential:,.0f} RON")
        
        st.markdown("---")
        
        # Opțiune 1: Treemap Ierarhic cu ambele valori
        st.markdown("#### 🗺️ Treemap Ierarhic - Gestiuni → Grupe")
        
        # Preparare date pentru treemap
        treemap_data = analiza_df.groupby(['DenumireGest', 'Grupa']).agg({
            'ValoareStocFinal': 'sum',
            'ValoareVanzare': 'sum'
        }).reset_index()
        
        treemap_data['Profit'] = treemap_data['ValoareVanzare'] - treemap_data['ValoareStocFinal']
        treemap_data['Label'] = treemap_data['Grupa'] + '<br>' + treemap_data['DenumireGest']
        
        # Crearea Treemap
        fig_treemap = px.treemap(
            treemap_data,
            path=[px.Constant("TOTAL"), 'DenumireGest', 'Grupa'],
            values='ValoareStocFinal',
            color='Profit',
            color_continuous_scale='RdYlGn',
            title="Treemap: Mărime=Stoc Final, Culoare=Profit (Vânzare-Stoc)"
        )
        
        fig_treemap.update_traces(
            hovertemplate='<b>%{label}</b><br>' +
                         'Stoc Final: %{value:,.0f} RON<br>' +
                         'Vânzare: %{customdata[0]:,.0f} RON<br>' +
                         'Profit: %{color:,.0f} RON<extra></extra>',
            customdata=treemap_data[['ValoareVanzare']].values
        )
        
        fig_treemap.update_layout(height=600)
        st.plotly_chart(fig_treemap, use_container_width=True)
        
        st.markdown("---")
        
        # Opțiune 2: Charts separate pentru fiecare gestiune
        st.markdown("#### 📊 Analiză pe Gestiuni cu Grupe")
        
        gestiuni = analiza_df['DenumireGest'].unique()
        
        for gestiune in gestiuni:
            gestiune_data = analiza_df[analiza_df['DenumireGest'] == gestiune]
            grupe_summary = gestiune_data.groupby('Grupa').agg({
                'ValoareStocFinal': 'sum',
                'ValoareVanzare': 'sum'
            }).reset_index()
            
            total_stoc_gestiune = grupe_summary['ValoareStocFinal'].sum()
            total_vanzare_gestiune = grupe_summary['ValoareVanzare'].sum()
            profit_gestiune = total_vanzare_gestiune - total_stoc_gestiune
            
            with st.expander(f"📦 {gestiune} - Stoc: {total_stoc_gestiune:,.0f} RON | Vânzare: {total_vanzare_gestiune:,.0f} RON | Profit: {profit_gestiune:,.0f} RON"):
                
                # Chart pentru grupe din această gestiune
                fig_bar = go.Figure()
                
                fig_bar.add_trace(go.Bar(
                    name='Stoc Final',
                    x=grupe_summary['Grupa'],
                    y=grupe_summary['ValoareStocFinal'],
                    yaxis='y',
                    marker_color='lightblue',
                    hovertemplate='Stoc Final: %{y:,.0f} RON<extra></extra>'
                ))
                
                fig_bar.add_trace(go.Bar(
                    name='Vânzare',
                    x=grupe_summary['Grupa'],
                    y=grupe_summary['ValoareVanzare'],
                    yaxis='y2',
                    marker_color='orange',
                    hovertemplate='Vânzare: %{y:,.0f} RON<extra></extra>'
                ))
                
                fig_bar.update_layout(
                    title=f"Grupe din {gestiune}",
                    xaxis_title="Grupa",
                    yaxis=dict(title="Stoc Final (RON)", side="left"),
                    yaxis2=dict(title="Vânzare (RON)", side="right", overlaying="y"),
                    height=400,
                    barmode='group'
                )
                
                st.plotly_chart(fig_bar, use_container_width=True)
                
                # Tabel pentru această gestiune
                grupe_summary['Profit'] = grupe_summary['ValoareVanzare'] - grupe_summary['ValoareStocFinal']
                grupe_summary = grupe_summary.sort_values('ValoareStocFinal', ascending=False)
                st.dataframe(grupe_summary, use_container_width=True)
        
        st.markdown("---")
        
        # Analiză detaliată pe gestiuni
        st.markdown("#### 📊 Sumar Gestiuni")
        gestiuni_summary = analiza_df.groupby('DenumireGest').agg({
            'ValoareStocFinal': 'sum',
            'ValoareVanzare': 'sum'
        }).reset_index()
        gestiuni_summary['Profit Potențial'] = gestiuni_summary['ValoareVanzare'] - gestiuni_summary['ValoareStocFinal']
        gestiuni_summary.columns = ['Gestiune', 'Valoare Stoc Final', 'Valoare Vânzare', 'Profit Potențial']
        gestiuni_summary = gestiuni_summary.sort_values('Valoare Stoc Final', ascending=False)
        
        st.dataframe(gestiuni_summary, use_container_width=True)
        
        # Metrici sumare
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            nr_gestiuni = analiza_df['DenumireGest'].nunique()
            st.metric("Gestiuni", f"{nr_gestiuni}")
        
        with col2:
            gestiune_top = gestiuni_summary.iloc[0]['Gestiune']
            st.metric("Top Gestiune", gestiune_top)
        
        with col3:
            valoare_top_stoc = gestiuni_summary.iloc[0]['Valoare Stoc Final']
            st.metric("Valoare Top Stoc", f"{valoare_top_stoc:,.0f} RON")
        
        with col4:
            profit_top = gestiuni_summary.iloc[0]['Profit Potențial']
            st.metric("Profit Top", f"{profit_top:,.0f} RON")
    
    else:
        st.warning("Nu sunt disponibile datele necesare pentru analiza Sunburst. Verifică că fișierul conține coloanele: DenumireGest, Grupa, ValoareStocFinal, ValoareVanzare.")
