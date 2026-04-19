from classes import NumRange

def query_selector_for_item(query: str, name: str, price_range: NumRange = None, calories_range: NumRange = None, protein_range: NumRange = None):
    params = []
    if name:
        query += " AND m.menu_item_name ILIKE %s"
        params.append(f"%{name}%")

    # price filter
    if price_range:
        if not price_range.is_min_none():
            query += " AND m.price >= %s"
            params.append(price_range.get_min)
        if not price_range.is_max_none():
            query += " AND m.price <= %s"
            params.append(price_range.get_max)

    # calorie filter
    if calories_range:
        if not calories_range.is_min_none():
            query += " AND n.calories >= %s"
            params.append(calories_range.get_min)
        if not calories_range.is_max_none():
            query += " AND n.calories <= %s"
            params.append(calories_range.get_max)

    # protein filter
    if protein_range:
        if not protein_range.is_min_none():
            query += " AND n.protein >= %s"
            params.append(protein_range.get_min)
        if not protein_range.is_max_none():
            query += " AND n.protein <= %s"
            params.append(protein_range.get_max)

    query += " ORDER BY n.protein DESC;"

    return (query, params)