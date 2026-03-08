## Implementation Ideas/Notes
# - Entree Combinations
#     - Don't need to store in DB, extra storage
#     - Already fast enough if base item is selected

# Flow:
# - User selects an item
# - While user is looking at item / typing their request
#     - Query DB for that restaurant's menu items
#     - Make entree combos based on selected item
#         - If not entree, # of combinations = n + (n+1) choose 2
#         - If entree, # of combinations = n + 2
# - User sends request, either selecting a template or typing request
#     - NLP for request, returns a JSON for what templates are required to fulfill request
#     - Still have to figure out specific item requests, like I want fries
# - Send result meals in JSON format to frontend

import json
import pandas as pd
import math
import numpy as np
import copy
import mc_functions

# ------- TO BE REPLACED WITH DB QUERY -------
with open('../restaurants.menu_item_variations.json', 'r') as file:
    item_list = json.load(file)
file.close()

chick_fil_a_items = []

for item in item_list:
    if item.get("restaurant_name") == "Chick-fil-A":
        chick_fil_a_items.append(item)

df_cfa = pd.DataFrame(chick_fil_a_items)
df_cfa.reset_index(inplace=True)

# NOTE: will need to join items and their nutrition info
def extract_nutrition(df):
    nutrition_df = df["nutrition_info"].apply(pd.Series)
    df = pd.concat([df.drop(columns=["nutrition_info"]), nutrition_df], axis=1)
    return df
df_cfa = extract_nutrition(df_cfa)
# ------- TO BE REPLACED WITH DB QUERY -------

# USER WEIGHTS
USER_PRICE = 14.00
USER_CAL = 800
USER_PROTEIN = 20

# TOLERANCES
PRICE_TOL = round(USER_PRICE * 0.20, 2)
CAL_TOL = math.ceil(USER_CAL * 0.10)
PROTEIN_TOL = math.ceil(USER_PROTEIN * 0.30)

# USER CONSTRAINTS
W_PRICE = 0.80
W_CAL = 0.10
W_PROTEIN = 0.10