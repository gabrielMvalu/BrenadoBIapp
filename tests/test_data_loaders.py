import sys
from pathlib import Path

import pandas as pd

# Ensure the project root is on the Python path when tests are executed
sys.path.append(str(Path(__file__).resolve().parents[1]))

from utils.data_loaders import load_balanta_la_data, load_balanta_perioada


def test_load_balanta_la_data_returns_placeholder(monkeypatch):
    def mock_read_excel(*args, **kwargs):
        raise FileNotFoundError("missing file")

    monkeypatch.setattr(pd, "read_excel", mock_read_excel)

    df = load_balanta_la_data()
    expected = pd.DataFrame({
        'DenumireGest': ['Demo Gestiune'],
        'Denumire': ['Produs Demo'],
        'Stoc final': [100],
        'ValoareStocFinal': [5000]
    })
    pd.testing.assert_frame_equal(df, expected)


def test_load_balanta_perioada_returns_placeholder(monkeypatch):
    def mock_read_excel(*args, **kwargs):
        raise FileNotFoundError("missing file")

    monkeypatch.setattr(pd, "read_excel", mock_read_excel)

    df = load_balanta_perioada()
    expected = pd.DataFrame({
        'Denumire gestiune': ['Demo Gestiune'],
        'Denumire': ['Produs Demo'],
        'Stoc final': [100],
        'ZileVechime': [10]
    })
    pd.testing.assert_frame_equal(df, expected)
