/* Weight presets for different user preferences */
import { Weights } from "../types/weights";

export const weightPresets: Record<string, Weights> = {
  bodybuilder: {
    price: 0.1,
    calories: 0.2,
    protein: 0.7,

    fiber: 0,
    sugar: 0,
    sodium: 0,
    drink_cal: 0,
    addon_cal: 0,
  },

  budgeter: {
    price: 0.7,
    calories: 0.15,
    protein: 0.15,

    fiber: 0,
    sugar: 0,
    sodium: 0,
    drink_cal: 0,
    addon_cal: 0,
  },

  dieting: {
    price: 0.2,
    calories: 0.7,
    protein: 0.1,

    fiber: 0,
    sugar: 0,
    sodium: 0,
    drink_cal: 0,
    addon_cal: 0,
  },

  balanced: {
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