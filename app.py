"""
Brenado For House - Aplicație Streamlit
"""

import streamlit as st
from config.settings import PAGE_CONFIG
from components.sidebar import render_sidebar
from pages import vanzari, balanta_stocuri, cumparari, plati_facturi

def main():
    """Funcția principală a aplicației"""
    
    # Configurare pagină
    st.set_page_config(**PAGE_CONFIG)
    
    # Sidebar
    category = render_sidebar()
    
    # Header
    st.title("Brenado For House")
    st.markdown("---")
    
    # Selectare categorie principală
    st.subheader("📂 Selectează Categoria")
    category = st.selectbox(
        "Alege categorie rapoarte:",
        ["Vânzări", "Balanță Stocuri", "Cumparari Intrari", "Plăți Facturi"]
    )
    st.markdown("---")
    
    # Routing către paginile respective
    if category == "Vânzări":
        vanzari.render_page()
    elif category == "Balanță Stocuri":
        balanta_stocuri.render_page()
    elif category == "Cumparari Intrari":
        cumparari.render_page()
    elif category == "Plăți Facturi":
        plati_facturi.render_page()

if __name__ == "__main__":
    main()
