"""
Edge case tests for the meal combo sandbox functions.
Run from the sandbox directory: python3 run_edge_case_tests.py
"""
import math, copy, itertools, traceback
import numpy as np
import pandas as pd
from dataclasses import dataclass

# ── classes (replicated from notebook) ───────────────────────────────────────

@dataclass
class UserConstraints:
    price: float
    calories: int
    protein: int

@dataclass
class UserPreferences2:
    w_price: float
    w_calories: float
    w_protein: float
    w_fiber: float
    w_sugar: float
    w_sodium: float
    w_drink_cal: float
    w_addon_cal: float

# ── constants ─────────────────────────────────────────────────────────────────

MAX_PRICE    = 100.0
MAX_CALORIES = 3000
MAX_PROTEIN  = 150

# ── functions (fixed versions from notebook cells 46 + 115) ──────────────────

def get_entree_combos(seed_id, df_entree_combos, is_entree):
    if is_entree:
        mask = df_entree_combos['entree_ids'].apply(lambda ids: seed_id in ids)
        return df_entree_combos[mask]
    return df_entree_combos

def get_cand_items(seed_id, category,
                   df_entree_combos=None, df_sides=None, df_drinks=None,
                   df_desserts=None, df_addons=None, is_entree=False):
    if category == 'Entree':
        return get_entree_combos(seed_id, df_entree_combos, is_entree)
    elif category == 'Side':
        return df_sides   if df_sides   is not None else pd.DataFrame()
    elif category == 'Drink':
        return df_drinks  if df_drinks  is not None else pd.DataFrame()
    elif category == 'Dessert':
        return df_desserts if df_desserts is not None else pd.DataFrame()
    elif category == 'Add-on':
        return df_addons  if df_addons  is not None else pd.DataFrame()
    return pd.DataFrame()

def calculate_expanded_entree_combos(entrees, max_count=2):
    entree_combos = []
    combo_id = 1
    for k in range(1, max_count + 1):
        for combo in itertools.combinations_with_replacement(entrees, k):
            total_price       = sum(item['price']                     for item in combo)
            total_calories    = sum(item['calories']                  for item in combo)
            total_protein     = sum(item['protein']                   for item in combo)
            total_fiber       = sum((item['dietary_fiber']       or 0) for item in combo)
            total_sugars      = sum((item['sugars']              or 0) for item in combo)
            total_sodium      = sum((item['sodium']              or 0) for item in combo)
            total_cholesterol = sum((item['cholesterol']         or 0) for item in combo)
            total_carbs       = sum((item['total_carbohydrates'] or 0) for item in combo)
            total_potassium   = sum((item['potassium']           or 0) for item in combo)
            total_fat         = sum((item['total_fat']           or 0) for item in combo)

            if total_price    > MAX_PRICE:    continue
            if total_calories > MAX_CALORIES: continue
            if total_protein  > MAX_PROTEIN:  continue

            entree_combos.append({
                "combo_id": combo_id,
                "entree_ids": tuple(item['index'] for item in combo),
                "entree_names": tuple(item['menu_item_name'] for item in combo),
                "n_entrees": k,
                "price": total_price, "calories": total_calories, "protein": total_protein,
                "dietary_fiber": total_fiber, "sugars": total_sugars, "sodium": total_sodium,
                "cholesterol": total_cholesterol, "total_carbohydrates": total_carbs,
                "potassium": total_potassium, "total_fat": total_fat,
                "serving_size_per_item": tuple(item['serving_size'] for item in combo),
            })
            combo_id += 1
    return pd.DataFrame(entree_combos)

def intermediate_prune_3(meals, prefs, constraints, k=100):
    scores = []
    for meal in meals:
        price_excess    = max(0, meal['total_price'] - constraints.price)    / constraints.price
        cal_excess      = max(0, meal['total_cal']   - constraints.calories) / constraints.calories
        protein_deficit = max(0, constraints.protein - meal['total_protein']) / constraints.protein
        drink_penalty   = meal['drink_cal']  / constraints.calories
        addon_penalty   = meal['addon_cal']  / constraints.calories
        golden_ratio    = (meal['total_protein'] * 10) / max(meal['total_cal'], 1)
        score = (
            prefs.w_price    * price_excess    +
            prefs.w_calories * cal_excess      +
            prefs.w_protein  * protein_deficit +
            prefs.w_drink_cal * drink_penalty  +
            prefs.w_addon_cal * addon_penalty  -
            prefs.w_protein  * golden_ratio * 0.5
        )
        scores.append(score)
    scores = np.array(scores)
    top_k  = scores.argsort()[:k]
    return [meals[i] for i in top_k], [scores[i] for i in top_k]

def precompute_similarity(meals):
    n         = len(meals)
    sim_matrix = np.zeros((n, n))
    item_sets  = [set(m['item_ids']) for m in meals]
    sizes      = [len(s) for s in item_sets]
    for i in range(n):
        for j in range(i + 1, n):
            inter = len(item_sets[i] & item_sets[j])
            union = sizes[i] + sizes[j] - inter
            sim_matrix[i, j] = inter / union if union > 0 else 0
            sim_matrix[j, i] = sim_matrix[i, j]
    return sim_matrix

def diversity_prune(meals, scores, sim_matrix, k=100, lambda_div=0.3):
    selected   = []
    candidates = list(range(len(meals)))
    for _ in range(k):
        best = None; best_score = float('inf')
        for i in candidates:
            sims = [sim_matrix[i][j] for j in selected] if selected else [0]
            penalty = 0 if not selected or (max(sims) - min(sims) < np.finfo(np.float64).eps) else max(sims)
            total = scores[i] + lambda_div * penalty
            if total < best_score:
                best = i; best_score = total
        if best is None: break
        selected.append(best); candidates.remove(best)
    return [meals[i] for i in selected]

CATEGORY_ORDER = ["Entree", "Side", "Drink", "Add-on", "Dessert"]

def build_meal_4(seed_id, required_categories, df_restaurant, prefs, constraints,
                 df_entree_combos=None, df_sides=None, df_drinks=None,
                 df_desserts=None, df_addons=None, build_full=True):
    PRICE_TOL = round(constraints.price * 0.15, 2)
    CAL_TOL   = math.ceil(constraints.calories * 0.10)
    current_meals = []

    if seed_id is None:
        current_meals.append({
            'item_ids': [], 'Entree_ids': [], 'Side_ids': [], 'Drink_ids': [],
            'Add-on_ids': [], 'Dessert_ids': [],
            'total_price': 0.0, 'total_cal': 0, 'total_protein': 0,
            'total_fiber': 0, 'total_sugars': 0, 'total_sodium': 0,
            'total_cholesterol': 0, 'total_carbohydrates': 0,
            'total_potassium': 0, 'total_fat': 0,
            'filled_categories': set(), 'drink_cal': 0, 'addon_cal': 0,
        })
        is_entree = False
    else:
        seed_item = df_restaurant.loc[seed_id].to_dict()
        category  = seed_item.get('meal_category')
        is_entree = (category == 'Entree')
        is_drink  = (category == 'Drink')
        is_addon  = (category == 'Add-on')

        if is_entree and build_full:
            for _, combo in get_entree_combos(seed_id, df_entree_combos, is_entree).iterrows():
                current_meals.append({
                    'item_ids': list(combo['entree_ids']), 'Entree_ids': list(combo['entree_ids']),
                    'Side_ids': [], 'Drink_ids': [], 'Add-on_ids': [], 'Dessert_ids': [],
                    'total_price':         combo['price'],
                    'total_cal':           combo['calories'],
                    'total_protein':       combo['protein'],
                    'total_fiber':         combo['dietary_fiber'],
                    'total_sugars':        combo['sugars'],
                    'total_sodium':        combo['sodium'],
                    'total_cholesterol':   combo['cholesterol'],
                    'total_carbohydrates': combo['total_carbohydrates'],
                    'total_potassium':     combo['potassium'],
                    'total_fat':           combo['total_fat'],
                    'filled_categories': {'Entree'}, 'drink_cal': 0, 'addon_cal': 0,
                })
        else:
            ms = {
                'item_ids': [seed_id], 'Entree_ids': [], 'Side_ids': [],
                'Drink_ids': [], 'Add-on_ids': [], 'Dessert_ids': [],
                'total_price':         seed_item.get('price') or 0.0,
                'total_cal':           seed_item.get('calories') or 0,
                'total_protein':       seed_item.get('protein') or 0,
                'total_fiber':         seed_item.get('dietary_fiber') or 0,
                'total_sugars':        seed_item.get('sugars') or 0,
                'total_sodium':        seed_item.get('sodium') or 0,
                'total_cholesterol':   seed_item.get('cholesterol') or 0,
                'total_carbohydrates': seed_item.get('total_carbohydrates') or 0,
                'total_potassium':     seed_item.get('potassium') or 0,
                'total_fat':           seed_item.get('total_fat') or 0,
                'filled_categories': {category}, 'drink_cal': 0, 'addon_cal': 0,
            }
            ms[f"{category}_ids"].append(seed_id)
            if is_drink:  ms['drink_cal'] = seed_item.get('calories') or 0
            elif is_addon: ms['addon_cal'] = seed_item.get('calories') or 0
            current_meals.append(ms)

    if not current_meals:
        return []

    filled = current_meals[0]['filled_categories']
    ordered_missing = [c for c in CATEGORY_ORDER if c in required_categories and c not in filled]

    for category in ordered_missing:
        new_meals = []
        for meal in current_meals:
            cand_items = get_cand_items(seed_id, category, df_entree_combos,
                                        df_sides, df_drinks, df_desserts, df_addons, is_entree)
            if cand_items.empty:
                continue
            cand_items = cand_items[
                (meal['total_price'] + cand_items['price'] <= constraints.price + PRICE_TOL) &
                (meal['total_cal']   + cand_items['calories'] <= constraints.calories + CAL_TOL)
            ]
            for _, item in cand_items.iterrows():
                nm = copy.deepcopy(meal)
                if category == 'Entree':
                    nm['item_ids'].extend(item['entree_ids'])
                    nm['Entree_ids'].extend(item['entree_ids'])
                else:
                    nm['item_ids'].append(item['index'])
                    nm[f"{category}_ids"].append(item['index'])
                if category == 'Drink':  nm['drink_cal'] += item['calories']
                elif category == 'Add-on': nm['addon_cal'] += item['calories']
                nm['total_price']         += item['price']
                nm['total_cal']           += item['calories']
                nm['total_protein']       += item['protein']
                nm['total_fiber']         += (item['dietary_fiber'] or 0)
                nm['total_sugars']        += (item['sugars'] or 0)
                nm['total_sodium']        += (item['sodium'] or 0)
                nm['total_cholesterol']   += (item['cholesterol'] or 0)
                nm['total_carbohydrates'] += (item['total_carbohydrates'] or 0)
                nm['total_potassium']     += (item['potassium'] or 0)
                nm['total_fat']           += (item['total_fat'] or 0)
                nm['filled_categories'].add(category)
                nm['total_price'] = round(nm['total_price'], 2)
                new_meals.append(nm)
        if new_meals:
            top_k, scores = intermediate_prune_3(new_meals, prefs, constraints, k=200)
            current_meals = diversity_prune(top_k, scores, precompute_similarity(top_k))
    return current_meals

def results_to_df(meal_results):
    if not meal_results:
        return pd.DataFrame()
    df = pd.DataFrame(meal_results)
    df['golden_ratio'] = (df['total_protein'] * 10) / np.maximum(df['total_cal'], 1)
    return df

def score_and_rank_meals_expanded(df_candidate_meals, constraints, weights, k=50, lambda_div=0.3):
    if df_candidate_meals.empty:
        return df_candidate_meals

    df_candidate_meals['price_excess']    = (df_candidate_meals['total_price'] - constraints.price).clip(lower=0) / constraints.price
    df_candidate_meals['cal_excess']      = (df_candidate_meals['total_cal']   - constraints.calories).clip(lower=0) / constraints.calories
    df_candidate_meals['protein_deficit'] = (constraints.protein - df_candidate_meals['total_protein']).clip(lower=0) / constraints.protein
    df_candidate_meals['drink_cal_penalty'] = df_candidate_meals['drink_cal'] / constraints.calories
    df_candidate_meals['addon_cal_penalty'] = df_candidate_meals['addon_cal'] / constraints.calories

    for col, norm_col in [('total_fiber','fiber_norm'),('total_sugars','sugars_norm'),('total_sodium','sodium_norm')]:
        mn, mx = df_candidate_meals[col].min(), df_candidate_meals[col].max()
        df_candidate_meals[norm_col] = 0.5 if mx - mn < np.finfo(np.float64).eps else (df_candidate_meals[col] - mn) / (mx - mn)

    df_candidate_meals['score'] = (
        weights.w_protein   * df_candidate_meals['protein_deficit']  +
        weights.w_calories  * df_candidate_meals['cal_excess']       +
        weights.w_price     * df_candidate_meals['price_excess']     -
        weights.w_fiber     * df_candidate_meals['fiber_norm']       +
        weights.w_sugar     * df_candidate_meals['sugars_norm']      +
        weights.w_sodium    * df_candidate_meals['sodium_norm']      +
        weights.w_drink_cal * df_candidate_meals['drink_cal_penalty'] +
        weights.w_addon_cal * df_candidate_meals['addon_cal_penalty'] -
        weights.w_protein   * df_candidate_meals['golden_ratio']
    )

    df_sorted  = df_candidate_meals.sort_values('score')
    indices    = list(df_sorted.index)
    item_sets  = {idx: set(df_sorted.loc[idx, 'item_ids']) for idx in indices}
    selected   = []
    candidates = indices.copy()

    while len(selected) < k and candidates:
        best_idx = None; best_score = float('inf')
        for idx in candidates:
            base = df_sorted.loc[idx, 'score']
            penalty = 0 if not selected else max(
                len(item_sets[idx] & item_sets[s]) / len(item_sets[idx] | item_sets[s])
                if (item_sets[idx] | item_sets[s]) else 0
                for s in selected
            )
            total = base + lambda_div * penalty
            if total < best_score:
                best_score = total; best_idx = idx
        if best_idx is None: break
        selected.append(best_idx); candidates.remove(best_idx)

    return df_sorted.loc[selected]

# ── test data ─────────────────────────────────────────────────────────────────

def make_item(index, name, price, calories, protein, category,
              dietary_fiber=5.0, sugars=3.0, sodium=400.0,
              cholesterol=50.0, total_carbohydrates=30.0,
              potassium=200.0, total_fat=10.0, serving_size="1 serving"):
    return {"index": index, "menu_item_name": name, "price": price,
            "calories": calories, "protein": protein, "meal_category": category,
            "dietary_fiber": dietary_fiber, "sugars": sugars, "sodium": sodium,
            "cholesterol": cholesterol, "total_carbohydrates": total_carbohydrates,
            "potassium": potassium, "total_fat": total_fat, "serving_size": serving_size}

# Keep 'index' as a column with pandas default integer index so both
# df.loc[0] and item['index'] work inside build_meal_4
items = [
    make_item(0, "Chicken Sandwich", 5.99, 440, 28, "Entree"),
    make_item(1, "Grilled Nuggets",  6.50, 370, 45, "Entree"),
    make_item(2, "Waffle Fries",     3.09, 420,  6, "Side"),
    make_item(3, "Water",            0.00,   0,  0, "Drink"),
]
df_test   = pd.DataFrame(items)
df_sides  = df_test[df_test["meal_category"] == "Side"].copy()
df_drinks = df_test[df_test["meal_category"] == "Drink"].copy()

entrees_dict = [items[0], items[1]]
real_combos  = calculate_expanded_entree_combos(entrees_dict)

test_constraints = UserConstraints(price=12.0, calories=900, protein=30)
test_prefs = UserPreferences2(
    w_price=0.10, w_calories=0.15, w_protein=0.55,
    w_fiber=0.07, w_sugar=0.05, w_sodium=0.03,
    w_drink_cal=0.03, w_addon_cal=0.02,
)

# ── run tests ─────────────────────────────────────────────────────────────────

PASS = 0; FAIL = 0

def report(name, passed, detail=""):
    global PASS, FAIL
    if passed: PASS += 1
    else: FAIL += 1
    print(f"  [{'PASS' if passed else 'FAIL'}] {name}" + (f": {detail}" if detail else ""))

print("=" * 60)
print("EDGE CASE TESTS")
print("=" * 60)

# ── TEST 1: empty entree combos ───────────────────────────────────────────────
print("\nTEST 1: Empty entree combos (seed entree has no matching combos)")
empty_combos = pd.DataFrame(columns=["combo_id","entree_ids","entree_names","n_entrees",
                                      "price","calories","protein","dietary_fiber","sugars",
                                      "sodium","cholesterol","total_carbohydrates","potassium",
                                      "total_fat","serving_size_per_item"])
try:
    result = build_meal_4(seed_id=0, required_categories={"Entree","Side"},
                          df_restaurant=df_test, prefs=test_prefs, constraints=test_constraints,
                          df_entree_combos=empty_combos, df_sides=df_sides)
    report("returns [] without crash", isinstance(result, list), f"got {len(result)} meals")
except Exception as e:
    report("returns [] without crash", False, f"{type(e).__name__}: {e}")

# ── TEST 2: required category DataFrame is None ───────────────────────────────
print("\nTEST 2: Required category whose DataFrame arg is None")
try:
    result = build_meal_4(seed_id=0, required_categories={"Entree","Side"},
                          df_restaurant=df_test, prefs=test_prefs, constraints=test_constraints,
                          df_entree_combos=real_combos, df_sides=None)
    report("df_sides=None doesn't crash", True, f"got {len(result)} meals")
except Exception as e:
    report("df_sides=None doesn't crash", False, f"{type(e).__name__}: {e}")

# ── TEST 3: seed item has None nutrition field ────────────────────────────────
print("\nTEST 3: Seed item has dietary_fiber=None")
bad_items = [
    make_item(0, "Chicken Sandwich", 5.99, 440, 28, "Entree"),
    make_item(1, "Waffle Fries",     3.09, 420,  6, "Side"),
]
bad_items[0]["dietary_fiber"] = None
df_bad       = pd.DataFrame(bad_items)
df_bad_sides = df_bad[df_bad["meal_category"] == "Side"].copy()
bad_combos   = calculate_expanded_entree_combos([bad_items[0]])
try:
    result = build_meal_4(seed_id=0, required_categories={"Entree","Side"},
                          df_restaurant=df_bad, prefs=test_prefs, constraints=test_constraints,
                          df_entree_combos=bad_combos, df_sides=df_bad_sides)
    report("dietary_fiber=None doesn't crash", True, f"got {len(result)} meals")
except Exception as e:
    report("dietary_fiber=None doesn't crash", False, f"{type(e).__name__}: {e}")
    traceback.print_exc()

# ── TEST 4: constraints too tight ─────────────────────────────────────────────
print("\nTEST 4: Constraints too tight, no candidates survive")
tight = UserConstraints(price=0.01, calories=1, protein=30)
try:
    result = build_meal_4(seed_id=0, required_categories={"Entree","Side","Drink"},
                          df_restaurant=df_test, prefs=test_prefs, constraints=tight,
                          df_entree_combos=real_combos, df_sides=df_sides, df_drinks=df_drinks)
    df_r   = results_to_df(result)
    scored = score_and_rank_meals_expanded(df_r, tight, test_prefs)
    report("empty results handled gracefully", True, f"got {len(scored)} meals")
except Exception as e:
    report("empty results handled gracefully", False, f"{type(e).__name__}: {e}")
    traceback.print_exc()

# ── TEST 5: MAX_PROTEIN filter ────────────────────────────────────────────────
print("\nTEST 5: calculate_expanded_entree_combos respects MAX_PROTEIN")
# single item = 100g protein (passes), pair = 200g (exceeds MAX_PROTEIN=150, filtered)
high_protein = make_item(0, "Protein Pack", 5.00, 300, 100, "Entree")
combos = calculate_expanded_entree_combos([high_protein], max_count=2)
if combos.empty:
    report("MAX_PROTEIN blocks over-limit combos", True,
           "200g pair filtered, result is empty DataFrame")
else:
    over = combos[combos["protein"] > MAX_PROTEIN]
    report("MAX_PROTEIN blocks over-limit combos", len(over) == 0,
           f"{len(over)} combos still exceed limit" if len(over) > 0 else
           f"all {len(combos)} combos within limit")

# ── TEST 6: protein logic consistency ─────────────────────────────────────────
print("\nTEST 6: Protein logic — prune and scorer both favor high-protein meals")
high_p = {"total_price":8.0,"total_cal":600,"total_protein":80,"drink_cal":0,"addon_cal":0}
low_p  = {"total_price":8.0,"total_cal":600,"total_protein":10,"drink_cal":0,"addon_cal":0}
_, prune_scores = intermediate_prune_3([high_p, low_p], test_prefs, test_constraints)
prune_winner = "high-protein" if prune_scores[0] < prune_scores[1] else "low-protein"

common = dict(total_fiber=5, total_sugars=3, total_sodium=400, total_cholesterol=50,
              total_carbohydrates=30, total_potassium=200, total_fat=10,
              Entree_ids=[], Side_ids=[], Drink_ids=[],
              **{"Add-on_ids": [], "Dessert_ids": []})
df_rank = results_to_df([{**high_p, "item_ids":[0,2], **common},
                          {**low_p,  "item_ids":[1,2], **common}])
ranked = score_and_rank_meals_expanded(df_rank, test_constraints, test_prefs)
rank_winner = "high-protein" if ranked.iloc[0]["total_protein"] == 80 else "low-protein"
report("prune and scorer agree on protein preference",
       prune_winner == rank_winner,
       f"prune={prune_winner}, scorer={rank_winner}")

# ── TEST 7: Jaccard division by zero ──────────────────────────────────────────
print("\nTEST 7: Jaccard division by zero with empty item_ids")
def empty_meal():
    return {"total_price":0,"total_cal":0,"total_protein":0,
            "drink_cal":0,"addon_cal":0,"item_ids":[],
            "total_fiber":0,"total_sugars":0,"total_sodium":0,
            "total_cholesterol":0,"total_carbohydrates":0,"total_potassium":0,
            "total_fat":0,"Entree_ids":[],"Side_ids":[],"Drink_ids":[],
            **{"Add-on_ids":[],"Dessert_ids":[]}}
try:
    df_e   = results_to_df([empty_meal(), empty_meal()])
    scored = score_and_rank_meals_expanded(df_e, test_constraints, test_prefs)
    report("empty item_ids no ZeroDivisionError", True, f"got {len(scored)} meals")
except ZeroDivisionError as e:
    report("empty item_ids no ZeroDivisionError", False, f"ZeroDivisionError: {e}")
except Exception as e:
    report("empty item_ids no ZeroDivisionError", False, f"{type(e).__name__}: {e}")

# ── summary ───────────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print(f"RESULTS: {PASS} passed, {FAIL} failed out of {PASS+FAIL} tests")
print("=" * 60)
