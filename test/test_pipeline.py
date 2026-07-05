import sys
from pathlib import Path

# Projekt-Wurzel zum Suchpfad hinzufügen, damit "engine" gefunden wird
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest
from engine.scoring_engine import calculate_priority
from engine.validator import validate_assets, Asset


# --- Testdaten: bewusst klein und kontrolliert ---

CRITERIA = [
    {"name": "damage", "column_name": "main_damage", "weight": 0.6, "max": 10,
     "mapping": {4: 10, 3: 6, 2: 4, 1: 2}},
    {"name": "criticality", "column_name": "facility", "weight": 0.4, "max": 10},
]


def make_asset(values):
    """Baut ein gültiges Asset-Objekt mit gegebenen Werten."""
    return Asset(
        id="T-001",
        name="Testcell",
        geometry={"x": 36.2, "y": 49.9},
        values=values,
    )


# --- Tests fürs Scoring ---

def test_score_is_normalized_between_0_and_1():
    asset = make_asset({"damage": 10, "criticality": 10})
    result = calculate_priority([asset], CRITERIA)
    assert result[0].score == 1.0  # maximaler Schaden + maximale Kritikalität


def test_score_minimum():
    asset = make_asset({"damage": 0, "criticality": 0})
    result = calculate_priority([asset], CRITERIA)
    assert result[0].score == 0.0


def test_score_weighting_is_applied():
    # damage=10 (Gewicht 0.6), criticality=0 (Gewicht 0.4)
    # erwartet: (10*0.6 + 0*0.4) / (10*0.6 + 10*0.4) = 6/10 = 0.6
    asset = make_asset({"damage": 10, "criticality": 0})
    result = calculate_priority([asset], CRITERIA)
    assert result[0].score == pytest.approx(0.6)


# --- Tests für den Validator ---

def test_valid_asset_passes():
    data = [{
        "id": "A1", "name": "ok",
        "geometry": {"x": 1.0, "y": 2.0},
        "values": {"damage": 5, "criticality": 3},
    }]
    result = validate_assets(data, CRITERIA)
    assert len(result) == 1


def test_negative_value_is_rejected():
    data = [{
        "id": "A2", "name": "bad",
        "geometry": {"x": 1.0, "y": 2.0},
        "values": {"damage": -5, "criticality": 3},
    }]
    result = validate_assets(data, CRITERIA)
    assert len(result) == 0  # wird wegen negativem Wert abgelehnt


def test_missing_criterion_is_rejected():
    data = [{
        "id": "A3", "name": "incomplete",
        "geometry": {"x": 1.0, "y": 2.0},
        "values": {"damage": 5},  # criticality fehlt
    }]
    result = validate_assets(data, CRITERIA)
    assert len(result) == 0


def test_empty_list_returns_empty():
    result = validate_assets([], CRITERIA)
    assert result == []
