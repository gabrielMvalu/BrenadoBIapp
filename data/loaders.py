"""
Funcții pentru încărcarea datelor din fișierele Excel
Toate funcțiile de tip load_* din codul original
"""

import streamlit as st
import pandas as pd
from config.settings import DATA_PATHS

@st.cache_data
def load_vanzari_zi_clienti():
    """Încarcă datele din Excel - Situația zi și clienți"""
    try:
        df = pd.read_excel(DATA_PATHS['vanzari_zi_clienti'])
        return df
    except:
        return pd.DataFrame({
            'Data': ['2024-01-01', '2024-01-02'],
            'Client': ['Client Demo 1', 'Client Demo 2'],
            'Pret Contabil': [100, 200],
            'Valoare': [1000, 2000],
            'Adaos': [50, 100],
            'Cost': [950, 1900]
        })

@st.cache_data
def load_top_produse():
    """Încarcă datele din Excel - Top produse"""
    try:
        df = pd.read_excel(DATA_PATHS['top_produse'])
        return df
    except:
        return pd.DataFrame({
            'Denumire': ['Produs Demo 1', 'Produs Demo 2'],
            'Cantitate': [100, 200],
            'Valoare': [5000, 8000],
            'Adaos': [500, 800]
        })

@st.cache_data
def load_balanta_la_data():
    """Încarcă datele din Excel - Balanță la dată"""
    try:
        df = pd.read_excel(DATA_PATHS['balanta_la_data'])
        return df
    except:
        return pd.DataFrame({
            'DenumireGest': ['Demo Gestiune'],
            'Denumire': ['Produs Demo'],
            'Stoc final': [100],
            'ValoareStocFinal': [5000]
        })

@st.cache_data
def load_balanta_perioada():
    """Încarcă datele din Excel - Balanță pe perioadă"""
    try:
        df = pd.read_excel(DATA_PATHS['balanta_perioada'])
        return df
    except:
        return pd.DataFrame({
            'Denumire gestiune': ['Demo Gestiune'],
            'Denumire': ['Produs Demo'],
            'Stoc final': [100],
            'ZileVechime': [10]
        })

@st.cache_data
def load_cumparari_cipd():
    """Încarcă datele din Excel - Cumparari CIPD"""
    try:
        df = pd.read_excel(DATA_PATHS['cumparari_cipd'])
        return df
    except:
        return pd.DataFrame({
            'Gestiune': ['Demo Gestiune'],
            'Denumire': ['Produs Demo'],
            'Cantitate': [100],
            'Valoare': [5000],
            'Furnizor': ['Demo Furnizor']
        })

@st.cache_data
def load_cumparari_ciis():
    """Încarcă datele din Excel - Cumparari CIIS"""
    try:
        df = pd.read_excel(DATA_PATHS['cumparari_ciis'])
        return df
    except:
        return pd.DataFrame({
            'Gestiune': ['Demo Gestiune'],
            'Denumire': ['Produs Demo'],
            'Cantitate': [100],
            'Valoare': [5000],
            'Furnizor': ['Demo Furnizor']
        })

@st.cache_data
def load_neachitate():
    """Încarcă datele din Excel - Facturi Neachitate"""
    try:
        df = None
        for path in DATA_PATHS['neachitate']:
            try:
                df = pd.read_excel(path)
                break
            except FileNotFoundError:
                continue
        
        if df is None:
            raise FileNotFoundError("Nu s-a găsit fișierul")
        
        # Filtrez doar facturile reale (nu totalurile)
        df = df[df['Furnizor'].notna() & ~df['Furnizor'].str.contains('Total  ', na=False) & df['Numar'].notna()]
        
        # Calculez zilele de întârziere
        df['Data'] = pd.to_datetime(df['Data'])
        df['DataScadenta'] = pd.to_datetime(df['DataScadenta'])
        today = pd.Timestamp.now()
        df['Zile Intarziere'] = (today - df['DataScadenta']).dt.days
        df['Zile Intarziere'] = df['Zile Intarziere'].apply(lambda x: max(0, x))
        
        return df
    except:
        return pd.DataFrame({
            'Furnizor': ['Furnizor Demo 1', 'Furnizor Demo 2'],
            'Numar': ['F001', 'F002'],
            'Data': ['2024-01-01', '2024-01-02'],
            'DataScadenta': ['2024-01-31', '2024-02-01'],
            'Total': [5000, 3000],
            'Sold': [5000, 1500],
            'Zile Intarziere': [5, 0],
            'Valuta': ['EUR', 'EUR'],
            'Serie': ['Demo1', 'Demo2'],
            'PL': ['PL 01', 'PL 02']
        })

@st.cache_data
def load_neincasate():
    """Încarcă datele din Excel - Facturi Neincasate"""
    try:
        df = None
        for path in DATA_PATHS['neincasate']:
            try:
                df = pd.read_excel(path)
                break
            except FileNotFoundError:
                continue
        
        if df is None:
            raise FileNotFoundError("Nu s-a găsit fișierul")
        
        # Filtrez doar facturile reale (nu totalurile)
        df = df[df['Client'].notna() & ~df['Client'].str.contains('Total  ', na=False) & df['NumarDoc'].notna()]
        
        # Calculez zilele de întârziere
        df['Data'] = pd.to_datetime(df['Data'])
        df['DataScadenta'] = pd.to_datetime(df['DataScadenta'])
        today = pd.Timestamp.now()
        df['Zile Intarziere'] = (today - df['DataScadenta']).dt.days
        df['Zile Intarziere'] = df['Zile Intarziere'].apply(lambda x: max(0, x))
        
        return df
    except:
        return pd.DataFrame({
            'Client': ['Client Demo 1', 'Client Demo 2'],
            'NumarDoc': ['V001', 'V002'],
            'Data': ['2024-01-01', '2024-01-02'],
            'DataScadenta': ['2024-01-31', '2024-02-01'],
            'Total': [8000, 6000],
            'Sold': [8000, 3000],
            'Zile Intarziere': [10, 0],
            'Valuta': ['LEI', 'LEI'],
            'Serie': ['Demo1', 'Demo2'],
            'Agent': ['Agent Demo', 'Agent Demo']
        })
