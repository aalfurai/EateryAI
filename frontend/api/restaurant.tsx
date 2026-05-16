import { apiFetch } from "./client";

export type Restaurant = {
  restaurant_id: string;
  restaurant_name: string;
  menu_card_image: string;
};

export const getRestaurants = () => 
  apiFetch<Restaurant[]>(`/restaurants`);

export const searchRestaurants = (query: string) =>
  apiFetch<Restaurant[]>(`/restaurants/search?name=${encodeURIComponent(query)}`);