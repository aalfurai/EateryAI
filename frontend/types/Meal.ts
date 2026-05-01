export type Meal = {
  item_ids: number[];

  entree_ids: number[];
  side_ids: number[];
  drink_ids: number[];
  addon_ids: number[];
  dessert_ids: number[];

  total_price: number;
  total_cal: number;
  total_protein: number;
  total_fiber: number;
  total_sugars: number;
  total_sodium: number;
  total_cholesterol: number;
  total_carbohydrates: number;
  total_potassium: number;
  total_fat: number;

  drink_cal: number;
  addon_cal: number;

  filled_categories: string[];

  golden_ratio: number;
}