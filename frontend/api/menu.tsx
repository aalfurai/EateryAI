import { apiFetch } from "./client";

export type MenuItem = {
  index: number;
  item_id: string;
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
  golden_ratio: number;
  ai_description: string;
  image_url: string;
};

type MenuResponse = {
  restaurant: string;
  items: MenuItem[];
};

export const getMenu = (restaurant: string) =>
  apiFetch<MenuResponse>(`/menu/${encodeURIComponent(restaurant)}`);