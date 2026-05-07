import { apiFetch } from "./client";
import { MenuItem } from "./menu";
export const getItem = (restaurant: string, item_id: string) =>
    apiFetch<MenuItem>(`/menu/${encodeURIComponent(restaurant)}/${encodeURIComponent(item_id)}`);
