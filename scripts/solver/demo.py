import json
import math
import itertools
import os
import mc_functions as mc
import data as data

def sync_globals():
    """To sync globals between files, better fix later"""
    mc.USER_PRICE   = USER_PRICE
    mc.USER_CAL     = USER_CAL
    mc.USER_PROTEIN = USER_PROTEIN
    mc.PRICE_TOL    = PRICE_TOL
    mc.CAL_TOL      = CAL_TOL
    mc.PROTEIN_TOL  = PROTEIN_TOL
    mc.W_PRICE      = W_PRICE
    mc.W_CAL        = W_CAL
    mc.W_PROTEIN    = W_PROTEIN

def clear_screen():
    """Clears terminal screen"""
    os.system('clear')

# GLOBAL DUMMY DATA

USER_PROFILES = {
    'bodybuilder': {
        'label':       'Bodybuilder  (Price: 10% Calories: 30%  Protein: 60%)',
        'constraints': {'price': 14.00, 'calories': 800, 'protein': 40},
        'weights':     {'W_PRICE': 0.10, 'W_CAL': 0.30, 'W_PROTEIN': 0.60},
    },
    'hungrystudent': {
        'label':       'Hungry Student  (Price: 60% Calories: 30%  Protein: 10%)',
        'constraints': {'price': 10.00, 'calories': 900, 'protein': 20},
        'weights':     {'W_PRICE': 0.60, 'W_CAL': 0.30, 'W_PROTEIN': 0.10},
    },
}

REQUIRED_CATEGORIES = {'Entree', 'Side', 'Drink'}

USER_PRICE   = 14.00
USER_CAL     = 800
USER_PROTEIN = 20
PRICE_TOL    = round(USER_PRICE * 0.20, 2)
CAL_TOL      = math.ceil(USER_CAL * 0.10)
PROTEIN_TOL  = math.ceil(USER_PROTEIN * 0.30)
W_PRICE      = 0.20
W_CAL        = 0.40
W_PROTEIN    = 0.40

def update_tolerances():
    global PRICE_TOL, CAL_TOL, PROTEIN_TOL
    PRICE_TOL   = round(USER_PRICE * 0.20, 2)
    CAL_TOL     = math.ceil(USER_CAL * 0.10)
    PROTEIN_TOL = math.ceil(USER_PROTEIN * 0.30)

# Demo Display ------------------------------------

DIVIDER  = '─' * 60
DIVIDER2 = '═' * 60

def print_header():
    print(f'\n{DIVIDER2}')
    print('EATERY MEAL SOLVER  —  Chick-fil-A Demo')
    print(f'{DIVIDER2}\n')

def print_constraints():
    print('  Current constraints:')
    print(f'    Price:    ${USER_PRICE:.2f}   (±${PRICE_TOL:.2f})')
    print(f'    Calories: {USER_CAL}    (±{CAL_TOL})')
    print(f'    Protein:  {USER_PROTEIN}g     (±{PROTEIN_TOL}g)')
    print(f'  Weights:  price={W_PRICE}  cal={W_CAL}  protein={W_PROTEIN}\n')

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

def select_profile():
    global USER_PRICE, USER_CAL, USER_PROTEIN, W_PRICE, W_CAL, W_PROTEIN
    clear_screen()
    print_header()
    print('  Select a user profile:\n')
    keys = list(USER_PROFILES.keys())
    for i, k in enumerate(keys):
        print(f'    {i+1}. {USER_PROFILES[k]["label"]}')

    choice = prompt_int('Choose', 1)
    if 1 <= choice <= len(keys):
        profile = USER_PROFILES[keys[choice - 1]]
        USER_PRICE   = profile['constraints']['price']
        USER_CAL     = profile['constraints']['calories']
        USER_PROTEIN = profile['constraints']['protein']
        W_PRICE      = profile['weights']['W_PRICE']
        W_CAL        = profile['weights']['W_CAL']
        W_PROTEIN    = profile['weights']['W_PROTEIN']
        print(f'\nLoaded profile: {profile["label"]}\n')
    else:
        print()
    update_tolerances()
    sync_globals()

def input_constraints():
    global USER_PRICE, USER_CAL, USER_PROTEIN
    clear_screen()
    print_header()
    print_constraints()
    print('  Enter your constraints:\n')
    USER_PRICE   = prompt_float('Max price ($)',   USER_PRICE)
    USER_CAL     = prompt_int  ('Max calories',    USER_CAL)
    USER_PROTEIN = prompt_int  ('Min protein (g)', USER_PROTEIN)
    update_tolerances()
    sync_globals()
    print()

def select_seed(menu: dict) -> int:
    entrees = [v for v in menu.values() if v['meal_category'] == 'Entree']
    clear_screen()
    print_header()
    print_constraints()
    print('  Chick-fil-A entrees:\n')
    for i, item in enumerate(entrees):
        print(f'    {i+1:>3}.  {item["menu_item_name"]:<45} ${item["price"]:.2f}  {item["calories"]}cal  {item["protein"]}g')
    print()
    choice = prompt_int('Select an entree (number)', 1)
    choice = max(1, min(choice, len(entrees)))
    seed = entrees[choice - 1]
    print(f'\nSeed: {seed["menu_item_name"]}\n')
    return seed['index']

def run_solver(seed_id, menu, entree_combos, sides, drinks):
    clear_screen()
    print_header()
    print_constraints()
    print('  Building meals...', end='', flush=True)
    results = mc.build_meal(seed_id, REQUIRED_CATEGORIES, menu,
                            entree_combos=entree_combos,
                            sides=sides, drinks=drinks)
    print(f' done - {len(results)} candidates\n')

    if not results:
        print('No meals found within your constraints. Try adjusting price or calories.\n')
        return

    ranked = mc.score_and_rank_meals(results, menu)
    top    = ranked[:3]

    print(f'  Top {len(top)} meals:\n')
    for i, meal in enumerate(top):
        print_meal(i, meal, menu)

def main():
    print_header()

    # hard coded path for demo, will add db access later
    path = "EateryAI/data/restaurants.menu_item_variations.json"
    chosen_restaurant = "Chick-fil-A"
    print(f'\n  Loading {chosen_restaurant.lower()} data...', end='', flush=True)
    try:
        menu = data.load_restaurant_data(path, chosen_restaurant)
    except FileNotFoundError:
        print(f'\n  x  File not found: {path}')
        return

    entrees, sides, drinks, desserts = data.build_category_lists(menu)
    print(f' {len(menu)} items loaded')
    print(f'  Computing entree combos...', end='', flush=True)
    entree_combos = data.calculate_entree_combos(entrees)
    print(f' {len(entree_combos)} combos\n')

    while True:
        select_profile()
        input_constraints()
        seed_id = select_seed(menu)
        run_solver(seed_id, menu, entree_combos, sides, drinks)

        if prompt('Build another meal? (y/n)', 'y').lower() != 'y':
            clear_screen()
            print('\n  Thanks for using Eatery!\n')
            break

if __name__ == '__main__':
    main()
