import math
from solver import functions as mc
from schemas import Restaurant, User, Constraints, Weights
from solver import data
from pathlib import Path
from solver.setup import setupData

# simulate user db
USERS = [User(1, "tyler")]

def select_user():
    print_header()
    print('  Select a user:\n')

    for i, u in enumerate(USERS):
        print(f'    {i+1}. {u.name}')
    print(f'    {len(USERS)+1}. Create new user\n')

    choice = prompt_int('Choose', len(USERS) + 1)

    if 1 <= choice <= len(USERS):
        selected = USERS[choice - 1]
        print(f'\n  Loaded user: {selected.name}\n')
        return selected
    else:
        return create_user()

def create_user():
    print_header()
    print('  Create a new user:\n')

    name = prompt('Name')

    print('\n  Define Constraints:')
    constraints = Constraints(
        price=prompt_float('Max price ($)', 14.00),
        calories=prompt_int('Max calories', 800),
        protein=prompt_int('Min protein (g)', 20),
    )

    print('\n  Define Weights:')
    weights = Weights(
        price=prompt_float('Weight for price (0-1)', 0.20),
        calories=prompt_float('Weight for calories (0-1)', 0.40),
        protein=prompt_float('Weight for protein (0-1)', 0.40),
    )

    new_user = User(
        user_id=f'user_{len(USERS)+1}',
        name=name,
        constraints=constraints,
        weights=weights,
    )
    USERS.append(new_user)
    print(f'\n  Created user: {new_user.name}\n')
    return new_user

def select_categories() -> set:
    print_header()
    print('  Select meal components:\n')

    # NOTE: should add option to request multiple categories
    options = [
        ('Entree',  True),
        ('Side',    True),
        ('Drink',   True),
        ('Dessert', False),
        ('Add-on',  False),
    ]

    selections = {}
    for name, default in options:
        default_str = 'y' if default else 'n'
        val = prompt(f'Include {name}? (y/n)', default_str)
        selections[name] = val.lower() == 'y'

    categories = {name for name, selected in selections.items() if selected}

    if 'Entree' not in categories:
        print('\n  ⚠  Entree is required. Adding it back.\n')
        categories.add('Entree')

    print(f'\n  Selected: {", ".join(sorted(categories))}\n')
    return categories

# Demo Display ------------------------------------

DIVIDER  = '─' * 60
DIVIDER2 = '═' * 60

def print_header():
    print(f'\n{DIVIDER2}')
    print('EATERY MEAL SOLVER  —  Demo')
    print(f'{DIVIDER2}\n')

def print_constraints(user: User):
    c = user.constraints
    w = user.weights
    print(f'  Current User: {user.name}\n')
    print('  Current constraints:')
    print(f'    Price:    ${c.price:.2f}   (±${c.price_tol_pct:.2f})')
    print(f'    Calories: {c.calories}    (±{c.calories_tol_pct})')
    print(f'    Protein:  {c.protein}g     (±{c.protein_tol_pct}g)')
    print(f'  Weights:  price={w.price}  cal={w.calories}  protein={w.protein}\n')

def print_meal(rank, meal, menu):
    print(f'  #{rank+1}  Score: {meal["score"]:.4f}')
    print(f'  {DIVIDER}')
    for item_id in meal['item_ids']:
        item = menu[item_id]
        print(f'    {item["menu_item_name"]:<40} ${item["price"]:.2f}  {item["calories"]}cal  {item["protein"]}g')
    print(f'  {DIVIDER}')
    print(f'    {"TOTAL":<40} ${meal["total_price"]:.2f}  {meal["total_cal"]}cal  {meal["total_protein"]}g')
    print(f'    Golden ratio: {meal["golden_ratio"]:.2f}\n')

def prompt(msg, default=None):
    suffix = f' [{default}]' if default is not None else ''
    val = input(f'  {msg}{suffix}: ').strip()
    return val if val else default

def prompt_float(msg, default):
    while True:
        try:
            return float(prompt(msg, default))
        except (TypeError, ValueError):
            print('Please enter a number.')

def prompt_int(msg, default):
    while True:
        try:
            return int(prompt(msg, default))
        except (TypeError, ValueError):
            print('Please enter a whole number.')

def select_seed(user: User, menu: dict) -> int:
    entrees = [v for v in menu.values() if v['category'] == 'Entree']
    print_header()
    print_constraints(user)
    print('  Chick-fil-A entrees:\n')
    for i, item in enumerate(entrees):
        print(f'    {i+1:>3}.  {item["menu_item_name"]:<45} ${item["price"]:.2f}  {item["calories"]}cal  {item["protein"]}g')
    print()
    choice = prompt_int('Select an entree (number)', 1)
    choice = max(1, min(choice, len(entrees)))
    seed = entrees[choice - 1]
    print(f'\nSeed: {seed["menu_item_name"]}\n')
    return seed['index']

def run_solver(user: User, seed_id: int, restaurant: Restaurant, categories: set):
    print_header()
    print_constraints(user)
    print('  Building meals...', flush=True)
    results = mc.build_meal(user, seed_id, categories, restaurant.menu,
                            entree_combos=restaurant.entree_combos,
                            sides=restaurant.sides, drinks=restaurant.drinks)
    print(f'  done - {len(results)} candidates\n')

    if not results:
        print('No meals found within your constraints. Try adjusting price or calories.\n')
        return

    ranked = mc.score_and_rank_meals(user, results)
    top    = ranked[:3]

    print(f'  Top {len(top)} meals:\n')
    for i, meal in enumerate(top):
        print_meal(i, meal, restaurant.menu)

def main():
    print_header()
    while True:
        chosen_restaurant = prompt("Enter Restaurant Name", "Chick-fil-a")
        restaurant = data.enter_restaurant(chosen_restaurant)
        if restaurant.item_count > 0:
            break
        print(f'\n  No data found for "{chosen_restaurant}". Please try again.\n')

    while True:
        selected_user = select_user()
        categories = select_categories()
        seed_id = select_seed(selected_user, restaurant.menu)
        run_solver(selected_user, seed_id, restaurant, categories)

        if prompt('Build another meal? (y/n)', 'y').lower() != 'y':
            print('\n  Thanks for using Eatery!\n')
            break

if __name__ == '__main__':
    if not Path('../restaurants_data_manual_recat.json').exists():
        setupData()
    main()
