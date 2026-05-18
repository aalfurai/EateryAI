import { apiFetch } from "./client";
import { MenuItem } from "./menu";

export const getItem = (restaurant: string, item_id: string) =>
    apiFetch<MenuItem>(`/menu/${encodeURIComponent(restaurant)}/${encodeURIComponent(item_id)}`);

export type SearchItem = {
  restaurant_name: string;
  item_id: string;
  menu_item_name: string;
  category: string;
  price: number;
  golden_ratio: number;
  calories: number;
  protein: number;
};

export type ItemSearchParams = {
  q?: string;

  price_min?: number;
  price_max?: number;

  calories_min?: number;
  calories_max?: number;

  protein_min?: number;
  protein_max?: number;
};

export async function searchItems(params: ItemSearchParams) {
  const query = new URLSearchParams();

  // text search
  if (params.q?.trim()) {
    query.append("q", params.q.trim());
  }

  // price
  if (params.price_min != null) {
    query.append("price_min", String(params.price_min));
  }

  if (params.price_max != null) {
    query.append("price_max", String(params.price_max));
  }

  // calories
  if (params.calories_min != null) {
    query.append("calories_min", String(params.calories_min));
  }

  if (params.calories_max != null) {
    query.append("calories_max", String(params.calories_max));
  }

  // protein
  if (params.protein_min != null) {
    query.append("protein_min", String(params.protein_min));
  }

  if (params.protein_max != null) {
    query.append("protein_max", String(params.protein_max));
  }

  return apiFetch<SearchItem[]>(`/search?${query.toString()}`);
}