export type MenuItem = {
  index: number;
  item_id: number;
  menu_item_name: string;
  category: string;
  price: number;
  calories: number;
  protein: number;
  dietary_fiber: number;
  sugars: number;
  sodium: number;
  cholesterol: number;
  total_carbohydrates: number;
  potassium: number;
  total_fat: number;
  serving_size: string;

  // not in backend structure for an item but would be useful to have for frontend
  image_url: string;
  restaurant_name: string; 
};