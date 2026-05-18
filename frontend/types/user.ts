import { Weights } from "./weights";
import { Constraints } from "./constraints";

export type User = {
  user_id: string;
  name: string;
  constraints: Constraints;
  weights: Weights;
};

export const getMinAndMaxValues = (user: User) => {
  const { constraints } = user;

  const minPrice = constraints.price - (constraints.price * constraints.price_tol_pct);
  const maxPrice = constraints.price + (constraints.price * constraints.price_tol_pct);

  const minCalories = (constraints.calories - 
    (constraints.calories * constraints.calories_tol_pct));
  const maxCalories = (constraints.calories + 
    (constraints.calories * constraints.calories_tol_pct));

  const minProtein = (constraints.protein - 
    (constraints.protein * constraints.protein_tol_pct));
  const maxProtein = (constraints.protein + 
      (constraints.protein * constraints.protein_tol_pct));

  return { minPrice, maxPrice, minCalories, maxCalories, minProtein, maxProtein };
};

/* Loosen the ranges for the sake of the discover page */
export const getRangesForDiscover = (user: User) => {
  const { constraints } = user;
  const tol_pct = 0.5;

  const minPrice = constraints.price - (constraints.price * tol_pct);
  const maxPrice = constraints.price + (constraints.price * tol_pct);

  const minCalories = Math.round(constraints.calories - (constraints.calories * tol_pct));
  const maxCalories = Math.round(constraints.calories + (constraints.calories * tol_pct));

  const minProtein = Math.round(constraints.protein - (constraints.protein * tol_pct));
  const maxProtein = Math.round(constraints.protein + (constraints.protein * tol_pct));

  return { minPrice, maxPrice, minCalories, maxCalories, minProtein, maxProtein };
};