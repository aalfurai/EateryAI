import math
import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.schemas.constraints import Constraints


# ── fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def default_constraints():
    return Constraints(price=14.00, calories=800, protein=20)

@pytest.fixture
def custom_constraints():
    return Constraints(price=20.00, calories=1000, protein=50,
                       price_tol_pct=0.15, calories_tol_pct=0.05, protein_tol_pct=0.25)

# ── instantiation ─────────────────────────────────────────────────────────────

def test_basic_instantiation(default_constraints):
    c = default_constraints
    assert c.price == 14.00
    assert c.calories == 800
    assert c.protein == 20

def test_default_tolerance_percentages(default_constraints):
    c = default_constraints
    assert c.price_tol_pct == 0.20
    assert c.calories_tol_pct == 0.10
    assert c.protein_tol_pct == 0.30

def test_custom_tolerance_percentages(custom_constraints):
    c = custom_constraints
    assert c.price_tol_pct == 0.15
    assert c.calories_tol_pct == 0.05
    assert c.protein_tol_pct == 0.25

# ── tolerance properties ──────────────────────────────────────────────────────

def test_price_tol(default_constraints):
    assert default_constraints.get_price == round(14.00 * 0.20, 2)

def test_cal_tol(default_constraints):
    assert default_constraints.get_calories == math.ceil(800 * 0.10)

def test_protein_tol(default_constraints):
    assert default_constraints.get_protein == math.ceil(20 * 0.30)

def test_tolerances_update_when_price_changes(default_constraints):
    default_constraints.update(price=20.00)
    assert default_constraints.get_price == round(20.00 * 0.20, 2)

# ── validation ────────────────────────────────────────────────────────────────

def test_negative_price_raises():
    with pytest.raises(ValueError, match="Price must be positive"):
        Constraints(price=-1.00, calories=800, protein=20)

def test_zero_price_raises():
    with pytest.raises(ValueError, match="Price must be positive"):
        Constraints(price=0, calories=800, protein=20)

def test_negative_calories_raises():
    with pytest.raises(ValueError, match="Calories must be positive"):
        Constraints(price=14.00, calories=-100, protein=20)

def test_negative_protein_raises():
    with pytest.raises(ValueError, match="Protein must be positive"):
        Constraints(price=14.00, calories=800, protein=-5)

def test_price_tol_pct_out_of_range_raises():
    with pytest.raises(ValueError, match="Price tolerance"):
        Constraints(price=14.00, calories=800, protein=20, price_tol_pct=1.5)

def test_price_tol_pct_zero_raises():
    with pytest.raises(ValueError, match="Price tolerance"):
        Constraints(price=14.00, calories=800, protein=20, price_tol_pct=0)

# ── update ────────────────────────────────────────────────────────────────────

def test_update_single_field(default_constraints):
    default_constraints.update(price=20.00)
    assert default_constraints.price == 20.00

def test_update_multiple_fields(default_constraints):
    default_constraints.update(price=16.00, calories=900, protein=30)
    assert default_constraints.price == 16.00
    assert default_constraints.calories == 900
    assert default_constraints.protein == 30

def test_update_unknown_field_raises(default_constraints):
    with pytest.raises(ValueError, match="Unknown constraint field"):
        default_constraints.update(unknown_field=99)

def test_update_invalid_value_raises(default_constraints):
    with pytest.raises(ValueError, match="Price must be positive"):
        default_constraints.update(price=-5.00)

# ── serialization ─────────────────────────────────────────────────────────────

def test_to_dict(default_constraints):
    d = default_constraints.to_dict()
    assert d['price'] == 14.00
    assert d['calories'] == 800
    assert d['protein'] == 20
    assert d['price_tol_pct'] == 0.20
    assert d['calories_tol_pct'] == 0.10
    assert d['protein_tol_pct'] == 0.30

def test_from_dict_full():
    data = {
        'price': 14.00, 'calories': 800, 'protein': 20,
        'price_tol_pct': 0.15, 'calories_tol_pct': 0.05, 'protein_tol_pct': 0.25
    }
    c = Constraints.from_dict(data)
    assert c.price == 14.00
    assert c.price_tol_pct == 0.15

def test_from_dict_uses_defaults_for_tolerances():
    data = {'price': 14.00, 'calories': 800, 'protein': 20}
    c = Constraints.from_dict(data)
    assert c.price_tol_pct == 0.20
    assert c.calories_tol_pct == 0.10
    assert c.protein_tol_pct == 0.30

def test_round_trip(default_constraints):
    restored = Constraints.from_dict(default_constraints.to_dict())
    assert restored.price    == default_constraints.price
    assert restored.calories == default_constraints.calories
    assert restored.protein  == default_constraints.protein