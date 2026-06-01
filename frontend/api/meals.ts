import { apiFetch } from "./client";
import { Meal } from "../types/Meal";

type SavedMealsResponse = {
  saved_meals: Meal[];
};

export const saveMeal = (meal: Meal, token: string) =>
  apiFetch<{ message: string; saved_count: number }>("/users/saved", {
    method: "POST",
    body: JSON.stringify({ meal }),
    headers: { Authorization: `Bearer ${token}` },
  });

export const unsaveMeal = (mealIndex: number, token: string) =>
  apiFetch<{ message: string }>(`/users/saved/${mealIndex}`, {
    method: "DELETE",
    headers: { Authorization: `Bearer ${token}` },
  });

export const getSavedMeals = (token: string) =>
  apiFetch<SavedMealsResponse>("/users/saved", {
    headers: { Authorization: `Bearer ${token}` },
  });
