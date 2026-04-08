import json

CATEGORIES = {
    "Entree": {"entree", "breakfast", "lunch", "dinner", "soup", "salad", "burrito", "taco", "kabob", "fish", "meal",
                "sandwich", "steak", "bagel", "bowl", "plate", "wing", "tender", "seafood", "pizza", "pancake", "sirloin", "burger",
                "dog", "pasta", "quesadilla", "main", "stromboli", "calzone", "rice", "noodle", "build", "sub", "taquito", "slider",
                "pita", "zalad", "loco", "wrap", "panini", "focaccia", "ciabatta", "rib", "shepard", "poke", "meatloaf", "halibut", 
                # shepard added to capture pie as entree vs dessert
                "bisque", "roll", "combo", "combination", "enchilada", "fajita", "tamales", "feast", "platter", "omelet", "waffle", 
                "chili", "melt", "flatizza", "nacho", "specialties", "dim sum", "stack", "hoagie", "spud", "quiche", "salmon", "liver", 
                "gizzard", "boat", "stir-fry", "grilled", "piccata", "crab", "lobster", "chalupa", "filet",  "menu hacks", "casserole", 
                "bruschett"},
    "Side": {"side", "starters", "chips", "snack", "munch", "kid", "children", "appetizer", "edamame", 
             "hummus", "fries", "popper", "bite", "fruit", "mac & cheese", "flatbread", "tornado", "dip", "potato", "pretzel", "croissant", 
             "toast", "shareable", "pups", "hash", "nudies"},
    "Drink": {"drink", "beverage", "coffee", "water", "beer", "slush", "smoothie", "cocktail", "wine", "refresher", "tea", "blend", "cappuccino", 
              "frappe", "lemonade", "mimosa", "margarita", "soda", "espresso", "juice", "limeade", "cervezas", "shots", "bloody mary"},
    "Dessert": {"dessert", "ice cream", "custard", "shake", "cake", "yogurt", "donut", "doughnut", "float", "blizzard", "blast", "chocolate", 
                "sundae", "freezee", "cooler", "brownie", "frosty", "caramel", "pie", "cookie", "pastries", "muffin", "bakery", "cone", "puddin", 
                "icee", "danish", "mixer", "baked goods", "signature creations", "moolattes", "coolattas", "lemon ice", "concrete", 'souffle', 
                "fritter", "bundt", "cobbler", "pastry", "bars", "treat", "banana", "novelties", "creams", "julius"},
    "Add-On": {"topping", "condiment", "add", "add-on", "add on", "addon", "mix-in", "ingredient", "dressing", "sauce", "proteins", "beans",
               "chicken", "pork", "beef", "option", "avocado", "flavor", "cheese", "aioli", "bacon", "meat", "vegetable", "supplement", 
               "family", "bread", "protein", "base", "sausage", "components", " for ", " on ", "extra", "boost", "turkey", "crust", "pastrami", 
               "shrimp", "tempura", "pepperoni", "hot bar", "oil", "pesto", "guac", "egg", "vinaigrette", "spinach"}
               # check calories to determine if items like "chicken" are entree or side/add-on
}

SDAO_UPGRAGE_THRESHOLD = 450
LOW_CAL_ADDON_THRESHOLD = 110
HIGH_CAL_ENTREE_THRESHOLD = 900
FORCE_DESSERT_RESTAURANTS = {"Cold Stone Creamery", "Cinnabon"}


def restaurant_category_override(item):
    if item["restaurant_name"] in FORCE_DESSERT_RESTAURANTS:
        item["category"] = "Dessert"
        return True
    return False

def categorize_item(item):
    # check both category and item name
    cat = item["category"].lower()
    name = item["menu_item_name"].lower()
    cals = item["nutrition_info"]["calories"]

    if restaurant_category_override(item):
        item["recategorize_reason"] = "override"
        return "Dessert"
    
    for standardized_cat, keywords in CATEGORIES.items():
        for word in keywords:
            if word in cat or word in name:
                # classify itemes that are more than 450 cals as entrees
                if standardized_cat in {"Side", "Add-On"} and cals >= SDAO_UPGRAGE_THRESHOLD:
                    item["recategorize_reason"] = "calorie_upgrade"
                    return "Entree"
                item["recategorize_reason"] = "category_match"
                return standardized_cat
            
    # usually items under 110 calories are a side/add-on
    if cals <= LOW_CAL_ADDON_THRESHOLD:
        item["recategorize_reason"] = "calorie_threshold"
        return "Add-On"
    elif cals >= HIGH_CAL_ENTREE_THRESHOLD:
        item["recategorize_reason"] = "calorie_threshold"
        return "Entree"
    return None

def setupData():
    with open("../restaurants.menu_item_variations.json", "r") as f:
        data = json.load(f)
    
    good_cat = []
    bad_cat = []

    for item in data:
        new_cat = categorize_item(item)
        if new_cat:
            item["category"] = new_cat
            good_cat.append(item)
        else:
            bad_cat.append(item)

    with open("../restaurants_data_manual_recat.json", "w") as correct:
        json.dump(good_cat, correct, indent=4)