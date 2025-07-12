"""
Configurări și setări pentru aplicația Brenado For House
"""

# Configurare pagină Streamlit
PAGE_CONFIG = {
    "page_title": "Brenado For House",
    "layout": "wide"
}

# Căi către fișierele de date
DATA_PATHS = {
    'vanzari_zi_clienti': "data/svzc.xlsx",
    'top_produse': "data/svtp.xlsx",
    'balanta_la_data': "data/LaData.xlsx",
    'balanta_perioada': "data/Perioada.xlsx",
    'cumparari_cipd': "data/CIPD.xlsx",
    'cumparari_ciis': "data/CIIS.xlsx",
    'neachitate': "data/Neachitate.xlsx",
    'neincasate': "data/Neincasate.xlsx",
    'plati_cu_efecte': "data/PlatiCuEfecte"
}

# Opțiuni pentru dropdown-uri
SHOW_OPTIONS = ["Top 10", "Top 20", "Top 50", "Top 100", "Toate produsele"]
DATE_OPTIONS_DEFAULT = ["Toate zilele"]

# Configurări cache
CACHE_TTL = 3600  # 1 oră în secunde

# Configurări pentru formatarea numerelor
NUMBER_FORMAT = {
    'decimal_places': 0,
    'thousands_separator': ',',
    'currency_symbol': 'RON'
}

# Configurări pentru filtre
FILTER_DEFAULTS = {
    'suma_minima': 0,
    'suma_step': 1000,
    'show_all_option': "Toate"
}
