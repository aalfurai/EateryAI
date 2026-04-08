import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.schemas.weights import Weights


# ── fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def default_weights():
    return Weights()

@pytest.fixture
def custom_weights():
    return Weights(price=0.10, calories=0.30, protein=0.60, cheap=0.10)

# ── instantiation ─────────────────────────────────────────────────────────────

def test_default_instantiation(default_weights):
    w = default_weights
    assert w.price    == 0.20
    assert w.calories == 0.40
    assert w.protein  == 0.40
    assert w.cheap    == 0.20

def test_custom_instantiation(custom_weights):
    w = custom_weights
    assert w.price    == 0.10
    assert w.calories == 0.30
    assert w.protein  == 0.60
    assert w.cheap    == 0.10

# ── validation ────────────────────────────────────────────────────────────────

def test_price_above_one_raises():
    with pytest.raises(ValueError, match="price weight"):
        Weights(price=1.5)

def test_price_below_zero_raises():
    with pytest.raises(ValueError, match="price weight"):
        Weights(price=-0.1)

def test_calories_above_one_raises():
    with pytest.raises(ValueError, match="calories weight"):
        Weights(calories=1.1)

def test_protein_above_one_raises():
    with pytest.raises(ValueError, match="protein weight"):
        Weights(protein=2.0)

def test_cheap_above_one_raises():
    with pytest.raises(ValueError, match="cheap weight"):
        Weights(cheap=1.5)

def test_zero_weights_are_valid():
    w = Weights(price=0, calories=0, protein=0, cheap=0)
    assert w.price == 0

def test_one_weights_are_valid():
    w = Weights(price=1.0, calories=1.0, protein=1.0, cheap=1.0)
    assert w.price == 1.0

# ── update ────────────────────────────────────────────────────────────────────

def test_update_single_field(default_weights):
    default_weights.update(protein=0.60)
    assert default_weights.protein == 0.60

def test_update_multiple_fields(default_weights):
    default_weights.update(price=0.30, calories=0.30, protein=0.40)
    assert default_weights.price    == 0.30
    assert default_weights.calories == 0.30
    assert default_weights.protein  == 0.40

def test_update_unknown_field_raises(default_weights):
    with pytest.raises(ValueError, match="Unknown weight field"):
        default_weights.update(unknown=0.5)

def test_update_invalid_value_raises(default_weights):
    with pytest.raises(ValueError, match="protein weight"):
        default_weights.update(protein=2.0)

# ── serialization ─────────────────────────────────────────────────────────────

def test_to_dict(default_weights):
    d = default_weights.to_dict()
    assert d['price']    == 0.20
    assert d['calories'] == 0.40
    assert d['protein']  == 0.40
    assert d['cheap']    == 0.20

def test_from_dict_full():
    data = {'price': 0.10, 'calories': 0.30, 'protein': 0.60, 'cheap': 0.10}
    w = Weights.from_dict(data)
    assert w.price   == 0.10
    assert w.protein == 0.60

def test_from_dict_uses_defaults():
    w = Weights.from_dict({})
    assert w.price    == 0.20
    assert w.calories == 0.40
    assert w.protein  == 0.40
    assert w.cheap    == 0.20

def test_round_trip(default_weights):
    restored = Weights.from_dict(default_weights.to_dict())
    assert restored.price    == default_weights.price
    assert restored.calories == default_weights.calories
    assert restored.protein  == default_weights.protein
    assert restored.cheap    == default_weights.cheap