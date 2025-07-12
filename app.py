import streamlit as st

# Configurare pagină
st.set_page_config(
    page_title="Brenado For House",
    layout="wide"
)

# Mesaj de bun venit
st.title("🏠 Welcome to Brenado For House - Rapoarte")

st.markdown("""
### Selectează o categorie din sidebar pentru a vizualiza rapoartele:

- **📊 Vânzări** - Analiza vânzărilor pe zile și clienți
- **📦 Balanță Stocuri** - Situația stocurilor și gestiunilor  
- **🛒 Cumpărări Intrări** - Rapoarte cumpărări și intrări în stoc
- **📥 Facturi Neincasate** - Facturi emise neincasate de la clienți
- **❌ Facturi Neachitate** - Facturi primite neachitate către furnizori
- **⏰ Scadențe Plăți Cu Efecte** - Monitorizarea scadențelor și efectelor
""")

st.markdown("---")
st.caption("Brenado For House - Segmentul Rezidențial")
