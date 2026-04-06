import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from scripts.schemas.user import User
from scripts.schemas.constraints import Constraints
from scripts.schemas.weights import Weights


# ── fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def default_user():
    return User(
        user_id='user_123',
        name='John Doe',
        constraints=Constraints(price=14.00, calories=800, protein=20),
        weights=Weights()
    )

@pytest.fixture
def user_dict():
    return {
        'user_id': 'user_123',
        'name': 'John Doe',
        'constraints': {
            'price': 14.00,
            'calories': 800,
            'protein': 20,
            'price_tol_pct': 0.20,
            'cal_tol_pct': 0.10,
            'protein_tol_pct': 0.30,
        },
        'weights': {
            'price': 0.20,
            'calories': 0.40,
            'protein': 0.40,
            'cheap': 0.20,
        }
    }

# ── instantiation ─────────────────────────────────────────────────────────────

def test_basic_instantiation(default_user):
    assert default_user.user_id == 'user_123'
    assert default_user.name    == 'John Doe'

def test_constraints_attached(default_user):
    assert default_user.constraints.price    == 14.00
    assert default_user.constraints.calories == 800
    assert default_user.constraints.protein  == 20

def test_weights_attached(default_user):
    assert default_user.weights.price    == 0.20
    assert default_user.weights.protein  == 0.40

# ── validation ────────────────────────────────────────────────────────────────

def test_empty_user_id_raises():
    with pytest.raises(ValueError, match="user_id cannot be empty"):
        User(
            user_id='',
            name='John Doe',
            constraints=Constraints(price=14.00, calories=800, protein=20),
            weights=Weights()
        )

def test_empty_name_raises():
    with pytest.raises(ValueError, match="name cannot be empty"):
        User(
            user_id='user_123',
            name='',
            constraints=Constraints(price=14.00, calories=800, protein=20),
            weights=Weights()
        )

# ── update constraints ────────────────────────────────────────────────────────

def test_update_constraints(default_user):
    default_user.update_constraints(price=20.00)
    assert default_user.constraints.price == 20.00

def test_update_constraints_multiple(default_user):
    default_user.update_constraints(price=16.00, calories=900, protein=30)
    assert default_user.constraints.price    == 16.00
    assert default_user.constraints.calories == 900
    assert default_user.constraints.protein  == 30

def test_update_constraints_invalid_raises(default_user):
    with pytest.raises(ValueError):
        default_user.update_constraints(price=-5.00)

def test_update_constraints_unknown_field_raises(default_user):
    with pytest.raises(ValueError, match="Unknown constraint field"):
        default_user.update_constraints(unknown=99)

# ── update weights ────────────────────────────────────────────────────────────

def test_update_weights(default_user):
    default_user.update_weights(protein=0.60)
    assert default_user.weights.protein == 0.60

def test_update_weights_invalid_raises(default_user):
    with pytest.raises(ValueError):
        default_user.update_weights(protein=2.0)

def test_update_weights_unknown_field_raises(default_user):
    with pytest.raises(ValueError, match="Unknown weight field"):
        default_user.update_weights(unknown=0.5)

# ── serialization ─────────────────────────────────────────────────────────────

def test_to_dict(default_user):
    d = default_user.to_dict()
    assert d['user_id'] == 'user_123'
    assert d['name']    == 'John Doe'
    assert isinstance(d['constraints'], dict)
    assert isinstance(d['weights'], dict)
    assert d['constraints']['price']   == 14.00
    assert d['weights']['protein']     == 0.40

def test_from_dict(user_dict):
    user = User.from_dict(user_dict)
    assert user.user_id                == 'user_123'
    assert user.name                   == 'John Doe'
    assert user.constraints.price      == 14.00
    assert user.constraints.calories   == 800
    assert user.weights.protein        == 0.40

def test_from_dict_invalid_user_id_raises(user_dict):
    user_dict['user_id'] = ''
    with pytest.raises(ValueError, match="user_id cannot be empty"):
        User.from_dict(user_dict)

def test_round_trip(default_user):
    restored = User.from_dict(default_user.to_dict())
    assert restored.user_id                  == default_user.user_id
    assert restored.name                     == default_user.name
    assert restored.constraints.price        == default_user.constraints.price
    assert restored.constraints.calories     == default_user.constraints.calories
    assert restored.constraints.protein      == default_user.constraints.protein
    assert restored.weights.price            == default_user.weights.price
    assert restored.weights.protein          == default_user.weights.protein

def test_round_trip_preserves_tolerance_pcts(default_user):
    restored = User.from_dict(default_user.to_dict())
    assert restored.constraints.price_tol_pct == default_user.constraints.price_tol_pct
    assert restored.constraints.calories_tol_pct == default_user.constraints.calories_tol_pct
    assert restored.constraints.protein_tol_pct == default_user.constraints.protein_tol_pct