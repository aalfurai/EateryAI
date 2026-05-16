import { User } from "../types/user";

export const defaultUser: User = {
  user_id: "demo-user",

  name: "Demo User",

  constraints: {
    price: 14,
    calories: 800,
    protein: 20,

    price_tol_pct: 0.2,
    calories_tol_pct: 0.1,
    protein_tol_pct: 0.3,
  },

  weights: {
    price: 0.33,
    calories: 0.33,
    protein: 0.34,

    fiber: 0,
    sugar: 0,
    sodium: 0,
    drink_cal: 0,
    addon_cal: 0,
  },
};