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