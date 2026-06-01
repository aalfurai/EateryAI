import { apiFetch } from "./client";
import { Meal } from "../types/Meal";

type RecommendRequest = {
  restaurant_name: string;
  categories: string[];
  seed_id?: string;
  // used to differenciate between same id items
  calories?: number;
};

type RecommendResponse = {
  user: unknown;
  recommendations: Meal[];
  summary?: string;
};

export const getRecommendations = (req: RecommendRequest, token: string) =>
  apiFetch<RecommendResponse>("/recommend", {
    method: "POST",
    body: JSON.stringify(req),
    headers: { Authorization: `Bearer ${token}` },
  });
